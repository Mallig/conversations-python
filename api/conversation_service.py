from api import db
from api.models import Conversation, Message
from api.models import ConversationUserJoin as JoinTable
from sqlalchemy import func

# TODO - declare methods such that line 17 & 27 don't need ConversationService prepended

class ConversationService:
    def find_or_create_conversation(user_ids):
        conversation_id = ConversationService.get_conversation(user_ids)
        return ConversationService.create_conversation(user_ids) if not conversation_id else conversation_id

    def get_conversation(user_ids):
        first_query = f"""SELECT DISTINCT(conversation_id)
                            FROM conversation_user_join
                            WHERE user_id
                            IN {ConversationService.convert_to_string(user_ids)}"""

        second_query = f"""SELECT conversation_id,
                            COUNT(user_id) AS total_users,
                            COUNT(user_id)
                        FILTER (
                            WHERE user_id
                            IN {ConversationService.convert_to_string(user_ids)}
                        ) AS provided_users
                        FROM conversation_user_join
                        WHERE conversation_id IN (
                            {first_query}
                        ) GROUP BY conversation_id"""

        query = f"""SELECT conversation_id
                    FROM (
                        {second_query}
                    ) AS subq
                    WHERE subq.provided_users=subq.total_users
                    AND subq.total_users={len(user_ids)};"""

        conversation_id = db.session.execute(query).fetchall()
        return None if not conversation_id else conversation_id[0][0]

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

    def convert_to_string(arr):
        return str.replace(
            str.replace(
                str(arr), '[', "("
            ), "]", ")"
        )
