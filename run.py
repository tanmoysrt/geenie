from app import app, db
from middleware import login_required
import os

# Database migrations
from models import User

with app.app_context():
    db.create_all()

# Import routes
import routes.pages.auth

@app.route("/")
@login_required
def index():
    return "Hello world!"

# Create default user
with app.app_context():
    if User.query.filter_by(username="admin").first() is None:
        user = User(name="Library Admin", username="admin")
        user.set_password("admin")
        db.session.add(user)
        db.session.commit()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", debug=True, port=port)