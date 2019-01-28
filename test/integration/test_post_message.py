import pytest
from flask import url_for, json

class TestApp:
    def test_post_message_for_existing_conversation(self, client, setup_database, seed_database):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }
        data = {
            'sender_id': 1,
            'receiver_ids': [
                2
            ],
            'content': 'test message'
        }
        res = client.post('/messages', data=json.dumps(data), headers=headers)
        assert res.status_code == 200
        assert res.json == { 'saved': True }


    def test_post_message_for_new_conversation(self, client, setup_database):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }
        data = {
            'sender_id': 1,
            'receiver_ids': [
                2
            ],
            'content': 'test message'
        }
        res = client.post('/messages', data=json.dumps(data), headers=headers)
        assert res.status_code == 200
        assert res.json == { 'saved': True }
