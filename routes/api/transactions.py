from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from app import app, db
from flask import render_template, request, flash, redirect, jsonify
from models import Member, Transaction
from middleware import login_required
from datetime import datetime


# Get transaction return details
# GET /transactions/<int:transaction_id>/return/details
@app.get("/transactions/<int:transaction_id>/return/details")
@login_required
def initiate_return_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    days = (datetime.now().date() - transaction.issue_date).days
    return jsonify(
        {
            "id": transaction.id,
            "total_charges": transaction.calculate_charges(),
            "charge_details": {
                "normal_days": min(days, app.config["BOOK_RETURN_DEADLINE"]),
                "late_days": max(days - app.config["BOOK_RETURN_DEADLINE"], 0),
                "normal_charge": app.config["PER_DAY_RENT"],
                "late_charge": app.config["PER_DAY_FINE"],
                "normal_total_charge": min(days, app.config["BOOK_RETURN_DEADLINE"])
                * app.config["PER_DAY_RENT"]
                * transaction.count,
                "late_total_charge": max(days - app.config["BOOK_RETURN_DEADLINE"], 0)
                * app.config["PER_DAY_FINE"]
                * transaction.count,
            },
        }
    )


# Return transaction
# POST /transactions/<int:transaction_id>/return
@app.post("/transactions/<int:transaction_id>/return")
@login_required
def return_transaction(transaction_id):
    try:
        transaction = Transaction.query.get(transaction_id)
        status = transaction.return_book()
        if not status:
            return jsonify({"message": "Return failed !"}), 400
        return jsonify({"message": "Transaction returned successfully"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Something went wrong"}), 500
