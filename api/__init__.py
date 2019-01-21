import os
import json

from flask import Flask, request, Response


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.cfg')

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
    
    @app.route("/hello/<id>")
    def hello_plus_id(id=None):
        return f"Hello {id}"

    @app.route("/hello", methods=['POST'])
    def post_hello():
        response = json.dumps({ "da response": request.get_json()['message'] }, ensure_ascii=False)
        return Response(response, mimetype='application/json')

    return app
