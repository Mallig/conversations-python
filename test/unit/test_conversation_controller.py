import pytest
from api import conversation_controller, conversation_service
from flask import url_for, json
from data import valid_json_message, post_message_headers

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

    def test_post_message(self, client, mocker):
        mocker.spy(conversation_service, 'create_and_commit_message')
        res = client.post(url_for('conversation_api.post_message'), data=json.dumps(valid_json_message), headers=post_message_headers)
        assert res.status_code == 200
        assert conversation_service.create_and_commit_message.call_count == 1