from flask import jsonify, request, Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db

from models.user import User

def register(data):
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    # age = data.get("age")
    # phone = data.get("phone")
    # gender = data.get("gender")

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

    new_user = User(
        name = name,
        email = email,
        hash_password = hash_pass,
        # age = age,
        # phone = phone,
        # gender = gender,

    )
    db.session.add(new_user)
    db.session.commit()

    return {
        "message": f"user with email id:{email} registered successfully"
    }, 201

#-------------------login-------------------------
def login(data):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {
            "message": "Email and password required"
        }, 400
    
    user = User.query.filter_by(email = email).first()

    if not user:
        return {
            "message": "Invalid email or password"
        }, 401
    
    is_valid_password = check_password_hash(user.hash_password, password)

    if not is_valid_password:
        return {
            "message":"Invalid email or password"
        }, 401
    
    status = user.status
    if status != "active":
        return {
            "message" : f"Account is {status}"
        }, 403
    
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role
        }
    )
    refresh_token = create_refresh_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role
        }
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token" : refresh_token,
        "role" : user.role,
        "name": user.name,
        "must_change_password" : user.must_change_password
    }, 200




    

    
    

