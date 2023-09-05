from functools import wraps
from flask import request, redirect, url_for
import helpers

# Middleware to verify JWT token


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.cookies.get("token")
        print(token)
        if not token:
            # Redirect to login page if token is not present
            return redirect("/login")
        user_id = helpers.verify_jwt(token)
        if not user_id:
            # Redirect to login page if token is not valid
            return redirect("/login")
        return func(*args, **kwargs)
    return wrapper
