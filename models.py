from app import db, app
import bcrypt
from datetime import datetime

# User model for authentication
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

# Book model
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
  transactions = db.relationship("Transaction", backref="book", cascade="all, delete")

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

# Member of the library
class Member(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(80), nullable=False)
  address = db.Column(db.String(200), nullable=False)
  phone = db.Column(db.String(80), nullable=False)
  email = db.Column(db.String(80), nullable=False, unique=True)
  transactions = db.relationship("Transaction", backref="member", cascade="all, delete")

  def __init__(self, id, name, address, phone, email):
    self.id = id
    self.name = name
    self.address = address
    self.phone = phone
    self.email = email

  def __repr__(self):
    return f"<Member {self.name}>"

  def to_json(self):
    return {
      "id": self.id,
      "name": self.name,
      "address": self.address,
      "phone": self.phone,
      "email": self.email
    }
  
  def get_outstanding_charges(self):
    # Fetch all pending transactions
    pending_transactions = Transaction.query.filter_by(member_id=self.id, is_returned=False).all()
    # Calculate total charges
    total_charges = 0
    for transaction in pending_transactions:
      total_charges += transaction.calculate_charges()
    return total_charges
  
# Transaction model
class Transaction(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  member_id = db.Column(db.Integer, db.ForeignKey("member.id"), nullable=False)
  book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
  count = db.Column(db.Integer, nullable=False, default=1)
  issue_date = db.Column(db.Date, nullable=False)
  is_returned = db.Column(db.Boolean, nullable=False, default=False)
  return_date = db.Column(db.Date, nullable=True)
  charges_paid = db.Column(db.Integer, nullable=True, default=0)

  def __init__(self, id, member_id, book_id, count, issue_date, return_date, charges_paid, is_returned=False):
    self.id = id
    self.member_id = member_id
    self.book_id = book_id
    self.count = count
    self.issue_date = issue_date
    self.return_date = return_date
    self.charges_paid = charges_paid
    self.is_returned = is_returned
    
  def __repr__(self):
    return f"<Transaction {self.id}>"

  def to_json(self):
    return {
      "id": self.id,
      "member_id": self.member_id,
      "book_id": self.book_id,
      "count": self.count,
      "issue_date": self.issue_date,
      "is_returned": self.is_returned,
      "return_date": self.return_date,
      "charges_paid": self.charges_paid
    }

  def calculate_charges(self):
    if self.is_returned:
      return self.charges_paid
    
    # Calculate no of days from issue date to current date
    days = (datetime.now().date() - self.issue_date).days
    # Calculate charges
    charges = 0
    # Normal rent charges
    charges += min(days, app.config["BOOK_RETURN_DEADLINE"]) * app.config["PER_DAY_RENT"] * self.count
    # Fine charges
    charges += max(days - app.config["BOOK_RETURN_DEADLINE"], 0) * app.config["PER_DAY_FINE"] * self.count

    return charges

  def return_book(self) -> bool:
    try:
      self.is_returned = True
      self.return_date = datetime.now().date()
      self.charges_paid = self.calculate_charges()
      db.session.commit()
      return True
    except:
      db.session.rollback()
      return False

