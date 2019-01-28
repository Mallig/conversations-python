import pytest
from flask import url_for

class TestApp:
    def test_get_convo_by_id(self, client, setup_database, seed_database):
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
