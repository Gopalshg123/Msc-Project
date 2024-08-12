from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Hardcoded user data
users = {
    'user': {'password': 'user', 'type': 'normal'},
    'healthcare': {'password': 'healthcare', 'type': 'healthcare_professional'}
}

# Hardcoded account data
user_data = {
    'user': {
        'username': 'user',
        'usertype': 'normal',
        'diseases': ['Jaundice', 'Diabetes', 'Common Cold', 'Hypertension']
    },
    'healthcare': {
        'username': 'healthcare',
        'usertype': 'healthcare_professional',
        'diseases': []  # Healthcare professionals don't have selected diseases
    }
}

# Sample user data for demonstration
professional_users = [
    {'username': 'user1', 'diseases': ['Jaundice', 'Diabetes'], 'professional_help': 'yes'},
    {'username': 'user2', 'diseases': ['Hypertension'], 'professional_help': 'yes'},
    {'username': 'user3', 'diseases': ['Common Cold'], 'professional_help': 'yes'}
]


@app.route('/')
def main():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Here you would handle form data, but we'll just redirect to the login page for now
        return redirect(url_for('main'))
    return render_template('signup.html')


# Login Page Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = users.get(username)
        if user and user['password'] == password:
            session['username'] = username  # Store username in session
            session['user_type'] = user['type']  # Store user type in session
            if user['type'] == 'normal':
                return redirect(url_for('uhome'))
            elif user['type'] == 'healthcare_professional':
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

# Account Page for Normal Users
@app.route('/uaccount')
def uaccount():
    if 'username' in session:
        data = user_data['user']
        return render_template('uaccount.html', user=data, user_type='normal')
    return redirect(url_for('main'))

# Account Page for Healthcare Professionals
@app.route('/haccount')
def haccount():
    if 'username' in session:
        data = user_data['healthcare']
        return render_template('haccount.html', user=data, user_type='healthcare_professional')
    return redirect(url_for('main'))

@app.route('/progress_report')
def progress_report():
    if 'username' in session:
        data = user_data['healthcare']
        return render_template('progress_report.html', user=data, user_type='normal')
    return redirect(url_for('main'))

@app.route('/food_recommendation')
def food_recommendation():
    if 'username' in session:
        data = user_data['healthcare']
        return render_template('food_recommendation.html', user=data, user_type='normal')
    return redirect(url_for('main'))

# Scan Barcode Page
@app.route('/scan_barcode')
def scan_barcode():
    if 'username' in session:
        return render_template('upload_barcode.html', user_type=session.get('user_type', 'normal'))
    return redirect(url_for('main'))

# Upload Barcode Page
@app.route('/upload_barcode', methods=['POST'])
def upload_barcode():
    return 'Coming soon'




"""                                     Healthcare management                               """
@app.route('/hmanage')
def hmanage():
    if 'username' in session:
        data = user_data['healthcare']
        return render_template('hmanage.html', user=data, user_type='healthcare_professional',users=professional_users)
    return redirect(url_for('main'))


@app.route('/edit_user/<username>', methods=['GET', 'POST'])
def edit_user(username):
    if request.method == 'POST':
        # Handle user data editing
        pass  # Implement edit functionality here
    return "Coming Soon" #f'Edit user: {username}'

@app.route('/delete_user/<username>')
def delete_user(username):
    # Handle user deletion
    global professional_users
    professional_users = [user for user in professional_users if user['username'] != username]
    return redirect(url_for('hmanage'))

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    diseases = request.form['diseases'].split(',')
    professional_help = request.form['professional_help']
    professional_users.append({
        'username': username,
        'diseases': diseases,
        'professional_help': professional_help
    })
    return redirect(url_for('hmanage'))




if __name__ == '__main__':
    app.run(debug=True)
