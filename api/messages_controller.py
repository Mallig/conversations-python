import json

from flask import Flask, request, Response, Blueprint
from api import db, models
from sqlalchemy.exc import SQLAlchemyError

conversations_api = Blueprint('conversations_api', __name__)

@conversations_api.route("/messages", methods=['POST'])
def post_messages():
    json_data = request.get_json()
    new_message = models.Message(sender_id=json_data['sender_id'], 
                                 receiver_id=json_data['receiver_id'], 
                                 content=json_data['content'])

    db.session.add(new_message)
    
    try:
        db.session.commit()
        response = json.dumps({ "saved": True }, ensure_ascii=False)
        return Response(response, mimetype='application/json')
    except SQLAlchemyError as e:
        error = str(e.orig)
        response = json.dumps({ "saved": False, "error": error }, ensure_ascii=False)
        return Response(response, mimetype='application/json')


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
    and save the 2 x user_id, conversation_id trio in the conversation table
    2) it will find the conversation between these two people and add that conversation_id
    and message_id pair in the conversation table
    '''

'''
@conversations_api.route("/messages", methods=['POST'])
def post_hello():
    response = json.dumps({ "da response": request.get_json()['message'] }, ensure_ascii=False)
    return Response(response, mimetype='application/json')
'''
    