from app import app, db
from flask import request, jsonify
from models import Book
import helpers
from middleware import login_required
import uuid

# POST /books/import
@app.route("/books/import", methods=["POST"])
@login_required
def import_books():
    try:
        title = request.form["title"]
        authors = request.form["authors"]
        isbn_code = request.form["isbn_code"]
        publisher = request.form["publisher"]
        num_pages = int(request.form["pages"])
        total_copies = int(request.form["copies"])
        img_url = request.form["img_url"]

        # Check if isbn_code already exists
        book = Book.query.filter_by(isbn=isbn_code).first()
        if book:
            return jsonify({"message": "Book already exists"}), 409
        
        # Download image from url
        filename = str(uuid.uuid4()) + ".png"
        helpers.download_image(img_url, filename)

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

        return jsonify({"message": "Book imported successfully"}), 200
    except:
        return jsonify({"message": "Failed to import book"}), 400
