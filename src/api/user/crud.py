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

    