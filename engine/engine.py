
from engine.gestureRecognition import GestureEnums, ThumbLandmark, FingerLandmark, HandLandmark, HandRecognition, GestureRecognition
from engine.database import UserStatusEnums
import random

class GameEngine:
    def __evaluate_gestures(self, gesture0:int, gesture1:int) -> int:
        """
        Evaluate gestures and return user status
        """
        if gesture0 == gesture1:
            return UserStatusEnums.TIED

        valid_gestures = [GestureEnums.ROCK, GestureEnums.PAPER, GestureEnums.SCISSORS]
        if gesture0 not in valid_gestures:
            return UserStatusEnums.LOSER

        if gesture0 == GestureEnums.ROCK and gesture1 == GestureEnums.SCISSORS:
            return UserStatusEnums.WINNER
        elif gesture0 == GestureEnums.PAPER and gesture1 == GestureEnums.ROCK:
            return UserStatusEnums.WINNER
        elif gesture0 == GestureEnums.SCISSORS and gesture1 == GestureEnums.PAPER:
            return UserStatusEnums.WINNER
        
        return UserStatusEnums.LOSER

    def __evaluate_results(self, gesture:int, history:list) -> tuple[int, int]:
        """
        Evaluate gesture and return status (win stay, lose change strategy)
        """
        # sourcery skip: merge-nested-ifs
        if history:
            if (
                history[-1]["user_status"] == UserStatusEnums.LOSER 
                and random.randint(0, 10) <= 8
            ):
                bot_gesture = history[-1]["bot_gesture"]
                return self.__evaluate_gestures(gesture, bot_gesture), bot_gesture

        valid_gestures = [GestureEnums.ROCK, GestureEnums.PAPER, GestureEnums.SCISSORS]
        bot_gesture = random.choice(valid_gestures)
        return self.__evaluate_gestures(gesture, bot_gesture), bot_gesture

    def process(self, gesture:int, user_status:int, history:list) -> tuple[int, int]:
        if user_status == UserStatusEnums.CONNECTED and gesture == GestureEnums.LIKE: 
            return UserStatusEnums.PLAYING, 0

        elif user_status == UserStatusEnums.SUBMITED:
            return self.__evaluate_results(gesture, history)

        return user_status, 0
