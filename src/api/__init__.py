from flask_restx import Api
from src.api.ping import ping_namespace

api = Api(version="1.0", title="ai receptionist docs")

api.add_namespace(ping_namespace, path="/ping")