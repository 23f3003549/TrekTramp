# models/trek_staff_assignment.py

from extensions import db
from datetime import datetime


class StaffAssign(db.Model):

    __tablename__ = "staff_assign"

    __table_args__ = (

    db.UniqueConstraint(
        "trek_id",
        "staff_id",
        name="unique_staff_trek_assignment"
    ),
)
    id = db.Column(db.Integer, primary_key=True)

    trek_id = db.Column(
        db.Integer,
        db.ForeignKey("treks.id"),
        nullable=False
    )

    staff_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    assigned_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

