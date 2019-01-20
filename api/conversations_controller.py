import json

from flask import Flask, request, Response, Blueprint

conversations_api = Blueprint('conversations_api', __name__)

@conversations_api.route("/hello/<id>")
def hello_plus_id(id=None):
    return f"Hello {id}"

@conversations_api.route("/hello", methods=['POST'])
def post_hello():
    response = json.dumps({ "da response": request.get_json()['message'] }, ensure_ascii=False)
    return Response(response, mimetype='application/json')
    