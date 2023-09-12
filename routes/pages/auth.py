from app import app, db
from flask import redirect, render_template, request
from models import User
from sqlalchemy import text
import helpers

# Login page
# GET /login
# POST /login
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # Check if username exists
        user = User.query.filter_by(username=username).first()
        if user:
            if user.verify_password(password):
                # Generate random session token
                token = helpers.generate_jwt(user.id)
                response = app.make_response(redirect("/"))
                # Set jwt token in cookie
                response.set_cookie("token", token)
                return response
        error = "Invalid username or password"

    return render_template("login.html", error=error)

# Logout page
# GET /logout
@app.route("/logout")
def logout():
    response = app.make_response(redirect("/login"))
    # Remove jwt token from cookie
    response.set_cookie("token", "", expires=0)
    return response