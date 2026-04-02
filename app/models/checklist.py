from sqlalchemy import Column, Integer, String, Boolean, Enum
import enum
from app import db


class TipoEnum(enum.Enum):
    PEDAGOGICA = "pedagógica"
    INSTITUCIONAL = "institucional"
    TECNOLOGICA = "tecnológica"


class Checklist(db.Model):
    __tablename__ = "checklists"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255))
    tipo = Column(Enum(TipoEnum), nullable=False, default=TipoEnum.PEDAGOGICA)
    obrigatoria = Column(Boolean, default=False)