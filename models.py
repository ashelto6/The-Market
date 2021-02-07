from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
 id = db.Column(db.Integer, primary_key=True)
 last_name = db.Column(db.String(100))
 first_name = db.Column(db.String(100))
 email = db.Column(db.String(100), unique=True)
 password = db.Column(db.String(100))

#add database table for admin to gain access to data page



