from api import db
from api.models import Conversation, Message
from api.models import ConversationUserJoin as JoinTable
from sqlalchemy import func
import numpy as np

# TODO - declare methods such that line 17 & 27 don't need ConversationService prepended

class ConversationService:
    def get_conversation(user_ids):
        query = f"""SELECT conversation_id 
                    FROM (
                        SELECT conversation_id, COUNT(user_id)
                        FROM conversation_user_join
                        WHERE conversation_id IN (
                            SELECT DISTINCT(conversation_id)
                            FROM conversation_user_join
                            WHERE user_id
                            IN {ConversationService.convert_to_string(user_ids)}
                        ) GROUP BY conversation_id 
                        ORDER BY count
                    ) as subq where subq.count={len(user_ids)};"""

        conversation = db.session.execute(query).fetchall()
        conversation_id = None
        user_ids.sort()
        for convo in conversation:
            res = db.session.execute(f"""SELECT user_id FROM conversation_user_join WHERE conversation_id={convo[0]};""").fetchall()
            arr = []
            for r in res:
                arr.append(r[0])

            arr.sort()
            if np.array_equal(arr, user_ids):
                conversation_id = convo[0]
                break
                
        return ConversationService.create_conversation(user_ids) if conversation_id == None else conversation_id

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

    def convert_to_string(arr):
        return str.replace(
            str.replace(
                str(arr), '[', "("
            ), "]", ")"
        )
