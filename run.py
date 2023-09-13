from flask import redirect, request
from app import app, db
from middleware import login_required
import os

# Database migrations
from models import User, Book, Transaction, Member
from seed import db_seed

with app.app_context():
    db.create_all()


# Register is_ajax middleware
@app.before_request
def ajax_request_check():
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        request.is_ajax = True
    else:
        request.is_ajax = False


# Import routes
import routes.pages.auth
import routes.pages.books
import routes.pages.members
import routes.pages.transactions
import routes.api.books
import routes.api.transactions

# Seed database
db_seed()


# Default route / to /books
@app.route("/")
@login_required
def index():
    return redirect("/books")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", debug=True, port=port)
