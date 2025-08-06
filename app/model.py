from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(130), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    birthdays = db.relationship('Birthday', backref='user', lazy=True)
class Birthday(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    relationship = db.Column(db.String(50)) 