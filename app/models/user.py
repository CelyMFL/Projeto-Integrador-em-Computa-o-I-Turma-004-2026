from sqlalchemy import Column, Integer, String, Enum
from flask_login import UserMixin
import enum
from app import db


class RoleEnum(enum.Enum):
    PROFESSOR = "professor"
    ADMIN = "admin"


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.PROFESSOR)

    # Relationships
    professor_trilhas = db.relationship('ProfessorTrilha', backref='professor_user', lazy=True)
    professor_checklists = db.relationship('ProfessorChecklist', backref='professor_user', lazy=True)
    feedbacks = db.relationship('Feedback', backref='professor_user', lazy=True)