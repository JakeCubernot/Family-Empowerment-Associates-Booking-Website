from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')

class Room(db.Model, UserMixin):
    name = db.Column(db.String(100), primary_key=True)

class Therapist(db.Model, UserMixin):
    therapist_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    email = db.Column(db.String(150),db.ForeignKey('user.email'))
    password = db.Column(db.String(150), db.ForeignKey('user.password'))
    first_name = db.Column(db.String(150), db.ForeignKey('user.first_name'))

class Admin(db.Model, UserMixin):
    admin_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    email = db.Column(db.String(150), db.ForeignKey('user.email'))