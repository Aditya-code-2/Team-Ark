import os
import time
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from user_data import load_users, save_users
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = 'your_secret_key_'

# Simulated user database
users = load_users()

@app.route('/')
def home():
    session.clear()  # TEMPORARY: Clears previous session
    return redirect(url_for('homepage'))

@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    return render_template('HomePage.html')


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        # Placeholder: Add logic to send reset link or verify user
        flash(f"If an account with {email} exists, a reset link has been sent.")
        return redirect(url_for('forgot_password'))
    return render_template('forgot_password.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = users.get(email)
        if user and check_password_hash(user['password'], password):
            # Store user information in session
            session['user'] = email
            session['name'] = user['name']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.')

    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    dob = request.form['dob']
    grad_year = request.form['grad_year']
    if email in users:
        flash('Email already registered.')
    else:
        users[email] = {
            "name": name,
            "password": generate_password_hash(password),
            "dob": "",
            "Grad_year": ""
            }
        save_users(users)  # Save to file
        flash('Registration successful. Please log in.')
    
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', name=session['name'])

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))

    email = session['user']
    user = users.get(email, {})

    if request.method == 'POST':
        user['name'] = request.form.get('name')
        user['dob'] = request.form.get('dob')
        user['about'] = request.form.get('about')
        session['name'] = user['name']

        # Save uploaded photo
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != '':
                filename = secure_filename(email + "_" + str(int(time.time())) + "_" + file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                user['photo'] = filename

        save_users(users)
        flash('Profile updated successfully.')
        return redirect(url_for('profile'))

    return render_template("profile.html",
                       name=user.get("name"),
                       email=email,
                       dob=user.get("dob", ""),
                       about=user.get("about", ""),
                       photo=user.get("photo"))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
