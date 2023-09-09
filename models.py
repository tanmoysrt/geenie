from app import db
import bcrypt
from flask_sqlalchemy.extension import Model

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(80), nullable=False)
  username = db.Column(db.String(80), nullable=False)
  password = db.Column(db.String(80), nullable=False)

  def __init__(self, id, name, username, password):
    self.id = id
    self.name = name
    self.username = username
    self.password = password

  def __repr__(self):
    return f"<User {self.username}>"
  
  def set_password(self, password):
    self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
  
  def verify_password(self, password):
    return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))


class Book(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  cover_image = db.Column(db.String(80), nullable=False)
  title = db.Column(db.String(80), nullable=False)
  authors = db.Column(db.String(80), nullable=False)
  publisher = db.Column(db.String(80), nullable=False)
  isbn = db.Column(db.String(80), nullable=False, unique=True)
  num_pages = db.Column(db.Integer, nullable=False)
  total_copies = db.Column(db.Integer, nullable=False)
  available_copies = db.Column(db.Integer, nullable=False)

  def __init__(self, id, title, authors, publisher, isbn, num_pages, total_copies, available_copies, cover_image):
    self.id = id
    self.title = title
    self.authors = authors
    self.publisher = publisher
    self.isbn = isbn
    self.num_pages = num_pages
    self.total_copies = total_copies
    self.available_copies = available_copies
    self.cover_image = cover_image

  def __repr__(self):
    return f"<Book {self.title}>"