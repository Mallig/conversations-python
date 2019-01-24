from api import db
from api.models import Conversation, Message
from api.models import ConversationUserJoin as JoinTable
from sqlalchemy import func

# TODO - declare methods such that line 17 & 27 don't need ConversationService prepended

class ConversationService:
    def get_conversation(user_ids):
        conversation = db.session.query(JoinTable.conversation_id)\
            .filter(JoinTable.user_id.in_(user_ids))\
            .group_by(JoinTable.conversation_id)\
            .having(func.count()==len(user_ids))\
            .all()
        
        if not conversation:
            return ConversationService.create_conversation(user_ids)
        elif len(conversation) > 1:
            for convo in conversation:
                print(convo)
                num_of_participants = ConversationService.num_of_participants(convo[0])
                if num_of_participants == len(user_ids):
                    found_convo = True
                    return convo[0]
                else: 
                    found_convo = False

            if not found_convo:
                return ConversationService.create_conversation(user_ids)
        else:
            return conversation[0]

    def create_conversation(user_ids):
        conversation = Conversation()
        db.session.add(conversation)
        db.session.commit()

        ConversationService.create_join_rows(user_ids, conversation.id)
        return conversation.id

    def create_join_rows(user_ids, convo_id):
        for user_id in user_ids:
            db.session.add(JoinTable(conversation_id = convo_id,
                                     user_id = user_id))
        db.session.commit()

    def num_of_participants(convo_id):
        count = db.session.query(JoinTable.conversation_id)\
            .filter(JoinTable.conversation_id==convo_id)\
            .all()
        return len(count)
