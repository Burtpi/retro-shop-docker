from flask import Flask
from flask_limiter.util import get_remote_address
from flask_security import SQLAlchemySessionUserDatastore, Security
from flask_mailman import Mail
from flask_limiter import Limiter
import os
from dotenv import load_dotenv

from database import db
from forms import ExtendedRegisterForm, ExtendedLoginForm
from models import User, Role, Product

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['SECURITY_PASSWORD_SALT'] = os.getenv("SALT")
app.config["SECURITY_REGISTERABLE"] = True
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Strict',
)
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_SEND_PASSWORD_CHANGE_EMAIL'] = False
app.config['SECURITY_USERNAME_ENABLE'] = True
app.config['SECURITY_PASSWORD_LENGTH_MIN'] = 12
app.config['SECURITY_PASSWORD_COMPLEXITY_CHECKER'] = 'zxcvbn'
app.config['SECURITY_PASSWORD_CHECK_BREACHED'] = 'best-effort'
app.config['SECURITY_TOTP_SECRETS'] = {1: os.getenv("TOTP_SECRET")}
app.config['SECURITY_TOTP_ISSUER'] = "RetroShop"
app.config['SECURITY_CONFIRMABLE'] = False
app.config['SECURITY_CHANGEABLE'] = True
app.config['SECURITY_TWO_FACTOR'] = True
app.config['SECURITY_TWO_FACTOR_REQUIRED'] = True
app.config['SECURITY_TWO_FACTOR_ENABLED_METHODS'] = ['authenticator']
app.config['SECURITY_TWO_FACTOR_ALWAYS_VALIDATE'] = True
app.config['SECURITY_TWO_FACTOR_VALIDITY_COOKIE'] = {'httponly': True, 'secure': True, 'samesite': 'Strict'}
app.config['SECURITY_TWO_FACTOR_RESCUE_EMAIL'] = False
app.config['SECURITY_EMAIL_VALIDATOR_ARGS'] = {"check_deliverability": False}
app.config['SECURITY_TRACKABLE'] = True
app.config['SECURITY_CONFIRM_EMAIL_WITHIN'] = "1 day"
app.config['SECURITY_CSRF_COOKIE'] = {"samesite": "Strict", "httponly": True, "secure": True}
app.config['SECURITY_TOKEN_MAX_AGE'] = 2592000
app.config['SECURITY_USERNAME_REQUIRED'] = True
app.config['SECURITY_PASSWORD_HASH'] = 'argon2'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQL_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv("RECAPTCHA_PUBLIC")
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv("RECAPTCHA_SECRET")
# app.config['MAIL_SERVER'] = 'smtp.google.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
# app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")


db.init_app(app)
mail = Mail(app)

user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
security = Security(app, user_datastore, register_form=ExtendedRegisterForm, login_form=ExtendedLoginForm)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "100 per hour", "5 per second"],
    storage_uri="memory://",
)

with app.app_context():
    db.create_all()

