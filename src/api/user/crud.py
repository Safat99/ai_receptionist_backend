from src import db
from src.models import SuperUser, User, UserImage, UserAudio

def add_admin(**kwargs):
    """this api will be removed later"""
    admin = SuperUser(
        email=kwargs["email"],
        password=kwargs["password"],
        name = kwargs["name"]
    )
    db.session.add(admin)
    db.session.commit()

def add_user(**kwargs):
    """add new user(don't add admin)"""
    user = User(
        uid = kwargs["uid"],
        userName=kwargs["userName"],
        role = kwargs["role"],
        # userImg=kwargs["userImg"],
        # userImg_mimetype=kwargs["userImg_mimetype"],
        # userAudioLocation=kwargs["userAudioLocation"]
    )
    db.session.add(user)
    db.session.commit()

def add_userImage(**kwargs):
    """add newUsers image to the userImage table"""
    image_file = UserImage(
        uid = kwargs["uid"],
        userImg = kwargs["filename"],
        userImg_mimetype = kwargs["mediatype"],
        userImg_encoded_value = kwargs["face_encoding"]
    )
    db.session.add(image_file)
    db.session.commit()


def add_userAudio(uid, userAudioPath,userAudioGMMPath):
    """add newUsers Audio file to the UserAudio table"""
    audio_obj = UserAudio(
        uid = uid,
        userAudioPath = userAudioPath
        userAudioGMMPath = userAudioGMMPath
    )
    db.session.add(audio_obj)
    db.session.commit()