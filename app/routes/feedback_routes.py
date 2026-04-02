"""Feedback routes for professor submissions and manager/admin review."""

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models.user import RoleEnum
from app.services.feedback_service import FeedbackService


feedback = Blueprint('feedback', __name__)


def _payload():
    """Read JSON or form payload without duplicating parsing code."""
    data = request.get_json(silent=True)
    if data is None:
        data = request.form.to_dict()
    return data


def _serialize_feedback(item):
    """Convert feedback model data into a JSON-safe dictionary."""
    return {
        'id': item.id,
        'professor_id': item.professor_id,
        'trilha_id': item.trilha_id,
        'comentario': item.comentario,
        'data_envio': item.data_envio.isoformat() if item.data_envio else None,
    }


@feedback.route('/', methods=['POST'])
@login_required
def submit_feedback():
    """Let a professor submit feedback about a trilha or the process."""
    if current_user.role != RoleEnum.PROFESSOR:
        return jsonify({'error': 'Acesso negado'}), 403

    data = _payload()
    try:
        item = FeedbackService.submit_feedback(
            professor_id=current_user.id,
            comentario=data.get('comentario'),
            trilha_id=int(data['trilha_id']) if data.get('trilha_id') not in (None, '') else None,
        )
        return jsonify(_serialize_feedback(item)), 201
    except (ValueError, TypeError) as error:
        return jsonify({'error': str(error)}), 400


@feedback.route('/my-feedback', methods=['GET'])
@login_required
def my_feedback():
    """List all feedback submitted by the current professor."""
    if current_user.role != RoleEnum.PROFESSOR:
        return jsonify({'error': 'Acesso negado'}), 403

    items = FeedbackService.get_professor_feedback(current_user.id)
    return jsonify([_serialize_feedback(item) for item in items])


@feedback.route('/trilha/<int:trilha_id>', methods=['GET'])
@login_required
def trilha_feedback(trilha_id):
    """List feedback linked to one trilha for gestao/admin review."""
    if current_user.role not in (RoleEnum.GESTAO, RoleEnum.ADMIN):
        return jsonify({'error': 'Acesso negado'}), 403

    try:
        items = FeedbackService.get_trilha_feedback(trilha_id)
        return jsonify([_serialize_feedback(item) for item in items])
    except ValueError as error:
        return jsonify({'error': str(error)}), 400


@feedback.route('/', methods=['GET'])
@login_required
def all_feedback():
    """List all feedback entries; restricted to admin users."""
    if current_user.role != RoleEnum.ADMIN:
        return jsonify({'error': 'Acesso negado'}), 403

    items = FeedbackService.get_all_feedback()
    return jsonify([_serialize_feedback(item) for item in items])


@feedback.route('/<int:feedback_id>', methods=['DELETE'])
@login_required
def delete_feedback(feedback_id):
    """Delete one feedback entry; restricted to admin users."""
    if current_user.role != RoleEnum.ADMIN:
        return jsonify({'error': 'Acesso negado'}), 403

    try:
        FeedbackService.delete_feedback(feedback_id)
        return jsonify({'message': 'Feedback removido com sucesso'})
    except ValueError as error:
        return jsonify({'error': str(error)}), 400
