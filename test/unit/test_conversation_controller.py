import pytest
from api import conversation_controller, conversation_service
from flask import url_for

class TestConversationController:
    def test_get_single_conversation_by_id(self, client, mocker):
        mocker.spy(conversation_service, 'conversation_messages')
        res = client.get(url_for('conversation_api.get_single_conversation_by_id', conversation_id=1))
        assert res.status_code == 200
        assert conversation_service.conversation_messages.call_count == 1

    def test_get_latest_conversations(self, client, mocker):
        mocker.spy(conversation_service, 'latest_conversations')
        res = client.get(url_for('conversation_api.get_latest_conversations', user_id=1))
        assert res.status_code == 200
        assert conversation_service.latest_conversations.call_count == 1
