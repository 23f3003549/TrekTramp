from werkzeug.security import generate_password_hash
from extensions import db
from datetime import datetime


from models.user import User
from models.trek import Trek
from models.staff_assign import StaffAssign
from models.booking import Booking

#----------------------------------create staff----------------------------
def create_staff(data):
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    # age = data.get("age")
    # gender = data.get("gender")
    # phone = data.get("phone")

    if not name or not email or not password:
        return {
            "message": "Give all credentials"
        }, 400
    
    if len(password) < 6:
        return {
            "message": "Password must be at least 6 characters"
        }, 400
    if len(password) > 20:
        return{
            "message": "Password must be less than 20 characters"
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

    return {
        "message": f"Staff with email id:{email} registered successfully by admin",
        "staff":{
            "id": new_staff.id,
            "name": new_staff.name,
            "email" : new_staff.email
        }
    }, 201

#--------------------------------------assign staff-----------------------------
def assign_staff(trek_id, data):
    trek = Trek.query.get(trek_id)
    staff_id = data.get("staff_id")

    if not staff_id:
        return{
            "message": "Staff id is required"
        }, 400
    
    if trek is None:
        return {
            "message": "Trek not found"
        }, 400
    
    staff = User.query.get(staff_id)

    if staff is None:
        return{
            "message": "Staff not found"
        }, 404
    
    if staff.role != "staff":
        return {
            "message": "Selected user is not a staff."
        }, 400
    
    if staff.status != "active":
        return {
            "message": f"Staff account is {staff.status}."
        }, 400
    
    assignments = StaffAssign.query.filter_by(staff_id = staff_id).all()

    for asssignment in assignments:
        if asssignment.trek_id == trek_id:
            continue

        assigned_trek = Trek.query.get(asssignment.trek_id)
        if(trek.start_date <= assigned_trek.end_date and trek.end_date >=assigned_trek.start_date):
            return{
                "message": f"Staff is already assigned to {assigned_trek.trek_name} durimg overlapping dates."
            }, 409
        
    existing_staff = StaffAssign.query.filter_by(trek_id = trek_id).first()   
    if existing_staff:
        existing_staff.staff_id = staff_id 
        existing_staff.assigned_at = datetime.utcnow()
        db.session.commit()

        return {
            "message": "Staff reassigned successfully.",
            "assignment": {
                "trek_id": trek_id,
                "trek_name": trek.trek_name,
                "staff_id": staff_id,
                "staff_name": staff.name
            }
        }, 200

    new_staff = StaffAssign(trek_id = trek_id, staff_id = staff_id) 
    db.session.add(new_staff)
    db.session.commit()

    return {
        "message": "Staff assigned successfully.",
        "assignment": {
            "trek_id": trek_id,
            "trek_name": trek.trek_name,
            "staff_id": staff_id,
            "staff_name": staff.name
        }
    }, 201

#--------------------------------------admin dashboard---------------------
def admin_dashboard():
    total_treks = Trek.query.count()

    total_users = User.query.filter_by(role="user").count()

    total_staff = User.query.filter_by(role="staff").count()

    total_bookings = Booking.query.count()

    return {
        "total_treks": total_treks,
        "total_users": total_users,
        "total_staff": total_staff,
        "total_bookings": total_bookings
    }, 200









    

