from app import app, db
from flask import redirect, render_template, request
from models import User
from sqlalchemy import text
import helpers
from middleware import login_required


# Fetch all books from database
# GET /books
@login_required
@app.route("/books")
def books_index():
  books = db.session.execute(text("SELECT * FROM book")).fetchall()
  return render_template("books.html", books=books)

# Fetch a single book details from database
# GET /books/:id

