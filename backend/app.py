from flask import Flask
from flask_cors import CORS

from config import Config
from extensions import db, jwt

from models import *
from default_admin import default_admin

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    CORS(app)

    db.init_app(app)
    jwt.init_app(app)

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