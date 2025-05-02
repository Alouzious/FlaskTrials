from flask import render_template, redirect, url_for, flash, request
from . import auth
from .forms import LoginForm, SignupForm
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User
from .. import db
import os
from werkzeug.utils import secure_filename
from .forms import ProfileUpdateForm  # Adjust path based on your app structure
from flask import current_app, session



# Login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            # Check if password matches admin secret
            if form.password.data == current_app.config['ADMIN_SECRET_PASSWORD']:
                session['is_admin'] = True
            else:
                session['is_admin'] = False

            flash('Login successful!', 'success')
            return redirect(url_for('dashboard.dashboard_page'))  # or redirect to admin if you prefer
        flash('Invalid email or password.', 'danger')
    return render_template('auth/login.html', form=form)


# Signup route
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            dob=form.dob.data,
            country=form.country.data,
            password=form.password.data  # Pass the password to the constructor
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html', form=form)

# Logout route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home.home_page'))

# Profile update route
@auth.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        if 'profile_picture' in request.files:
            profile_picture = request.files['profile_picture']
            if profile_picture:
                # Secure the filename and save it
                filename = secure_filename(profile_picture.filename)
                filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static', 'profile_pics', filename)
                filepath = os.path.normpath(filepath)
                profile_picture.save(filepath)
                
                # Update the user's profile picture in the database
                current_user.profile_picture = filename
                db.session.commit()

                flash('Profile updated successfully.', 'success')
                return redirect(url_for('auth.update_profile'))  # Redirect back to profile page
    form = ProfileUpdateForm()  # or whatever your form class is
    return render_template('partials/profile_update.html', form=form)

