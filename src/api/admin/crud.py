from src import db
from src.models import User

def verify_user(uid, verify):
    user = User.query.filter_by(uid=uid).first()
    user.isVerified = verify
    db.session.add(user)
    db.session.commit()    