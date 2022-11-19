from flask import request
from flask_restx import Resource, Namespace, fields
from src.models import User
from src.api.admin.crud import (
    verify_user
)

admin_namespace = Namespace('admin')

new_user = admin_namespace.model(
    "Admin opertaion on new user",
    {
        "uid": fields.String(),
    },
)

user_model = admin_namespace.model(
    "Show all new users",
    {
        "uid": fields.String(),
        "userName": fields.String(),
        "role": fields.String(),
        "isVerified": fields.Boolean(),
        "userImg": fields.String(),
        "userImg_mimetype": fields.String(),
        "userAudioLocation": fields.String(),
        "registeredDate": fields.DateTime(),
    },
)

class New_Users(Resource):
    @admin_namespace.marshal_with(user_model, as_list=True)
    @admin_namespace.doc(params={'Authorization': {"type": "Bearer", "in": "header"}})
    def get(self):
        """new user list"""
        all_new_users = User.query.filter_by(isVerified=False).all()
        return all_new_users, 200
    
    @admin_namespace.expect(new_user)
    def put(self):
        """Verify user"""
        resp = {}
        payload = request.get_json()
        uid = payload.get("uid")
        user = User.query.filter_by(uid=uid).first()
        if not user:
            resp["message"]= "User doesn't exist"
            return resp, 400
        verify_user(uid, verify=True)   
        resp['uid'] = uid
        resp['message'] = 'User verified successfully!' 
        return resp, 201


admin_namespace.add_resource(New_Users, "/new_users")
