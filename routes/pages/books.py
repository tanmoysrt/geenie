from app import app, db
from flask import redirect, render_template, request
from models import User
from sqlalchemy import text
import helpers
from middleware import login_required


# Fetch all books from database
# GET /books
@login_required
@app.route("/books", methods=["GET"])
def books_index():
  books = db.session.execute(text("SELECT * FROM book")).fetchall()
  return render_template("books/show.html", books=books)

# Fetch a single book details from database
# GET /books/:id

# Add new book
# GET /books/new
# POST /books/new
@login_required
@app.route("/books/new", methods=["GET", "POST"])
def new_book():
  return render_template("books/new.html")

# Import book from Frappe API 
# GET /books/import
# POST /books/import
@login_required
@app.route("/books/import", methods=["GET", "POST"])
def import_book():
  return render_template("books/import.html")