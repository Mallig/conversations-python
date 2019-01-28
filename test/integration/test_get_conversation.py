import pytest
from flask import url_for

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

@pytest.fixture
def setup_database():
    print('in the database setup fixture')
    from api import db
    clear_database_tables(db)
    seed_database(db)


class TestApp:
    def test_get_convo_by_id(self, client, setup_database):
        res = client.get(url_for('conversation_api.get_single_conversation_by_id', conversation_id=1))
        assert res.status_code == 200
        assert res.json == [
                                {
                                    "id": 1,
                                    "sender_id": 1,
                                    "content": "test message"
                                },
                                {
                                    "id": 2,
                                    "sender_id": 2,
                                    "content": "test reply"
                                }
                            ]
