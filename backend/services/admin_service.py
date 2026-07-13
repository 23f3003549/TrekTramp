from werkzeug.security import generate_password_hash
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
    password = "".join(
    secrets.choice(alphabet)
    for _ in range(10)
    )
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

def get_all_staff():

    staffs = User.query.filter_by(
        role="staff"
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


    # ---------------- Activate ----------------

    if status == "active":

        staff.status = "active"

        staff.status_reason = None


    # ---------------- Inactive ----------------

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


    # ---------------- Blacklisted ----------------

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

#------------------------------------ Update User Account Status ------------------------------------

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


    db.session.commit()


    return{

        "message":"User account updated successfully."

    },200

#------------------------------------ Get All Users ------------------------------------

def get_all_users():

    users = User.query.filter_by(

        role="trekker"

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

#------------------------------------ Get Single User ------------------------------------

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
    

    
    
    
    
    
    





    

