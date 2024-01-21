
from engine.gestureRecognition import GestureEnums, ThumbLandmark, FingerLandmark, HandLandmark, HandLandmarks, HandRecognition, GestureRecognition
from engine.database import Database, UserStatusEnums, User, Session

class GameEngine:
    def process(db:Database, session:Session, user:User) -> (Session, int, User):
        if user.id == session.user1_id:
            user_status = session.user1_status
            if user_status == UserStatusEnums.WAITING: return session, user_status, User("None", "?????", 0)
            opponent_status = session.user2_status
            #opponent = db.get_user(session.user2_id)
        else:
            user_status = session.user2_status
            if user_status == UserStatusEnums.WAITING: return session, user_status, User("None", "?????", 0)
            opponent_status = session.user1_status
            #opponent = db.get_user(session.user1_id)

        return session, user_status, User("None", "?????", 0)