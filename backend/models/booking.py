from extensions import db
from datetime import datetime


class Booking(db.Model):

    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    trek_id = db.Column(
        db.Integer,
        db.ForeignKey("treks.id"),
        nullable=False
    )

    booking_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    number_of_people = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    booking_status = db.Column(
        db.String(20),
        nullable=False,
        default="booked"
    )

    payment_status = db.Column(
        db.String(20),
        nullable=False,
        default="pending"
    )

    total_amount = db.Column(
        db.Float,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
