
from engine.gestureRecognition import GestureEnums, ThumbLandmark, FingerLandmark, HandLandmark, HandLandmarks, HandRecognition, GestureRecognition
from engine.database import UserStatusEnums
import random


class GameEngine:
    def __evaluate_gestures(self, user_gesture:int, bot_gesture:int) -> int:
        """
        Evaluate gestures and return user status
        """
        if user_gesture == bot_gesture:
            return UserStatusEnums.TIED, UserStatusEnums.TIED

        valid_gestures = [GestureEnums.ROCK, GestureEnums.PAPER, GestureEnums.SCISSORS]
        if user_gesture not in valid_gestures:
            return UserStatusEnums.LOSER

        if user_gesture == GestureEnums.ROCK and bot_gesture == GestureEnums.SCISSORS:
            return UserStatusEnums.WINNER
        elif user_gesture == GestureEnums.PAPER and bot_gesture == GestureEnums.ROCK:
            return UserStatusEnums.WINNER
        elif user_gesture == GestureEnums.SCISSORS and bot_gesture == GestureEnums.PAPER:
            return UserStatusEnums.WINNER
        
        return UserStatusEnums.LOSER

    def __evaluate_results(self, gesture:int) -> int:
        """
        Evaluate gesture and return status
        """
        bot_gesture = random.randint(1, 3)
        return self.__evaluate_gestures(gesture, bot_gesture)

    def process(self, gesture:int, user_status:int) -> int:
        if user_status == UserStatusEnums.CONNECTED and gesture == GestureEnums.LIKE: 
            user_status = UserStatusEnums.PLAYING

        elif user_status == UserStatusEnums.SUBMITED:
            user_status = self.__evaluate_results(gesture)

        return user_status