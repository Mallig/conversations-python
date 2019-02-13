from flask import Flask, request, Response, Blueprint, jsonify
from api import ConversationService

conversation_api = Blueprint('conversation_api', __name__)

@conversation_api.route("/conversation/<int:conversation_id>/id", methods=["GET"])
def get_single_conversation_by_id(conversation_id):
    response = ConversationService.conversation_messages(conversation_id)
    return jsonify(response)

@conversation_api.route("/messages", methods=['POST'])
def post_messages():
    json_data = request.get_json()
    user_ids = [json_data['sender_id']]
    user_ids.extend(json_data['receiver_ids'])

    conversation_id = ConversationService.find_or_create_conversation(user_ids)
    response = ConversationService.create_and_commit_message(json_data, conversation_id)
    return jsonify(response)

@conversation_api.route("/conversation/<int:user_id>/latest", methods=['GET'])
def get_conversation(user_id):
    response = ConversationService.get_latest_conversations(user_id)
    return jsonify(response)
