from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True )
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False)
    hash_password = db.Column(db.String(200), nullable = False)
    phone = db.Column(db.String(15), unique=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    role = db.Column(db.String(20), nullable = False, default = "trekker")
    status = db.Column(db.String(20), nullable = False, default = "active")
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    updated_at = db.Column(db.DateTime, default = datetime.utcnow, onupdate = datetime.utcnow)

    bookings = db.relationship("Booking", backref = "user", lazy = True, cascade = "all, delete")
    reviews = db.relationship("Review", backref = "user", lazy = True, cascade = "all, delete")
    staff_assignments = db.relationship("StaffAssign", backref="staff", lazy=True, foreign_keys="StaffAssign.staff_id", cascade = "all, delete")