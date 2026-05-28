# models/review.py

from extensions import db
from datetime import datetime


class Review(db.Model):

    __tablename__ = "reviews"
    __table_args__ = (

    db.UniqueConstraint(
        "user_id",
        "trek_id",
        name="unique_user_trek_review"
    ),)

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

    rating = db.Column(
        db.Integer,
        nullable=False
    )

    comment = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

