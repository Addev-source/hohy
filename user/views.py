from flask import Blueprint, render_template, session, redirect, url_for
from models.models import User
from app import logout_user

user = Blueprint('user', __name__, template_folder='templates')

@user.route('/panel')
def panel():
    if not session.get('user_id'):
        return redirect(url_for('main.login'))
    return render_template('panel.html')

@user.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))