
from engine.gestureRecognition import GestureEnums, ThumbLandmark, FingerLandmark, HandLandmark, HandLandmarks, HandRecognition, GestureRecognition
from engine.database import Database, UserStatusEnums, User, Session

class GameEngine:
    def process(session:Session, user:User, opponent:User) -> (Session, int, User):
        if user.id == session.user1_id:
            user_status = session.user1_status
            opponent_status = session.user2_status
        else:
            user_status = session.user2_status
            opponent_status = session.user1_status

        return session, user_status, opponent