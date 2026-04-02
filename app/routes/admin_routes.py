"""Admin routes for dashboard access and aggregated metrics."""

from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app.models.user import RoleEnum
from app.models.user import User
from app.models.checklist import Checklist
from app.models.feedback import Feedback
from app.models.professor_trilha import ProfessorTrilha, StatusEnum

admin = Blueprint('admin', __name__)


def build_dashboard_metrics():
    """Build a compact set of metrics for the admin dashboard."""
    total_users = User.query.count()
    total_professores = User.query.filter_by(role=RoleEnum.PROFESSOR).count()
    total_gestao = User.query.filter_by(role=RoleEnum.GESTAO).count()
    total_trilhas = Checklist.query.count()
    total_obrigatorias = Checklist.query.filter_by(obrigatoria=True).count()
    total_feedbacks = Feedback.query.count()
    trilhas_concluidas = ProfessorTrilha.query.filter_by(status=StatusEnum.CONCLUIDO).count()

    return {
        'total_users': total_users,
        'total_professores': total_professores,
        'total_gestao': total_gestao,
        'total_trilhas': total_trilhas,
        'total_obrigatorias': total_obrigatorias,
        'total_feedbacks': total_feedbacks,
        'trilhas_concluidas': trilhas_concluidas,
    }

@admin.route('/')
@login_required
def home():
    """Render the admin dashboard template."""
    if current_user.role != RoleEnum.ADMIN:
        return "Acesso negado", 403

    return render_template('admin.html', user=current_user, metrics=build_dashboard_metrics())


@admin.route('/analytics')
@login_required
def analytics():
    """Expose the same dashboard metrics as JSON for future UI use."""
    if current_user.role != RoleEnum.ADMIN:
        return jsonify({'error': 'Acesso negado'}), 403

    return jsonify(build_dashboard_metrics())