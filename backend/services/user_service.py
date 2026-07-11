from werkzeug.security import generate_password_hash
from extensions import db
from datetime import datetime


from models.user import User
from models.trek import Trek
from models.staff_assign import StaffAssign
from models.booking import Booking
from models.review import Review

# ------------------------- Dashboard Statistics -------------------------

def dashboard_statistics(user_id):

    user = User.query.filter_by(

        id=user_id,

        role="trekker"

    ).first()

    if user is None:

        return {

            "message": "User not found."

        }, 404

    upcoming_bookings = (
        Booking.query
        .join(Trek, Booking.trek_id == Trek.id)
        .filter(

            Booking.user_id == user.id,

            Booking.booking_status == "booked",

            Trek.status.in_(["open", "started"]),

            Trek.is_deleted == False

        )
        .count()
    )

    completed_treks = Booking.query.filter_by(

        user_id=user.id,

        booking_status="completed"

    ).count()

    reviews_given = Review.query.filter_by(

        user_id=user.id

    ).count()

    return {

        "statistics": {

            "upcoming_bookings": upcoming_bookings,

            "completed_treks": completed_treks,

            "reviews_given": reviews_given

        }

    }, 200

# ------------------------- Browse Treks -------------------------

def browse_treks():

    treks = Trek.query.filter(

        Trek.is_deleted == False,

        Trek.status == "open"

    ).order_by(

        Trek.start_date.asc()

    ).all()

    trek_list = []

    for trek in treks:

        trek_list.append({

            "id": trek.id,

            "trek_name": trek.trek_name,

            "location": trek.location,

            "difficulty": trek.difficulty,

            "duration_days": trek.duration_days,

            "price": trek.price,

            "available_slots": trek.available_slots,

            "max_slots": trek.max_slots,

            "start_date": trek.start_date.isoformat(),

            "end_date": trek.end_date.isoformat(),

            "description": trek.description

        })

    return {

        "treks": trek_list

    }, 200

# ------------------------- Book Trek -------------------------

def book_trek(user_id, trek_id):

    user = User.query.filter_by(

        id=user_id,

        role="trekker"

    ).first()

    if user is None:

        return {

            "message":"User not found."

        },404


    trek = Trek.query.filter_by(

        id=trek_id,

        is_deleted=False

    ).first()

    if trek is None:

        return{

            "message":"Trek not found."

        },404


    if trek.status!="open":

        return{

            "message":"Booking is allowed only for open treks."

        },400
    
    if (not user.phone or user.age is None or not user.gender): 
        return{
            "message":
            "Please complete your profile before booking."
        },400
    
    if(user.age < trek.min_age or user.age > trek.max_age ):
        return{
            "message":"You are not eligible for this trek due to age restriction."
        }, 400
    
    existing_booking = Booking.query.filter_by(

        user_id=user.id,

        trek_id=trek.id

    ).first()

    if existing_booking:

         if existing_booking.booking_status in [

            "booked",

            "completed"

        ]:
             return{

                "message":

                "You have already booked this trek."

            },409
         
         if existing_booking.booking_status == "cancelled":

            existing_booking.booking_date = datetime.utcnow()

            existing_booking.booking_status = "booked"

            existing_booking.payment_status = "pending"

            existing_booking.cancelled_by = None

            existing_booking.status_reason = None

            existing_booking.total_amount = trek.price

            trek.available_slots -= 1

            db.session.commit()

            return{

                "message":"Trek booked successfully.",

                "booking":{

                    "booking_id":existing_booking.id,

                    "trek_name":trek.trek_name,

                    "booking_status":existing_booking.booking_status,

                    "payment_status":existing_booking.payment_status,

                    "total_amount":existing_booking.total_amount

                }
             }, 200

        
    
    if trek.available_slots<=0:

        return{

            "message":"No slots available."

        },400
    

    booking = Booking(

        user_id=user.id,

        trek_id=trek.id,

        total_amount=trek.price,

        booking_status="booked",

        payment_status="pending"

    )
    trek.available_slots-=1

    db.session.add(booking)

    db.session.commit()

    return{

        "message":"Trek booked successfully.",

        "booking":{

            "booking_id":booking.id,

            "trek_name":trek.trek_name,

            "payment_status":booking.payment_status,

            "booking_status":booking.booking_status,

            "total_amount":booking.total_amount

        }

    },201