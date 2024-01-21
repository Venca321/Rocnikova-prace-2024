
from engine.gestureRecognition import GestureEnums, ThumbLandmark, FingerLandmark, HandLandmark, HandLandmarks, HandRecognition, GestureRecognition
from engine.database import Database, UserStatusEnums, User, Session

class GameEngine:
    def process(db:Database, session:Session, user:User, opponent_id:str) -> (Session, int, User):
        try: opponent = db.get_user(opponent_id)
        except Exception: return session, user_status, User("None", "?????", 0)

        if user.id == session.user1_id:
            user_status = session.user1_status
            opponent_status = session.user2_status
        else:
            user_status = session.user2_status
            opponent_status = session.user1_status

        

        return session, user_status, opponent