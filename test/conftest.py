import pytest
from api import create_app
from flask_sqlalchemy import SQLAlchemy
from api.database import db

@pytest.fixture(scope='session')
def _db():
    '''
    Provide the transactional fixtures with access to the database via a Flask-SQLAlchemy
    database connection.
    '''
    return db

@pytest.fixture(scope='session')
def app(db=db):
    app = create_app('test_config.py', db)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def setup_database():
    clear_database_tables(db)
    seed_database

@pytest.fixture
def seed_database():
    add_one_conversation(db)

@pytest.fixture
def seed_with_conversations():
    add_latest_conversations()

@pytest.fixture(scope='session')
def database(request):
    '''
    Create a Postgres database for the tests, and drop it when the tests are done.
    '''
    pg_host = DB_OPTS.get("host")
    pg_port = DB_OPTS.get("port")
    pg_user = DB_OPTS.get("username")
    pg_db = DB_OPTS["database"]

    init_postgresql_database(pg_user, pg_host, pg_port, pg_db)

    @request.addfinalizer
    def drop_database():
        drop_postgresql_database(pg_user, pg_host, pg_port, pg_db, 9.6)

# @pytest.fixture(scope='session')
# def _db():
#     '''
#     Provide the transactional fixtures with access to the database via a Flask-SQLAlchemy
#     database connection.
#     '''
#     db = SQLAlchemy()

#     return db

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

