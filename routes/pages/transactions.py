from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from app import app, db
from flask import render_template, request, flash, redirect
from models import Member, Transaction
from middleware import login_required


# Show all transactions
# GET /transactions
@app.get("/transactions")
@login_required
def transactions():
    transactions = []
    search_type = request.args.get("type", "")
    search_query = request.args.get("query", "")
    if search_type and search_query:
        sql_query = ""
        if search_type == "book_name":
            sql_query = (
                "SELECT * FROM `transaction` WHERE book_id IN (SELECT id FROM `book` WHERE title LIKE '%"
                + search_query
                + "%')"
            )
        elif search_type == "book_isbn":
            sql_query = (
                "SELECT * FROM `transaction` WHERE book_id IN (SELECT id FROM `book` WHERE isbn LIKE '%"
                + search_query
                + "%') ORDER BY id DESC"
            )
        elif search_type == "member_name":
            sql_query = (
                "SELECT * FROM `transaction` WHERE member_id IN (SELECT id FROM `member` WHERE name LIKE '%"
                + search_query
                + "%')  ORDER BY id DESC"
            )
        elif search_type == "member_id":
            sql_query = "SELECT * FROM `transaction` WHERE member_id = " + search_query
        elif search_type == "member_email":
            sql_query = (
                "SELECT * FROM `transaction` WHERE member_id IN (SELECT id FROM `member` WHERE email LIKE '%"
                + search_query
                + "%')  ORDER BY id DESC"
            )
        elif search_type == "member_phone":
            sql_query = (
                "SELECT * FROM `transaction` WHERE member_id IN (SELECT id FROM `member` WHERE phone LIKE '%"
                + search_query
                + "%')  ORDER BY id DESC"
            )
        elif search_type == "transaction_id":
            sql_query = (
                "SELECT * FROM `transaction` WHERE id = "
                + search_query
                + "  ORDER BY id DESC"
            )
        transactions = Transaction.query.from_statement(text(sql_query)).all()
    else:
        # order by id desc
        transactions = Transaction.query.order_by(Transaction.id.desc()).all()
    return render_template("transactions/show.html", transactions=transactions)
