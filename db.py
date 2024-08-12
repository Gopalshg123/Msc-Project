import sqlite3

# Function to connect to the SQLite3 database
def connect_db():
    conn = sqlite3.connect('dietary_management.db')
    return conn

# Function to initialize the database
def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL,
                        user_type TEXT NOT NULL
                      )''')
    conn.commit()
    conn.close()

# Function to test the database connection
def test_db_connection():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in the database:", tables)
    cursor.close()
    conn.close()

if __name__ == '__main__':
    init_db()  # Initialize the database
    test_db_connection()  # Test the connection and list tables
