import os

class Config:
    SQL_ALCHEMY_TRACK_MODIFICATIONS= False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    SECRET_KEY = os.environ.get("SECRET_KEY")