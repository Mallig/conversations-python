import pytest
from flask import url_for

class TestApp:
    def test_get_latest_conversations(self, client, setup_database, seed_with_conversations):
        res = client.get(url_for('conversation_api.get_conversation', user_id=1))
        assert res.status_code == 200
        assert res.json == [
                            {
                              "conversation_id": 1,
                              "last_message": "test message",
                              "participant_ids": [
                                  2
                              ]  
                            },
                            {
                              "conversation_id": 2,
                              "last_message": "test message",
                              "participant_ids": [
                                  3
                              ]  
                            },
                            {
                              "conversation_id": 3,
                              "last_message": "test message",
                              "participant_ids": [
                                  4
                              ]  
                            },
                            {
                              "conversation_id": 4,
                              "last_message": "test message",
                              "participant_ids": [
                                  5
                              ]  
                            },
                            {
                              "conversation_id": 5,
                              "last_message": "test message",
                              "participant_ids": [
                                  6
                              ]  
                            }
                           ]