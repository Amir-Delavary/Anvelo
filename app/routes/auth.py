from flask import Blueprint, render_template, redirect, request, url_for, flash, session, current_app
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash
from flask_mail import Message
from app.forms import SignUpForm, LoginForm
from app.extensions import db, mail
from app.models import User
from functools import wraps
import secrets
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)


# User LoggedIn or no?
def anonymous_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('main.Home'))
        return f(*args, **kwargs)
    return decorated_function


def generate_token(length=6):
    token = secrets.token_urlsafe(length)[:length] # For sure token is 6 char
    expiration_time = datetime.utcnow() + timedelta(seconds=120)
    return token, expiration_time


@auth_bp.route("/signup", methods=['POST', 'GET'])
@anonymous_required  # If user LoggedIn dont show this page
def SignUp():
    form = SignUpForm()  # Add Forms
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            
            existing_email = User.query.filter_by(email= email).first()  # Find first user with this id in Database
            existing_username = User.query.filter_by(username= username).first()  # Find first user with this id in Database
            if existing_email and existing_username:
                flash("Error, Username and email is exist")
                return redirect(url_for('auth.SignUp'))
            elif existing_username:
                flash("Error, Username is exist")
                return redirect(url_for('auth.SignUp'))
            elif existing_email:
                flash("Error, email is exist")
                return redirect(url_for('auth.SignUp'))
            else:
                token, expiration_time = generate_token()
                user = User(username = username, email = email, password = password, token=token, token_expiration=expiration_time, tasks_done=0, theme="light")
                db.session.add(user)  # Add new user
                db.session.commit()  # Confirm it
                msg = Message(subject="ToDoList | Confirm Email Code", sender=current_app.config['MAIL_USERNAME'], recipients=[f"{user.email}"])
                msg.body = f"""
                Your confirmation code:
                {user.token}
                Code Expiration Time : 10 minutes
                """
                mail.send(msg)
                session['user_id'] = user.id
                session['confirm_flag'] = True
                return redirect(url_for('user.ConfirmAccount'))

    return render_template("SignUp.html", form=form)  # Next arg will use for send form to html



@auth_bp.route("/login", methods=['GET', 'POST'])
@anonymous_required  # If user LoggedIn dont show this page
def Login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            nextparam = request.form['next']  # Find what route user need
            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):  # Check hashed password in database with user password for login
                    login_user(user)  # Login with this user to the app
                    return redirect(nextparam or url_for('main.Home'))  # Use nextparam for to help what user need
                else:
                    flash("Wrong password")
                    return redirect(url_for('auth.Login'))
            else:
                flash("User not exist")
                return redirect(url_for('auth.Login'))
            
    return render_template("Login.html", form=form)


@auth_bp.route('/logout', methods=['POST', 'GET'])
@login_required
def LogOut():
    if request.method == 'POST':
        logout_user()  # LogOut user
        return redirect(url_for('auth.Login'))
    return redirect(url_for('main.Home'))
