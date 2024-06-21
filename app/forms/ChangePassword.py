from flask_wtf import FlaskForm
from wtforms.fields import PasswordField
from wtforms.validators import DataRequired, length, EqualTo


class ChangePasswordForm(FlaskForm):
    last = PasswordField(validators=[DataRequired("Password is Empty !")])
    new = PasswordField(validators=[DataRequired("NewPassword is Empty !"),length(min= 8, message="Password cant be reach less than 8 !")])
    confirm = PasswordField(validators=[DataRequired("ConfirmPassword is Empty !"), EqualTo('new', message="Password is not Confirm !")])
