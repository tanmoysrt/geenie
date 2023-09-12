from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Create Flask app
app = Flask(__name__)

# App configurations
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static/media")
app.config["PER_DAY_RENT"] = int(os.getenv("PER_DAY_RENT", 10)) # paisa
app.config["BOOK_RETURN_DEADLINE"] = int(os.getenv("BOOK_RETURN_DEADLINE", 7)) # days
app.config["PER_DAY_FINE"] = int(os.getenv("PER_DAY_FINE", 200)) # paisa
app.config["OUTSTANDING_DEBT_LIMIT"] = int(os.getenv("OUTSTANDING_DEBT_LIMIT", 50000)) # paisa

# secret_key
app.secret_key = os.getenv("SECRET_KEY")

# Set up database
db = SQLAlchemy()
db.init_app(app)