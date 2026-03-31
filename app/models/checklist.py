from sqlalchemy import Column, Integer, String
from app import db


class Checklist(db.Model):
    __tablename__ = "checklists"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    descricao = Column(String(255))