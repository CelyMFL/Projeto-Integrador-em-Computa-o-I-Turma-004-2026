from flask import Blueprint, render_template, request, redirect
from flask_login import login_user, logout_user
from app.models.user import User
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__)



## Login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.senha, senha):
            login_user(user)

            if user.tipo == 'admin':
                return redirect('/admin')
            else:
                return redirect('/checklist')

    return render_template('login.html')




## Logout route
@auth.route('/logout')
def logout():
    logout_user()
    return redirect('/login')