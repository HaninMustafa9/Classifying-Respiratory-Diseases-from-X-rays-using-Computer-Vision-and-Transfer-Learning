from flask import Blueprint, render_template, request, redirect, url_for, session

auth_bp = Blueprint('auth', __name__)

# Dictionary to store users with their types (doctor/patient)
users = {}

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    success_message = None
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['psw']
        user_type = request.form['user_type']  # Get the user type from the form

        # Check if the email already exists (implement your own user storage logic)
        if email in users:
            error = 'Email already exists!'
        else:
            # Save the user information along with their type
            users[email] = {'password': password, 'type': user_type}
            success_message = 'Account created successfully! Please log in.'
            return redirect(url_for('auth.login'))  # Redirect to login route

    return render_template('signup.html', error=error, success_message=success_message)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['psw']

        # Check if the email exists and password matches
        if email in users and users[email]['password'] == password:
            session['user'] = email  # Store the user in session
            session['user_type'] = users[email]['type']  # Store the user type in session
            return redirect(url_for('index'))  # Redirect to the main page
        else:
            error = 'Invalid email or password!'

    return render_template('login.html', error=error)

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)  # Remove user from session
    session.pop('user_type', None)  # Remove user type from session
    return redirect(url_for('index'))  # Redirect to main index after logout
