from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail , Message 
from flask_caching import Cache

mail = Mail()
cache = Cache()

db = SQLAlchemy()
jwt = JWTManager()