from flask import Blueprint, render_template, request, redirect, url_for, session
from models.models import User, OTP
from extensions import db
import random
from app import login_user

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    phone_number = ''
    if request.method == 'POST':
        phone_number = request.form.get('phone_number', '')
        user = User.query.filter_by(phone_number=phone_number).first()
        if user:
            # Generowanie kodu OTP
            otp_code = f"{random.randint(100000, 999999)}"
            otp = OTP(otp_code=otp_code, user_id=user.id)
            db.session.add(otp)
            db.session.commit()
            # Wersja demo: wyświetl kod na stronie (w produkcji: wysyłka SMS)
            return render_template('login.html', phone_number=phone_number, otp_code=otp_code)
        else:
            error = "niepoprawny numer telefonu."
    return render_template('login.html', phone_number=phone_number, error=error)

@main.route('/verify', methods=['POST'])
def verify():
    phone_number = request.form.get('phone_number', '')
    code = request.form.get('code', '')
    user = User.query.filter_by(phone_number=phone_number).first()
    if user:
        otp = OTP.query.filter_by(user_id=user.id, otp_code=code).first()
        if otp:
            # Usuwamy kod po użyciu
            db.session.delete(otp)
            db.session.commit()
            login_user(user)
            return redirect(url_for('user.panel'))
        else:
            error = "Nieprawidłowy kod."
            return render_template('login.html', phone_number=phone_number, error=error)
    error = "Nie znaleziono użytkownika."
    return render_template('login.html', error=error)