from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from app import db


class StatusEnum(enum.Enum):
    NAO_INICIADO = "nao_iniciado"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDO = "concluido"


class ProfessorTrilha(db.Model):
    __tablename__ = "professor_trilhas"

    id = Column(Integer, primary_key=True)
    professor_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    trilha_id = Column(Integer, ForeignKey('checklists.id'), nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.NAO_INICIADO, nullable=False)
    data_inicio = Column(DateTime, nullable=True)
    data_conclusao = Column(DateTime, nullable=True)
    
    # Relationships
    professor = relationship('User', foreign_keys=[professor_id], back_populates='professor_trilhas')
    trilha = relationship('Checklist', foreign_keys=[trilha_id])
