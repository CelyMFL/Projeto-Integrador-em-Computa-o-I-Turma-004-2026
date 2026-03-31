from app.models import User
from app import db

def create_user(name, email):
    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    return user