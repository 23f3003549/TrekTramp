import csv
from io import StringIO
from flask import make_response
from sqlalchemy import extract , or_
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from datetime import datetime

from utils.email_service import send_staff_email

import secrets
import string


from models.user import User
from models.trek import Trek
from models.staff_assign import StaffAssign
from models.booking import Booking

#----------------------------------create staff----------------------------
def create_staff(data):
    name = data.get("name")
    email = data.get("email")
    alphabet = string.ascii_letters + string.digits + "@#$%&"
    password = "Newstaff@123"
    name = name.strip()
    email = email.strip().lower()


    if not name or not email:
        return {
            "message": "Give all credentials"
        }, 400
    
    
    existing_email = User.query.filter_by(email = email).first()
    if existing_email:
        return {
            "message": "Email already exist"
        }, 409
    
    hash_pass = generate_password_hash(password)

    new_staff = User(
        name = name,
        email = email,
        hash_password = hash_pass,
        # age = age,
        # phone = phone,
        # gender = gender,
        role = "staff",
        must_change_password = True

    )
    db.session.add(new_staff)
    db.session.commit()
    
    try:
        send_staff_email(
    
            new_staff.name,
        
            new_staff.email,
        
            password
    
        )
    except Exception as e:
        print(e)



    return {
        "message": f"Staff with email id:{email} registered successfully by admin",
        "staff":{
            "id": new_staff.id,
            "name": new_staff.name,
            "email" : new_staff.email
        }
    }, 201


#--------------------------------------admin dashboard---------------------
def admin_dashboard():
    total_treks = Trek.query.filter_by(is_deleted=False).count()

    total_users = User.query.filter_by(role="trekker").count()

    total_staff = User.query.filter_by(role="staff").count()

    total_bookings = Booking.query.count()

    return {
        "total_treks": total_treks,
        "total_users": total_users,
        "total_staff": total_staff,
        "total_bookings": total_bookings
    }, 200

#----------------------------------------get all staff----------------------------------

def get_all_staff(search=""):

    query = User.query.filter_by(
        role="staff"
    )
    if search:

        query = query.filter(

            or_(

                User.name.ilike(f"%{search}%"),

                User.email.ilike(f"%{search}%")

            )

        )
    staffs = query.order_by(

        User.created_at.desc()

    ).all()    

    staff_list = []

    updated = False

    for staff in staffs:

        assignments = StaffAssign.query.filter_by(
            staff_id=staff.id,
            status="active"
        ).all()

        assigned_treks = []

        for assignment in assignments:

            trek = Trek.query.filter_by(
                id=assignment.trek_id,
                is_deleted=False
            ).first()

            if trek:

                assigned_treks.append(trek.trek_name)

            else:

                assignment.status = "cancelled"
                assignment.released_at = datetime.utcnow()

                updated = True

        staff_list.append({

            "id": staff.id,

            "name": staff.name,

            "email": staff.email,

            "status": staff.status,

            "assigned_treks": assigned_treks

        })

    if updated:

        db.session.commit()

    return {

        "staffs": staff_list

    }, 200

#--------------------------------------------get a single staff  details ----------------------------
def get_staff_details(staff_id):

    staff = User.query.filter_by(

        id=staff_id,

        role="staff"

    ).first()

    if staff is None:

        return{

            "message":"Staff not found."

        },404


    assignments = StaffAssign.query.filter_by(

        staff_id=staff.id

    ).order_by(

        StaffAssign.assigned_at.desc()

    ).all()


    completed = 0

    cancelled = 0

    active = 0

    recent_treks = []


    for assignment in assignments:

        trek = Trek.query.get(

            assignment.trek_id

        )

        if trek is None:

            continue


        if assignment.status == "completed":

            completed += 1

        elif assignment.status == "cancelled":

            cancelled += 1

        elif assignment.status == "active":

            active += 1


        recent_treks.append({

            "trek_id": trek.id,

            "trek_name": trek.trek_name,

            "location": trek.location,

            "start_date": trek.start_date.strftime("%Y-%m-%d"),

            "end_date": trek.end_date.strftime("%Y-%m-%d"),

            "status": assignment.status

        })


    return{

        "staff":{

            "id":staff.id,

            "name":staff.name,

            "email":staff.email,

            "phone":staff.phone,

            "age":staff.age,

            "gender":staff.gender,

            "status":staff.status,

            "status_reason":staff.status_reason,

            "must_change_password":staff.must_change_password

        },

        "statistics":{

            "active":active,

            "completed":completed,

            "cancelled":cancelled,

            "total":len(assignments)

        },

        "recent_treks":recent_treks[:5]

    },200

#------------------------------------ Update Staff Account Status ------------------------------------

def update_staff_account_status(staff_id, data):

    staff = User.query.filter_by(

        id=staff_id,

        role="staff"

    ).first()

    if staff is None:

        return{

            "message":"Staff not found."

        },404


    status = data.get("status")

    reason = data.get("reason","").strip()


    if status not in [

        "active",

        "inactive",

        "blacklisted"

    ]:

        return{

            "message":"Invalid account status."

        },400


    if status == "active":

        staff.status = "active"

        staff.status_reason = None

    elif status == "inactive":

        staff.status = "inactive"

        staff.status_reason = reason if reason else None

        active_assignments = StaffAssign.query.filter_by(

            staff_id=staff.id,

            status="active"

        ).all()

        for assignment in active_assignments:

            assignment.status = "cancelled"

            assignment.released_at = datetime.utcnow()

    else:

        staff.status = "blacklisted"

        staff.status_reason = reason if reason else None

        active_assignments = StaffAssign.query.filter_by(

            staff_id=staff.id,

            status="active"

        ).all()

        for assignment in active_assignments:

            assignment.status = "cancelled"

            assignment.released_at = datetime.utcnow()


    db.session.commit()


    return{

        "message":"Staff account updated successfully."

    },200


#------------------------------------ Get User Details ------------------------------------

def get_user_details(user_id):

    user = User.query.filter_by(

        id=user_id,

        role="trekker"

    ).first()

    if user is None:

        return{

            "message":"User not found."

        },404


    bookings = Booking.query.filter_by(

        user_id=user.id

    ).order_by(

        Booking.booking_date.desc()

    ).all()


    total = 0

    upcoming = 0

    completed = 0

    cancelled = 0

    recent_bookings = []


    for booking in bookings:

        trek = Trek.query.get(

            booking.trek_id

        )

        if trek is None:

            continue


        total += 1


        if booking.booking_status == "completed":

            completed += 1

        elif booking.booking_status == "cancelled":

            cancelled += 1

        else:

            upcoming += 1


        recent_bookings.append({

            "booking_id":booking.id,

            "trek_name":trek.trek_name,

            "location":trek.location,

            "booking_date":booking.booking_date.strftime("%Y-%m-%d"),

            "booking_status":booking.booking_status,

            "payment_status":booking.payment_status

        })


    return{

        "user":{

            "id":user.id,

            "name":user.name,

            "email":user.email,

            "phone":user.phone,

            "age":user.age,

            "gender":user.gender,

            "status":user.status,

            "status_reason":user.status_reason

        },

        "statistics":{

            "total":total,

            "upcoming":upcoming,

            "completed":completed,

            "cancelled":cancelled

        },

        "recent_bookings":recent_bookings[:5]

    },200

#-------------------- Update User Account Status --------------

def update_user_account_status(user_id, data):

    user = User.query.filter_by(

        id=user_id,

        role="trekker"

    ).first()

    if user is None:

        return{

            "message":"User not found."

        },404


    status = data.get("status")

    reason = data.get("reason","").strip()


    if status not in [

        "active",

        "inactive",

        "blacklisted"

    ]:

        return{

            "message":"Invalid account status."

        },400


    user.status = status
    
    if status == "active":
    
        user.status_reason = None
    
    else:
    
        user.status_reason = reason if reason else None
    
        bookings = Booking.query.filter_by(
    
            user_id=user.id,
    
            booking_status="booked"
    
        ).all()
    
        for booking in bookings:
    
            booking.booking_status = "cancelled"
    
            booking.cancelled_by = "admin"
    
            booking.status_reason = (
    
                reason if reason
    
                else f"Account {status} by Admin"
    
            )
    
            if booking.payment_status == "paid":
    
                booking.payment_status = "refunded"
    
            trek = Trek.query.get(
    
                booking.trek_id
    
            )
    
            if trek:
    
                trek.available_slots += 1
        
    db.session.commit()
    
    return{
    
        "message":"User account updated successfully."

    },200

from sqlalchemy import or_

#--------------------------- Get All Users -----------------------

def get_all_users(search=""):

    query = User.query.filter_by(

        role="trekker"

    )

    if search:

        query = query.filter(

            or_(

                User.name.ilike(f"%{search}%"),

                User.email.ilike(f"%{search}%")

            )

        )

    users = query.order_by(
        User.created_at.desc()
    ).all()

    user_list = []

    for user in users:

        total_bookings = Booking.query.filter_by(

            user_id=user.id

        ).count()

        user_list.append({

            "id": user.id,

            "name": user.name,

            "email": user.email,

            "status": user.status,

            "total_bookings": total_bookings

        })

    return{

        "users": user_list

    },200

#------------------- Get Single User -----------------------

def get_user(user_id):

    user = User.query.filter_by(

        id=user_id,

        role="trekker"

    ).first()

    if user is None:

        return{

            "message":"User not found."

        },404

    return{

        "user":{

            "id":user.id,

            "name":user.name,

            "email":user.email,

            "phone":user.phone,

            "age":user.age,

            "gender":user.gender,

            "status":user.status

        }

    },200

#------------------------Get All Bookings ---------------------

def get_all_bookings(search=""):

    trek_list = []

    treks = Trek.query.filter_by(

        is_deleted=False

    ).all()

    for trek in treks:

        query = db.session.query(

            Booking

        ).join(

            User

        ).filter(

            Booking.trek_id == trek.id

        )

        if search:

            query = query.filter(

                or_(

                    User.name.ilike(f"%{search}%"),

                    User.email.ilike(f"%{search}%"),

                    Booking.id.cast(db.String).ilike(f"%{search}%")

                )

            )

        bookings = query.all()

        participants = []

        booked = 0

        completed = 0

        cancelled = 0

        for booking in bookings:

            user = User.query.get(

                booking.user_id

            )

            if user is None:

                continue

            if booking.booking_status == "booked":

                booked += 1

            elif booking.booking_status == "completed":

                completed += 1

            elif booking.booking_status == "cancelled":

                cancelled += 1

            participants.append({

                "booking_id": booking.id,

                "user_name": user.name,

                "email": user.email,

                "booking_status": booking.booking_status,

                "payment_status": booking.payment_status

            })

        if participants:

            trek_list.append({

                "trek_id": trek.id,

                "trek_name": trek.trek_name,

                "location": trek.location,

                "start_date": trek.start_date.strftime("%Y-%m-%d"),

                "end_date": trek.end_date.strftime("%Y-%m-%d"),

                "statistics":{

                    "total":len(participants),

                    "booked":booked,

                    "completed":completed,

                    "cancelled":cancelled

                },

                "participants":participants

            })

    return{

        "treks":trek_list

    },200
#--------------------------- Get Booking Details ---------------------

def get_booking_details(booking_id):

    booking = Booking.query.get(

        booking_id

    )

    if booking is None:

        return{

            "message":"Booking not found."

        },404


    user = User.query.get(

        booking.user_id

    )

    trek = Trek.query.get(

        booking.trek_id

    )


    return{

        "booking":{

            "booking_id":booking.id,

            "booking_date":booking.booking_date.strftime("%Y-%m-%d"),

            "booking_status":booking.booking_status,

            "payment_status":booking.payment_status,

            "status_reason":booking.status_reason,

            "cancelled_by":booking.cancelled_by,

            "is_active": booking.booking_status == "booked",

            "user":{

                "id":user.id,

                "name":user.name,

                "email":user.email,

                "phone":user.phone,

                "age":user.age,

                "gender":user.gender,

                "status":user.status

            },

            "trek":{

                "id":trek.id,

                "trek_name":trek.trek_name,

                "location":trek.location,

                "start_date":trek.start_date.strftime("%Y-%m-%d"),

                "end_date":trek.end_date.strftime("%Y-%m-%d"),

                "difficulty":trek.difficulty,

                "price":trek.price,

            }

        }

    },200

#--------------------------Update Booking -------------

def update_booking(booking_id, data):

    booking = Booking.query.get(

        booking_id

    )

    if booking is None:

        return{

            "message":"Booking not found."

        },404


    status = data.get(

        "booking_status"

    )

    reason = data.get(

        "reason",

        ""

    ).strip()


    if status != "cancelled":

        return{

            "message":"Admin can only cancel bookings."

        },400


    if booking.booking_status != "booked":

        return{

            "message":"Only booked participants can be cancelled."

        },400


    booking.booking_status = "cancelled"

    booking.cancelled_by = "admin"

    booking.status_reason = reason


    if booking.payment_status == "paid":

        booking.payment_status = "refunded"


    trek = Trek.query.get(

        booking.trek_id

    )

    if trek:

        trek.available_slots += 1


    db.session.commit()

    return{

        "message":"Booking cancelled successfully."

    },200

#-------------------------- Reports Dashboard -------------------

def get_reports():

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

    booked = Booking.query.filter_by(

        booking_status="booked"

    ).count()

    completed = Booking.query.filter_by(

        booking_status="completed"

    ).count()

    cancelled = Booking.query.filter_by(

        booking_status="cancelled"

    ).count()

    paid = Booking.query.filter_by(

        payment_status="paid"

    ).count()

    pending = Booking.query.filter_by(

        payment_status="pending"

    ).count()

    refunded = Booking.query.filter_by(

        payment_status="refunded"

    ).count()

    revenue = 0

    for booking in Booking.query.filter_by(

        payment_status="paid"

    ).all():

        trek = Trek.query.get(

            booking.trek_id

        )

        if trek:

            revenue += trek.price


    trek_stats = []

    treks = Trek.query.filter_by(

        is_deleted=False

    ).all()

    for trek in treks:

        count = Booking.query.filter_by(

            trek_id=trek.id

        ).count()

        trek_stats.append({

            "name":trek.trek_name,

            "bookings":count

        })

    trek_stats.sort(

        key=lambda x:x["bookings"],

        reverse=True

    )

    staff_statistics = []

    staffs = User.query.filter_by(

        role="staff"

    ).all()

    for staff in staffs:

        active = StaffAssign.query.filter_by(

            staff_id=staff.id,

            status="active"

        ).count()

        completed_count = StaffAssign.query.filter_by(

            staff_id=staff.id,

            status="completed"

        ).count()

        cancelled_count = StaffAssign.query.filter_by(

            staff_id=staff.id,

            status="cancelled"

        ).count()

        staff_statistics.append({

            "name":staff.name,

            "active":active,

            "completed":completed_count,

            "cancelled":cancelled_count

        })

        monthly_bookings=[]

        months=[
        
            "Jan","Feb","Mar","Apr","May","Jun",
        
            "Jul","Aug","Sep","Oct","Nov","Dec"
        
        ]
        
        for i in range(1,13):
        
            count=Booking.query.filter(
        
                extract(
        
                    "month",
        
                    Booking.booking_date
        
                )==i
        
            ).count()
        
            monthly_bookings.append({
        
                "month":months[i-1],
        
                "count":count
        
            })
        
    return{

        "dashboard":{

            "treks":total_treks,

            "users":total_users,

            "staff":total_staff,

            "bookings":total_bookings,

            "revenue":revenue

        },

        "booking_statistics":{

            "booked":booked,

            "completed":completed,

            "cancelled":cancelled

        },

        "payment_statistics":{

            "paid":paid,

            "pending":pending,

            "refunded":refunded

        },

        "popular_treks":trek_stats[:5],

        "staff_statistics":staff_statistics,
        "monthly_bookings":monthly_bookings

    },200

#-------------------------------- Export Users Report --------------

def export_users_report():

    output = StringIO()

    writer = csv.writer(output)

    writer.writerow([

        "ID",

        "Name",

        "Email",

        "Status",

        "Phone",

        "Age",

        "Gender",

        "Created At"

    ])

    users = User.query.filter_by(

        role="trekker"

    ).all()

    for user in users:

        writer.writerow([

            user.id,

            user.name,

            user.email,

            user.status,

            user.phone,

            user.age,

            user.gender,

            user.created_at

        ])

    response = make_response(

        output.getvalue()

    )

    response.headers["Content-Disposition"] = (

        "attachment; filename=users_report.csv"

    )

    response.headers["Content-Type"] = "text/csv"

    return response

#---------------------------- Export Staff Report --------------

def export_staff_report():

    output = StringIO()

    writer = csv.writer(output)

    writer.writerow([

        "ID",

        "Name",

        "Email",

        "Status",

        "Assigned Treks"

    ])

    staffs = User.query.filter_by(

        role="staff"

    ).all()

    for staff in staffs:

        total = StaffAssign.query.filter_by(

            staff_id=staff.id

        ).count()

        writer.writerow([

            staff.id,

            staff.name,

            staff.email,

            staff.status,

            total

        ])

    response = make_response(

        output.getvalue()

    )

    response.headers["Content-Disposition"] = (

        "attachment; filename=staff_report.csv"

    )

    response.headers["Content-Type"] = "text/csv"

    return response

#------------------------ Export Booking Report ----------------------

def export_booking_report():

    output = StringIO()

    writer = csv.writer(output)

    writer.writerow([

        "Booking ID",

        "User",

        "Trek",

        "Booking Status",

        "Payment Status",

        "Booking Date"

    ])

    bookings = Booking.query.all()

    for booking in bookings:

        user = User.query.get(

            booking.user_id

        )

        trek = Trek.query.get(

            booking.trek_id

        )

        writer.writerow([

            booking.id,

            user.name,

            trek.trek_name,

            booking.booking_status,

            booking.payment_status,

            booking.booking_date

        ])

    response = make_response(

        output.getvalue()

    )

    response.headers["Content-Disposition"] = (

        "attachment; filename=booking_report.csv"

    )

    response.headers["Content-Type"] = "text/csv"

    return response

#-------------------------------- Export Trek Report ------------

def export_trek_report():

    output = StringIO()

    writer = csv.writer(output)

    writer.writerow([

        "ID",

        "Trek",

        "Location",

        "Status",

        "Capacity",

        "Available"

    ])

    treks = Trek.query.filter_by(

        is_deleted=False

    ).all()

    for trek in treks:

        writer.writerow([

            trek.id,

            trek.trek_name,

            trek.location,

            trek.status,

            trek.max_slots,

            trek.available_slots

        ])

    response = make_response(

        output.getvalue()

    )

    response.headers["Content-Disposition"] = (

        "attachment; filename=trek_report.csv"

    )

    response.headers["Content-Type"] = "text/csv"

    return response

#------------------------ Get Admin Profile ---------------------

def get_admin_profile(admin_id):

    admin = User.query.filter_by(

        id=admin_id,

        role="admin"

    ).first()

    if admin is None:

        return {

            "message":"Admin not found."

        },404

    return {

        "admin":{

            "id":admin.id,

            "name":admin.name,

            "email":admin.email,

            "role":admin.role

        }

    },200

#------------------------ Update Admin Profile -------------------

def update_admin_profile(admin_id,data):

    admin = User.query.filter_by(

        id=admin_id,

        role="admin"

    ).first()

    if admin is None:

        return{

            "message":"Admin not found."

        },404


    name = data.get(

        "name",

        ""

    ).strip()

    email = data.get(

        "email",

        ""

    ).strip().lower()


    if not name or not email:

        return{

            "message":"Name and Email are required."

        },400


    existing = User.query.filter(

        User.email==email,

        User.id!=admin.id

    ).first()

    if existing:

        return{

            "message":"Email already exists."

        },409


    admin.name = name

    admin.email = email

    db.session.commit()

    return{

        "message":"Profile updated successfully."

    },200

#------------------- Change Admin Password -----------------------

def change_admin_password(admin_id,data):

    admin = User.query.filter_by(

        id=admin_id,

        role="admin"

    ).first()

    if admin is None:

        return{

            "message":"Admin not found."

        },404


    current_password = data.get(

        "current_password",

        ""

    )

    new_password = data.get(

        "new_password",

        ""

    )

    confirm_password = data.get(

        "confirm_password",

        ""

    )


    if not check_password_hash(

        admin.hash_password,

        current_password

    ):

        return{

            "message":"Current password is incorrect."

        },400


    if new_password != confirm_password:

        return{

            "message":"Passwords do not match."

        },400


    if len(new_password) < 8:

        return{

            "message":"Password must contain at least 8 characters."

        },400


    admin.hash_password = generate_password_hash(

        new_password

    )

    db.session.commit()

    return{

        "message":"Password updated successfully."

    },200

    

    
    
    
    
    
    





    

