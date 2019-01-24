import os
import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URL'] if 'DATABASE_URL' in app.config else 'postgresql://localhost/conversations_python'

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # create db instance
    # TODO - REMOVE GLOBAL VARIABLE 
    global db
    db = SQLAlchemy(app)
    from api import models
    db.create_all()

    from api.messages_controller import conversations_api
    app.register_blueprint(conversations_api)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
