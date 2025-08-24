from flask import Flask, session
from extensions import db
from flask_migrate import Migrate
from main.views import main
from user.views import user
from models.models import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.secret_key = 'super_secret_key_change_me'  # Dodano klucz sesji

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(main)
app.register_blueprint(user)

# --- current_user context processor ---
@app.context_processor
def inject_current_user():
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return dict(current_user=user)

# --- login_user/logout_user helpers ---
def login_user(user):
    session['user_id'] = user.id

def logout_user():
    session.pop('user_id', None)

if __name__ == "__main__":
    app.run(debug=True)