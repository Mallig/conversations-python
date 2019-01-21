import os
import json

from api.messages_controller import conversations_api
from flask import Flask, request, Response, Blueprint


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.cfg')
    app.register_blueprint(conversations_api)


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.cfg', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    

    return app
