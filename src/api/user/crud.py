from src import db
from src.models import SuperUser, User

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


