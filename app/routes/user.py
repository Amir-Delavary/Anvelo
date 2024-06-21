from flask import Blueprint, render_template, redirect, url_for, session, jsonify, request, flash, current_app, send_from_directory
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user, login_required, login_user, logout_user
from app.forms import ChangePasswordForm, ConfirmEmailForm
from werkzeug.utils import secure_filename
from app.config import allowed_file
from app.extensions import db
from app.models import User
import os
from datetime import datetime

user_bp = Blueprint('user', __name__)


@user_bp.route("/signup/ConfirmAccount", methods=['GET', 'POST'])
def ConfirmAccount():
    if not session.get('confirm_flag'):
        return redirect(url_for("auth.SignUp"))
    
    form = ConfirmEmailForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            token = form.confirm.data
            user_id = session.get('user_id')
            user = User.query.get(user_id)
            if user and token == user.token:
                if  datetime.utcnow() <= user.token_expiration:
                    login_user(user)
                    current_user.token = None
                    user.token_expiration = None
                    db.session.commit()
                    session.pop('confirm_flag', None)
                    return redirect(url_for('main.Home'))
                else:
                    db.session.query(User).filter_by(id = user.id).delete()
                    db.session.commit()
                    flash("Token has expired")
                    return redirect(url_for('auth.SignUp'))
            else:
                if user:
                    db.session.query(User).filter_by(id = user.id).delete()
                    db.session.commit()
                return redirect(url_for('auth.SignUp'))
            
    return render_template("Confirm.html", form=form)


@user_bp.route("/signup/cancel", methods=['POST', 'GET'])
def CancelAccount():
    if not session.get('confirm_flag'):
        return redirect(url_for("auth.SignUp"))
    
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if user:
        db.session.query(User).filter_by(id=user.id).delete()
        db.session.commit()
    session.pop('confirm_flag', None)
    return redirect(url_for('auth.SignUp'))



@user_bp.route("/panel")
@login_required
def Panel():
    return render_template("Panel.html")

@user_bp.route("/panel/password", methods=['GET','POST'])
@login_required
def Password():
    form = ChangePasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            last = form.last.data
            new = form.new.data
            if check_password_hash(current_user.password, last):
                current_user.password = generate_password_hash(new)  # Replace new password
                db.session.commit()

                flash("Password changed succesfuly")
                return redirect(url_for('user.Panel'))
            else:
                flash("Wrong password")
                return redirect(url_for('user.Password'))
            
    
    return render_template("Password.html", form=form)


@user_bp.route('/DeleteAccount', methods=['POST', 'GET'])
@login_required
def DeleteAccount():
    if request.method == 'POST':
        user = User.query.get(current_user.id)
        if user:
            db.session.delete(user)  # Delete user
            db.session.commit()
            logout_user()
            return redirect(url_for('main.Home'))
        else:
            return jsonify({"message": "User not found"}), 404

    return redirect(url_for('main.Home'))

# Photo Link
@user_bp.route('/uploads/<path:filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

# Photo Upload
@user_bp.route('/upload-avatar', methods=['POST'])
@login_required
def upload_avatar():
    if 'avatar' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'})

    file = request.files['avatar']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        current_user.avatar = f'/uploads/{filename}'
        db.session.commit()

        return jsonify({'success': True, 'avatarPath': f'/uploads/{filename}'})
    return jsonify({'success': False, 'message': 'File upload failed'})