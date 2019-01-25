from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from api.database import db
class Conversation(db.Model):
    __tablename__ = 'conversation'
    id = db.Column(db.Integer, primary_key=True)

class ConversationUserJoin(db.Model):
    __tablename__ = 'conversation_user_join'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)

    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    conversation = db.relationship('Conversation')

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(140), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    conversation = db.relationship('Conversation')

