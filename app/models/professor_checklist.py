from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app import db


class ProfessorChecklist(db.Model):
    __tablename__ = "professor_checklists"

    id = Column(Integer, primary_key=True)
    professor_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    concluido = Column(Boolean, default=False)
    data_conclusao = Column(DateTime, nullable=True)
    
    # Relationships
    professor = relationship('User', foreign_keys=[professor_id])
    task = relationship('Task', foreign_keys=[task_id])
