from werkzeug.security import generate_password_hash
from extensions import db

from models.user import User

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
        "message": f"Staff with email id:{email} registered successfully by admin"
    }, 201

