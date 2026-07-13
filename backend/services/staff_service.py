from datetime import datetime
from flask_jwt_extended import get_jwt_identity
from werkzeug.security import generate_password_hash

from models.staff_assign import StaffAssign
from models.trek import Trek
from models.user import User
from models.staff_assign import StaffAssign
from models.booking import Booking

from extensions import db

def cleanup_invalid_assignments():

    assignments = StaffAssign.query.filter_by(
        status="active"
    ).all()

    updated = False

    for assignment in assignments:

        trek = Trek.query.filter_by(
            id=assignment.trek_id,
            is_deleted=False
        ).first()

        if trek is None:

            assignment.status = "cancelled"
            assignment.released_at = datetime.utcnow()
            updated = True

    if updated:
        db.session.commit()

#----------------------------update staff-----------------------------
def update_staff(staff_id, data):

    staff = User.query.filter_by(
        id=staff_id,
        role="staff"
    ).first()

    if staff is None:

        return {
            "message": "Staff not found."
        }, 404

    name = data.get("name", staff.name).strip()

    email = data.get(
        "email",
        staff.email
    ).strip().lower()

    status = data.get(
        "status",
        staff.status
    ).lower()

    if not name or not email:

        return {
            "message": "Name and email are required."
        }, 400

    if status not in [
        "active",
        "inactive",
        "blacklisted"
    ]:

        return {
            "message": (
                "Status must be active, inactive "
                "or blacklisted."
            )
        }, 400

    existing_email = User.query.filter(
        User.email == email,
        User.id != staff_id
    ).first()

    if existing_email:

        return {
            "message": "Email already exists."
        }, 409

    assignment = StaffAssign.query.filter_by(
        staff_id=staff.id
    ).first()

    if (
        assignment
        and status in ["inactive", "blacklisted"]
    ):

        return {
            "message": (
                "Assigned staff cannot be marked "
                "inactive or blacklisted."
            )
        }, 400

    staff.name = name
    staff.email = email
    staff.status = status

    db.session.commit()

    return {

        "message": "Staff updated successfully.",

        "staff":{

            "id": staff.id,

            "name": staff.name,

            "email": staff.email,

            "status": staff.status

        }

    }, 200

#---------------------------get a staff---------------------------
def get_staff(staff_id):

    staff = User.query.filter_by(
        id=staff_id,
        role="staff"
    ).first()

    if staff is None:
        return {
            "message": "Staff not found."
        }, 404

    assignment = StaffAssign.query.filter_by(
        staff_id=staff.id
    ).first()

    assigned_trek = None

    if assignment:

        trek = Trek.query.get(assignment.trek_id)

        if trek:
            assigned_trek = {
                "id": trek.id,
                "trek_name": trek.trek_name,
                "status": trek.status
            }

    return {
        "staff": {

            "id": staff.id,

            "name": staff.name,

            "email": staff.email,

            "phone": staff.phone,

            "age": staff.age,

            "gender": staff.gender,

            "status": staff.status,

            "must_change_password": staff.must_change_password,

            "created_at": staff.created_at.isoformat(),

            "assigned_trek": assigned_trek
        }

    }, 200

#------------------------------------------assign staff------------------------

def staff_assignment(data):

    cleanup_invalid_assignments()

    staff_id = data.get("staff_id")
    trek_id = data.get("trek_id")

    if not staff_id or not trek_id:

        return {
            "message": "Staff and Trek are required."
        }, 400

    staff = User.query.filter_by(
        id=staff_id,
        role="staff"
    ).first()

    if staff is None:

        return {
            "message": "Staff not found."
        }, 404

    if staff.status != "active":

        return {
            "message": "Only active staff can be assigned."
        }, 400

    trek = Trek.query.filter_by(
        id=trek_id,
        is_deleted=False
    ).first()

    if trek is None:

        return {
            "message": "Trek not found."
        }, 404

    if trek.status != "open":

        return {
            "message": "Staff can only be assigned to an open trek."
        }, 400

    active_assignments = StaffAssign.query.filter_by(
        staff_id=staff_id,
        status="active"
    ).all()

    for assignment in active_assignments:

        # Ignore if checking the same trek
        if assignment.trek_id == trek.id:
            continue

        assigned_trek = Trek.query.filter_by(
            id=assignment.trek_id,
            is_deleted=False
        ).first()

        if assigned_trek is None:
            continue

        if (
            trek.start_date <= assigned_trek.end_date
            and
            trek.end_date >= assigned_trek.start_date
        ):

            return {
                "message": f"Staff is already assigned to '{assigned_trek.trek_name}' during overlapping dates."
            }, 409
    existing_assignment = StaffAssign.query.filter_by(
        trek_id=trek.id,
        status="active"
    ).first()

    if existing_assignment:

        existing_assignment.staff_id = staff.id
        existing_assignment.assigned_at = datetime.utcnow()
        existing_assignment.released_at = None
        existing_assignment.status = "active"

        db.session.commit()

        return {

            "message": "Staff changed successfully.",

            "assignment": {

                "staff_id": staff.id,

                "staff_name": staff.name,

                "trek_id": trek.id,

                "trek_name": trek.trek_name

            }

        }, 200

    assignment = StaffAssign(

        staff_id=staff.id,

        trek_id=trek.id,

        status="active"

    )

    db.session.add(assignment)

    db.session.commit()

    return {

        "message": "Staff assigned successfully.",

        "assignment": {

            "staff_id": staff.id,

            "staff_name": staff.name,

            "trek_id": trek.id,

            "trek_name": trek.trek_name

        }

    }, 201
#------------------------available staff--------------------------------

def get_available_staff():

    cleanup_invalid_assignments()

    staffs = User.query.filter_by(
        role="staff",
        status="active"
    ).all()

    available = []

    for staff in staffs:

        assignment = StaffAssign.query.filter_by(
            staff_id=staff.id,
            status="active"
        ).first()

        # No active assignment -> available
        if assignment is None:

            available.append({

                "id": staff.id,

                "name": staff.name,

                "email": staff.email

            })

            continue

        # Check whether the assigned trek still exists
        trek = Trek.query.filter_by(
            id=assignment.trek_id,
            is_deleted=False
        ).first()

        # Trek is deleted -> release staff automatically
        if trek is None:

            assignment.status = "cancelled"

            assignment.released_at = datetime.utcnow()

            db.session.commit()

            available.append({

                "id": staff.id,

                "name": staff.name,

                "email": staff.email

            })

    return {

        "staffs": available

    }, 200

#----------------------change staff status----------------------

def change_staff_status(staff_id, data):

    staff = User.query.filter_by(
        id=staff_id,
        role="staff"
    ).first()

    if staff is None:
        return {
            "message":"Staff not found."
        },404

    status = data.get("status")

    allowed = [

        "active",

        "inactive",

        "blacklisted"

    ]

    if status not in allowed:

        return {

            "message":"Invalid status."

        },400

    assignment = StaffAssign.query.filter_by(

        staff_id=staff.id,

        status="active"

    ).first()

    if assignment and status!="active":

        return{

            "message":"Staff is currently assigned to a trek."

        },409

    staff.status=status

    db.session.commit()

    return{

        "message":"Status updated successfully."

    },200

#---------------------------get own profile---------------------------

def get_profile(user_id):

    staff = User.query.filter_by(
        id=user_id,
        role="staff"
    ).first()

    if staff is None:

        return{
            "message":"Staff not found."
        },404

    return{

        "profile":{

            "id":staff.id,

            "name":staff.name,

            "email":staff.email,

            "phone":staff.phone,

            "age":staff.age,

            "gender":staff.gender,

            "status":staff.status,

            "must_change_password":staff.must_change_password

        }

    },200


#-----------------------complete/update profile-----------------------

def update_profile(user_id,data):

    staff = User.query.filter_by(
        id=user_id,
        role="staff"
    ).first()

    if staff is None:

        return{
            "message":"Staff not found."
        },404


    phone=data.get("phone")
    age=data.get("age")
    gender=data.get("gender")
    password=data.get("password")


    if not phone or not age or not gender or not password:

        return{

            "message":"Please fill all fields."

        },400


    existing_phone = User.query.filter(
        User.phone==phone,
        User.id!=staff.id
    ).first()

    if existing_phone:

        return{

            "message":"Phone number already exists."

        },409


    if len(password)<6:

        return{

            "message":"Password should be at least 6 characters."

        },400
    if len(phone) != 10 or not phone.isdigit():


        return {
 
            "message": "Phone number must contain exactly 10 digits."

        },400


    staff.phone=phone
    staff.age = age
    staff.gender = gender
    staff.hash_password = generate_password_hash(password)
    staff.must_change_password = False
    
    db.session.commit()

    return {
       "message": "Profile updated successfully.",
       "profile": {
           "id": staff.id,

            "name": staff.name,
    
            "email": staff.email,
    
            "phone": staff.phone,
    
            "age": staff.age,
    
            "gender": staff.gender,
    
            "must_change_password": staff.must_change_password
           
       }
    }, 200

#-----------------------complete/update profile-----------------------

from werkzeug.security import generate_password_hash

def update_profile(user_id, data):

    staff = User.query.filter_by(
        id=user_id,
        role="staff"
    ).first()

    if staff is None:
        return {
            "message": "Staff not found."
        }, 404

    phone = data.get("phone")
    age = data.get("age")
    gender = data.get("gender")
    password = data.get("password")

    if not phone or not age or not gender or not password:
        return {
            "message": "Please fill all fields."
        }, 400

    if len(phone) != 10 or not phone.isdigit():
        return {
            "message": "Phone number must contain exactly 10 digits."
        }, 400

    if len(password) < 6:
        return {
            "message": "Password should be at least 6 characters."
        }, 400

    existing_phone = User.query.filter(
        User.phone == phone,
        User.id != staff.id
    ).first()

    if existing_phone:
        return {
            "message": "Phone number already exists."
        }, 409

    staff.phone = phone
    staff.age = age
    staff.gender = gender
    staff.hash_password = generate_password_hash(password)
    staff.must_change_password = False

    db.session.commit()

    return {
        "message": "Profile updated successfully.",
        "profile": {
            "id": staff.id,
            "name": staff.name,
            "email": staff.email,
            "phone": staff.phone,
            "age": staff.age,
            "gender": staff.gender,
            "must_change_password": staff.must_change_password
        }
    }, 200

#----------------------------------staff dashboard-------------------

def get_dashboard_statistics(user_id):
    cleanup_invalid_assignments()

    staff = User.query.filter_by(
        id=user_id,
        role="staff"
    ).first()

    if staff is None:

        return{

            "message":"Staff not found."

        },404

    assigned_treks = StaffAssign.query.filter_by(

        staff_id=staff.id,

        status="active"

    ).count()

    completed_treks = StaffAssign.query.filter_by(

        staff_id=staff.id,

        status="completed"

    ).count()

    assignments = StaffAssign.query.filter_by(

        staff_id=staff.id,

        status="active"

    ).all()

    total_participants = 0

    for assignment in assignments:

        booked = Booking.query.filter_by(

            trek_id=assignment.trek_id,

            booking_status="booked"

        ).count()

        total_participants += booked


    return{

        "statistics":{

            "assigned_treks":assigned_treks,

            "total_participants":total_participants,

            "completed_treks":completed_treks

        }

    },200

#---------------------------my assigned treks---------------------------

def get_my_treks(user_id):

    staff = User.query.filter_by(
        id=user_id,
        role="staff"
    ).first()

    if staff is None:

        return {
            "message": "Staff not found."
        },404

    assignments = StaffAssign.query.filter_by(
        staff_id=staff.id
    ).all()

    trek_list = []

    updated = False

    for assignment in assignments:

        trek = Trek.query.filter_by(
            id=assignment.trek_id,
            is_deleted=False
        ).first()

        # Trek deleted -> release assignment
        if trek is None:

            assignment.status = "cancelled"
            assignment.released_at = datetime.utcnow()

            updated = True

            continue

        participants = Booking.query.filter_by(
            trek_id=trek.id,
            booking_status="booked"
        ).count()

        trek_list.append({

            "id": trek.id,

            "trek_name": trek.trek_name,

            "start_date": trek.start_date.isoformat(),

            "end_date": trek.end_date.isoformat(),

            "participants": participants,

            "max_slots": trek.max_slots,

            "status": trek.status

        })

    if updated:

        db.session.commit()

    return {

        "treks": trek_list

    },200

#--------------------------update trek capacity--------------------------

def update_trek_capacity(user_id, trek_id, data):

    staff = User.query.filter_by(
        id=user_id,
        role="staff"
    ).first()

    if staff is None:

        return {
            "message": "Staff not found."
        }, 404

    assignment = StaffAssign.query.filter_by(
        staff_id=staff.id,
        trek_id=trek_id,
        status="active"
    ).first()

    if assignment is None:

        return {
            "message": "You are not assigned to this trek."
        }, 403

    trek = Trek.query.filter_by(
        id=trek_id,
        is_deleted=False
    ).first()

    if trek is None:

        return {
            "message": "Trek not found."
        }, 404

    if trek.status != "open":

        return {
            "message": "Capacity can only be updated before the trek starts."
        }, 400

    max_slots = data.get("max_slots")

    if max_slots is None:

        return {
            "message": "Maximum capacity is required."
        }, 400

    try:

        max_slots = int(max_slots)

    except (TypeError, ValueError):

        return {
            "message": "Maximum capacity must be a valid number."
        }, 400

    if max_slots <= 0:

        return {
            "message": "Maximum capacity must be greater than zero."
        }, 400

    booked_participants = Booking.query.filter_by(
        trek_id=trek.id,
        booking_status="booked"
    ).count()

    if max_slots < booked_participants:

        return {
            "message": (
                "Maximum capacity cannot be less than the "
                "number of booked participants."
            )
        }, 400

    trek.max_slots = max_slots

    trek.available_slots = (
        max_slots - booked_participants
    )

    db.session.commit()

    return {

        "message": "Trek capacity updated successfully.",

        "trek": {

            "max_slots": trek.max_slots,

            "available_slots": trek.available_slots

        }

    }, 200
#-----------------------update trek status-----------------------

def update_trek_status(user_id, trek_id, data):

    staff = User.query.filter_by(
        id=user_id,
        role="staff"
    ).first()

    if staff is None:

        return{
            "message":"Staff not found."
        },404

    assignment = StaffAssign.query.filter_by(
        staff_id=staff.id,
        trek_id=trek_id,
        status="active"
    ).first()

    if assignment is None:

        return{
            "message":"You are not assigned to this trek."
        },403

    trek = Trek.query.filter_by(
        id=trek_id,
        is_deleted=False
    ).first()

    if trek is None:

        return{
            "message":"Trek not found."
        },404

    status = data.get("status")

    if status not in ["started","completed","cancelled"]:

        return{
            "message":"Invalid trek status."
        },400

    # OPEN -> STARTED

    if status=="started":

        if trek.status!="open":

            return{
                "message":"Only open treks can be started."
            },400

        trek.status="started"

    # STARTED -> COMPLETED

    elif status=="completed":

        if trek.status!="started":

            return{
                "message":"Only started treks can be completed."
            },400

        trek.status="completed"

        assignment.status="completed"

        assignment.released_at=datetime.utcnow()

        bookings = Booking.query.filter_by(
            trek_id=trek.id,
            booking_status="booked"
        ).all()

        for booking in bookings:

            booking.booking_status="completed"

    # CANCEL

    elif status=="cancelled":

        if trek.status=="completed":

            return{
                "message":"Completed trek cannot be cancelled."
            },400

        trek.status="cancelled"

        assignment.status="cancelled"

        assignment.released_at=datetime.utcnow()

        bookings = Booking.query.filter(
            Booking.trek_id==trek.id,
            Booking.booking_status.in_(["booked"])
        ).all()

        for booking in bookings:

            booking.booking_status="cancelled"

            if booking.payment_status=="paid":

                booking.payment_status="refunded"

    db.session.commit()

    return{

        "message":"Trek status updated successfully."

    },200

#--------------------------get participants--------------------------

def get_participants(user_id):

    staff = User.query.filter_by(
        id=user_id,
        role="staff"
    ).first()

    if staff is None:

        return {
            "message": "Staff not found."
        }, 404

    assignments = StaffAssign.query.filter_by(
        staff_id=staff.id
    ).all()

    trek_list = []

    for assignment in assignments:

        trek = Trek.query.filter_by(
            id=assignment.trek_id,
            is_deleted=False
        ).first()

        if trek is None:
            continue

        bookings = Booking.query.filter(
            Booking.trek_id == trek.id,
            Booking.booking_status.in_(
                ["booked", "completed", "cancelled", "rejected"]
            )
        ).all()

        participant_list = []

        for booking in bookings:

            user = User.query.get(booking.user_id)

            if user is None:
                continue

            participant_list.append({

                "booking_id": booking.id,

                "user_id": user.id,

                "name": user.name,

                "email": user.email,

                "phone": user.phone,

                "booking_status": booking.booking_status,

                "payment_status": booking.payment_status

            })

        trek_list.append({

            "trek_id": trek.id,

            "trek_name": trek.trek_name,

            "trek_status": trek.status,

            "participant_count": len(participant_list),

            "participants": participant_list

        })

    return {

        "treks": trek_list

    }, 200

# ---------------------- Trek Participants ----------------------

def get_trek_participants(user_id, trek_id):

    staff = User.query.filter_by(

        id=user_id,

        role="staff"

    ).first()

    if staff is None:

        return{

            "message":"Staff not found."

        },404

    assignment = StaffAssign.query.filter_by(

        staff_id=staff.id,

        trek_id=trek_id

    ).first()

    if assignment is None:

        return{

            "message":"You are not assigned to this trek."

        },403

    trek = Trek.query.filter_by(

        id=trek_id,

        is_deleted=False

    ).first()

    if trek is None:

        return{

            "message":"Trek not found."

        },404

    bookings = Booking.query.filter(

        Booking.trek_id==trek.id

    ).order_by(

        Booking.booking_date.desc()

    ).all()

    participant_list=[]

    for booking in bookings:

        user = User.query.get(

            booking.user_id

        )

        if user is None:

            continue

        participant_list.append({

            "booking_id":booking.id,

            "user_id":user.id,

            "name":user.name,

            "email":user.email,

            "phone":user.phone,

            "gender":user.gender,

            "booking_status":booking.booking_status,

            "payment_status":booking.payment_status

        })

    return{

        "trek":{

            "id":trek.id,

            "trek_name":trek.trek_name,

            "status":trek.status

        },

        "participants":participant_list

    },200

# ---------------------- Participant Details ----------------------

def get_participant_details(user_id, booking_id):

    staff = User.query.filter_by(

        id=user_id,

        role="staff"

    ).first()

    if staff is None:

        return{

            "message":"Staff not found."

        },404

    booking = Booking.query.get(

        booking_id

    )

    if booking is None:

        return{

            "message":"Booking not found."

        },404

    assignment = StaffAssign.query.filter_by(

        staff_id=staff.id,

        trek_id=booking.trek_id

    ).first()

    if assignment is None:

        return{

            "message":"Access denied."

        },403

    trek = Trek.query.get(

        booking.trek_id

    )

    user = User.query.get(

        booking.user_id

    )

    return{

        "participant":{

            "booking_id":booking.id,

            "name":user.name,

            "email":user.email,

            "phone":user.phone,

            "gender":user.gender,

            "age":user.age,
            "user_status_reason": user.status_reason,
            "user_status": user.status,

            "trek_name":trek.trek_name,

            "booking_date":booking.booking_date.strftime("%d/%m/%Y"),

            "booking_status":booking.booking_status,

            "payment_status":booking.payment_status,

            "total_amount":booking.total_amount,

            "status_reason":booking.status_reason,
           

        }

    },200

# ---------------------- Update Participant ----------------------

def update_participant(user_id, booking_id, data):

    staff = User.query.filter_by(

        id=user_id,

        role="staff"

    ).first()

    if staff is None:

        return{

            "message":"Staff not found."

        },404


    booking = Booking.query.get(booking_id)

    if booking is None:

        return{

            "message":"Booking not found."

        },404


    assignment = StaffAssign.query.filter_by(

        staff_id=staff.id,

        trek_id=booking.trek_id,

        status="active"

    ).first()

    if assignment is None:

        return{

            "message":"You are not assigned to this trek."

        },403


    user = User.query.get(

        booking.user_id

    )

    trek = Trek.query.get(

        booking.trek_id

    )


    booking_status = data.get("booking_status")

    user_status = data.get("user_status")

    reason = data.get("status_reason","").strip()


    # ----------------------------------------------------
    # Validate Booking Status
    # ----------------------------------------------------

    allowed_booking_status = [

        "booked",

        "completed",

        "cancelled"

    ]

    if booking_status not in allowed_booking_status:

        return{

            "message":"Invalid booking status."

        },400


    # ----------------------------------------------------
    # Validate User Status
    # ----------------------------------------------------

    if user_status not in [

        "active",

        "inactive"

    ]:

        return{

            "message":"Invalid user status."

        },400


    # ----------------------------------------------------
    # Prevent Impossible Combination
    # ----------------------------------------------------

    if(

        user_status == "inactive"

        and

        booking_status != "cancelled"

    ):

        return{

            "message":"Inactive user must have cancelled booking."

        },400


    # ----------------------------------------------------
    # Booking Completed
    # ----------------------------------------------------

    if booking_status == "completed":

        booking.booking_status = "completed"


    # ----------------------------------------------------
    # Booking Cancelled
    # ----------------------------------------------------

    elif(

        booking_status == "cancelled"

        and

        booking.booking_status != "cancelled"

    ):

        if not reason:

            return{

                "message":"Reason is required."

            },400

        booking.booking_status = "cancelled"

        booking.cancelled_by = "staff"

        booking.status_reason = reason

        trek.available_slots += 1

        if booking.payment_status == "paid":

            booking.payment_status = "refunded"


    # ----------------------------------------------------
    # User Active
    # ----------------------------------------------------

    if user_status == "active":

        user.status = "active"

        user.status_reason = None


    # ----------------------------------------------------
    # User Inactive
    # ----------------------------------------------------

    else:

        if not reason:

            return{

                "message":"Reason is required."

            },400

        user.status = "inactive"

        user.status_reason = (

            f"Inactivated by Staff | {reason}"

        )

        if booking.booking_status != "cancelled":

            booking.booking_status = "cancelled"

            booking.cancelled_by = "staff"

            booking.status_reason = reason

            trek.available_slots += 1

            if booking.payment_status == "paid":

                booking.payment_status = "refunded"


    db.session.commit()

    return{

        "message":"Participant updated successfully."

    },200

# ---------------------- All Assigned Participants ----------------------

def get_all_assigned_participants(user_id):

    staff = User.query.filter_by(

        id=user_id,

        role="staff"

    ).first()

    if staff is None:

        return{

            "message":"Staff not found."

        },404

    assignments = StaffAssign.query.filter_by(

        staff_id=staff.id

    ).all()

    trek_list=[]

    for assignment in assignments:

        trek = Trek.query.filter_by(

            id=assignment.trek_id,

            is_deleted=False

        ).first()

        if trek is None:

            continue

        bookings = (

            Booking.query

            .filter(

                Booking.trek_id == trek.id

            )

            .order_by(

                Booking.booking_date.desc()

            )

            .all()

        )

        participant_list=[]

        for booking in bookings:

            user = User.query.get(

                booking.user_id

            )

            if user is None:

                continue

            participant_list.append({

                "booking_id":booking.id,

                "user_id":user.id,

                "name":user.name,

                "email":user.email,

                "phone":user.phone,

                "gender":user.gender,

                "booking_status":booking.booking_status,

                "payment_status":booking.payment_status

            })

        trek_list.append({

            "trek_id":trek.id,

            "trek_name":trek.trek_name,

            "start_date":trek.start_date.strftime("%d/%m/%Y"),

            "end_date":trek.end_date.strftime("%d/%m/%Y"),

            "status":trek.status,

            "participant_count":len(participant_list),

            "participants":participant_list

        })

    return{

        "treks":trek_list

    },200
