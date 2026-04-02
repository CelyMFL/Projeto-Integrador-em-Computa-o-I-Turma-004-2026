"""Checklist route used as the minimal professor landing page.

It shows all onboarding tasks and whether the current professor has
already completed each one.
"""

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from types import SimpleNamespace
from app.models.task import Task
from app.models.professor_checklist import ProfessorChecklist

checklist = Blueprint('checklist', __name__)

@checklist.route('/')
@login_required
def home():
    """Render a minimal task overview for the logged-in professor."""
    completed_ids = {
        item.task_id
        for item in ProfessorChecklist.query.filter_by(professor_id=current_user.id, concluido=True).all()
    }
    all_tasks = Task.query.order_by(Task.checklist_id, Task.ordem).all()
    user_tasks = [
        SimpleNamespace(
            descricao=task.descricao,
            status='concluído' if task.id in completed_ids else 'pendente',
        )
        for task in all_tasks
    ]

    return render_template(
        'checklist.html',
        user=current_user,
        tasks=user_tasks
    )
