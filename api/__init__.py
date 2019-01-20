import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # TODO - SECRET_KEY is used by Flask and extensions to keep data safe.
        # It’s set to 'dev' to provide a convenient value during development, but it should be overridden with a random value when deploying.
        # SECRET_KEY can be stored in instance/config.py 
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI= os.environ['HOME'],
        SQLALCHEMY_ECHO = True,
        SQLALCHEMY_TRACK_MODIFICATIONS = False

    )

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

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'


    # from . import db
    # db.init_app(app)

    return app