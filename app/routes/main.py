from flask import Blueprint, render_template, jsonify, request
from flask_login import current_user, login_required


main_bp = Blueprint('main', __name__)

@main_bp.route("/home")
@main_bp.route("/")
def Home():
    if current_user.is_authenticated:  # Use 2 Home Page :D
        return render_template("TaskList.html")
    else:
        return render_template("Home.html")


@main_bp.app_errorhandler(404)  # 404 Error
def NotFoundError(err):
    return render_template('Error.html'), 404
