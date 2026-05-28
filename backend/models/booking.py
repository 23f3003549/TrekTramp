from extensions import db
from datetime import datetime


class Booking(db.Model):

    __tablename__ = "bookings"
    __table_args__ = (
        db.UniqueConstraint(
            "user_id","trek_id"
        ),
    )
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column( db.Integer, db.ForeignKey("users.id"),nullable=False)
    trek_id = db.Column( db.Integer,db.ForeignKey("treks.id"),nullable=False)
    booking_date = db.Column(db.DateTime,default=datetime.utcnow)
    booking_status = db.Column(db.String(20),nullable=False,default="booked") #booked, cancelled, rejected
    status_reason = db.Column(db.String(255))
    cancelled_by = db.Column(db.String(30)) #admin, staff, user
    payment_status = db.Column(db.String(20),nullable=False,default="pending" ) #pending,paid, refunded, failed
    total_amount = db.Column( db.Float, nullable=False)
    created_at = db.Column( db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default = datetime.utcnow, onupdate = datetime.utcnow)
