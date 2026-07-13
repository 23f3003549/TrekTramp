from datetime import datetime

from extensions import db
from models.trek import Trek
from models.booking import Booking
from models.staff_assign import StaffAssign
from models.user import User


#-------------------------------create trek------------------------------
def create_trek(data):
    trek_name = data.get("trek_name")
    location = data.get("location")
    difficulty = data.get("difficulty")
    min_age = data.get("min_age")
    max_age = data.get("max_age")
    description = data.get("description")
    max_slots = data.get("max_slots")
    price = data.get("price")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    necessary_attributes = [trek_name, location, difficulty, max_slots, start_date, end_date]

    if not all(necessary_attributes):
        return{
            "message": "Please fill all the required fields."
        }, 400
    
    difficulty_value = ["easy", "medium", "hard"]

    if difficulty.lower() not in difficulty_value:
        return {
            "message": "Difficulty value must be Easy, Medium, Hard."
        }, 400
    
    if min_age and max_age:
        if min_age > max_age:
            return{
                "message": "Minimum age can't be greater than maximum age."
            }, 400
        
    if max_slots <= 0:
        return {
            "message": "Maximum slots must be greater than 0."
        }, 400   

    if price is not None and price < 0:
        return {
            "message": "Price cannot be negative."
        }, 400 
    
    try:

        start_date = datetime.strptime(
            start_date,
            "%Y-%m-%d"
        ).date()

        end_date = datetime.strptime(
            end_date,
            "%Y-%m-%d"
        ).date()

        duration_days = (end_date - start_date).days + 1

    except ValueError:

        return {
            "message": "Invalid date format. Use YYYY-MM-DD."
        }, 400

    if start_date >= end_date:

        return {
            "message": "End date must be after start date."
        }, 400
    

    duplicate_trek = Trek.query.filter_by(trek_name = trek_name, location = location, start_date = start_date, is_deleted=False).first()

    if duplicate_trek:
        return{
            "message": " A trek with same name, location and start date already exists."
        }, 409
    
    new_trek = Trek(
        trek_name=trek_name,
        location=location,
        difficulty=difficulty.lower(),
        min_age=min_age,
        max_age=max_age,
        duration_days=duration_days,
        description=description,
        max_slots=max_slots,
        available_slots=max_slots,
        price=price if price else 0,
        start_date=start_date,
        end_date=end_date,

    )

    db.session.add(new_trek)
    db.session.commit()

    return{
        "message": "Trek created successfully.",
        "trek": {
            "id": new_trek.id,
            "trek_name" : new_trek.trek_name,
            "location" : new_trek.location

        }
    }, 201


#---------------------------------------get all treks-----------------------------
def get_all_treks():
    treks = Trek.query.filter_by(is_deleted=False).all()
    trek_list = []

    for trek in treks:
        trek_list.append({
            "id": trek.id,
            "trek_name": trek.trek_name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "available_slots": trek.available_slots,
            "status": trek.status
            
        })
    return {
        "treks": trek_list
    } , 200   

#------------------------------get single trek-------------------------

def get_trek(trek_id):

    trek = Trek.query.filter_by(id = trek_id , is_deleted =False).first()

    if trek is None:

        return {
            "message":"Trek not found"
        },404


    assignment = StaffAssign.query.filter_by(

        trek_id=trek.id,

        status="active"

    ).first()


    assigned_staff = None


    if assignment:

        staff = User.query.get(
            assignment.staff_id
        )

        if staff:

            assigned_staff = {

                "id":staff.id,

                "name":staff.name,

                "email":staff.email,

                "phone":staff.phone,

                "status":staff.status

            }


    return{

        "trek":{

            "id":trek.id,

            "trek_name":trek.trek_name,

            "location":trek.location,

            "difficulty":trek.difficulty,

            "duration_days":trek.duration_days,

            "min_age":trek.min_age,

            "max_age":trek.max_age,

            "price":trek.price,

            "max_slots":trek.max_slots,

            "available_slots":trek.available_slots,

            "status":trek.status,

            "start_date":trek.start_date.isoformat(),

            "end_date":trek.end_date.isoformat(),

            "description":trek.description,

            "assigned_staff":assigned_staff

        }

    },200       
#------------------------------------update trek---------------------------
def update_trek(trek_id , data):
    trek = Trek.query.filter_by(id=trek_id, is_deleted = False).first()  

    if trek is None:
        return{
            "message" :"Trek not found"
        } , 404     
    
    confirmed_bookings = Booking.query.filter_by(trek_id = trek_id, booking_status = "booked").count()
    
    trek_name = data.get("trek_name", trek.trek_name)
    location = data.get("location", trek.location)
    difficulty = data.get("difficulty", trek.difficulty)
    min_age = data.get("min_age", trek.min_age)
    max_age = data.get("max_age", trek.max_age)
    description = data.get("description", trek.description)
    max_slots = data.get("max_slots", trek.max_slots)
    price = data.get("price", trek.price)

    start_date = data.get("start_date", trek.start_date.strftime("%Y-%m-%d"))
    end_date = data.get("end_date", trek.end_date.strftime("%Y-%m-%d"))
    
    try:

        start_date = datetime.strptime(
            start_date,
            "%Y-%m-%d"
        ).date()

        end_date = datetime.strptime(
            end_date,
            "%Y-%m-%d"
        ).date()
        duration_days = (end_date - start_date).days + 1

    except ValueError:

        return {
            "message": "Invalid date format. Use YYYY-MM-DD."
        }, 400

    if start_date >= end_date:

        return {
            "message": "End date must be after start date."
        }, 400
    
    difficulty_value = ["easy", "medium", "hard"]
    if difficulty.lower() not in difficulty_value:
        return {
            "message": "Difficulty value must be Easy, Medium, Hard."
        }, 400
    
    if min_age and max_age:
        if min_age > max_age:
            return{
                "message": "Minimum age can't be greater than maximum age."
            }, 400
        
    if max_slots <= 0:
        return {
            "message": "Maximum slots must be greater than 0."
        }, 400   

    if price is not None and price < 0:
        return {
            "message": "Price cannot be negative."
        }, 400 
    
    if confirmed_bookings > 0:

        if (
            location != trek.location
            or difficulty != trek.difficulty
            or min_age != trek.min_age
            or max_age != trek.max_age
            or start_date != trek.start_date
            or end_date != trek.end_date
            or price != trek.price
        ):

            return {
                "message": (
                    "Location, difficulty, age restriction, "
                    "duration, dates and price cannot be changed "
                    "after confirmed bookings exist."
                )
            }, 400
        
        if max_slots < confirmed_bookings:

            return {
                "message": (
                    "Maximum slots cannot be less than "
                    "confirmed bookings."
                )
            }, 400
    
    trek.trek_name = trek_name
    trek.location = location
    trek.difficulty = difficulty
    trek.min_age = min_age
    trek.max_age = max_age
    trek.duration_days = duration_days
    trek.description = description
    trek.max_slots = max_slots
    trek.price = price
    trek.start_date = start_date
    trek.end_date = end_date

    if confirmed_bookings == 0:
        trek.available_slots = max_slots
    else:
        trek.available_slots = (
            max_slots - confirmed_bookings
        )

    db.session.commit()

    return {
        "message": "Trek updated successfully."
        }, 200

#-------------------------------------------------delete  trek---------------
def delete_trek(trek_id):

    trek = Trek.query.filter_by(id=trek_id, is_deleted = False).first() 

    if trek is None:
        return {
            "message": "Trek not found."
        }, 404
    
    booking_count = Booking.query.filter_by(
        trek_id=trek_id
    ).count()
    
    if not (
        trek.status in ["completed", "cancelled"] or
        (trek.status == "open" and booking_count == 0)
    ):

        return {
            "message": (
                "This trek has active bookings. "
                "Ask the assigned staff to cancel the trek first."
            )
        }, 403

    assignment = StaffAssign.query.filter_by(
        trek_id=trek_id, status="active"
    ).first()

    if assignment:
        
        assignment.status = "cancelled"

        assignment.released_at = datetime.utcnow()

    trek.is_deleted = True
    db.session.commit()

    return {
        "message": (
            "Trek deleted successfully. "
            "Assigned staff has been released."

        )
    }, 200


