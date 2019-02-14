import os
import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from api.database import db

def create_app(config='config.py', db=db):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    if config:
        app.config.from_pyfile(config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # add app to db instance
    from api import models
    db.init_app(app)
    db.app = app
    db.create_all()

    from api.conversation_controller import conversation_api
    app.register_blueprint(conversation_api)

    return app
