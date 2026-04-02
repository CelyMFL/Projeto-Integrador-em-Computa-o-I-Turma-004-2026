"""Routes for trilhas, progress tracking, and task creation.

The goal is to keep the UI minimal and expose predictable JSON payloads
for a future front-end to consume.
"""

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models.user import RoleEnum
from app.models.checklist import TipoEnum
from app.services.trilha_service import TrilhaService
from app.services.professor_trilha_service import ProfessorTrilhaService
from app.services.task_service import TaskService


trilhas = Blueprint('trilhas', __name__)


def _payload():
    """Read JSON or form data with the same code path."""
    data = request.get_json(silent=True)
    if data is None:
        data = request.form.to_dict()
    return data


def _serialize_task(task):
    """Convert a task model into a small JSON-safe dictionary."""
    return {
        'id': task.id,
        'descricao': task.descricao,
        'ordem': task.ordem,
    }


def _serialize_trilha(trilha):
    """Convert a trilha and its tasks into a JSON-friendly payload."""
    return {
        'id': trilha.id,
        'nome': trilha.nome,
        'descricao': trilha.descricao,
        'tipo': trilha.tipo.value if trilha.tipo else None,
        'obrigatoria': trilha.obrigatoria,
        'tasks': [_serialize_task(task) for task in sorted(trilha.tasks, key=lambda item: item.ordem)],
    }


@trilhas.route('/', methods=['GET'])
@login_required
def list_trilhas():
    """List all trilhas available in the system."""
    trilhas_data = TrilhaService.list_trilhas()
    return jsonify([_serialize_trilha(trilha) for trilha in trilhas_data])


@trilhas.route('/<int:trilha_id>', methods=['GET'])
@login_required
def get_trilha(trilha_id):
    """Return one trilha with its ordered task list."""
    trilha = TrilhaService.get_trilha(trilha_id)
    if not trilha:
        return jsonify({'error': 'Trilha não encontrada'}), 404
    return jsonify(_serialize_trilha(trilha))


@trilhas.route('/', methods=['POST'])
@login_required
def create_trilha():
    """Create a new trilha; restricted to admin users."""
    if current_user.role != RoleEnum.ADMIN:
        return jsonify({'error': 'Acesso negado'}), 403

    data = _payload()
    tipo_value = data.get('tipo', TipoEnum.PEDAGOGICA.value)
    tipo = next((item for item in TipoEnum if item.value == tipo_value), None)

    try:
        trilha = TrilhaService.create_trilha(
            nome=data.get('nome'),
            descricao=data.get('descricao', ''),
            tipo=tipo,
            obrigatoria=str(data.get('obrigatoria', 'false')).lower() in ('true', '1', 'sim', 'yes'),
        )
        return jsonify(_serialize_trilha(trilha)), 201
    except ValueError as error:
        return jsonify({'error': str(error)}), 400


@trilhas.route('/<int:trilha_id>', methods=['PUT', 'PATCH'])
@login_required
def update_trilha(trilha_id):
    """Update trilha metadata; restricted to admin users."""
    if current_user.role != RoleEnum.ADMIN:
        return jsonify({'error': 'Acesso negado'}), 403

    data = _payload()
    tipo = None
    if data.get('tipo') is not None:
        tipo = next((item for item in TipoEnum if item.value == data.get('tipo')), None)

    obrigatoria = None
    if data.get('obrigatoria') is not None:
        obrigatoria = str(data.get('obrigatoria')).lower() in ('true', '1', 'sim', 'yes')

    try:
        trilha = TrilhaService.update_trilha(
            trilha_id=trilha_id,
            nome=data.get('nome'),
            descricao=data.get('descricao'),
            tipo=tipo,
            obrigatoria=obrigatoria,
        )
        return jsonify(_serialize_trilha(trilha))
    except ValueError as error:
        return jsonify({'error': str(error)}), 400


@trilhas.route('/<int:trilha_id>', methods=['DELETE'])
@login_required
def delete_trilha(trilha_id):
    """Delete a trilha and its tasks; restricted to admin users."""
    if current_user.role != RoleEnum.ADMIN:
        return jsonify({'error': 'Acesso negado'}), 403

    try:
        TrilhaService.delete_trilha(trilha_id)
        return jsonify({'message': 'Trilha removida com sucesso'})
    except ValueError as error:
        return jsonify({'error': str(error)}), 400


@trilhas.route('/<int:trilha_id>/start', methods=['POST'])
@login_required
def start_trilha(trilha_id):
    """Register the current professor in a trilha."""
    if current_user.role != RoleEnum.PROFESSOR:
        return jsonify({'error': 'Acesso negado'}), 403

    try:
        enrollment = ProfessorTrilhaService.start_trilha(current_user.id, trilha_id)
        return jsonify({
            'message': 'Trilha iniciada com sucesso',
            'status': enrollment.status.value,
            'trilha_id': enrollment.trilha_id,
        }), 201
    except ValueError as error:
        return jsonify({'error': str(error)}), 400


@trilhas.route('/<int:trilha_id>/progress', methods=['GET'])
@login_required
def trilha_progress(trilha_id):
    """Return progress data for the current professor in one trilha."""
    if current_user.role != RoleEnum.PROFESSOR:
        return jsonify({'error': 'Acesso negado'}), 403

    try:
        progress = ProfessorTrilhaService.get_trilha_progress(current_user.id, trilha_id)
        return jsonify(progress)
    except ValueError as error:
        return jsonify({'error': str(error)}), 400


@trilhas.route('/<int:trilha_id>/tasks', methods=['POST'])
@login_required
def add_task(trilha_id):
    """Create a task under a trilha; restricted to admin users."""
    if current_user.role != RoleEnum.ADMIN:
        return jsonify({'error': 'Acesso negado'}), 403

    data = _payload()
    try:
        task = TaskService.create_task(
            checklist_id=trilha_id,
            descricao=data.get('descricao'),
            ordem=int(data['ordem']) if data.get('ordem') not in (None, '') else None,
        )
        return jsonify(_serialize_task(task)), 201
    except (ValueError, TypeError) as error:
        return jsonify({'error': str(error)}), 400
