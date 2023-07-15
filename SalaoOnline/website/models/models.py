from flask_login import UserMixin
from sqlalchemy.sql import func

from ..database import db

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10))
    # date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(300))
    name = db.Column(db.String(150))
    age = db.Column(db.Integer)
    phone = db.Column(db.String(20))
    type = db.Column(db.String(1))
    schedules = db.relationship('Schedule', backref='responsible', lazy=True)