
from datetime import timezone
from engine.gestureRecognition import GestureEnums, ThumbLandmark, FingerLandmark, HandLandmark, HandLandmarks, HandRecognition, GestureRecognition
from engine.database import Database, UserStatusEnums, User, Session
from datetime import datetime, timedelta

class GameEngine:
    def __evaluate_gestures(gesture1:int, gesture2:int) -> (int, int):
        """
        Evaluate gestures and return statuses
        """
        if gesture1 not in [GestureEnums.ROCK, GestureEnums.PAPER, GestureEnums.SCISSORS]:
            user1_status = UserStatusEnums.LOSER
            user2_status = UserStatusEnums.WINNER
        if gesture2 not in [GestureEnums.ROCK, GestureEnums.PAPER, GestureEnums.SCISSORS]:
            if not user1_status == UserStatusEnums.LOSER:
                user1_status = UserStatusEnums.WINNER
            user2_status = UserStatusEnums.LOSER

        if gesture1 == GestureEnums.ROCK and gesture2 == GestureEnums.PAPER:
            user1_status = UserStatusEnums.LOSER
            user2_status = UserStatusEnums.WINNER
        elif gesture1 == GestureEnums.ROCK and gesture2 == GestureEnums.SCISSORS:
            user1_status = UserStatusEnums.WINNER
            user2_status = UserStatusEnums.LOSER
        elif gesture1 == GestureEnums.ROCK and gesture2 == GestureEnums.ROCK:
            user1_status = UserStatusEnums.TIED
            user2_status = UserStatusEnums.TIED
        elif gesture1 == GestureEnums.PAPER and gesture2 == GestureEnums.PAPER:
            user1_status = UserStatusEnums.TIED
            user2_status = UserStatusEnums.TIED
        elif gesture1 == GestureEnums.PAPER and gesture2 == GestureEnums.SCISSORS:
            user1_status = UserStatusEnums.LOSER
            user2_status = UserStatusEnums.WINNER
        elif gesture1 == GestureEnums.PAPER and gesture2 == GestureEnums.ROCK:
            user1_status = UserStatusEnums.WINNER
            user2_status = UserStatusEnums.LOSER
        elif gesture1 == GestureEnums.SCISSORS and gesture2 == GestureEnums.PAPER:
            user1_status = UserStatusEnums.WINNER
            user2_status = UserStatusEnums.LOSER
        elif gesture1 == GestureEnums.SCISSORS and gesture2 == GestureEnums.SCISSORS:
            user1_status = UserStatusEnums.TIED
            user2_status = UserStatusEnums.TIED
        elif gesture1 == GestureEnums.SCISSORS and gesture2 == GestureEnums.ROCK:
            user1_status = UserStatusEnums.LOSER
            user2_status = UserStatusEnums.WINNER
        return user1_status, user2_status


    def __process_bot(db:Database, session:Session, user:User) -> (Session, int, User):
        user_status = session.user1_status
        bot = db.get_user(session.user2_id)

        if user_status == UserStatusEnums.CONNECTED and user.gesture == GestureEnums.LIKE:
            user_status = UserStatusEnums.READY
            db.update_session(user.id, user_status)

        if user_status == UserStatusEnums.READY:
            user_status = UserStatusEnums.PLAYING
            db.update_session(user.id, user_status)

        if user_status == UserStatusEnums.SUBMITED:
            user_status, _ = GameEngine.__evaluate_gestures(user.gesture, bot.gesture)
            db.update_session(user.id, user_status)
            
        return session, user_status, bot

    def process(db:Database, session:Session, user:User) -> (Session, int, User):
        if user.id == session.user1_id:
            try:
                user_status = session.user1_status
                opponent_status = session.user2_status
                opponent = db.get_user(session.user2_id)
            except Exception:
                return session, user_status, User("None", "?????", 0)
        else:
            try:
                user_status = session.user2_status
                opponent_status = session.user1_status
                opponent = db.get_user(session.user1_id)
            except Exception:
                return session, user_status, User("None", "?????", 0)

        if opponent.id.startswith("bot_"): return GameEngine.__process_bot(db, session, user)

        if user_status == UserStatusEnums.CONNECTED and user.gesture == GestureEnums.LIKE:
            user_status = UserStatusEnums.READY
            db.update_session(user.id, user_status)

        if user_status == UserStatusEnums.READY and opponent_status == UserStatusEnums.READY:
            user_status = UserStatusEnums.PLAYING
            opponent_status = UserStatusEnums.PLAYING
            db.update_session(user.id, user_status)
            db.update_session(opponent.id, opponent_status)

        if user_status == UserStatusEnums.SUBMITED and opponent_status == UserStatusEnums.SUBMITED:
            user_status, opponent_status = GameEngine.__evaluate_gestures(user.gesture, opponent.gesture)
            db.update_session(user.id, user_status)
            db.update_session(opponent.id, opponent_status)
            
        return session, user_status, opponent