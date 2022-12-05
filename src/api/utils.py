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

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def save_photo(file):
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(current_app.config.get("UPLOAD_FOLDER"), filename))
        mediatype = filename.rsplit('.',1)[1].lower()
        return filename, mediatype

def save_audio(file):
    filename = file.filename
    file.save(os.path.join(current_app.config.get("UPLOAD_AUDIO_FOLDER"), filename))
    return filename

def save_temp_audio(file,filename):
    file.save(os.path.join(current_app.config.get("UPLOAD_AUDIO_FOLDER"), filename))
    
def save_temp_photo(file,filename):
    if file and allowed_file(filename):
        file_extension = filename.rsplit('.', 1)[1]
        filename = 'test_temp_photo' + file_extension
        file.save(os.path.join(current_app.config.get("UPLOAD_FOLDER"), filename))
        mediatype = file_extension.lower()
        return filename, mediatype
    



