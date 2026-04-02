"""Auth routes for login and logout.

This module only handles authentication flow and role-based redirects.
The actual access rules live in the route/service layers.
"""

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from app.models.user import User, RoleEnum
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__)



## Login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Authenticate the user and redirect to the correct dashboard by role."""
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.senha, senha):
            login_user(user)

            if user.role == RoleEnum.ADMIN:
                return redirect(url_for('admin.home'))
            elif user.role == RoleEnum.GESTAO:
                return redirect(url_for('gestao.home'))
            else:
                return redirect(url_for('checklist.home'))

    return render_template('login.html')




## Logout route
@auth.route('/logout')
def logout():
    """End the current session and return the user to the login screen."""
    logout_user()
    return redirect('/login')