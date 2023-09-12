from app import app, db
from flask import request, jsonify
from models import Book, Member, Transaction
import helpers
from middleware import login_required
import uuid
import math
import datetime

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

# POST /books/issue
@app.route("/books/issue", methods=["POST"])
@login_required
def issue_book():
    try:
        member_id = int(request.form["member_id"])
        book_id = int(request.form["book_id"])
        count = int(request.form["count"])

        # Check if member exists
        member = Member.query.filter_by(id=member_id).first()
        if not member:
            raise Exception("Member does not exist")
        
        # Check if book exists
        book = Book.query.filter_by(id=book_id).first()
        if not book:
            raise Exception("Book does not exist")
        
        # Check if any copy of the book is available
        if book.available_copies == 0:
            raise Exception("No copy of the book is available")
        
        # Check if count is greater than available copies
        if count > book.available_copies:
            raise Exception(f"Only {book.available_copies} copies of the book are available")
        
        # Check if member has outstanding charges more than the limit
        outstanding_charges = member.get_outstanding_charges()
        if outstanding_charges > app.config["OUTSTANDING_DEBT_LIMIT"]:
            outstanding_charges_rs = math.floor(outstanding_charges / 100)
            outstanding_charges_limit_rs = math.floor(app.config["OUTSTANDING_DEBT_LIMIT"] / 100)
            raise Exception(f"{member.name} has total {outstanding_charges_rs} Rs more than the limit of {outstanding_charges_limit_rs} Rs")
        
        # Update quantity of book
        book.available_copies = book.available_copies - count
        
        # Insert transaction details into database
        transaction = Transaction(
            id=None,
            member_id=member_id,
            book_id=book_id,
            count=count,
            issue_date=datetime.datetime.now().date(),
            return_date=None,
            is_returned=False,
            charges_paid=0
        )

        db.session.add(transaction)
        db.session.commit()

        return jsonify({
            "message": "Book issued successfully",
            "transaction_id": transaction.id
        }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500