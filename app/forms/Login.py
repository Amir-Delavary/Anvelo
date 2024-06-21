from flask_wtf import FlaskForm, RecaptchaField
from wtforms.fields import PasswordField, EmailField
from wtforms.validators import DataRequired, length

# Login
class LoginForm(FlaskForm):
    email = EmailField(validators=[DataRequired("Email is Empty !")])
    password = PasswordField(validators=[DataRequired("Password is Empty !"),length(min= 8, message="Password cant be reach less than 8 !")])
    # recaptcha = RecaptchaField()