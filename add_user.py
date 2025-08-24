from app import app
from extensions import db
from models.models import User

if __name__ == "__main__":
    with app.app_context():
        user = User(phone_number="234567890", points=100)
        db.session.add(user)
        db.session.commit()
        print("Dodano użytkownika testuser")
