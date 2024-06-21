from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from app.models.User import User
    return User.query.get(int(user_id))