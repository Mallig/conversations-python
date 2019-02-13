from flask import Flask, request, Response, Blueprint, jsonify
from api import db
from api.models import Message, Conversation
from api.models import  ConversationUserJoin as JoinTable
from sqlalchemy.exc import SQLAlchemyError
from api import ConversationService

conversation_api = Blueprint('conversation_api', __name__)
db_session = db.session

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

    new_message = Message(sender_id = json_data['sender_id'], 
                          conversation_id = conversation_id, 
                          content = json_data['content'])

    db_session.add(new_message)

    try:
        db_session.commit()
        return jsonify({ "saved": True })
    except SQLAlchemyError as e:
        error = str(e.orig).split('\n')[0]
        return jsonify({ "saved": False, "error": error })


@conversation_api.route("/conversation/<int:user_id>/latest", methods=['GET'])
def get_conversation(user_id):
    conversation = db_session.query(JoinTable.conversation_id)\
        .filter(JoinTable.user_id==user_id)\
        .all()

    response = []

    for convo_id in conversation:
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
            "last_message": last_message[0] if last_message else None
        })
        
    return jsonify(response)
