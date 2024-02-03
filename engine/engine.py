
from datetime import timezone
from engine.gestureRecognition import GestureEnums, ThumbLandmark, FingerLandmark, HandLandmark, HandLandmarks, HandRecognition, GestureRecognition
from engine.database import Database, UserStatusEnums, User, Session
from datetime import datetime, timedelta
import random

class GameEngine:
    def __evaluate_gestures(gesture1:int, gesture2:int) -> (int, int):
        """
        Evaluate gestures and return statuses
        """
        if gesture1 == gesture2:
            return UserStatusEnums.TIED, UserStatusEnums.TIED

        if gesture1 not in [GestureEnums.ROCK, GestureEnums.PAPER, GestureEnums.SCISSORS]:
            return UserStatusEnums.LOSER, UserStatusEnums.WINNER
        if gesture2 not in [GestureEnums.ROCK, GestureEnums.PAPER, GestureEnums.SCISSORS]:
            return UserStatusEnums.WINNER, UserStatusEnums.LOSER

        if gesture1 == GestureEnums.ROCK and gesture2 == GestureEnums.SCISSORS:
            return UserStatusEnums.WINNER, UserStatusEnums.LOSER
        elif gesture1 == GestureEnums.PAPER and gesture2 == GestureEnums.ROCK:
            return UserStatusEnums.WINNER, UserStatusEnums.LOSER
        elif gesture1 == GestureEnums.SCISSORS and gesture2 == GestureEnums.PAPER:
            return UserStatusEnums.WINNER, UserStatusEnums.LOSER
        return UserStatusEnums.LOSER, UserStatusEnums.WINNER

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
            bot_gesture = random.randint(1, 3)
            db.update_user(bot, bot_gesture)
            user_status, _ = GameEngine.__evaluate_gestures(user.gesture, bot_gesture)
            db.update_session(user.id, user_status)
            
        return session, user_status, bot

    def __sort_users(db:Database, session:Session, user:User) -> (int, int, User):
        """
        Return user1_status, user2_status, opponent
        """
        if user.id == session.user1_id:
            return session.user1_status, session.user2_status, db.get_user(session.user2_id)
        return session.user2_status, session.user1_status, db.get_user(session.user1_id)

    def process(db:Database, session:Session, user:User) -> (Session, int, User):
        try:
            user_status, opponent_status, opponent = GameEngine.__sort_users(db, session, user)
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