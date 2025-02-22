from src.models import User
import string
import random
import os
from flask import current_app
import base64

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

def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(bytes(data, 'utf-8'))

def write_file_image(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(bytes(data))



ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def save_photo(file):
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(current_app.config.get("UPLOAD_FOLDER"), filename))
        mediatype = filename.rsplit('.',1)[1].lower()
        return filename, mediatype

def write_photo(file,name):
    if file:
        filename = 'data/images/{}.jpg'.format(name)
        write_file_image(data=file, filename=filename)
        return filename


def save_audio(file):
    filename = file.filename
    file.save(os.path.join(current_app.config.get("UPLOAD_AUDIO_FOLDER"), filename))
    return filename

def save_temp_photo(file,filename):
    """a photo will be saved"""
    if file and allowed_file(filename):
        file_extension = filename.rsplit('.', 1)[1]
        filename = 'test_temp_photo' + file_extension
        file.save(os.path.join(current_app.config.get("UPLOAD_FOLDER"), filename))
        mediatype = file_extension.lower()
        return filename, mediatype

def write_temp_photo(file):
    """ A temp photo will be write and stored"""
    if file:
        filename = 'data/images/temp_photo.jpg'
        write_file_image(data=file, filename=filename)
        return filename

###################### audio portion ############################################

def write_audio(file,name):
    if file:
        filename = 'data/audios/{}.wav'.format(name)
        write_file(data=file, filename=filename)
        return filename

def save_temp_audio(file,filename):
    file.save(os.path.join(current_app.config.get("UPLOAD_AUDIO_FOLDER"), filename))
    
def write_temp_audio(file):
    ##prv version
    # filename = 'data/audios/temp_audio.wav'
    # write_file(data=file, filename=filename)
    # return filename
    ## base64..
    filename = 'data/audios/temp_base64_audio.wav'
    wav_file = open(filename, "wb")
    decode_string = base64.urlsafe_b64decode(file)
    wav_file.write(decode_string)
    return filename