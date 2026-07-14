from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    JWT_REFRESH_TOKEN_EXPIRES = 86400

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    
    MAIL_USERNAME = "23f3003549@ds.study.iitm.ac.in"
    
    MAIL_PASSWORD = "nsnh iuge gaeo nobd"
    
    MAIL_DEFAULT_SENDER = "23f3003549@ds.study.iitm.ac.in"



    REDIS_URL = "redis://localhost:6379/0"

    CACHE_TYPE = "RedisCache"

    CACHE_REDIS_URL = REDIS_URL

    CACHE_DEFAULT_TIMEOUT = 300


    broker_url = REDIS_URL

    result_backend = REDIS_URL
    
    timezone = "Asia/Kolkata"
    
    enable_utc = False