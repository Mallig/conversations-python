import pytest
from api import conversation_service
from data import conversation_request, create_message_response, latest_conversations_response, valid_json_message, invalid_json_message

class TestConversationService:
    def test_conversation_messages(self, client, setup_database, seed_database, db_session):
        messages = conversation_service.conversation_messages(1, db_session)
        assert messages == conversation_request

    def test_create_and_commit_message(self, client, setup_database, db_session):
        commit_response = conversation_service.create_and_commit_message(valid_json_message, db_session)
        assert commit_response == create_message_response["succeeded"]

    def test_create_and_commit_invalid_message(self, client, setup_database, db_session):
        commit_response = conversation_service.create_and_commit_message(invalid_json_message, db_session)
        assert commit_response == create_message_response["failed"]

    def test_get_latest_conversations(self, client, setup_database, add_latest_conversations, db_session):
        response = conversation_service.latest_conversations(1, db_session)
        assert response == latest_conversations_response