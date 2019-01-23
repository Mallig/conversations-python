from flask import Flask, request, Response, Blueprint, json
from api import db, models
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

conversations_api = Blueprint('conversations_api', __name__)
db_session = db.session

@conversations_api.route("/messages", methods=['POST'])
def post_messages():
    json_data = request.get_json()

    # TODO - flatten this array, then multiple receiver ids can be sent and the code will still execute correctly
    user_ids = [json_data['sender_id'], json_data['receiver_id']]
    conversation = get_conversation(user_ids)

    if not conversation:
        conversation = models.Conversation()
        db_session.add(conversation)
        db_session.commit()

        for user_id in user_ids:
            db_session.add(models.ConversationUserJoin(conversation_id = conversation.id,
                                                       user_id = user_id))
            
        db_session.commit()

        conversation_id = conversation.id
    else:
        conversation_id = conversation[0]

    # create message object with conversation_id and try to commit to database
    new_message = models.Message(sender_id = json_data['sender_id'], 
                                 conversation_id = conversation_id, 
                                 content = json_data['content'])

    db_session.add(new_message)

    try:
        db_session.commit()
        return json.jsonify({ "saved": True })
    except SQLAlchemyError as e:
        error = str(e.orig).split('\n')[0]
        return json.jsonify({ "saved": False, "error": error })


def get_conversation(user_ids):
    conversation = db_session.query(models.ConversationUserJoin.conversation_id)\
    .filter(models.ConversationUserJoin.user_id.in_(user_ids))\
    .group_by(models.ConversationUserJoin.conversation_id)\
    .having(func.count()==len(user_ids))\
    .all()
    return conversation

@conversations_api.route("/testroute", methods=['GET'])
def test_route():
    new_conversation = models.Conversation()
    db_session.add(new_conversation)
    db_session.commit()

    convo_join = models.ConversationUserJoin(conversation_id = 2, user_id = 1)
    db_session.add(convo_join)
    db_session.commit()
    convo_join = models.ConversationUserJoin(conversation_id = 2, user_id = 3)
    db_session.add(convo_join)
    db_session.commit()

    return "hello"

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
    