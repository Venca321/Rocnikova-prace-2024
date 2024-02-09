
from engine.gestureRecognition import GestureEnums, ThumbLandmark, FingerLandmark, HandLandmark, HandLandmarks, HandRecognition, GestureRecognition
from engine.database import UserStatusEnums
import random


class GameEngine:
    def __evaluate_results(self, gesture:int) -> int:
        """
        Evaluate gesture and return status
        """
        valid_gestures = [GestureEnums.ROCK, GestureEnums.PAPER, GestureEnums.SCISSORS]
        if gesture not in valid_gestures: return UserStatusEnums.LOSER
        return random.randint(UserStatusEnums.WINNER, UserStatusEnums.TIED)

    def process(self, gesture:int, user_status:int) -> int:
        if user_status == UserStatusEnums.CONNECTED and gesture == GestureEnums.LIKE: 
            return UserStatusEnums.PLAYING

        elif user_status == UserStatusEnums.SUBMITED:
            return self.__evaluate_results(gesture)

        return user_status