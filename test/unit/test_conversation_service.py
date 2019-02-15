import pytest
from api import conversation_service
from data import conversation_request, create_message_response, latest_conversations_response

class TestConversationService:
    def test_find_existing_conversation(self, client, setup_database, seed_database, monkeypatch, db_session):
        mock_statement = 'select * from messages;'
        monkeypatch.setattr(db_session.execute(mock_statement), 'fetchall', [(1,)])
        conversation = conversation_service.find_or_create_conversation([1,2], db_session)
        assert conversation == 1
    
    def test_find_nonexistent_conversation(self, client, setup_database, monkeypatch, db_session):
        conversation = conversation_service.find_or_create_conversation([1,3], db_session)
        assert conversation == 1

    def test_conversation_messages(self, client, setup_database, seed_database, db_session):
        messages = conversation_service.conversation_messages(1, db_session)
        assert messages == conversation_request

    def test_create_and_commit_message(self, client, setup_database, db_session):
        valid_json_message = { "content": "test message", "sender_id": 1, "receiver_ids": [2] }
        commit_response = conversation_service.create_and_commit_message(valid_json_message, db_session)
        assert commit_response == create_message_response["succeeded"]

    def test_create_and_commit_invalid_message(self, client, setup_database, db_session):
        invalid_json_message = { "content": None, "sender_id": 1, "receiver_ids": [2] }
        commit_response = conversation_service.create_and_commit_message(invalid_json_message, db_session)
        assert commit_response == create_message_response["failed"]

    def test_get_latest_conversations(self, client, setup_database, add_latest_conversations, db_session):
        response = conversation_service.latest_conversations(1, db_session)
        assert response == latest_conversations_response