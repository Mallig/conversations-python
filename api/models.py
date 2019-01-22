from datetime import datetime
from api import db

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, nullable=False)
    receiver_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(140), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
