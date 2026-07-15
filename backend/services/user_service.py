from werkzeug.security import generate_password_hash
from extensions import db, cache
from datetime import datetime, date


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

from sqlalchemy import or_

# ------------------------- Browse Treks -------------------------
@cache.memoize(timeout=300)
def browse_treks(search=""):

    query = Trek.query.filter(

        Trek.is_deleted == False,

        Trek.status == "open"

    )

    if search:

        query = query.filter(

            or_(

                Trek.trek_name.ilike(f"%{search}%"),

                Trek.location.ilike(f"%{search}%")

            )

        )

    treks = query.order_by(

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

    },200

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
    
    if trek.available_slots<=0:

        return{

            "message":"No slots available."

        },400
    
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
            if trek.available_slots <= 0:

                return {
            
                    "message":"No slots available."
            
                },400
            trek.available_slots -= 1

            existing_booking.booking_date = datetime.utcnow()

            existing_booking.booking_status = "booked"

            existing_booking.payment_status = "pending"

            existing_booking.cancelled_by = None

            existing_booking.status_reason = None

            existing_booking.total_amount = trek.price


            db.session.commit()
            cache.delete_memoized(browse_treks)

            return{

                "message":"Trek rebooked successfully.",

                "booking":{

                    "booking_id":existing_booking.id,

                    "trek_name":trek.trek_name,

                    "booking_status":existing_booking.booking_status,

                    "payment_status":existing_booking.payment_status,

                    "total_amount":existing_booking.total_amount

                }
             }, 200
    

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
    cache.delete_memoized(browse_treks)

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


# ------------------------- My Bookings -------------------------

from datetime import date

def get_my_bookings(user_id, search=""):

    user = User.query.filter_by(

        id=user_id,

        role="trekker"

    ).first()

    if user is None:

        return {

            "message": "User not found."

        }, 404

    query = (

        Booking.query
    
        .join(Trek)
    
        .filter(
    
            Booking.user_id == user.id
    
        )
    
    )
    
    if search:
    
        query = query.filter(
    
            or_(
    
                Trek.trek_name.ilike(f"%{search}%"),
    
                Trek.location.ilike(f"%{search}%")
    
            )
    
        )
    
    bookings = query.order_by(
    
        Trek.start_date.asc()
    
    ).all()
    
    today = date.today()

    result = []

    summary = {

        "all": 0,

        "upcoming": 0,

        "ongoing": 0,

        "completed": 0,

        "cancelled": 0

    }

    for booking in bookings:

        trek = Trek.query.get(booking.trek_id)

        review = Review.query.filter_by(

        user_id=user.id,

        trek_id=trek.id

        ).first()

        has_review = review is not None

    
        if booking.booking_status == "cancelled":

            current_status = "Cancelled"

            summary["cancelled"] += 1

        elif booking.booking_status == "completed":

            current_status = "Completed"

            summary["completed"] += 1

        elif trek.start_date > today:

            current_status = "Upcoming"

            summary["upcoming"] += 1

        elif trek.start_date <= today <= trek.end_date:

            current_status = "Ongoing"

            summary["ongoing"] += 1

        else:

            current_status = "Completed"

            summary["completed"] += 1

        summary["all"] += 1

        result.append({

            "booking_id": booking.id,

            "trek_id": trek.id,

            "trek_name": trek.trek_name,

            "location": trek.location,

            "difficulty": trek.difficulty,

            "duration_days": trek.duration_days,

            "start_date": trek.start_date.strftime("%Y-%m-%d"),

            "end_date": trek.end_date.strftime("%Y-%m-%d"),

            "booking_date": booking.booking_date.strftime("%Y-%m-%d"),

            "booking_status": booking.booking_status,

            "payment_status": booking.payment_status,

            "total_amount": booking.total_amount,

            "status": current_status,
            "has_review": has_review

        })

    return {

        "summary": summary,

        "bookings": result

    }, 200

# ------------------------- Cancel Booking -------------------------

def cancel_booking(user_id, booking_id):

    booking = Booking.query.filter_by(

        id=booking_id,

        user_id=user_id

    ).first()

    if booking is None:

        return {

            "message":"Booking not found."

        },404

    if booking.booking_status != "booked":

        return {

            "message":"Only active bookings can be cancelled."

        },400

    trek = Trek.query.filter_by(

        id=booking.trek_id,

        is_deleted=False

    ).first()

    if trek is None:

        return {

            "message":"Trek not found."

        },404

    if trek.start_date <= date.today():

        return {

            "message":"Trek has already started."

        },400

    booking.booking_status = "cancelled"

    booking.cancelled_by = "user"

    booking.status_reason = "Cancelled by user"

    if booking.payment_status == "paid":

        booking.payment_status = "refunded"

    trek.available_slots += 1

    db.session.commit()
    cache.delete_memoized(browse_treks)

    return {

        "message":"Booking cancelled successfully."

    },200

# ------------------------- Pay Booking -------------------------

def pay_booking(user_id, booking_id):

    booking = Booking.query.filter_by(

        id=booking_id,

        user_id=user_id

    ).first()

    if booking is None:

        return {

            "message":"Booking not found."

        },404

    if booking.booking_status != "booked":

        return {

            "message":"This booking has already been cancelled."

        },400

    if booking.payment_status != "pending":

        return {

            "message":"Payment already completed."

        },400

    booking.payment_status = "paid"

    db.session.commit()

    return {

        "message":"Payment completed successfully."

    },200

# ------------------------- Submit Review -------------------------

def submit_review(user_id, booking_id, data):

    booking = Booking.query.filter_by(

        id=booking_id,

        user_id=user_id

    ).first()

    if booking is None:

        return {

            "message":"Booking not found."

        },404

    if booking.booking_status != "completed":

        return {

            "message":"You can review only completed treks."

        },400

    if booking.payment_status != "paid":

        return {

            "message":"Complete payment before reviewing."

        },400

    existing_review = Review.query.filter_by(

        user_id=user_id,

        trek_id=booking.trek_id

    ).first()

    if existing_review:

        return {

            "message":"You have already reviewed this trek."

        },409

    rating = data.get("rating")

    comment = data.get("comment")

    if rating is None:

        return {

            "message":"Rating is required."

        },400

    if not isinstance(rating, int):

        return {

            "message":"Rating must be an integer."

        },400

    if rating < 1 or rating > 5:

        return {

            "message":"Rating must be between 1 and 5."

        },400

    review = Review(

        user_id=user_id,

        trek_id=booking.trek_id,

        rating=rating,

        comment=comment

    )

    db.session.add(review)

    db.session.commit()

    return {

        "message":"Review submitted successfully."

    },201

# ------------------------- Get Review -------------------------

def get_review(user_id, trek_id):

    review = Review.query.filter_by(

        user_id=user_id,

        trek_id=trek_id

    ).first()

    if review is None:

        return {

            "review":None

        },200

    return {

        "review":{

            "rating":review.rating,

            "comment":review.comment,

            "created_at":review.created_at.strftime("%Y-%m-%d")

        }

    },200

# ------------------------- Update Review -------------------------

def update_review(user_id, trek_id, data):

    review = Review.query.filter_by(

        user_id=user_id,

        trek_id=trek_id

    ).first()

    if review is None:

        return {

            "message":"Review not found."

        },404

    rating = data.get("rating")

    comment = data.get("comment")

    if rating < 1 or rating > 5:

        return {

            "message":"Rating must be between 1 and 5."

        },400

    review.rating = rating

    review.comment = comment

    db.session.commit()

    return {

        "message":"Review updated successfully."

    },200

