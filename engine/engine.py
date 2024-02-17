
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

    def __evaluate_results(self, gesture:int, history:list) -> tuple[int, int]:
        """
        Evaluate gesture and return status (win stay, lose change strategy)
        """
        valid_gestures = [GestureEnums.ROCK, GestureEnums.PAPER, GestureEnums.SCISSORS]
        # sourcery skip: merge-nested-ifs
        if history:
            if history[-1]["user_status"] == UserStatusEnums.LOSER and random.randint(0, 10) <= 8:
                bot_gesture = history[-1]["bot_gesture"]
                return self.__evaluate_gestures(gesture, bot_gesture), bot_gesture
            valid_gestures.remove(history[-1]["bot_gesture"])

        bot_gesture = random.choice(valid_gestures)
        return self.__evaluate_gestures(gesture, bot_gesture), bot_gesture

    def process(self, gesture:int, user_status:int, history:list) -> tuple[int, int]:
        if user_status == UserStatusEnums.CONNECTED and gesture == GestureEnums.LIKE: 
            return UserStatusEnums.PLAYING, 0

        elif user_status == UserStatusEnums.SUBMITED:
            return self.__evaluate_results(gesture, history)

        return user_status, 0
