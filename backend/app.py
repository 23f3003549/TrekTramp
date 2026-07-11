from flask import Flask
from flask_cors import CORS

from config import Config
from extensions import db, jwt
from extensions import mail

from default_admin import default_admin


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    # ---------------------------blueprint----------------------------

    from routes.auth_route import auth_bp
    from routes.admin_route import admin_bp
    from routes.trek_route import trek_bp
    from routes.staff_route import staff_bp
    from routes.user_route import user_bp


    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(trek_bp, url_prefix ="/api")
    app.register_blueprint(staff_bp,url_prefix="/api/staff")
    app.register_blueprint(user_bp,url_prefix="/api/user")

    

    @app.route("/")
    def home():
        return{
            "message": "TrekTramp Backend Running !!!!"
        }
    
    with app.app_context():
        db.create_all()
        print("All dtabase are created successfully!!")
        default_admin()

    return app