from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app import db


class Feedback(db.Model):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True)
    professor_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    trilha_id = Column(Integer, ForeignKey('checklists.id'), nullable=True)
    comentario = Column(Text, nullable=False)
    data_envio = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    professor = relationship('User', foreign_keys=[professor_id], back_populates='feedbacks')
    trilha = relationship('Checklist', foreign_keys=[trilha_id])
