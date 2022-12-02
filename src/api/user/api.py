from flask import request, flash
from flask_restx import Resource, Namespace, fields
from src.models import User, SuperUser
from src.api import utils
from src import bcrypt
from src.api.user.crud import (
    add_admin,
    add_user
)
from src.api.utils import save_photo

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



class RegisterNewUser(Resource):
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


class UploadImage(Resource):
    def post(self):
        # check if the post request has the file part
        resp = {}
        if 'file' not in request.files:
            flash('No file part')
            resp["message"] = "No file part"
            return resp, 400
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash("No selected file")
            resp["message"] = "No selected file"
            return resp, 400
        save_photo(file)
        resp["message"] = "done"
        return resp, 200

        

user_namespace.add_resource(LoginSuperUser, "/loginAsSuperUser")
user_namespace.add_resource(RegisterSuperUser, "/registerSuperUser")
user_namespace.add_resource(RegisterNewUser, "/registerNewUser")
user_namespace.add_resource(UploadImage, "/upload_image")