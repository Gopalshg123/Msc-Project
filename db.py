import sqlite3

# Function to connect to the SQLite3 database
def connect_db():
    conn = sqlite3.connect('dietary_management.db')
    return conn

# Function to initialize the database and create tables if they don't exist
def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    # Create table for storing user data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            diseases TEXT,  -- Comma-separated list of diseases
            professional_help TEXT NOT NULL,  -- 'yes' or 'no'
            calorie_intake INTEGER,
            water_intake REAL,
            user_type TEXT NOT NULL  -- 'normal' or 'healthcare_professional'
        )
    ''')

    # Create table for storing food data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS foods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease_type TEXT NOT NULL,
            food_name TEXT NOT NULL,
            food_type TEXT NOT NULL  -- 'recommended' or 'avoid'
        )
    ''')

    # Create table for storing medical professional recommendations
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medical_recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            professional_id INTEGER NOT NULL,
            recommendations TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(professional_id) REFERENCES users(id)
        )
    ''')

    # Insert default values into foods table
    cursor.executescript('''
        -- Recommended Foods
        -- For Jaundice
        INSERT INTO foods (disease_type, food_name, food_type) VALUES ('jaundice', 'Carrot', 'recommended');
        INSERT INTO foods (disease_type, food_name, food_type) VALUES ('jaundice', 'Beetroot', 'recommended');
        INSERT INTO foods (disease_type, food_name, food_type) VALUES ('jaundice', 'Spinach', 'recommended');
        -- For Diabetes
        INSERT INTO foods (disease_type, food_name, food_type) VALUES ('diabetes', 'Broccoli', 'recommended');
        INSERT INTO foods (disease_type, food_name, food_type) VALUES ('diabetes', 'Almonds', 'recommended');
        INSERT INTO foods (disease_type, food_name, food_type) VALUES ('diabetes', 'Chia Seeds', 'recommended');
        -- For Hypertension
        INSERT INTO foods (disease_type, food_name, food_type) VALUES ('hypertension', 'Oats', 'recommended');
        INSERT INTO foods (disease_type, food_name, food_type) VALUES ('hypertension', 'Avocado', 'recommended');
        INSERT INTO foods (disease_type, food_name, food_type) VALUES ('hypertension', 'Garlic', 'recommended');
        -- For Common Cold
        INSERT INTO foods (disease_type, food_name, food_type) VALUES ('common_cold', 'Chicken Soup', 'recommended');
        INSERT INTO foods (disease_type, food_name, food_type) VALUES ('common_cold', 'Ginger Tea', 'recommended');
        INSERT INTO foods (disease_type, food_name, food_type) VALUES ('common_cold', 'Citrus Fruits', 'recommended');

                         
        -- Foods to Avoid
        -- For Jaundice
        INSERT INTO foods (disease_type, food_name, food_type) VALUES ('jaundice', 'Fried Foods', 'avoid');
        INSERT INTO foods (disease_type, food_name, food_type) VALUES ('jaundice', 'Sugary Drinks', 'avoid');
        INSERT INTO foods (disease_type, food_name, food_type) VALUES ('jaundice', 'Fatty Meats', 'avoid');
        -- For Diabetes
        INSERT INTO foods (disease_type, food_name, food_type) VALUES ('diabetes', 'Sugary Cereals', 'avoid');
        INSERT INTO foods (disease_type, food_name, food_type) VALUES ('diabetes', 'White Bread', 'avoid');
        INSERT INTO foods (disease_type, food_name, food_type) VALUES ('diabetes', 'Pastries', 'avoid');
        -- For Hypertension
        INSERT INTO foods (disease_type, food_name, food_type) VALUES ('hypertension', 'Salted Snacks', 'avoid');
        INSERT INTO foods (disease_type, food_name, food_type) VALUES ('hypertension', 'Processed Foods', 'avoid');
        INSERT INTO foods (disease_type, food_name, food_type) VALUES ('hypertension', 'Fried Foods', 'avoid');
        -- For Common Cold
        INSERT INTO foods (disease_type, food_name, food_type) VALUES ('common_cold', 'Ice Cream', 'avoid');
        INSERT INTO foods (disease_type, food_name, food_type) VALUES ('common_cold', 'Cold Drinks', 'avoid');
        INSERT INTO foods (disease_type, food_name, food_type) VALUES ('common_cold', 'Chips', 'avoid');
    ''')

    conn.commit()
    conn.close()
"""
# Function to test the database connection
def test_db_connection():
    conn = connect_db()
    print("Connection to database successful")
    conn.close()

if __name__ == '__main__':
    init_db()  # Initialize the database
    test_db_connection()  # Test the connection and print success message
"""