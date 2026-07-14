import csv
import os
from flask_mail import Message

from extensions import mail, db
from celery_app import celery
from datetime import datetime, date , timedelta
from sqlalchemy import extract

from models.user import User
from models.booking import Booking
from models.trek import Trek
from models.staff_assign import StaffAssign



@celery.task(name="tasks.hello_task")
def hello_task():

    print("=" * 60)
    print("Hello TrekTramp!")
    print("Celery is working successfully.")
    print("Current Time :", datetime.now())
    print("=" * 60)

    return "Celery Working Successfully!"


#------------------------daily reminder--------------

@celery.task(name="tasks.daily_trek_reminder")
def daily_trek_reminder():

    tomorrow = date.today() + timedelta(days=1)

    treks = Trek.query.filter(
        Trek.start_date == tomorrow,
        Trek.status == "open",
        Trek.is_deleted == False
    ).all()

    total_sent = 0

    for trek in treks:

        bookings = Booking.query.filter(
            Booking.trek_id == trek.id,
            Booking.booking_status == "booked",
            Booking.payment_status == "paid"
        ).all()

        for booking in bookings:

            user = User.query.get(booking.user_id)

            if user is None:
                continue

            if user.status != "active":
                continue

            try:

                msg = Message(

                    subject=f"Reminder: {trek.trek_name} starts tomorrow!",

                    recipients=[user.email]

                )

                msg.body = f"""
Hello {user.name},

Your trek is almost here!

Trek Name : {trek.trek_name}

Location : {trek.location}

Start Date : {trek.start_date}

End Date : {trek.end_date}

Please reach the reporting location on time.

Carry:

• Government ID
• Water Bottle
• Trek Shoes
• Raincoat (if required)
• Basic Medicines

Have a wonderful trekking experience!

Team TrekTramp
"""

                mail.send(msg)

                total_sent += 1

            except Exception as e:

                print(e)

    return f"{total_sent} reminder emails sent."


#_--------------------------------------Booking History-----------

@celery.task(name="tasks.export_booking_history")
def export_booking_history(user_id):

    user = User.query.get(user_id)

    if user is None:
        return "User not found."

    bookings = (
        Booking.query
        .join(Trek)
        .filter(Booking.user_id == user.id)
        .order_by(Trek.start_date.asc())
        .all()
    )

    filename = f"booking_history_{user.id}.csv"

    filepath = os.path.join("exports", filename)

    os.makedirs("exports", exist_ok=True)

    with open(filepath, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Booking ID",
            "Trek Name",
            "Location",
            "Difficulty",
            "Start Date",
            "End Date",
            "Booking Status",
            "Payment Status",
            "Amount"
        ])

        for booking in bookings:

            trek = Trek.query.get(booking.trek_id)

            writer.writerow([
                booking.id,
                trek.trek_name,
                trek.location,
                trek.difficulty,
                trek.start_date,
                trek.end_date,
                booking.booking_status,
                booking.payment_status,
                booking.total_amount
            ])

    msg = Message(

        subject="Your Trek Booking History",

        recipients=[user.email]

    )

    msg.body = f"""
Hello {user.name},

Your booking history has been generated successfully.

Please find the attached CSV file.

Thank you,
Team TrekTramp
"""

    with open(filepath, "rb") as file:

        msg.attach(

            filename,

            "text/csv",

            file.read()

        )

    mail.send(msg)

    return "Booking history exported successfully."

#------------------------monthly report------------
@celery.task(name="tasks.monthly_admin_report")
def monthly_admin_report():

    # ---------------- Dashboard ----------------

    total_treks = Trek.query.filter_by(
        is_deleted=False
    ).count()

    total_users = User.query.filter_by(
        role="trekker"
    ).count()

    total_staff = User.query.filter_by(
        role="staff"
    ).count()

    total_bookings = Booking.query.count()

    # ---------------- Booking Statistics ----------------

    booked = Booking.query.filter_by(
        booking_status="booked"
    ).count()

    completed = Booking.query.filter_by(
        booking_status="completed"
    ).count()

    cancelled = Booking.query.filter_by(
        booking_status="cancelled"
    ).count()

    # ---------------- Payment Statistics ----------------

    paid = Booking.query.filter_by(
        payment_status="paid"
    ).count()

    pending = Booking.query.filter_by(
        payment_status="pending"
    ).count()

    refunded = Booking.query.filter_by(
        payment_status="refunded"
    ).count()

    # ---------------- Revenue ----------------

    revenue = 0

    for booking in Booking.query.filter_by(
        payment_status="paid"
    ).all():

        trek = Trek.query.get(
            booking.trek_id
        )

        if trek:

            revenue += trek.price

    # ---------------- Popular Treks ----------------

    trek_stats = []

    treks = Trek.query.filter_by(
        is_deleted=False
    ).all()

    for trek in treks:

        count = Booking.query.filter_by(
            trek_id=trek.id
        ).count()

        trek_stats.append(
            (trek.trek_name, count)
        )

    trek_stats.sort(
        key=lambda x: x[1],
        reverse=True
    )

    # ---------------- HTML ----------------

    html = f"""
    <html>
    <body>

    <h2>TrekTramp Monthly Activity Report</h2>

    <hr>

    <h3>Dashboard</h3>

    <ul>
        <li>Total Treks : {total_treks}</li>
        <li>Total Users : {total_users}</li>
        <li>Total Staff : {total_staff}</li>
        <li>Total Bookings : {total_bookings}</li>
        <li>Total Revenue : ₹{revenue}</li>
    </ul>

    <h3>Booking Statistics</h3>

    <ul>
        <li>Booked : {booked}</li>
        <li>Completed : {completed}</li>
        <li>Cancelled : {cancelled}</li>
    </ul>

    <h3>Payment Statistics</h3>

    <ul>
        <li>Paid : {paid}</li>
        <li>Pending : {pending}</li>
        <li>Refunded : {refunded}</li>
    </ul>

    <h3>Top 5 Popular Treks</h3>

    <ol>
    """

    for trek_name, count in trek_stats[:5]:

        html += f"<li>{trek_name} ({count} bookings)</li>"

    html += """

    </ol>

    <hr>

    <p>
    This report was generated automatically by TrekTramp.
    </p>

    </body>
    </html>

    """

    # ---------------- Send Mail ----------------

    msg = Message(

        subject="TrekTramp Monthly Activity Report",

        recipients=["23f3003549@ds.study.iitm.ac.in"]

    )

    msg.html = html

    mail.send(msg)

    return "Monthly report sent successfully."

#-----------------------------Automatic Booking Cancellation--------------------
@celery.task(name="tasks.auto_cancel_pending_bookings")
def auto_cancel_pending_bookings():

    expiry_time = datetime.utcnow() - timedelta(minutes=15)

    bookings = Booking.query.filter(

        Booking.booking_status == "booked",

        Booking.payment_status == "pending",

        Booking.created_at <= expiry_time

    ).all()

    cancelled = 0

    for booking in bookings:

        trek = Trek.query.get(

            booking.trek_id

        )

        user = User.query.get(

            booking.user_id

        )

        if trek is None or user is None:

            continue

        # ---------------- Cancel Booking ----------------

        booking.booking_status = "cancelled"

        booking.payment_status = "failed"

        booking.cancelled_by = "system"

        booking.status_reason = "Payment not completed within 15 minutes."

        # ---------------- Release Slot ----------------

        if trek.available_slots < trek.max_slots:

            trek.available_slots += 1

        cancelled += 1

        # ---------------- Send Email ----------------

        try:

            msg = Message(

                subject="Booking Cancelled",

                recipients=[user.email]

            )

            msg.body = f"""
Hello {user.name},

Your booking for

{trek.trek_name}

has been cancelled because payment was not completed within 15 minutes.

You may book the trek again if slots are available.

Team TrekTramp
"""

            mail.send(msg)

        except Exception as e:

            print(e)

    db.session.commit()

    return f"{cancelled} booking(s) cancelled."