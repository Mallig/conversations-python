from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(140), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    

class ConversationUserJoin(db.Model):
    conversation_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)