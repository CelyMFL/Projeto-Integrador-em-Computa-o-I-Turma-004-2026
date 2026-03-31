from sqlalchemy import Column, Integer, String, ForeignKey
from app import db


class Task(db.Model):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    descricao = Column(String(255))
    
    checklist_id = Column(Integer, ForeignKey('checklists.id'))
    checklist = db.relationship('Checklist', backref='tasks')