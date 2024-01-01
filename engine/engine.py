
from engine.gestureRecognition import GestureEnums, ThumbLandmark, FingerLandmark, HandLandmark, HandLandmarks, HandRecognition, GestureRecognition

class GameEngine:
    def __init__(self):
        self.player_left_ready = False
        self.player_right_ready = False
        self.seconds_to_start = 3

    def checkPlayersReadiness(self, gestureLeft, gestureRight):
        if not self.player_left_ready and gestureLeft == GestureEnums.LIKE:
            self.player_left_ready = True

        if not self.player_right_ready and gestureRight == GestureEnums.LIKE:
            self.player_right_ready = True

    def arePlayersReady(self):
        return bool(self.player_left_ready and self.player_right_ready)