from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app import db


class UserTask(db.Model):
    __tablename__ = "user_tasks"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'))
    task_id = Column(Integer, ForeignKey('tasks.id'))

    status = Column(String(20), default="pendente")
    data_conclusao = Column(DateTime, nullable=True)

    user = relationship('User', backref='user_tasks')
    task = relationship('Task')