from flask import current_app
import datetime
from src import db, bcrypt
from sqlalchemy.sql import func
import jwt

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, nullable = False, unique = True, autoincrement = True)
    uid = db.Column(db.String(128), primary_key = True, unique = True, nullable = False)
    userName = db.Column(db.String(128), nullable = False)
    role = db.Column(db.String(32), nullable = False)
    isVerified = db.Column(db.Boolean(), default = True, nullable = False)
    userImg = db.Column(db.Text, nullable = False)
    userImg_mimetype = db.Column(db.Text, nullable = False) #media type
    userAudioLocation = db.Column(db.Text, nullable=False)
    registeredDate = db.Column(db.DateTime,default=func.now(), nullable=False)

    def __init__(self, uid, userName, role, userImg, userImg_mimetype, userAudioLocation):
        self.uid = uid
        self.userName = userName
        self.role = role
        self.userImg = userImg
        self.userImg_mimetype = userImg_mimetype
        self.userAudioLocation = userAudioLocation



class SuperUser(db.Model):
    __tablename__ = "super_users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)    
    # uid = db.Column(db.String(128), db.ForeignKey("users.uid"))    
    email = db.Column(db.String(128), nullable = False)
    password = db.Column(db.String(128), nullable = False)
    name = db.Column(db.String(128), nullable = False)

    def __init__(self, email, password, name):
        self.email = email
        self.name = name
        self.password = bcrypt.generate_password_hash(password, current_app.config.get("BCRYPT_LOG_ROUNDS")).decode()
    
    def encode_token(self, user_id, token_type):
        if token_type == "access_token":
            expire = current_app.config.get("ACCESS_TOKEN_EXPIRATION")
        elif token_type == "refresh_token":
            expire = current_app.config.get("REFRESH_TOKEN_EXPIRATION")
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=expire),
            "iat": datetime.datetime.utcnow(),
            "sub": user_id
        }
        return jwt.encode(payload, key=current_app.config.get("SECRET_KEY"), algorithm="HS256")

    def decode_token(token):
        try:
            decoded = jwt.decode(token, key=current_app.config.get("SECRET_KEY"), algorithms="HS256")
            sub = decoded["sub"]
            return sub
        except:
            return "expired"



