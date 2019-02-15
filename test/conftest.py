import pytest
from api import create_app
from flask_sqlalchemy import SQLAlchemy
from api.database import db

@pytest.fixture(scope='session')
def _db(db=db):
    return db

@pytest.fixture(scope='session')
def app(db=db):
    app = create_app(db=db)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def setup_database(db=db):
    clear_database_tables(db)

@pytest.fixture
def seed_database(db=db):
    add_one_conversation(db)

@pytest.fixture
def seed_with_conversations(db=db):
    add_latest_conversations(db)

@pytest.fixture(scope='session')
def database(request):
    pg_host = DB_OPTS.get("host")
    pg_port = DB_OPTS.get("port")
    pg_user = DB_OPTS.get("username")
    pg_db = DB_OPTS["database"]

    init_postgresql_database(pg_user, pg_host, pg_port, pg_db)

    @request.addfinalizer
    def drop_database():
        drop_postgresql_database(pg_user, pg_host, pg_port, pg_db, 9.6)

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
    
    db.session.commit()


def add_latest_conversations(db=db):
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

