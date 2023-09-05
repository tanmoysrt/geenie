from app import db
import bcrypt

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
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

