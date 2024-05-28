from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


conn = sqlite3.connect('vulnerable.db')
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')

cursor.execute("INSERT INTO users (username, password) VALUES ('user1', 'password1')")
cursor.execute("INSERT INTO users (username, password) VALUES ('user2', 'password2')")

conn.commit()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']


    conn = sqlite3.connect('vulnerable.db')
    cursor = conn.cursor()

    # Vulnerable to SQL injection
    query = "SELECT * FROM users WHERE username='%s' AND password='%s'"%(username,password)

    cursor.execute(query)
    user = cursor.fetchone()

    conn.close()

    if user:
        return f"Welcome, {username}!"
    else:
        return "Invalid username or password. Please try again."

if __name__ == '__main__':
    app.run(debug=True)
