import pytest
from flask import url_for

class TestApp:
    def test_get_convo_by_id(self, client):
        res = client.get(url_for('conversation_api.get_single_conversation_by_id', conversation_id=1))
        assert res.status_code == 200
        assert res.json == [{
                                "content": "hell0 number 2", 
                                "id": 1, 
                                "sender_id": 1
                            }]
