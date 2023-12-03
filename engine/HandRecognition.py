
import mediapipe as mp
import cv2

class HandRecognition:
    """
    Code for recognizing hands on image
    """
    def __init__(self, mode:bool=False, maxHands:float=1, modelComplex:float=1, detectionCon:float=0.5, trackCon:float=0.5): 
        """
        Initialize HandRecognition class
        """
        self.video = cv2.VideoCapture(0)
        self.image = None
        self.imageRight = None
        self.imageLeft = None
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(mode, maxHands, modelComplex, detectionCon, trackCon)

    def processImage(self) -> [list, list]:
        """
        Return list of hand maps
        """
        _, image = self.video.read()
        self.image = image
        self.imageLeft = image[0:image.shape[0], 0:int(image.shape[1]/2)]
        self.imageRight = image[0:image.shape[0], int(image.shape[1]/2):image.shape[1]]
        
        imageRgbLeft = cv2.cvtColor(self.imageLeft, cv2.COLOR_BGR2RGB)
        resultsLeft = self.hands.process(imageRgbLeft).multi_hand_landmarks
        imageRgbRight = cv2.cvtColor(self.imageRight, cv2.COLOR_BGR2RGB)
        resultsRight = self.hands.process(imageRgbRight).multi_hand_landmarks

        if not resultsLeft: resultsLeft= []
        if not resultsRight: resultsRight = []
        return [resultsLeft, resultsRight]

    def drawHandLandmarks(self, handMaps, image):
        """
        Draw hand landmarks on image
        """
        mpDraw = mp.solutions.drawing_utils
        mpDraw.draw_landmarks(image, handMaps, self.mpHands.HAND_CONNECTIONS)

    def stop(self):
        self.video.release()
        cv2.destroyAllWindows()