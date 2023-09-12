from app import app, db

# Database migrations
from models import User, Book, Transaction, Member

def db_seed():
    # Create default user
    with app.app_context():
        if User.query.filter_by(username="admin").first() is None:
            user = User(name="Library Admin", username="admin", id=1, password="")
            user.set_password("admin")
            db.session.add(user)
            db.session.commit()