from ..extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
# Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(150))
    password = db.Column(db.String())
    admin = db.Column(db.Boolean(), default = False)
    avatar = db.Column(db.String,nullable=True, default='https://i.ibb.co/g9062qQ/free-user-icon-3296-thumb.png')
    token = db.Column(db.String(6), default='') # also you can use md5 hash of email for token field 
    token_expiration = db.Column(db.DateTime, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.now())
    tasks_done = db.Column(db.Integer, default=0)
    tasks_done = db.Column(db.Integer, default=0)
    theme = db.Column(db.String(7), default="light")  # فیلد جدید برای ذخیره تم
    tasks = db.relationship('Task', backref='author', lazy="dynamic", cascade='all, delete-orphan')
    
    def __init__(self, username, email, password, token, token_expiration, tasks_done, theme) -> None:
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.token = token
        self.token_expiration = token_expiration
        self.tasks_done = tasks_done
        self.theme = theme
