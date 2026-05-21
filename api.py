from flask import Flask, render_template, request, redirect, url_for, session
from userclass import User 
import uuid
import os

app = Flask(__name__)
app.secret_key = "super_secret_key_for_session"


@app.route('/register', methods=['GET', 'POST'])
def register():
    errors = []
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password')

        # Create a unique UserID
        user_id = uuid.uuid4().int & ((1 << 31) - 1)

        if User.register_user(username, password, user_id):
            return redirect(url_for('login'))
        else:
            errors.append("This username is already taken.")

    return render_template('register.html', errors=errors)


@app.route('/login', methods=['GET', 'POST'])
def login():
    errors = []
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password')

        user = User.login(username, password)
        if user:
            # IMPORTANT: We store user info in the session
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            errors.append("Invalid username or password.")

    return render_template('login.html', errors=errors)


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)