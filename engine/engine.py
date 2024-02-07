
from engine.gestureRecognition import GestureEnums, ThumbLandmark, FingerLandmark, HandLandmark, HandLandmarks, HandRecognition, GestureRecognition
from engine.database import UserStatusEnums


class GameEngine:
    def __evaluate_gestures(gesture1:int, gesture2:int) -> (int, int):
        """
        Evaluate gestures and return statuses
        """
        if gesture1 == gesture2:
            return UserStatusEnums.TIED, UserStatusEnums.TIED

        valid_gestures = [GestureEnums.ROCK, GestureEnums.PAPER, GestureEnums.SCISSORS]
        if gesture1 not in valid_gestures:
            return UserStatusEnums.LOSER, UserStatusEnums.WINNER
        if gesture2 not in valid_gestures:
            return UserStatusEnums.WINNER, UserStatusEnums.LOSER

        if gesture1 == GestureEnums.ROCK and gesture2 == GestureEnums.SCISSORS:
            return UserStatusEnums.WINNER, UserStatusEnums.LOSER
        elif gesture1 == GestureEnums.PAPER and gesture2 == GestureEnums.ROCK:
            return UserStatusEnums.WINNER, UserStatusEnums.LOSER
        elif gesture1 == GestureEnums.SCISSORS and gesture2 == GestureEnums.PAPER:
            return UserStatusEnums.WINNER, UserStatusEnums.LOSER
        return UserStatusEnums.LOSER, UserStatusEnums.WINNER

    def process():
        raise NotImplementedError