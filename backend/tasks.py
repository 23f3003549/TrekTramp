from celery_app import celery
from datetime import datetime


@celery.task(name="tasks.hello_task")
def hello_task():

    print("=" * 60)
    print("Hello TrekTramp!")
    print("Celery is working successfully.")
    print("Current Time :", datetime.now())
    print("=" * 60)

    return "Celery Working Successfully!"

from celery_app import celery

from datetime import date, timedelta

from flask_mail import Message

from extensions import mail

from models.trek import Trek
from models.booking import Booking
from models.user import User


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