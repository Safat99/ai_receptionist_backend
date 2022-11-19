from flask import request
from flask import current_app
from flask_restx import Resource
from src.models import User, SuperUser
from src.api import utils
from src.api.user.crud import (
    add_admin
)


class RegisterSuperUser(Resource):
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
    def post(self):
        """Login Admin"""
        resp = {}
        payload = request.get_json()
        email = payload.get("email")
        password = payload.get("password")

        admin = SuperUser.query.filter_by("email").first()
        if not admin or not bcrypt.check_password_hash(user.password, password):
            resp["message"] = "Wrong credentials provided. Check your email or password, or signup."
            return resp, 401
        
        access_token = admin.encode_token(user_id=admin.id, "access_token")
        refresh_token = admin.encode_token(user_id=admin.id, "refresh_token")

        resp["acces_token"] = access_token
        resp["refresh_token"] = refresh_token
        resp["email"] = email
        resp["message"] = "Admin name={} logged in successfully".format(admin.name)
        return resp, 201 