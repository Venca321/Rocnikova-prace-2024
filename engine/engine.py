
from engine.gestureRecognition import GestureEnums, ThumbLandmark, FingerLandmark, HandLandmark, HandLandmarks, HandRecognition, GestureRecognition
from engine.database import Database, UserStatusEnums, User, Session

class GameEngine:
    def process(session:Session, user:User, opponent:User) -> (Session, int, User):
        pass