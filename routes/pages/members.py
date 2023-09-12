from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from app import app, db
from flask import render_template, request, flash, redirect
from models import Member
from middleware import login_required

# Fetch all members from database
# GET /members
@app.get("/members")
@login_required
def members():
    search_type = request.args.get("type", "")
    search_query = request.args.get("query", "")
    members = []
    if search_type and search_query:
        members = Member.query.filter(text(search_type + " LIKE '%" + search_query + "%'")).all()
    else:
        members = Member.query.all()
    return render_template("members/show.html", members=members)

# Create a new member
# GET /members/new
# POST /members/new
@app.route("/members/new", methods=["GET", "POST"])
@login_required
def create_member():
    if request.method == "POST":
        name = request.form.get("name")
        address = request.form.get("address")
        phone = request.form.get("phone")
        email = request.form.get("email")

        try:
            member = Member(id=None, name=name, address=address, phone=phone, email=email)
            db.session.add(member)
            db.session.commit()
            flash("Member created successfully", "success")
        except IntegrityError:
            flash("Member with this email already exists", "danger")
        except:
            flash("Member could not be created", "danger")
    
    return render_template("members/new.html")

# Delete a member
# GET /members/<id>/delete
@app.get("/members/<int:id>/delete")
@login_required
def delete_member(id):
    member = Member.query.get(id)
    if member:
        try:
            db.session.delete(member)
            db.session.commit()
            flash("Member deleted successfully", "success")
        except:
            flash("Member could not be deleted", "danger")
    else:
        flash("Member not found", "danger")
    return redirect("/members")