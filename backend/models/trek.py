# models/trek.py

from extensions import db
from datetime import datetime


class Trek(db.Model):

    __tablename__ = "treks"
    id = db.Column(db.Integer, primary_key=True)
    trek_name = db.Column(db.String(150),nullable=False, index= True)
    location = db.Column( db.String(150),nullable=False, index = True)
    difficulty = db.Column( db.String(20), nullable=False, index = True) #hard, medium , easy
    max_age = db.Column(db.Integer)
    min_age = db.Column(db.Integer)
    duration_days = db.Column( db.Integer,nullable=False )
    description = db.Column( db.Text )
    max_slots = db.Column( db.Integer, nullable=False)
    available_slots = db.Column( db.Integer,nullable=False)
    price = db.Column( db.Float, default=0)
    status = db.Column( db.String(20), nullable=False, default="open", index = True) #open, closed,started, completed, cancelled
    start_date = db.Column( db.Date,nullable=False)
    end_date = db.Column( db.Date, nullable=False)
    created_at = db.Column( db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    bookings = db.relationship("Booking", backref="trek", lazy=True, cascade = "all, delete-orphan" )
    reviews = db.relationship("Review", backref="trek", lazy=True, cascade = "all, delete-orphan" )
    staff_assignments = db.relationship("StaffAssign", backref="trek", lazy=True, cascade = "all, delete-orphan")

