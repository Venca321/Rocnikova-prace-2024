
import mediapipe as mp
import cv2

class HandRecognition:
    """
    Code for recognizing hands on image
    """
    def __init__(self, mode=False, maxHands=1, modelComplex=1, detectionCon=0.5, trackCon=0.5): 
        self.video = cv2.VideoCapture(0)
        self.image = None
        self.image1 = None
        self.image2 = None
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(mode, maxHands, modelComplex, detectionCon, trackCon)

    def processImage(self) -> [list, list]:
        """
        Return list of hand maps
        """
        _, image = self.video.read()
        self.image = image
        self.image0 = image[0:image.shape[0], 0:int(image.shape[1]/2)]
        self.image1 = image[0:image.shape[0], int(image.shape[1]/2):image.shape[1]]
        
        imageRGB0 = cv2.cvtColor(self.image0, cv2.COLOR_BGR2RGB)
        results0 = self.hands.process(imageRGB0).multi_hand_landmarks
        imageRGB1 = cv2.cvtColor(self.image1, cv2.COLOR_BGR2RGB)
        results1 = self.hands.process(imageRGB1).multi_hand_landmarks


        if not results0: results0 = []
        if not results1: results1 = []
        return [results0, results1]

    def drawHandLandmarks(self, handMaps, image):
        """
        Draw hand landmarks on image
        """
        mpDraw = mp.solutions.drawing_utils
        mpDraw.draw_landmarks(image, handMaps, self.mpHands.HAND_CONNECTIONS)

    def stop(self):
        self.video.release()
        cv2.destroyAllWindows()
