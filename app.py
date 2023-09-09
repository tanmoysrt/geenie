from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Create Flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static/media")
# secret_key
app.secret_key = os.getenv("SECRET_KEY")

# Set up database
db = SQLAlchemy()
db.init_app(app)