
from datetime import timezone
from engine.gestureRecognition import GestureEnums, ThumbLandmark, FingerLandmark, HandLandmark, HandLandmarks, HandRecognition, GestureRecognition
from engine.database import Database, UserStatusEnums, User, Session
from datetime import datetime, timedelta

class GameEngine:
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

        if user_status == UserStatusEnums.CONNECTED and user.gesture == GestureEnums.LIKE:
            user_status = UserStatusEnums.READY
            db.update_session(user.id, user_status)

        if user_status == UserStatusEnums.READY and opponent_status == UserStatusEnums.READY:
            user_status = UserStatusEnums.PLAYING
            opponent_status = UserStatusEnums.PLAYING
            db.update_session(user.id, user_status)
            db.update_session(opponent.id, opponent_status)

        if user_status == UserStatusEnums.PLAYING and opponent_status == UserStatusEnums.PLAYING:
            three_seconds_ago = (datetime.now(timezone.utc) - timedelta(seconds=3)).strftime('%Y-%m-%d %H:%M:%S')
            if three_seconds_ago > session.updated_at:
                user_status = UserStatusEnums.SUBMITED
                opponent_status = UserStatusEnums.SUBMITED
                db.update_session(user.id, user_status)
                db.update_session(opponent.id, opponent_status)

        if user_status == UserStatusEnums.SUBMITED and opponent_status == UserStatusEnums.SUBMITED:
            if user.gesture == GestureEnums.ROCK and opponent.gesture == GestureEnums.PAPER:
                user_status = UserStatusEnums.LOSER
                opponent_status = UserStatusEnums.WINNER
            elif user.gesture == GestureEnums.ROCK and opponent.gesture == GestureEnums.SCISSORS:
                user_status = UserStatusEnums.WINNER
                opponent_status = UserStatusEnums.LOSER
            elif user.gesture == GestureEnums.ROCK and opponent.gesture == GestureEnums.ROCK:
                user_status = UserStatusEnums.TIED
                opponent_status = UserStatusEnums.TIED
            elif user.gesture == GestureEnums.PAPER and opponent.gesture == GestureEnums.PAPER:
                user_status = UserStatusEnums.TIED
                opponent_status = UserStatusEnums.TIED
            elif user.gesture == GestureEnums.PAPER and opponent.gesture == GestureEnums.SCISSORS:
                user_status = UserStatusEnums.LOSER
                opponent_status = UserStatusEnums.WINNER
            elif user.gesture == GestureEnums.PAPER and opponent.gesture == GestureEnums.ROCK:
                user_status = UserStatusEnums.WINNER
                opponent_status = UserStatusEnums.LOSER
            elif user.gesture == GestureEnums.SCISSORS and opponent.gesture == GestureEnums.PAPER:
                user_status = UserStatusEnums.WINNER
                opponent_status = UserStatusEnums.LOSER
            elif user.gesture == GestureEnums.SCISSORS and opponent.gesture == GestureEnums.SCISSORS:
                user_status = UserStatusEnums.TIED
                opponent_status = UserStatusEnums.TIED
            elif user.gesture == GestureEnums.SCISSORS and opponent.gesture == GestureEnums.ROCK:
                user_status = UserStatusEnums.LOSER
                opponent_status = UserStatusEnums.WINNER

            db.update_session(user.id, user_status)
            db.update_session(opponent.id, opponent_status)

        if user_status in [UserStatusEnums.WINNER, UserStatusEnums.LOSER, UserStatusEnums.TIED] and opponent_status in [UserStatusEnums.WINNER, UserStatusEnums.LOSER, UserStatusEnums.TIED]:
            ten_seconds_ago = (datetime.now(timezone.utc) - timedelta(seconds=10)).strftime('%Y-%m-%d %H:%M:%S')
            if ten_seconds_ago > session.updated_at:
                user_status = UserStatusEnums.CONNECTED
                opponent_status = UserStatusEnums.CONNECTED
                db.update_session(user.id, user_status)
                db.update_session(opponent.id, opponent_status)

        return session, user_status, opponent