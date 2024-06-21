from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.validators import DataRequired

# Confirm Email
class ConfirmEmailForm(FlaskForm):
    confirm = StringField(validators=[DataRequired("Field is Empty !")])
