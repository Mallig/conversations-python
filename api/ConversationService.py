from api import db
from api.models import Conversation, Message
from api.models import ConversationUserJoin as JoinTable
from sqlalchemy import func, and_

db_session = db.session

def find_or_create_conversation(user_ids, db_session=db_session):
    conversation_id = get_conversation_id(user_ids, db_session=db_session)
    return create_conversation(user_ids, db_session=db_session) if not conversation_id else conversation_id

def get_conversation_id(user_ids, db_session=db_session):
    first_query = f"""SELECT DISTINCT(conversation_id)
                        FROM conversation_user_join
                        WHERE user_id
                        IN {convert_to_string(user_ids)}"""

    second_query = f"""SELECT conversation_id,
                        COUNT(user_id) AS total_users,
                        COUNT(user_id)
                    FILTER (
                        WHERE user_id
                        IN {convert_to_string(user_ids)}
                    ) AS provided_users
                    FROM conversation_user_join
                    WHERE conversation_id IN (
                        {first_query}
                    ) GROUP BY conversation_id"""

    query = f"""SELECT conversation_id
                FROM (
                    {second_query}
                ) AS subq
                WHERE subq.provided_users=subq.total_users
                AND subq.total_users={len(user_ids)};"""

    conversation_id = db_session.execute(query).fetchall()
    return None if not conversation_id else conversation_id[0][0]

def create_conversation(user_ids, db_session=db_session):
    conversation = Conversation()
    db_session.add(conversation)
    db_session.commit()

    create_join_rows(user_ids, conversation.id, db_session)
    return conversation.id

def create_join_rows(user_ids, convo_id, db_session=db_session):
    for user_id in user_ids:
        db_session.add(JoinTable(conversation_id = convo_id,
                                    user_id = user_id))
    db_session.commit()

def convert_to_string(arr):
    return str.replace(
        str.replace(
            str(arr), '[', "("
        ), "]", ")"
    )

def conversation_messages(conversation_id):
    messages = db_session.query(Message)\
    .filter(Message.conversation_id==conversation_id)\
    .order_by(Message.created_at)\
    .all()

    return parse_conversation_messages(messages)

def parse_conversation_messages(sqlalchemy_messages):
    response = []
    for message in sqlalchemy_messages:
        response.append({
            "sender_id": message.sender_id,
            "content": message.content,
            "id": message.id
        })
    return response

def get_conversation_interlocutors(convo_id, user_id):
    user_ids = db_session.query(JoinTable.user_id)\
    .filter(and_(JoinTable.conversation_id==convo_id[0], JoinTable.user_id!=user_id))\
    .all()

    return [i[0] for i in user_ids]

def get_conversation_latest_message(convo_id):
    return db_session.query(Message.content)\
    .filter(Message.conversation_id==convo_id[0])\
    .order_by(Message.created_at.desc())\
    .first()

def construct_conversation(convo_id, user_id):
    interlocutors = get_conversation_interlocutors(convo_id, user_id)
    latest_message = get_conversation_latest_message(convo_id)

    return {
        "conversation_id": convo_id[0],
        "participant_ids": interlocutors,
        "last_message": latest_message[0] if latest_message else None
    }

def get_latest_conversations(user_id):
    conversations = db_session.query(JoinTable.conversation_id)\
        .filter(JoinTable.user_id==user_id)\
        .all()

    response = map(lambda convo_id: construct_conversation(convo_id, user_id) ,conversations)

    return list(response)
