from flask import Blueprint, render_template, jsonify, request
from flask_login import current_user, login_required
from app.extensions import db
from app.models import User, Task

task_bp = Blueprint('task', __name__)


# Theme
@task_bp.route('/update-theme', methods=['POST'])
@login_required
def update_theme():
    data = request.get_json()
    theme = data.get('theme')
    if theme in ['light', 'dark']:
        current_user.theme = theme
        db.session.commit()
        return jsonify({"message": "Theme updated successfully!"}), 200
    else:
        return jsonify({"message": "Invalid theme"}), 400

@task_bp.route('/get-theme', methods=['GET'])
@login_required
def get_theme():
    return jsonify({"theme": current_user.theme}), 200




@task_bp.route('/current-user', methods=['GET'])
@login_required
def current_user_info():
    return jsonify({"id": current_user.id, "username": current_user.username}), 200



@task_bp.route('/save-task', methods=['POST'])
def save_task():
    data = request.get_json()
    user_id = current_user.id
    user = User.query.get(user_id)
    if user:
        new_task = Task(title=data['title'], description=data['description'], deadline=data['deadline'], user_id=user_id)
        db.session.add(new_task)
        db.session.commit()
        print("Task saved successfully")  # Log success
        return jsonify({"message": "Task saved successfully!", "task_id": new_task.id}), 201
    else:
        print("User not found")  # Log error
        return jsonify({"message": "User not found"}), 404


@task_bp.route('/update-task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    task = Task.query.get(task_id)
    if task:
        task.title = data['title']
        task.description = data['description']
        task.deadline = data['deadline']
        db.session.commit()
        return jsonify({"message": "Task updated successfully!"}), 200
    else:
        return jsonify({"message": "Task not found"}), 404
    


@task_bp.route('/delete-task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted successfully!"}), 200
    else:
        return jsonify({"message": "Task not found"}), 404
    

@task_bp.route('/mark-task-done/<int:task_id>', methods=['PUT'])
def mark_task_done(task_id):
    task = Task.query.get(task_id)
    if task:
        user = User.query.get(task.user_id)
        if user:
            user.tasks_done += 1  # Increment tasks_done for the user
            db.session.delete(task)
            db.session.commit()
            return jsonify({"message": "Task marked as done and deleted successfully!"}), 200
        else:
            return jsonify({"message": "User not found"}), 404
    else:
        return jsonify({"message": "Task not found"}), 404
    


@task_bp.route('/get-tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    tasks_list = []
    for task in tasks:
        tasks_list.append({"id": task.id, "title": task.title, "description": task.description, "deadline": task.deadline, "user_id": task.user_id})
    return jsonify(tasks_list), 200
