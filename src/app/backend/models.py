from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)