
from engine.gestureRecognition import Gesture, ThumbLandmark, FingerLandmark, HandLandmark, HandRecognition, GestureRecognition

class GameEngine:
    def __init__(self):
        self.player_left_ready = False
        self.player_right_ready = False
        self.seconds_to_start = 3

    def checkPlayersReadyness(self, gestureLeft, gestureRight):
        if not self.player_left_ready and gestureLeft == Gesture.LIKE:
            self.player_left_ready = True

        if not self.player_right_ready and gestureRight == Gesture.LIKE:
            self.player_right_ready = True

    def arePlayersReady(self):
        return bool(self.player_left_ready and self.player_right_ready)