import os

DEBUG = True
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/test.db"
SQLALCHEMY_BINDS = {
    "blogdb": SQLALCHEMY_DATABASE_URI,
}

UPLOADED_IMAGES_DEST = os.path.join(os.path.dirname(__file__), "madapp/static/uploads")
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif", "cr2"])

CSRF_ENABLED = True
CSRF_SESSION_KEY = "9bd7fa0e9238e509a18259470a1144eb"
SECRET_KEY = "9bd7fa0e9238e509a18259470a1144eb"

# Flask-Security config
SECURITY_URL_PREFIX = "/admin"
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "Ms2CoXZOo9aCnBWWUwJJaUYL"

# Flask-Security URLs, overridden because they don't put a / at the end
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_REGISTER_URL = "/register/"

SECURITY_POST_LOGIN_VIEW = "/admin/"
SECURITY_POST_LOGOUT_VIEW = "/admin/"
SECURITY_POST_REGISTER_VIEW = "/admin/"

# Flask-Security features
SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = False
