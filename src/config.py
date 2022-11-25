import os
from urllib.parse import quote
from dotenv import load_dotenv
load_dotenv()


class LocalConfig:
    SQL_ALCHEMY_TRACK_MODIFICATIONS= False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") % quote(os.environ.get("pass")) 
    SECRET_KEY = os.environ.get("SECRET_KEY")
    BCRYPT_LOG_ROUNDS = 8
    ACCESS_TOKEN_EXPIRATION = 3600
    REFRESH_TOKEN_EXPIRATION = 2592000
    UPLOAD_FOLDER = 'data/images/'