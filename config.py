from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BAN_SYSTEM_ENABLED = False
    EMAIL_VERIFICATION_ENABLED = False

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "app.fleetstore@gmail.com"
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = "RoboGeb <app.fleetstore@gmail.com"

ALLOWED_IMG_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
