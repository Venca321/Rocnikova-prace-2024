
import mediapipe as mp
import cv2


class GestureEnums:
    NONE = 0
    ROCK = 1
    PAPER = 2
    SCISSORS = 3
    LIKE = 4

class ThumbLandmark:
    def __init__(self, finger_cmc, finger_mcp, finger_ip, finger_tip):
        self.finger_cmc = finger_cmc
        self.finger_mcp = finger_mcp
        self.finger_ip = finger_ip
        self.finger_tip = finger_tip

class FingerLandmark:
    def __init__(self, finger_mcp, finger_pip, finger_dip, finger_tip):
        self.finger_mcp = finger_mcp
        self.finger_pip = finger_pip
        self.finger_dip = finger_dip
        self.finger_tip = finger_tip

class HandLandmark:
    def __init__(self, raw_landmark:list):
        self.wrist = raw_landmark[0]
        self.thumb = ThumbLandmark(raw_landmark[1], raw_landmark[2], raw_landmark[3], raw_landmark[4])
        self.index_finger = FingerLandmark(raw_landmark[5], raw_landmark[6], raw_landmark[7], raw_landmark[8])
        self.middle_finger = FingerLandmark(raw_landmark[9], raw_landmark[10], raw_landmark[11], raw_landmark[12])
        self.ring_finger = FingerLandmark(raw_landmark[13], raw_landmark[14], raw_landmark[15], raw_landmark[16])
        self.pinky = FingerLandmark(raw_landmark[17], raw_landmark[18], raw_landmark[19], raw_landmark[20])

class HandLandmarks:
    def __init__(self, right_landmark:HandLandmark, left_landmark:HandLandmark):
        self.left_landmark = left_landmark
        self.right_landmark = right_landmark

class HandRecognition:
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.image = self.video.read()
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(False, 1, 1, 0.5, 0.5) #mode, maxHands, modelComplex, detectionCon, trackCon

    def __getLandmark(self, image, draw_landmarks:bool=False) -> HandLandmark | None:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb).multi_hand_landmarks

        if not results: return HandLandmark([[None, None, None] for _ in range(21)])

        if draw_landmarks:
            mpDraw = mp.solutions.drawing_utils
            mpDraw.draw_landmarks(image, results[0], self.mpHands.HAND_CONNECTIONS)

        # remap landmarks to list of points and calculate their position in image
        hand_landmarks = []
        for hand_point in results[0].landmark:
            image_height, image_width, _ = image.shape
            point_x, point_y = int(hand_point.x * image_width), int(hand_point.y * image_height)
            hand_landmarks.append([point_x, point_y, hand_point.z])

        return HandLandmark(hand_landmarks)

    def getLandmarks(self, draw_landmarks:bool=False) -> HandLandmarks:
        _, image = self.video.read()
        self.image = image

        # split image to left and right side
        self.imageLeft = image[0:image.shape[0], 0:int(image.shape[1]/2)]
        self.imageRight = image[0:image.shape[0], int(image.shape[1]/2):image.shape[1]]

        resultsLeft = self.__getLandmark(self.imageLeft, draw_landmarks)
        resultsRight = self.__getLandmark(self.imageRight, draw_landmarks)

        return HandLandmarks(resultsRight, resultsLeft)

    def stop(self):
        self.video.release()
        cv2.destroyAllWindows()

class GestureRecognition:
    def __calculatePointsDistance(self, point1:list, point2:list) -> float:
        return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5
    
    def __calculateThumbLength(self, thumb:ThumbLandmark) -> float:
        return self.__calculatePointsDistance(thumb.finger_cmc, thumb.finger_mcp) + self.__calculatePointsDistance(thumb.finger_mcp, thumb.finger_ip) + self.__calculatePointsDistance(thumb.finger_ip, thumb.finger_tip)

    def __isTipToWristLongerThanPipToWrist(self, finger:FingerLandmark, wrist) -> bool:
        return self.__calculatePointsDistance(finger.finger_tip, wrist) > self.__calculatePointsDistance(finger.finger_pip, wrist)

    def __isThumbToIndexFingerDistanceShorterThanThumbLenght(self, thumb:ThumbLandmark, index_finger:FingerLandmark) -> bool:
        __THUMB_DISTANCE_TO_INDEX_FINGER_RATIO = 2
        return self.__calculatePointsDistance(thumb.finger_ip, index_finger.finger_pip) < self.__calculateThumbLength(thumb) / __THUMB_DISTANCE_TO_INDEX_FINGER_RATIO

    def detectGesture(self, hand_landmark:HandLandmark):
        try:
            if self.isHandRock(hand_landmark): return GestureEnums.ROCK
            if self.isHandPaper(hand_landmark): return GestureEnums.PAPER
            if self.isHandScissors(hand_landmark): return GestureEnums.SCISSORS
            if self.isHandLike(hand_landmark): return GestureEnums.LIKE
        except Exception: None
        return GestureEnums.NONE

    def isHandRock(self, hand_landmark:HandLandmark) -> bool:
        if self.__isTipToWristLongerThanPipToWrist(hand_landmark.index_finger, hand_landmark.wrist): return False
        if self.__isTipToWristLongerThanPipToWrist(hand_landmark.middle_finger, hand_landmark.wrist): return False
        if self.__isTipToWristLongerThanPipToWrist(hand_landmark.ring_finger, hand_landmark.wrist): return False
        if self.__isTipToWristLongerThanPipToWrist(hand_landmark.pinky, hand_landmark.wrist): return False
        return self.__isThumbToIndexFingerDistanceShorterThanThumbLenght(hand_landmark.thumb, hand_landmark.index_finger)

    def isHandPaper(self, hand_landmark:HandLandmark) -> bool:
        if not self.__isTipToWristLongerThanPipToWrist(hand_landmark.index_finger, hand_landmark.wrist): return False
        if not self.__isTipToWristLongerThanPipToWrist(hand_landmark.middle_finger, hand_landmark.wrist): return False
        if not self.__isTipToWristLongerThanPipToWrist(hand_landmark.ring_finger, hand_landmark.wrist): return False
        return self.__isTipToWristLongerThanPipToWrist(hand_landmark.pinky, hand_landmark.wrist)

    def isHandScissors(self, hand_landmark:HandLandmark) -> bool:
        if not self.__isTipToWristLongerThanPipToWrist(hand_landmark.index_finger, hand_landmark.wrist): return False
        if not self.__isTipToWristLongerThanPipToWrist(hand_landmark.middle_finger, hand_landmark.wrist): return False
        if self.__isTipToWristLongerThanPipToWrist(hand_landmark.ring_finger, hand_landmark.wrist): return False
        return not self.__isTipToWristLongerThanPipToWrist(hand_landmark.pinky, hand_landmark.wrist)

    def isHandLike(self, hand_landmark:HandLandmark) -> bool:
        if self.__isTipToWristLongerThanPipToWrist(hand_landmark.index_finger, hand_landmark.wrist): return False
        if  self.__isTipToWristLongerThanPipToWrist(hand_landmark.middle_finger, hand_landmark.wrist): return False
        if  self.__isTipToWristLongerThanPipToWrist(hand_landmark.ring_finger, hand_landmark.wrist): return False
        if  self.__isTipToWristLongerThanPipToWrist(hand_landmark.pinky, hand_landmark.wrist): return False
        return not self.__isThumbToIndexFingerDistanceShorterThanThumbLenght(hand_landmark.thumb, hand_landmark.index_finger)

if __name__ == "__main__":
    hand_recognizer = HandRecognition()
    gesture_recognizer = GestureRecognition()

    while True:
        landmarks = hand_recognizer.getLandmarks(True)
        cv2.imshow("Output", hand_recognizer.image)
        cv2.waitKey(1)
        
        print("Left:", gesture_recognizer.detectGesture(landmarks.left_landmark))
        print("Right:", gesture_recognizer.detectGesture(landmarks.right_landmark))