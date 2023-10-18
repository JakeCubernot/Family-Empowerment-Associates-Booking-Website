from flask import Blueprint, render_template, request, flash, redirect, url_for
from . models import User
from werkzeug.security import generate_password_hash, check_password_hash  #Converts password to hash for security
from .import db
from flask_login import login_user, logout_user, login_required, current_user  #UserMixin in models allows for these methods

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  #Requests email and password from the database
        email = request.form.get('email')
        password = request.form.get('password')

        #Find users that have the email that was typed. The .first will give you the first user that matches that email.
        user=user = User.query.filter_by(email=email).first()
        if user: #Checks if the password assigned to user matches password in database.
            if check_password_hash(user.password, password): 
                flash('Logged in!', category='success')
                login_user(user, remember=True) #will login the user and stores in cookies. 
                return redirect(url_for('views.home')) #Redirects user to home page.
            else:
                flash('Incorrect Password!', category='error')
        else: # If user is false, it means that there no user with that email found in the database.
            flash('Email does not exist!', category='error')

    return render_template('login.html', user=current_user) #current_user retrives data if user is logged in.

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Account already exists!', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash((password1), method='sha256'))
            db.session.add(new_user) #Adds user above to db.
            db.session.commit()
            login_user(new_user, remember=True) #will login the user after creating account. 


            flash('Account Created!', category='success')
            return redirect(url_for('views.home')) #Redirects to home page.
            
    return render_template('register.html', user=current_user) #current_user retrives data if user is logged in.

@auth.route('/logout')
@login_required  #Cannot access unless logged in.
def logout():
    logout_user()
    return redirect(url_for('auth.login'))