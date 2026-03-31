from app import create_app, db
from app.models.user import User
from app.models.task import Task
from app.models.checklist import Checklist
from app.models.user_task import UserTask
from werkzeug.security import generate_password_hash


app = create_app()

with app.app_context():
    user = User(
        nome="Professor Teste",
        email="prof@test.com",
        senha=generate_password_hash("123"),
        tipo="professor"
    )

    db.session.add(user)
    db.session.commit()