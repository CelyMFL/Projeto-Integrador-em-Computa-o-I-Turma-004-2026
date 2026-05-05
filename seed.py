from app import create_app, db
from app.models.user import User, RoleEnum
from app.models.task import Task
from app.models.checklist import Checklist
from werkzeug.security import generate_password_hash


app = create_app()

with app.app_context():
    # user = User(
    #     nome="Professor Teste",
    #     email="prof@test.com",
    #     senha=generate_password_hash("123"),
    #     role=RoleEnum.PROFESSOR
    # )

    admin = User(
        nome="Admin Teste",
        email="admin@test.com",
        senha=generate_password_hash("123"),
        role=RoleEnum.ADMIN
    )

    # db.session.add(user)
    db.session.add(admin)
    db.session.commit()