from werkzeug.security import generate_password_hash

from extensions import db
from models.user import User

# ------------------------- Get Profile -------------------------

def get_profile(user_id):

    user = User.query.filter_by(
        id=user_id
    ).first()

    if user is None:

        return {
            "message": "User not found."
        }, 404

    return {

        "profile": {

            "id": user.id,

            "name": user.name,

            "email": user.email,

            "phone": user.phone,

            "age": user.age,

            "gender": user.gender,

            "role": user.role

        }

    }, 200

# ------------------------- Update Profile -------------------------

def update_profile(user_id, data):

    user = User.query.filter_by(
        id=user_id
    ).first()

    if user is None:

        return {
            "message": "User not found."
        }, 404

    phone = data.get("phone")
    age = data.get("age")
    gender = data.get("gender")

    if not phone or age is None or not gender:

        return {
            "message": "Please fill all required fields."
        }, 400

    if len(phone) != 10 or not phone.isdigit():

        return {
            "message": "Phone number must contain exactly 10 digits."
        }, 400

    if age < 5 or age > 100:

        return {
            "message": "Please enter a valid age."
        }, 400

    if gender not in [

        "Male",

        "Female",

        "Other"

    ]:

        return {
            "message": "Invalid gender."
        }, 400

    existing_phone = User.query.filter(

        User.phone == phone,

        User.id != user.id

    ).first()

    if existing_phone:

        return {
            "message": "Phone number already exists."
        }, 409

    if user.role in ["staff", "admin"]:

        user.phone = phone
        user.age = age
        user.gender = gender

    elif user.role == "trekker":

        name = data.get("name")
        email = data.get("email")

        if not name or not email:

            return {

                "message":"Name and email are required."

            },400

        existing_email = User.query.filter(

            User.email == email,

            User.id != user.id

        ).first()

        if existing_email:

            return{

                "message":"Email already exists."

            },409

        user.name = name
        user.email = email
        user.phone = phone
        user.age = age
        user.gender = gender


    db.session.commit()

    return {

        "message":"Profile updated successfully.",

        "profile":{

            "id":user.id,

            "name":user.name,

            "email":user.email,

            "phone":user.phone,

            "age":user.age,

            "gender":user.gender,

            "role":user.role

        }

    },200

