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
    print('in the database setup fixture')
    clear_database_tables(db)
    seed_database(db)


def clear_database_tables(db):
    db.drop_all()
    db.create_all()

def seed_database(db):
    from api.models import Message, Conversation, ConversationUserJoin

    convo = Conversation()
    db.session.add(convo)
    db.session.commit()

    db.session.add(ConversationUserJoin(conversation_id = convo.id, user_id = 1))
    db.session.add(ConversationUserJoin(conversation_id = convo.id, user_id = 2))
    db.session.commit()

    from data import conversation
    for message in conversation:
        db.session.add(Message(
            sender_id = message['sender_id'],
            conversation_id = convo.id,
            content = message['content']
        ))