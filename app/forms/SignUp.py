from flask_wtf import FlaskForm, RecaptchaField
from wtforms.fields import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, length, Email

# SignUp
class SignUpForm(FlaskForm):
    username = StringField(validators=[DataRequired("Username is Empty !")])
    email = EmailField(validators=[DataRequired("Email is Empty !"), Email('Email is Inavlid !')])
    password = PasswordField(validators=[DataRequired("Password is Empty !"), length(min= 8, message="Password cant be reach less than 8 !")])
    recaptcha = RecaptchaField()