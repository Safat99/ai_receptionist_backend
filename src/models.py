import datetime
from src import db
from sqlalchemy.sql import func


class User(db.model):
    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement = True)
    uid = db.Column(db.String(128), primary_key = True, unique = True, nullable = False)
    userName = db.Column(db.String(128), nullable = False)
    role = db.Column(db.String(32), nullable = False)
    isVerified = db.Column(db.Boolean(), default = False, nullable = False)
    userImg = db.Columnn(db.Text, nullable = False)
    userImg_mimetype = db.Column(db.Text, nullable = False) #media type
    userAudioLocation = db.Column(db.Text, nullable=False)
    registeredDate = db.Column(db.DateTime,default=func.now() ,nullable=False)

    def __init__(self, uid, userName, role, userImg, userImg_mimetype, userAudioLocation):
        self.uid = uid
        self.userName = userName
        self.role = role
        self.userImg = userImg
        self.userImg_mimetype = userImg_mimetype
        self.userAudioLocation = userAudioLocation



class SuperUser(db.model):
    __table__ = "super_users"
    
    email = db.Column(db.String(128), nullable = True)
    password = db.Column(db.String(128), nullable = True)


