"""Gestao routes for lightweight operational visibility.

These endpoints expose summary metrics so the team can monitor onboarding
without needing a full UI in this phase.
"""

from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from app.models.user import RoleEnum, User
from app.models.checklist import Checklist
from app.models.feedback import Feedback
from app.models.professor_trilha import ProfessorTrilha, StatusEnum


gestao = Blueprint('gestao', __name__)


def build_gestao_metrics():
    """Build a short analytics snapshot for the gestao role."""
    return {
        'total_users': User.query.count(),
        'total_professores': User.query.filter_by(role=RoleEnum.PROFESSOR).count(),
        'total_gestao': User.query.filter_by(role=RoleEnum.GESTAO).count(),
        'total_trilhas': Checklist.query.count(),
        'total_obrigatorias': Checklist.query.filter_by(obrigatoria=True).count(),
        'total_feedbacks': Feedback.query.count(),
        'trilhas_concluidas': ProfessorTrilha.query.filter_by(status=StatusEnum.CONCLUIDO).count(),
    }


@gestao.route('/')
@login_required
def home():
    """Return the current gestao dashboard payload as JSON."""
    if current_user.role not in (RoleEnum.GESTAO, RoleEnum.ADMIN):
        return jsonify({'error': 'Acesso negado'}), 403

    return jsonify({
        'role': current_user.role.value,
        'user': {
            'id': current_user.id,
            'nome': current_user.nome,
            'email': current_user.email,
        },
        'metrics': build_gestao_metrics(),
    })


@gestao.route('/analytics')
@login_required
def analytics():
    """Return gestao metrics as JSON for reports or a future UI."""
    if current_user.role not in (RoleEnum.GESTAO, RoleEnum.ADMIN):
        return jsonify({'error': 'Acesso negado'}), 403

    return jsonify(build_gestao_metrics())
