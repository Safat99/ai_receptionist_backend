import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS


cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    cors.__init__(app)
    db.init_app(app)
    bcrypt.init_app(app)

    from src import models
    migrate.init_app(app,db)
    from src.api import api
    api.init_app(app)

    # app.run(debug=True)
    return app

if __name__=='__main__':
    create_app.run(debug=True)