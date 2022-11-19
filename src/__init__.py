import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from src.api import api

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
from src import models

def create_app():
    app = Flask(__name__)
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app,db)
    bcrypt.init_app(app)
    # app.run(debug=True)
    return app