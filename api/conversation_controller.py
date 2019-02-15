from flask import Flask, request, Response, Blueprint, jsonify
from api import conversation_service

conversation_api = Blueprint('conversation_api', __name__)

@conversation_api.route("/conversation/<int:conversation_id>/id", methods=["GET"])
def get_single_conversation_by_id(conversation_id):
    response = conversation_service.conversation_messages(conversation_id)
    return jsonify(response)

@conversation_api.route("/messages", methods=['POST'])
def post_message():
    json_data = request.get_json()
    response = conversation_service.create_and_commit_message(json_data)
    return jsonify(response)

@conversation_api.route("/conversation/<int:user_id>/latest", methods=['GET'])
def get_latest_conversations(user_id):
    response = conversation_service.latest_conversations(user_id)
    return jsonify(response)

@conversation_api.route("/")
def welcome():
    return "Whatsapp Conversation 2 Python Boogaloo"