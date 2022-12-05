from flask import request, flash
from flask_restx import Resource, Namespace, fields
from src.models import User, SuperUser, UserAudio
from src.api import utils
from src import bcrypt
from src.api.user.crud import (
    add_admin,
    add_user,
    add_userImage,
    add_userAudio
)
from src.api.utils import save_photo, save_audio, save_temp_audio, save_temp_photo
from src.fr_module import face_recognition_module
from src.speech_recognition_module import speaker_recognition_module


user_namespace = Namespace('user')
login_admin = user_namespace.model(
    "LoginAdmin",
    {
        "email": fields.String(required=True),
        "password": fields.String(required=True),
    },
)
register_admin = user_namespace.model(
    "register for admin",
    {
        "email": fields.String(required=True),
        "password": fields.String(required=True),
        "name": fields.String(required=True),
    },
)
register_user = user_namespace.model(
    "register for user",
    {
        "userName": fields.String(required=True),
        "role": fields.String(required=True),
        # "userImg": fields.String(required=True),
        # "userImg_mimetype": fields.String(required=True),
        # "userAudioLocation": fields.String(required=True),
    },
)
# upload_image = user_namespace.model(
#     "upload image"
#     {
#         "file" : fields
#     }
# )


class RegisterSuperUser(Resource):
    @user_namespace.expect(register_admin)
    def post(self):
        """Register new admin"""
        resp = {}
        payload = request.get_json()
        name = payload.get("name")
        email = payload.get("email")
        password = payload.get("password")
        if name == None or email == None or password == None:
            resp["message"] = "Invalid payload given"
            return resp, 400
        admin = SuperUser.query.filter_by(email=email).first()
        if admin:
            resp["message"] = "This email has already been used. Try with another"
            return resp, 400
        add_admin(email=email, name=name, password = password)
        admin = SuperUser.query.filter_by(email=email).first()
        resp["email"] = email
        resp["message"] = "new Admin added. Wait for verification"
        resp["admin_id"] = admin.id
        return resp, 201
    

class LoginSuperUser(Resource):
    @user_namespace.expect(login_admin)
    def post(self):
        """Login Admin"""
        resp = {}
        payload = request.get_json()
        email = payload.get("email")
        password = payload.get("password")

        admin = SuperUser.query.filter_by(email = email).first()
        if not admin or not bcrypt.check_password_hash(admin.password, password):
            resp["message"] = "Wrong credentials provided. Check your email or password, or signup."
            return resp, 401
        
        access_token = admin.encode_token(user_id=admin.id, token_type="access_token")
        refresh_token = admin.encode_token(user_id=admin.id, token_type="refresh_token")

        resp["acces_token"] = access_token
        resp["refresh_token"] = refresh_token
        resp["email"] = email
        resp["message"] = "Admin name={} logged in successfully".format(admin.name)
        return resp, 201



class RegisterNewUserBasic(Resource):
    @user_namespace.expect(register_user)
    def post(self):
        """Register new user"""
        resp = {}
        payload = request.get_json()
        userName = payload.get("userName")
        role = payload.get("role")
        # userImg = payload.get("userImg")
        # userImg_mimetype = payload.get("userImg_mimetype")
        # userAudioLocation = payload.get("userAudioLocation")
        uid = utils.unique_user_id(role=role)

        if userName == None or role == None:
            resp["message"] = "Invalid payload given"
            return resp, 400
        user = User.query.filter_by(userName=userName).first()
        if user:
            resp["message"] = "This userName has already been used. Try with another"
            return resp, 400
        add_user(uid=uid, userName=userName, role=role)
        
        resp["userName"] = userName
        resp["message"] = "User added"
        resp["uid"] = str(uid)
        return resp, 201

class RegisterNewUserImage(Resource):
    def post(self):
        """add user image"""
        resp = {}
        uid = request.form['uid']
        try:
            users_image_obj = User.query.filter_by(uid=uid).first()
            userName = users_image_obj.userName
        except:
            users_image_obj = None
            resp["message"] = "no user found against this uid"
            return resp, 405
        
        if 'file' not in request.files:
            flash('No file part')
            resp["message"] = "No file part"
            return resp, 405
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash("No selected file")
            resp["message"] = "No selected file"
            return resp, 405
        filename, mediatype = save_photo(file)
        face_encoding = face_recognition_module.register_face(image_file_path=('data/images/' + filename), user_id=uid, name=userName)
        if type(face_encoding) != list:
            resp["message"] = "cannot encode image file properly!! returned with {}".format(face_encoding)
            return resp, 405
        add_userImage(uid=uid, filename=filename, mediatype=mediatype, face_encoding=str(face_encoding))
        resp["message"] = "saved in json and db succesfully"
        return resp, 200
        
class RecognizeWithImage(Resource):
    def post(self):
        """upload image for recognize"""
        resp = {}
        
        if 'file' not in request.files:
            resp["message"] = "No file part"
            return resp, 405
        file = request.files['file']
        if file.filename == '':
            resp["message"] = "No selected file"
            return resp, 405
        
        filename, mediatype = save_temp_photo(file=file, filename=file.filename)
        result = face_recognition_module.recognize_face(image_file_path="data/images/" + filename)
        if type(result) == int:
            resp["message"] = "cannot encode image, please capture again"
            return resp, 405
        # elif type(result) == str:
        else: 
            if result[0] == 'U':
                resp["message"] = "Unknown user"
                return resp, 405
            else:
                person_uid = result
                person_name = User.query.filter_by(uid=person_uid).first().userName
        resp["message"] = "User {} found succesfully!!! Ready for login".format(person_name)
        resp["userName"] = person_name
        resp["uid"] = person_uid
        return resp, 200


class RegisterNewUserAudio(Resource):
    def post(self):
        """upload audio for registration"""
        resp = {}
        uid = request.form['uid']
        try:
            users_image_obj = User.query.filter_by(uid=uid).first()
            userName = users_image_obj.userName
        except:
            users_image_obj = None
            resp["message"] = "no user found against this uid"
            return resp, 405
        
        if 'file' not in request.files:
            resp["message"] = "No file part"
            return resp, 405
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        filename = file.filename
        if filename == '':
            resp["message"] = "No selected file"
            return resp, 405
        ## the model can only work with .wav file
        elif filename.rsplit('.',1)[1] != 'wav':
            resp["message"] = "only .wav files are allowed"
            return resp, 405

        filename = save_audio(file=file)
        speaker_model_path = speaker_recognition_module.register_speaker('data/audios/'+ filename, user_id = userName)
        if speaker_model_path == -1:
            resp["message"] = "speaker register operation failed"
            return resp, 405
        add_userAudio(uid=uid, userAudioPath='data/audios/'+filename, userAudioGMMPath=speaker_model_path)
        resp["message"] = "saved in .gmm and location in db succesfully"
        return resp, 200

class RecognizeWithAudio(Resource):
    def post(self):
        """the audio login api"""
        resp = {}
        if 'file' not in request.files:
            resp["message"] = "No file part"
            return resp, 405
        file = request.files['file']
        if file.filename == '':
            resp["message"] = "No selected file"
            return resp, 405
        ## the model can only work with .wav file
        elif file.filename.rsplit('.',1)[1] != 'wav':
            resp["message"] = "only .wav files are allowed"
            return resp, 405
        save_temp_audio(file=file, filename='test_temp_audio.wav')
        ## manually searching from the audio files and recognize
        detected_user_name, score = speaker_recognition_module.recognize_speaker(audio_path='data/audios/test_temp_audio.wav')
        if detected_user_name == -1:
            resp["message"] = "fails to recognize any audios"
            return resp, 405
        user = User.query.filter_by(userName=detected_user_name).first()
        if user == None:
            resp["message"] = "audio detected but cannot find any relavant user in DB"
            return resp, 405
        else:
            uid = user.uid
        userAudio = UserAudio.query.filter_by(uid=uid).first()
        if userAudio == None:
            resp["message"] = "userAudio table data missing"
            return resp, 405
        else:
            userAudioPath = userAudio.userAudioPath
        
        resp["message"] = "successfully Detected USER for log in"
        resp["uid"] = uid
        resp["userAudioPath"] = userAudioPath
        return resp, 200


class UploadImage(Resource):
    def post(self):
        # check if the post request has the file part
        resp = {}
        if 'file' not in request.files:
            flash('No file part')
            resp["message"] = "No file part"
            return resp, 405
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash("No selected file")
            resp["message"] = "No selected file"
            return resp, 405
        filename, mediatype = save_photo(file)
        resp["message"] = "pic uploaded and saved successfully with name:{}".format(filename)
        resp["filename"] = filename
        resp["mediatype"] = mediatype
        return resp, 200
        

user_namespace.add_resource(LoginSuperUser, "/loginAsSuperUser")
user_namespace.add_resource(RegisterSuperUser, "/registerSuperUser")
user_namespace.add_resource(RegisterNewUserBasic, "/registerNewUser")
user_namespace.add_resource(UploadImage, "/upload_image")
user_namespace.add_resource(RegisterNewUserImage, "/registerNewUserImage")
user_namespace.add_resource(RegisterNewUserAudio, "/registerNewUserAudio")
user_namespace.add_resource(RecognizeWithAudio, "/recognizeWithAudio")
user_namespace.add_resource(RecognizeWithImage,"/RecognizeWithImage")