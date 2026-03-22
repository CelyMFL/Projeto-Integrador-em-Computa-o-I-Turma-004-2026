from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.user_task import UserTask

checklist = Blueprint('checklist', __name__)

@checklist.route('/')
@login_required
def home():
    user_tasks = UserTask.query.filter_by(user_id=current_user.id).all()

    return render_template(
        'checklist.html',
        user=current_user,
        tasks=user_tasks
    )
