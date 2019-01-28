import os
import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from api.database import db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_pyfile(test_config, silent=True)

    # ensure the instance folder exists
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

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
