from flask_restx import Api
from src.api.ping import ping_namespace
from src.api.user.api import user_namespace
from src.api.admin.api import admin_namespace

api = Api(version="1.0", title="ai receptionist docs", doc="/docs", prefix= "/api/v1")

api.add_namespace(ping_namespace, path="/ping")
api.add_namespace(user_namespace, path="/user")
api.add_namespace(admin_namespace, path="/admin")
