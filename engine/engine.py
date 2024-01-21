
from engine.gestureRecognition import GestureEnums, ThumbLandmark, FingerLandmark, HandLandmark, HandLandmarks, HandRecognition, GestureRecognition
from engine.database import Database, UserStatusEnums, User, Session

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

        return session, user_status, opponent