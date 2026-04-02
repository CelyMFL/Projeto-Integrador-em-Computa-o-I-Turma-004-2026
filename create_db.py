from app import create_app, db
from app.models.user import User
from app.models.task import Task
from app.models.checklist import Checklist
from app.models.user_task import UserTask
from app.models.professor_trilha import ProfessorTrilha
from app.models.professor_checklist import ProfessorChecklist
from app.models.feedback import Feedback

app = create_app()

with app.app_context():
    db.create_all()