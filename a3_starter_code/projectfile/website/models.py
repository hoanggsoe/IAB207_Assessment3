from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(150), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    street_address = db.Column(db.Text, nullable=False)
    
    comments = db.relationship('Comment', backref='user')
    orders = db.relationship('Order', backref='user')
    events = db.relationship('Event', backref='creator')

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    venue = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(400), nullable=True, default='default_event.jpg')
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    tickets_available = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    comments = db.relationship('Comment', backref='event', cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='event')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
