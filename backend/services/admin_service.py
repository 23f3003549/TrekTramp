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
    
    
    
    
    
    





    

