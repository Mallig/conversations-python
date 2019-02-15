import pytest
from flask import url_for, json
from data import post_message_headers, valid_json_message, invalid_json_message, create_message_response

class TestApp:
    def test_post_message_for_existing_conversation(self, client, setup_database, seed_database):
        res = client.post('/messages', data=json.dumps(valid_json_message), headers=post_message_headers)
        assert res.status_code == 200
        assert res.json == create_message_response["succeeded"]

    def test_post_message_for_new_conversation(self, client, setup_database):
        res = client.post('/messages', data=json.dumps(valid_json_message), headers=post_message_headers)
        assert res.status_code == 200
        assert res.json == create_message_response["succeeded"]

    def test_post_invalid_message(self, client, setup_database):
        res = client.post('/messages', data=json.dumps(invalid_json_message), headers=post_message_headers)
        assert res.status_code == 200
        assert res.json == create_message_response["failed"]