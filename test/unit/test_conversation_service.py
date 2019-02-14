import pytest
from api import conversation_service
from api import db
from api.models import Conversation
from flask import current_app

class TestConversationService:
    def test_find_existing_conversation(self, client, setup_database, monkeypatch, db_session):
        mock_statement = 'select * from messages;'
        monkeypatch.setattr(db.session.execute(mock_statement), 'fetchall', [(1,)])
        conversation = conversation_service.find_or_create_conversation([1,2], db_session)
        assert conversation == 1
    
    def test_find_nonexistent_conversation(self, client, setup_database, monkeypatch, db_session):
        mock_statement = 'select * from messages;'
        conversation = conversation_service.find_or_create_conversation([1,3], db_session)
        new_latest_record = db.session.execute('SELECT id FROM conversation ORDER BY id DESC LIMIT 1')
        assert conversation == 1

    # def test_conversation_messages(self, client, setup_database, monkeypatch, db_session):

    # def test_create_and_commit_message():

    # def test_get_latest_conversations():