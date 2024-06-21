from flask import Blueprint

main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
user_bp = Blueprint('user', __name__)
task_bp = Blueprint('task', __name__)
