from flask import Flask
from flask_cors import CORS

from config import Config
from extensions import db, jwt

from default_admin import default_admin


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    jwt.init_app(app)

    # ---------------------------blueprint----------------------------

    from routes.auth_route import auth_bp
    from routes.admin_route import admin_bp
    from routes.trek_route import trek_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(trek_bp, url_prefix ="/api")

    

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