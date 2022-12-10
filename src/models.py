from flask import current_app
import datetime
from src import db, bcrypt
from sqlalchemy.sql import func
import jwt

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, nullable = False, unique = True, autoincrement = True) ##this will need to be manually done in the db level
    # sqlalchemy probably does not allow auto increment feature in the non primary key
    uid = db.Column(db.String(128), primary_key = True, unique = True, nullable = False)
    userName = db.Column(db.String(128), nullable = False)
    role = db.Column(db.String(32), nullable = False)
    isVerified = db.Column(db.Boolean(), default = True, nullable = False)
    # userAudioLocation = db.Column(db.Text, nullable=True)
    registeredDate = db.Column(db.DateTime,default=func.now(), nullable=False)

    def __init__(self, uid, userName, role):
        self.uid = uid
        self.userName = userName
        self.role = role
        # self.userAudioLocation = userAudioLocation

class UserImage(db.Model):
    __tablename__ = "users_image"

    id = db.Column(db.Integer, nullable = False, primary_key = True, unique = True, autoincrement = True)
    uid = db.Column(db.String(128), db.ForeignKey("users.uid"), nullable = True)
    userImg = db.Column(db.Text, nullable = True) ## this will be a folder location
    userImg_mimetype = db.Column(db.String(128), nullable = True) #media type
    userImg_encoded_value = db.Column(db.Text, nullable=True) ## the pythonic list

    def ___init__(self, uid, userImg, userImg_mimetype, userImg_encoded_value):
        self.uid = uid
        self.userImg = userImg
        self.userImg_mimetype = userImg_mimetype
        self.userImg_encoded_value = userImg_encoded_value

class UserAudio(db.Model):
    __tablename__ = "users_audio"

    id = db.Column(db.Integer, nullable = False, primary_key = True, unique = True, autoincrement = True)
    uid = db.Column(db.String(128), db.ForeignKey("users.uid"), nullable = True)
    userAudioPath = db.Column(db.Text, nullable = True) ## this will be a folder location
    userAudioGMMPath = db.Column(db.Text, nullable = True) ## this will be the model file location of the audio

    def ___init__(self, uid, userAudioPath,userAudioGMMPath):
        self.uid = uid
        self.userAudioPath = userAudioPath
        userAudioGMMPath = userAudioGMMPath


class UserFeedback(db.Model):
    __tablename__ = "users_feedback"
    
    id = db.Column(db.Integer, nullable = False, primary_key = True, unique = True, autoincrement = True)
    uid = db.Column(db.String(128), db.ForeignKey("users.uid"), nullable = True)
    rating = db.Column(db.Integer, nullable = True)
    comment = db.Column(db.Text, nullable = True)
    feedback_time = db.Column(db.DateTime,default=func.now(), nullable=False)

    def __init__(self, uid, rating, comment):
        self.uid = uid
        self.rating = rating
        self.comment = comment

class UserUnknownQuestions(db.Model):
    __tablename__ = "users_unknown_questions"

    id = db.Column(db.Integer, nullable = False, primary_key = True, unique = True, autoincrement = True)
    uid = db.Column(db.String(128), db.ForeignKey("users.uid"), nullable = True)
    unknown_question = db.Column(db.Text, nullable = False)
    question_time = db.Column(db.DateTime,default=func.now(), nullable=False)


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
    @staticmethod
    def encode_token(user_id, token_type):
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
    @staticmethod
    def decode_token(token):
        try:
            decoded = jwt.decode(token, key=current_app.config.get("SECRET_KEY"), algorithms="HS256")
            sub = decoded["sub"]
            return sub
        except:
            return "expired"
