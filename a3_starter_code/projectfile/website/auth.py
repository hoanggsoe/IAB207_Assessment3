from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db

# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

# Registration route
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        first_name = register_form.first_name.data
        surname = register_form.surname.data
        user_name = register_form.user_name.data
        email = register_form.email.data
        contact_number = register_form.contact_number.data
        street_address = register_form.street_address.data
        password = register_form.password.data

        # Hash password
        hashed_password = generate_password_hash(password).decode('utf-8')

        # Save user with the hashed password
        new_user = User(
            first_name=first_name,
            surname=surname,
            name=user_name, 
            email=email,
            contact_number=contact_number,
            street_address=street_address,
            password_hash=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=register_form, heading='Register')

# Login route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit():
        user_name = login_form.user_name.data
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.name == user_name))
        if user is None:
            error = 'Incorrect user name'
        elif not check_password_hash(user.password_hash, password):  # Hashed password
            error = 'Incorrect password'
        if error is None:
            login_user(user)
            nextp = request.args.get('next')  
            if nextp is None or not nextp.startswith('/'):
                return redirect(url_for('main.index'))
            return redirect(nextp)
        else:
            flash(error)
    return render_template('login.html', form=login_form, heading='Login')

# Logout route
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

# Test form submission
@auth_bp.route('/test-form', methods=['POST'])
def test_form():
    email = request.form.get('email')
    password = request.form.get('password')
    return f"Received: Email: {email}, Password: {password}"
