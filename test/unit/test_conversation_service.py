import pytest
from api.conversation_service import ConversationService
from api import db
from api.models import Conversation
from flask import current_app

class TestConversationService:
    def test_find_existing_conversation(self, client, setup_database, monkeypatch, db_session):
        print('**********')
        print(current_app.config)
        print('**********')
        mock_statement = 'select * from messages;'
        monkeypatch.setattr(db.session.execute(mock_statement), 'fetchall', [(1,)])
        conversation = ConversationService.find_or_create_conversation([1,2], db_session)
        assert conversation == 1
    
    def test_find_nonexistent_conversation(self, client, setup_database, monkeypatch, db_session):
        mock_statement = 'select * from messages;'
        print(db_session.query(Conversation).all())
        conversation = ConversationService.find_or_create_conversation([1,3], db_session)
        print(db_session.query(Conversation).all())
        new_latest_record = db.session.execute('SELECT id FROM conversation ORDER BY id DESC LIMIT 1')
        assert conversation == 1
