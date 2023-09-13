
import mediapipe as mp
import cv2

class HandRecognition:
    def __init__(self, mode=False, maxHands=1, modelComplex=1, detectionCon=0.5, trackCon=0.5): 
        self.video = cv2.VideoCapture(0)
        self.image = None
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(mode, maxHands, modelComplex, detectionCon, trackCon)

    def processImage(self):
        _, image = self.video.read()
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imageRGB)
        self.image = image

        if results.multi_hand_landmarks: return results.multi_hand_landmarks
        else: return []

    def drawHandLandmarks(self, handLms):
        mpDraw = mp.solutions.drawing_utils
        mpDraw.draw_landmarks(self.image, handLms, self.mpHands.HAND_CONNECTIONS)

    def stop(self):
        self.video.release()
        cv2.destroyAllWindows()
