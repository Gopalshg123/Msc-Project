from PIL import Image
import pyzbar.pyzbar as pyzbar
import io
import random
import base64
from flask import Flask, render_template, request, redirect, url_for, session
from db import connect_db, init_db

app = Flask(__name__)
app.secret_key = '121212'  # Needed for session management

# Initialize the database
init_db()

# Function to get user data from the database
def get_user_data(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE name = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

@app.route('/')
def main():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        diseases = ','.join(request.form.getlist('disease'))  # Comma-separated string of selected diseases
        professional_help = request.form['professional_help']
        calorie_intake = request.form['calorie_intake']
        water_intake = request.form['water_intake']
        user_type = request.form.get('user_type', 'normal')  # Default to 'normal' if not specified

        conn = connect_db()
        cursor = conn.cursor()

        # Insert user data into the database
        cursor.execute('''
            INSERT INTO users (name, password, diseases, professional_help, calorie_intake, water_intake, user_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, password, diseases, professional_help, calorie_intake, water_intake, user_type))

        conn.commit()
        conn.close()

        return redirect(url_for('main'))
    
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = connect_db()
        cursor = conn.cursor()

        # Retrieve the user from the database
        cursor.execute('SELECT * FROM users WHERE name = ? AND password = ?', (username, password))
        user = cursor.fetchone()

        conn.close()

        if user:
            session['username'] = user[1]  # Store username in session
            session['user_type'] = user[7]  # Store user type in session

            if user[7] == 'normal':
                return redirect(url_for('uhome'))
            elif user[7] == 'healthcare_professional':
                return redirect(url_for('hhome'))
        else:
            return 'Invalid credentials. Please try again.'

    return render_template('login.html')

# Logout Route
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    session.pop('user_type', None)  # Remove user type from session
    return redirect(url_for('main'))





# Home Page for Normal Users
@app.route('/uhome')
def uhome():
    if 'username' in session:
        return render_template('uhome.html', user_type='normal')
    return redirect(url_for('main'))

# Home Page for Healthcare Professionals
@app.route('/hhome')
def hhome():
    if 'username' in session:
        return render_template('hhome.html', user_type='healthcare_professional')
    return redirect(url_for('main'))





@app.route('/uaccount')
def uaccount():
    if 'username' in session:
        username = session['username']
        user_data = get_user_data(username)
        
        if user_data:
            # Extract user data
            user_info = {
                'username': user_data[1],  # Adjust based on column order
                'usertype': user_data[7],  # Adjust based on column order
                'diseases': user_data[3].split(',') if user_data[3] else []  # Split comma-separated list of diseases
            }
            return render_template('uaccount.html', user=user_info)
    
    return redirect(url_for('main'))

@app.route('/haccount')
def haccount():
    if 'username' in session:
        username = session['username']
        user_data = get_user_data(username)
        
        if user_data:
            # Extract user data
            user_info = {
                'username': user_data[1],  # Adjust based on column order
                'usertype': user_data[7]  # Adjust based on column order
            }
            return render_template('haccount.html', user=user_info)
    
    return redirect(url_for('main'))




@app.route('/add_disease', methods=['POST'])
def add_disease():
    if 'username' in session:
        username = session['username']
        new_diseases = request.form.getlist('new_diseases')  # Get list of selected diseases
        
        # Fetch current user diseases from the database
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT diseases FROM users WHERE name = ?', (username,))
        current_diseases = cursor.fetchone()[0]
        
        # Prepare the updated list of diseases
        if current_diseases:
            updated_diseases = current_diseases.split(',')
        else:
            updated_diseases = []
        
        updated_diseases.extend(new_diseases)
        updated_diseases = ','.join(list(set(updated_diseases)))  # Remove duplicates
        
        # Update the database
        cursor.execute('UPDATE users SET diseases = ? WHERE name = ?', (updated_diseases, username))
        conn.commit()
        conn.close()
        
        return redirect(url_for('uaccount')) 

@app.route('/remove_disease', methods=['POST'])
def remove_disease():
    if 'username' in session:
        username = session['username']
        disease_to_remove = request.form['disease']
        
        # Fetch current user diseases from the database
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT diseases FROM users WHERE name = ?', (username,))
        current_diseases = cursor.fetchone()[0]
        
        # Remove the disease
        updated_diseases = ','.join([d for d in current_diseases.split(',') if d != disease_to_remove])
        
        # Update the database
        cursor.execute('UPDATE users SET diseases = ? WHERE name = ?', (updated_diseases, username))
        conn.commit()
        conn.close()
        
        return redirect(url_for('uaccount')) 



@app.route('/progress_report')
def progress_report():
    if 'username' in session:
        # Connect to the database
        conn = connect_db()
        cursor = conn.cursor()
        
        # Get the logged-in user's username
        username = session['username']
        
        # Fetch the user's data
        cursor.execute("""
            SELECT id, name, diseases, calorie_intake, water_intake
            FROM users
            WHERE name = ?
        """, (username,))
        user_data = cursor.fetchone()
        
        if not user_data:
            return "User not found", 404
        
        user_id = user_data[0]

        # Fetch unique doctor's recommendations for the user
        cursor.execute("""
            SELECT DISTINCT recommendations
            FROM medical_recommendations
            WHERE user_id = ?
        """, (user_id,))
        recommendations = cursor.fetchall()
        
        return render_template('progress_report.html', user=user_data, recommendations=[r[0] for r in recommendations])
    
    return redirect(url_for('main'))








@app.route('/food_recommendation')
def food_recommendation():
    if 'username' in session:
        username = session['username']
        
        # Connect to the database and retrieve the user's diseases
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT diseases FROM users WHERE name = ?', (username,))
        user_diseases = cursor.fetchone()[0]
        diseases_list = user_diseases.split(',')

        # Dictionary to store recommendations
        recommendations = {}

        for disease in set(diseases_list):  # Use set to avoid duplicates
            # Retrieve recommended foods for the disease
            cursor.execute('SELECT DISTINCT food_name FROM foods WHERE disease_type = ? AND food_type = "recommended"', (disease,))
            recommended_foods = [row[0] for row in cursor.fetchall()]
            
            # Retrieve foods to avoid for the disease
            cursor.execute('SELECT DISTINCT food_name FROM foods WHERE disease_type = ? AND food_type = "avoid"', (disease,))
            foods_to_avoid = [row[0] for row in cursor.fetchall()]
            
            # Store the recommendations for the disease
            recommendations[disease] = {
                'recommended': list(set(recommended_foods)),  # Remove duplicates
                'avoid': list(set(foods_to_avoid))  # Remove duplicates
            }

        conn.close()

        return render_template('food_recommendation.html', recommendations=recommendations, user_type='normal')

    return redirect(url_for('main'))







@app.route('/scan_barcode')
def scan_barcode():
    if 'username' in session:
        return render_template('upload_barcode.html', user_type=session.get('user_type', 'normal'))
    return redirect(url_for('main'))

@app.route('/upload_barcode', methods=['POST'])
def upload_barcode():
    if request.form['barcode_image']:
        image_data = request.form['barcode_image'].split(",")[1]
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
    
    elif 'fileUpload' in request.files:
        image_file = request.files['fileUpload']
        if image_file:
            image = Image.open(image_file)
        else:
            return 'No file uploaded or no barcode found in the image.'

    else:
        return 'No image data provided.'

    barcodes = pyzbar.decode(image)
    
    if barcodes:
        barcode_data = barcodes[0].data.decode('utf-8')

        # Randomly decide "recommended" or "avoid"
        recommendation = random.choice(['recommended', 'avoid'])

        # Return both the barcode data and the recommendation
        return f'Barcode data: {barcode_data} - {recommendation}.'
    else:
        return 'No barcode found in the image.'





"""                                     Healthcare management                               """
# Function to get users who have opted for professional help
def get_professional_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, diseases, professional_help, calorie_intake, water_intake FROM users WHERE professional_help = 'yes'")
    users = cursor.fetchall()
    return [{'id': row[0], 'username': row[1], 'diseases': row[2].split(','), 'professional_help': row[3], 'calorie_intake': row[4], 'water_intake': row[5]} for row in users]

@app.route('/hmanage')
def hmanage():
    if 'username' in session:
        # Connect to the database
        conn = connect_db()
        cursor = conn.cursor()
        
        # Get the user type from the session or fetch all professional users
        cursor.execute("""
            SELECT id, name, diseases, calorie_intake, water_intake
            FROM users
            WHERE user_type = 'normal' AND professional_help = 'yes'
        """)
        user_rows = cursor.fetchall()
        
        # Prepare user data and fetch recommendations
        users = []
        user_recommendations = {}
        for user_row in user_rows:
            user_id, name, diseases, calorie_intake, water_intake = user_row
            users.append({
                'id': user_id,
                'name': name,
                'diseases': diseases,
                'calorie_intake': calorie_intake,
                'water_intake': water_intake
            })
            
            # Fetch recommendations for this user and aggregate them
            cursor.execute('''
                SELECT DISTINCT recommendations
                FROM medical_recommendations
                WHERE user_id = ?
            ''', (user_id,))
            recommendations = cursor.fetchall()
            user_recommendations[user_id] = [rec[0] for rec in recommendations]
        
        return render_template('hmanage.html', users=users, recommendations=user_recommendations)
    
    return redirect(url_for('main'))



@app.route('/edit_user/<int:user_id>', methods=['POST'])
def edit_user(user_id):
    # Retrieve the recommendation from the form
    recommendation = request.form['recommendation']

    # Insert the recommendation using a complex query with UNION
    conn = connect_db()
    cursor = conn.cursor()
    
    # Assuming the professional is the one currently logged in, get the professional's user_id
    cursor.execute('''
        INSERT INTO medical_recommendations (user_id, professional_id, recommendations)
        SELECT ?, id, ? FROM users WHERE name = ?
        UNION
        SELECT ?, id, ? FROM users WHERE id = ?
    ''', (user_id, recommendation, session['username'], user_id, recommendation, user_id))
    
    conn.commit()

    return redirect(url_for('hmanage'))

@app.route('/remove_recommendation/<int:user_id>', methods=['POST'])
def remove_recommendation(user_id):
    data = request.get_json()
    recommendation = data.get('recommendation')
    
    conn = connect_db()
    cursor = conn.cursor()
    
    # Remove the recommendation for the specified user
    cursor.execute('''
        DELETE FROM medical_recommendations
        WHERE user_id = ? AND recommendations = ?
    ''', (user_id, recommendation))
    
    conn.commit()
    conn.close()
    
    return '', 204  # No content response




if __name__ == '__main__':
    app.run(debug=True)
