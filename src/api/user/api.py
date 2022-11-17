from flask import request
from flask import current_app
from flask_restx import Resource
from src.models import User, SuperUser
from src.api import utils

class RegisterSuperUser(Resource):
    def post(self):
        """Register new admin"""
        payload = request.get_json()
        email = payload.get("email")
        password = payload.get("password")
        
