from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db

# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

# This is a hint for a login function
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login"""
    login_form = LoginForm()
    error = None

    if login_form.validate_on_submit():
        user_name = login_form.user_name.data
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.name == user_name))
        
        if user is None:
            error = 'Incorrect user name'
        elif not check_password_hash(user.password_hash, password):  # Takes the hash and cleartext password
            error = 'Incorrect password'

        if error is None:
            # Log in the user
            login_user(user)
            
            # Determine where to redirect
            nextp = request.args.get('next')
            if nextp is None or not nextp.startswith('/'):
                nextp = url_for('index')  # Default to 'index' if 'next' is invalid
            return redirect(nextp)
        else:
            # Flash the error message
            flash(error)

    # Render the login form
    return render_template('login.html', form=login_form, heading='Login')
