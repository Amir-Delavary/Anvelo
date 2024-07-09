from flask_wtf import FlaskForm
from wtforms.fields import PasswordField
from wtforms.validators import DataRequired, length, EqualTo, Regexp


class ChangePasswordForm(FlaskForm):
    last = PasswordField(validators=[DataRequired("Password is Empty !")])
    new = PasswordField(validators=[DataRequired("NewPassword is Empty !"),length(min= 8, message="Password cant be reach less than 8 !")])
    confirm = PasswordField(validators=[DataRequired("ConfirmPassword is Empty !"),
                                        EqualTo('new', message="Password is not Confirm !"),
                                        Regexp(
            '^(?=.*[a-z])(?=.*[A-Z])(?=.*[_@]).*$',
            message="The password must contain 'a-z', 'A-Z' and '@' or '_'")])
