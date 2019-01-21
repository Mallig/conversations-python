import json

from flask import Flask, request, Response, Blueprint

conversations_api = Blueprint('conversations_api', __name__)

@conversations_api.route("/messages", methods=['POST'])
def post_messages():
    '''
    form_data = request.form
    id = Message.create({
        sender_id: form_data['sender_id],
        content: form_data['content']
    }).id
    Conversation.create({
        sender_id: form_data['sender_id'],
        receiver_id: form_data['receiver_id'],
        message_id: id
    })
    this conversation create will do one of two things:
    1) it will create a new row in the conversation/user with these people in it
    and save the message_id, conversation_id pair in the conversation table
    2) it will find the conversation between these two people and add that conversation_id
    and message_id pair in the conversation table
    '''

@conversations_api.route("/messages", methods=['POST'])
def post_hello():
    response = json.dumps({ "da response": request.get_json()['message'] }, ensure_ascii=False)
    return Response(response, mimetype='application/json')
    