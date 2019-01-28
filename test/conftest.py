import pytest
from api import create_app, db

@pytest.fixture
def app():
    app = create_app('test_config.py')
    app.debug = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def setup_database():
    clear_database_tables(db)

@pytest.fixture
def seed_database():
    add_one_conversation(db)

@pytest.fixture
def seed_with_conversations():
    add_latest_conversations()


def clear_database_tables(db):
    db.drop_all()
    db.create_all()

def add_one_conversation(db):
    from api.models import Message, Conversation, ConversationUserJoin

    convo = Conversation()
    db.session.add(convo)
    db.session.commit()

    db.session.add(ConversationUserJoin(conversation_id = convo.id, user_id = 1))
    db.session.add(ConversationUserJoin(conversation_id = convo.id, user_id = 2))
    db.session.commit()

    from data import conversation_seed
    for message in conversation_seed:
        db.session.add(Message(
            sender_id = message['sender_id'],
            conversation_id = convo.id,
            content = message['content']
        ))

def add_latest_conversations():
    from api.models import Message, Conversation, ConversationUserJoin
    from data import latest_conversations_seed
    for message in latest_conversations_seed:
        convo = Conversation()
        db.session.add(convo)
        db.session.commit()

        db.session.add(ConversationUserJoin(conversation_id = convo.id, user_id = 1))
        db.session.add(ConversationUserJoin(conversation_id = convo.id, user_id = message['receiver_ids'][0]))
        db.session.commit()

        db.session.add(Message(
            sender_id = message['sender_id'],
            conversation_id = convo.id,
            content = message['content']
        ))
        db.session.commit()

