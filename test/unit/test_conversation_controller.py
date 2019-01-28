import pytest
from flask import url_for

@pytest.fixture
def setup_database():
    print('in the database setup fixture')
    from api import db
    db.drop_all()
    db.create_all()


class TestApp:
    def test_get_convo_by_id(self, client, setup_database):
        setup_database()
        res = client.get(url_for('conversation_api.get_single_conversation_by_id', conversation_id=1))
        assert res.status_code == 200
        assert res.json == [{
                                "content": "hell0 number 2", 
                                "id": 1, 
                                "sender_id": 1
                            }]
