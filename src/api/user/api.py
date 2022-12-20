from flask import request, flash
from flask_restx import Resource, Namespace, fields
from src.models import User, SuperUser, UserAudio
from src.api import utils
from src import bcrypt
from src.api.user.crud import (
    add_admin,
    add_user,
    add_userImage,
    add_userAudio,
    save_feedback,
    save_unknown_question
)
from src.api.utils import write_photo, write_audio, write_temp_audio, write_temp_photo, save_photo
from src.api.asr import stt
from src.fr_module import face_recognition_module
from src.speech_recognition_module import speaker_recognition_module
from src.conversation_agent_module.conversation_agent_package.ConvAgent import ConvAgent
import base64


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

coversation_agent = user_namespace.model(
    "recognize question and give answer",
    {
        "uid": fields.String(required=True),
        "questions":fields.String(required=True),
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

# class RegisterNewUserImage(Resource):
#     def post(self):
#         """add user image"""
#         resp = {}
#         uid = request.form['uid']
#         try:
#             users_image_obj = User.query.filter_by(uid=uid).first()
#             userName = users_image_obj.userName
#         except:
#             users_image_obj = None
#             resp["message"] = "no user found against this uid"
#             return resp, 405
        
#         if 'file' not in request.files:
#             flash('No file part')
#             resp["message"] = "No file part"
#             return resp, 405
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit a empty part without filename
#         if file.filename == '':
#             flash("No selected file")
#             resp["message"] = "No selected file"
#             return resp, 405
#         filename, mediatype = save_photo(file)
#         face_encoding = face_recognition_module.register_face(image_file_path=('data/images/' + filename), user_id=uid, name=userName)
#         if type(face_encoding) != list:
#             resp["message"] = "cannot encode image file properly!! returned with {}".format(face_encoding)
#             return resp, 405
#         add_userImage(uid=uid, filename=filename, mediatype=mediatype, face_encoding=str(face_encoding))
#         resp["message"] = "saved in json and db succesfully"
#         return resp, 200

class RegisterNewUserImage(Resource):
    def post(self):
        """add user image blob file"""
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
            return resp, 404
        file = request.files['file'].read()
        # if user does not select file, browser also
        # submit a empty part without filename
        filename = write_photo(file=file, name=userName)
        face_encoding = face_recognition_module.register_face(image_file_path=filename, user_id=uid, name=userName)
        if type(face_encoding) != list:
            resp["message"] = "cannot encode image file properly!! returned with {}".format(face_encoding)
            return resp, 405
        add_userImage(uid=uid, filename=filename, mediatype='jpg', face_encoding=str(face_encoding))
        resp["message"] = "saved in json and db succesfully"
        return resp, 200
        
# class RecognizeWithImage(Resource):
#     def post(self):
#         """upload image for recognize"""
#         resp = {}
        
#         if 'file' not in request.files:
#             resp["message"] = "No file part"
#             return resp, 405
#         file = request.files['file']
#         if file.filename == '':
#             resp["message"] = "No selected file"
#             return resp, 405
        
#         filename, mediatype = save_temp_photo(file=file, filename=file.filename)
#         result = face_recognition_module.recognize_face(image_file_path="data/images/" + filename)
#         # print(result)``
#         if type(result) == int: 
#             resp["message"] = "cannot encode image, please capture again"
#             return resp, 405
#         # elif type(result) == str:
#         else: 
#             if result[0] == 'U':
#                 resp["message"] = "Unknown user"
#                 return resp, 405
#             else:
#                 person_uid = result
#                 person_name = User.query.filter_by(uid=person_uid).first().userName
        
#         access_token = SuperUser.encode_token(user_id=person_uid, token_type="access_token")
#         refresh_token = SuperUser.encode_token(user_id=person_uid, token_type="refresh_token")
        
#         resp["message"] = "User {} found succesfully!!! Ready for login".format(person_name)
#         resp["userName"] = person_name
#         resp["uid"] = person_uid
#         resp["access_token"] = access_token
#         resp["refresh_token"] = refresh_token
#         return resp, 200

class RecognizeWithImage2(Resource):
    def post(self):
        """with this API base64 image will be stored as file"""
        resp = {}
        if 'file' not in request.files:
            flash('No file part')
            resp["message"] = "No file part"
            return resp, 404
        file = request.files['file'].read() ##this will be the blob file
        filename = write_temp_photo(file=file)
        # mediatype = 'jpg'
        result = face_recognition_module.recognize_face(image_file_path=filename)
        # print(result)``
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

        access_token = SuperUser.encode_token(user_id=person_uid, token_type="access_token")
        refresh_token = SuperUser.encode_token(user_id=person_uid, token_type="refresh_token")
        
        resp["message"] = "User {} found succesfully!!! Ready for login".format(person_name)
        resp["userName"] = person_name
        resp["uid"] = person_uid
        resp["access_token"] = access_token
        resp["refresh_token"] = refresh_token
        return resp, 200
        


# class RegisterNewUserAudio(Resource):
#     def post(self):
#         """upload audio for registration"""
#         resp = {}
#         uid = request.form['uid']
#         try:
#             users_image_obj = User.query.filter_by(uid=uid).first()
#             userName = users_image_obj.userName
#         except:
#             users_image_obj = None
#             resp["message"] = "no user found against this uid"
#             return resp, 405
        
#         if 'file' not in request.files:
#             resp["message"] = "No file part"
#             return resp, 405
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit a empty part without filename
#         filename = file.filename
#         if filename == '':
#             resp["message"] = "No selected file"
#             return resp, 405
#         ## the model can only work with .wav file
#         elif filename.rsplit('.',1)[1] != 'wav':
#             resp["message"] = "only .wav files are allowed"
#             return resp, 405

#         filename = save_audio(file=file)
#         speaker_model_path = speaker_recognition_module.register_speaker('data/audios/'+ filename, user_id = userName)
#         if speaker_model_path == -1:
#             resp["message"] = "speaker register operation failed!! data path not found"
#             return resp, 405
#         add_userAudio(uid=uid, userAudioPath='data/audios/'+filename, userAudioGMMPath=speaker_model_path)
#         resp["message"] = "saved in .gmm and location in db succesfully"
#         return resp, 200

class RegisterNewUserAudio(Resource):
    def post(self):
        """upload audio for registration with blob"""
        resp = {}
        uid = request.form['uid']
        try:
            users_image_obj = User.query.filter_by(uid=uid).first()
            userName = users_image_obj.userName
        except:
            users_image_obj = None
            resp["message"] = "no user found against this uid"
            return resp, 405
        
        # if 'file' not in request.files:
        #     resp["message"] = "No file part"
        #     return resp, 404
        # file = request.files['file'].read()
        file = request.form['base64']

        wav_file = open('data/audios/{}.wav'.format(userName), "wb")
        decode_string = base64.b64decode(file)
        wav_file.write(decode_string)

        filename = 'data/audios/{}.wav'.format(userName)
        # filename = write_audio(file=file, name=userName)
        speaker_model_path = speaker_recognition_module.register_speaker(audio_path = filename, user_id = userName)
        if speaker_model_path == -1:
            resp["message"] = "speaker register operation failed!! data path not found"
            return resp, 405
        add_userAudio(uid=uid, userAudioPath=filename, userAudioGMMPath=speaker_model_path)
        resp["message"] = "saved in .gmm and location in db succesfully"
        return resp, 200

# class RecognizeWithAudio(Resource):
#     def post(self):
#         """the audio login api"""
#         resp = {}
#         if 'file' not in request.files:
#             resp["message"] = "No file part"
#             return resp, 405
#         file = request.files['file']
#         if file.filename == '':
#             resp["message"] = "No selected file"
#             return resp, 405
#         ## the model can only work with .wav file
#         elif file.filename.rsplit('.',1)[1] != 'wav':
#             resp["message"] = "only .wav files are allowed"
#             return resp, 405
#         save_temp_audio(file=file, filename='test_temp_audio.wav')
#         ## manually searching from the audio files and recognize
#         detected_user_name, score = speaker_recognition_module.recognize_speaker(audio_path='data/audios/test_temp_audio.wav')
#         if detected_user_name == -1:
#             resp["message"] = "fails to recognize any audios"
#             return resp, 405
#         user = User.query.filter_by(userName=detected_user_name).first()
#         if user == None:
#             resp["message"] = "audio detected but cannot find any relavant user in DB"
#             return resp, 405
#         else:
#             uid = user.uid
#         userAudio = UserAudio.query.filter_by(uid=uid).first()
#         if userAudio == None:
#             resp["message"] = "userAudio table data missing"
#             return resp, 405
#         else:
#             userAudioPath = userAudio.userAudioPath
        
#         access_token = SuperUser.encode_token(user_id=uid, token_type="access_token")
#         refresh_token = SuperUser.encode_token(user_id=uid, token_type="refresh_token")
        
#         resp["message"] = "successfully Detected USER for log in"
#         resp["uid"] = uid
#         resp["userAudioPath"] = userAudioPath
#         resp["access_token"] = access_token
#         resp["refresh_token"] = refresh_token
#         return resp, 200

class RecognizeWithAudio2(Resource):
    def post(self):
        """the audio login api"""
        resp = {}
        # if 'file' not in request.files:
        #     resp["message"] = "No file part"
        #     return resp, 404
        # file = request.files['file'].read()
        file = request.form['base64']
        # print(type(file)) ##bytes file
        # print(len(file))
        filename = write_temp_audio(file=file)
        ## manually searching from the audio files and recognize
        detected_user_name, score = speaker_recognition_module.recognize_speaker(audio_path=filename)
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
        
        access_token = SuperUser.encode_token(user_id=uid, token_type="access_token")
        refresh_token = SuperUser.encode_token(user_id=uid, token_type="refresh_token")
        
        resp["message"] = "successfully Detected USER for log in"
        resp["uid"] = uid
        resp["userAudioPath"] = userAudioPath
        resp["access_token"] = access_token
        resp["refresh_token"] = refresh_token
        return resp, 200



class UploadImage(Resource):
    def post(self):
        # check if the post request has the file part
        resp = {}
        if 'file' not in request.files:
            flash('No file part')
            resp["message"] = "No file part"
            return resp, 404
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
        
class FeedbackUser(Resource):
    def post(self):
        """user will give feedback through this api"""
        resp = {}
        payload = request.get_json()
        uid = payload.get("uid")
        comment = payload.get("comment")
        rating = payload.get("rating")
        if rating<1 or rating >5:
            resp["message"] = "user ratings have to be between 1-5"
            return resp, 405
        save_feedback(uid=uid, rating=rating, comment=comment)
        resp["message"] = "Thank you for your feedback"
        return resp, 200

class StoreUnknownQuestion(Resource):
    def post(self):
        """Unknown question will be stored in DB"""
        resp = {}
        payload = request.get_json()
        uid = payload.get("uid")
        unknown_question = payload.get("unknown_question")
        save_unknown_question(uid=uid, unknown_question=unknown_question)
        resp["message"] = "Saved your unknown questions"
        return resp, 200

class RecognizeQuestion(Resource):
    @user_namespace.expect(coversation_agent)
    def post(self):
        """with this API, a given question will be listed as known or unknown"""
        payload = request.get_json()
        uid = payload.get("uid")
        question = payload.get("question")
        conversational_agent_module = ConvAgent("multi-qa-distilbert-cos-v1")
        conversation_data = conversational_agent_module.conversation(question=question)
        # conversation_data = conversational_agent_module.conversation("ক্রেডিট ট্রান্সফার করতে চাই কি করতে হবে")
        if conversation_data["success"] == False:
            return conversation_data, 405
        else:
            if conversation_data["unknown"] == True: #don't need to store data
                return conversation_data, 401
            else:
                return conversation_data, 200 ##user will get prompt

class SpeechToText(Resource):
    def post(self):
        """generate string from speech to text in bangla"""
        resp = {}
        # if 'file' not in request.files:
        #     resp["message"] = "No file part"
        #     return resp, 404
        # file = request.files['file'].read()
        file = request.form['base64']
        # print(type(file))
        # print(len(file))
        temp_audio = write_temp_audio(file=file)
        data = stt(temp_audio)
        if data["error"] == "":
            resp["success"] = True
            resp["error"] = ""
            resp["text"] = data["text"]
            return resp, 200
        else:
            resp["success"] = False
            resp["error"] = data["error"]
            resp["text"] = ""
            return resp, 404
        

user_namespace.add_resource(LoginSuperUser, "/loginAsSuperUser")
user_namespace.add_resource(RegisterSuperUser, "/registerSuperUser")
user_namespace.add_resource(RegisterNewUserBasic, "/registerNewUser")
user_namespace.add_resource(UploadImage, "/uploadImage")
user_namespace.add_resource(RegisterNewUserImage, "/registerNewUserImage")
user_namespace.add_resource(RegisterNewUserAudio, "/registerNewUserAudio")
user_namespace.add_resource(RecognizeWithAudio2, "/recognizeWithAudio2")
user_namespace.add_resource(RecognizeWithImage2,"/RecognizeWithImage2")
user_namespace.add_resource(FeedbackUser,"/userFeedback")
user_namespace.add_resource(StoreUnknownQuestion,"/storeUnknownQuestion")
user_namespace.add_resource(RecognizeQuestion, "/recognizeQuestion")
user_namespace.add_resource(SpeechToText, "/speechToText")