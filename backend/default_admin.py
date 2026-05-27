from werkzeug.security import generate_password_hash
from extensions import db
from models import User

def default_admin():
    admin = User.query.filter_by(role = "admin").first()

    if not admin:
        hash_pass = generate_password_hash("Admin@123")

        admin = User(
            name = "Admin User",
            email = "trekadmin1@gmail.com",
            hash_password = hash_pass,
            role = "admin",
            status = "active",


        )
        db.session.add(admin)
        db.session.commit()
        print("Default admin created successfully!!!")

    else:
        print("Default admin already exist!!!")    