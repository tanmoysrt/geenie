import os
from app import app, db
from flask import redirect, render_template, request, flash
from models import User, Book
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
import helpers
from middleware import login_required
from frappe_book import FrappeBook


# Fetch all books from database
# GET /books
@app.route("/books", methods=["GET"])
@login_required
def books_index():
    books = []
    search_type = request.args.get("type", "")
    search_query = request.args.get("query", "")
    if search_type and search_query:
        books = Book.query.filter(text(search_type + " LIKE '%" + search_query + "%'")).all()
    else:
        books = Book.query.all()
    return render_template("books/show.html", books=books)

# Add new book
# GET /books/new
# POST /books/new
@app.route("/books/new", methods=["GET", "POST"])
@login_required
def new_book():
    if request.method == "POST":
        try:
            title = request.form["title"]
            authors = request.form["authors"]
            isbn_code = request.form["isbn_code"]
            publisher = request.form["publisher"]
            num_pages = int(request.form["num_pages"])
            total_copies = int(request.form["total_copies"])
            cover_image = request.files["cover_image"]

            # Validate form data
            if not title or not authors or not isbn_code or not publisher or not num_pages or not total_copies or not cover_image:
                flash("All fields are required", "danger")
                return render_template("books/new.html")

            # Store the image in /static/media folder with a unique name with actual extension
            filename = helpers.generate_unique_filename(cover_image.filename)
            cover_image.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename))

            # Insert book details into database
            book = Book(
                id=None,
                title=title,
                authors=authors,
                isbn=isbn_code,
                publisher=publisher,
                num_pages=num_pages,
                total_copies=total_copies,
                available_copies=total_copies,
                cover_image=filename
            )
            db.session.add(book)
            db.session.commit()
            flash("Book added successfully", "success")
        except IntegrityError:
            flash("Book already exists !", "danger")
        except Exception as e:
            print(e)
            flash("Something went wrong", "danger")
        return redirect("/books/new")
    return render_template("books/new.html")

# Import book from Frappe API
# GET /books/import
@app.get("/books/import")
@login_required
def import_book():
    frappeBook = FrappeBook()
    books = []
    search_type = request.args.get("type", "")
    search_query = request.args.get("query", "")

    # If request is ajax, then fetch the page number from query string
    if request.is_ajax:
        page_no = int(request.args.get("page", 1))
        books = frappeBook.get_books(page_no=page_no, search_type=search_type,search_query=search_query)
        # if books is empty, then return 204 status code
        if len(books) == 0:
            return "", 204
        # return the partial html
        return render_template("partials/books_import_list.html", books=books)

    # If request is not ajax, then render the full html
    return render_template("books/import.html", books=books)

# Fetch a single book details from database
# GET /books/:id
@app.route("/books/<int:id>", methods=["GET"])
@login_required
def show_book(id):
    book = Book.query.get(id)
    return render_template("partials/books_details.html", book=book)