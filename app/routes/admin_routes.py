from flask import Blueprint, render_template
from flask_login import login_required, current_user

admin = Blueprint('admin', __name__)

@admin.route('/')
@login_required
def home():
    if current_user.tipo != 'admin':
        return "Acesso negado", 403

    return render_template('admin.html', user=current_user)