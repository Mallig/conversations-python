from flask import Flask, request, Response, Blueprint, json
from api import db
from api.models import Message, Conversation
from api.models import  ConversationUserJoin as JoinTable
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
        conversation = Conversation()
        db_session.add(conversation)
        db_session.commit()

        for user_id in user_ids:
            db_session.add(JoinTable(conversation_id = conversation.id,
                                     user_id = user_id))
            
        db_session.commit()

        conversation_id = conversation.id
    else:
        conversation_id = conversation[0]

    # create message object with conversation_id and try to commit to database
    new_message = Message(sender_id = json_data['sender_id'], 
                          conversation_id = conversation_id, 
                          content = json_data['content'])

    db_session.add(new_message)

    try:
        db_session.commit()
        return json.jsonify({ "saved": True })
    except SQLAlchemyError as e:
        error = str(e.orig).split('\n')[0]
        return json.jsonify({ "saved": False, "error": error })


@conversations_api.route("/conversations/<int:user_id>", methods=['GET'])
def get_conversations(user_id):
    conversations = db_session.query(JoinTable.conversation_id)\
        .filter(JoinTable.user_id==user_id)\
        .all()

    response = []

    for convo_id in conversations:
        user_ids = db_session.query(JoinTable.user_id)\
            .filter(JoinTable.conversation_id==convo_id[0])\
            .all()

        participants = []
        for id in user_ids:
            if id[0] != user_id:
                participants.append(id[0])

        last_message = db_session.query(Message.content)\
            .filter(Message.conversation_id==convo_id[0])\
            .order_by(Message.created_at.desc())\
            .first()

        response.append({
            "conversation_id": convo_id[0],
            "participant_ids": participants,
            "last_message": last_message[0]
        })
        
    return json.jsonify(response)


def get_conversation(user_ids):
    conversation = db_session.query(JoinTable.conversation_id)\
        .filter(JoinTable.user_id.in_(user_ids))\
        .group_by(JoinTable.conversation_id)\
        .having(func.count()==len(user_ids))\
        .all()
    return conversation
