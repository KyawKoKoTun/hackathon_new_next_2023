from flask_sqlalchemy import SQLAlchemy
import datetime


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024), unique=True, nullable=False)
    email = db.Column(db.String(1024), unique=True, nullable=False)
    password = db.Column(db.String(1024), unique=False, nullable=False)
    token = db.Column(db.String(64), unique=False, nullable=False)
    chairs =  db.relationship('Chair', backref='user')


class Chair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    name = db.Column(db.String(1024), unique=False, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    safe = db.Column(db.Boolean, default=True)
    qr_code = db.Column(db.String(1024), unique=False, nullable=True)
    battery = db.Column(db.Integer, nullable=True)
    alarm_state = db.Column(db.Integer, nullable=True)
    lat = db.Column(db.Integer, nullable=True)
    lng = db.Column(db.Integer, nullable=True)
    bmp = db.Column(db.Integer, nullable=True)
    mmhg = db.Column(db.Integer, nullable=True)
    temp = db.Column(db.Integer, nullable=True)
    oxygen = db.Column(db.Integer, nullable=True)
    respiratory_rate = db.Column(db.Integer, nullable=True)


class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chair_hash =  db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.datetime.now())

    


