from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from authsys_app import db



class User(db.Model):
    user_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    user_fname = db.Column(db.String(100))
    user_lname = db.Column(db.String(100))
    user_email = db.Column(db.String(100), unique=True)
    user_password=db.Column(db.String(200))
    user_regdate = db.Column(db.DateTime(), default=datetime.utcnow)
    confirmation_token = db.Column(db.String(100), nullable=True)