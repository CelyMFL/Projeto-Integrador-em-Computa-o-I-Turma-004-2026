from sqlalchemy import Column, Integer, String, ForeignKey
from app import db


class Task(db.Model):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    descricao = Column(String(255))
    ordem = Column(Integer, nullable=False, default=1)
    material_apoio = Column(String(255), nullable=True)
    link_apoio = Column(String(500), nullable=True)
    documento_apoio = Column(String(255), nullable=True)
    
    checklist_id = Column(Integer, ForeignKey('checklists.id'))
    checklist = db.relationship('Checklist', backref='tasks')