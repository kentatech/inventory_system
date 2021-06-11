import secrets
import os
class Base:
    SECRET_KEY = secrets.token_hex(16)
class Development(Base):
    FLASK_APP = os.environ.get("FLASK_APP")
    FLASK_ENV= os.environ.get("FLASK_ENV")
    DATABASE = os.environ.get("DATABASE")
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")