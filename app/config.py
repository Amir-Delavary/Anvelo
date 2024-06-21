import os
import secrets

class Config:

    SECRET_KEY = secrets.token_hex(16)
    SECURITY_PASSWORD_SALT = secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RECAPTCHA_PUBLIC_KEY = '6Le4avwpAAAAAF0v1ykopYO90eYs_Po453Y-djIq'
    RECAPTCHA_PRIVATE_KEY = '6Le4avwpAAAAAOOc2vaaXaEsfFy5FpCLkbk6zISO'
    
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'upload/avatar')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'afk.anvelo@gmail.com'
    MAIL_PASSWORD = 'nuwn zwwg znht aiei'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    SERVER_NAME = 'https://anvelo.onrender.com'


# app.config['SQLALCHEMY_BINDS'] = False


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

