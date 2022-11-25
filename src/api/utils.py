from src.models import User
import string
import random
import os
from flask import current_app

def random_string(digit):
    chars = string.ascii_lowercase + string.digits
    random_string = "".join(random.choice(chars) for _ in range(digit))
    return random_string


def unique_user_id(role):
    roles = {
        'guest' : 'G',
        'faculty' : 'F',
        'student' : 'S',
        'guardian': 'P'
    }

    if (roles.get(role,"invalid_role") == 'invalid_role'):
        return 'error'

    uid = roles.get(role) + random_string(5)
    user = User.query.filter_by(uid=uid).first()
    if user:
        while user.uid == uid:
            uid = roles.get(role) + random_string(5)
    return uid

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def save_photo(file):
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(current_app.config.get("UPLOAD_FOLDER"), filename))


    



