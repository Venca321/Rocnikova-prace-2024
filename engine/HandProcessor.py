
from enum import Enum

class HandEnums(Enum):
    NONE = 0
    ROCK = 1
    PAPER = 2
    SCISSORS = 3
    LIKE = 4

class HandProcessor:
    # Fingers
    __FINGER_INDEX = (8, 6)
    __FINGER_MIDDLE = (12, 10)
    __FINGER_RING = (16, 14)
    __FINGER_LITTLE = (20, 18)
    __THUMB_DISTANCE_TO_INDEX_FINGER_RATIO = 2.5
    __FINGER_DISTANCE_FIX = 1.1

    def __init__(self, handMap, handRecognitionImage):
        self.handMap = handMap
        self.handData = {}
        self.handRecognitionImage = handRecognitionImage

    def __calculateWristToFingerTipDistance(self, fingers:tuple) -> tuple:
        fingerTipToWristDistance = (abs(self.handData[fingers[0]][0] - self.handData[0][0]) + abs(self.handData[fingers[0]][1] - self.handData[0][1]))
        fingerCenterToWristDistance = (abs(self.handData[fingers[1]][0] - self.handData[0][0]) + abs(self.handData[fingers[1]][1] - self.handData[0][1])) * self.__FINGER_DISTANCE_FIX
        return (fingerTipToWristDistance, fingerCenterToWristDistance)
    
    def __calculateThumbToIndexFingerDistance(self) -> tuple:
        thumbLenght = (abs(self.handData[4][0] - self.handData[3][0]) + abs(self.handData[4][1] - self.handData[3][1])) ** 0.5
        thumbLenght += (abs(self.handData[3][0] - self.handData[2][0]) + abs(self.handData[3][1] - self.handData[2][1])) ** 0.5
        thumbLenght += (abs(self.handData[2][0] - self.handData[1][0]) + abs(self.handData[2][1] - self.handData[1][1])) ** 0.5
        thumb_to_index_finger_distance = (abs(self.handData[6][0] - self.handData[3][0]) + abs(self.handData[6][1] - self.handData[3][1])) ** 0.5
        return thumbLenght, thumb_to_index_finger_distance

    def process(self) -> int:  # sourcery skip: assign-if-exp, reintroduce-else
        self.handData = {}
        for point_index, hand_point in enumerate(self.handMap.landmark):
            image_height, image_width, _ = self.handRecognitionImage.shape
            point_x, point_y = int(hand_point.x * image_width), int(hand_point.y * image_height)
            self.handData[point_index] = [point_x, point_y, hand_point.z]

        if self.isHandRock(): return HandEnums.ROCK.value
        if self.isHandPaper(): return HandEnums.PAPER.value
        if self.isHandScissors(): return HandEnums.SCISSORS.value
        if self.isHandLike(): return HandEnums.LIKE.value
        return HandEnums.NONE.value

    def isHandRock(self) -> bool:
        fingerTipToWristDistance, fingerCenterToWristDistance = self.__calculateWristToFingerTipDistance(self.__FINGER_INDEX)
        if fingerTipToWristDistance > fingerCenterToWristDistance: return False

        fingerTipToWristDistance, fingerCenterToWristDistance = self.__calculateWristToFingerTipDistance(self.__FINGER_MIDDLE)
        if fingerTipToWristDistance > fingerCenterToWristDistance: return False

        fingerTipToWristDistance, fingerCenterToWristDistance = self.__calculateWristToFingerTipDistance(self.__FINGER_RING)
        if fingerTipToWristDistance > fingerCenterToWristDistance: return False

        fingerTipToWristDistance, fingerCenterToWristDistance = self.__calculateWristToFingerTipDistance(self.__FINGER_LITTLE)
        if fingerTipToWristDistance > fingerCenterToWristDistance: return False

        finger_lenght, thumb_index_finger_distance = self.__calculateThumbToIndexFingerDistance()
        return thumb_index_finger_distance <= finger_lenght / self.__THUMB_DISTANCE_TO_INDEX_FINGER_RATIO

    def isHandPaper(self) -> bool:
        fingerTipToWristDistance, fingerCenterToWristDistance = self.__calculateWristToFingerTipDistance(self.__FINGER_INDEX)
        if fingerTipToWristDistance < fingerCenterToWristDistance: return False

        fingerTipToWristDistance, fingerCenterToWristDistance = self.__calculateWristToFingerTipDistance(self.__FINGER_MIDDLE)
        if fingerTipToWristDistance < fingerCenterToWristDistance: return False

        fingerTipToWristDistance, fingerCenterToWristDistance = self.__calculateWristToFingerTipDistance(self.__FINGER_RING)
        if fingerTipToWristDistance < fingerCenterToWristDistance: return False

        fingerTipToWristDistance, fingerCenterToWristDistance = self.__calculateWristToFingerTipDistance(self.__FINGER_LITTLE)
        return fingerTipToWristDistance >= fingerCenterToWristDistance

    def isHandScissors(self) -> bool:
        fingerTipToWristDistance, fingerCenterToWristDistance = self.__calculateWristToFingerTipDistance(self.__FINGER_INDEX)
        if fingerTipToWristDistance < fingerCenterToWristDistance: return False

        fingerTipToWristDistance, fingerCenterToWristDistance = self.__calculateWristToFingerTipDistance(self.__FINGER_MIDDLE)
        if fingerTipToWristDistance < fingerCenterToWristDistance: return False

        fingerTipToWristDistance, fingerCenterToWristDistance = self.__calculateWristToFingerTipDistance(self.__FINGER_RING)
        if fingerTipToWristDistance > fingerCenterToWristDistance: return False

        fingerTipToWristDistance, fingerCenterToWristDistance = self.__calculateWristToFingerTipDistance(self.__FINGER_LITTLE)
        return fingerTipToWristDistance <= fingerCenterToWristDistance
    
    def isHandLike(self) -> bool:
        fingerTipToWristDistance, fingerCenterToWristDistance = self.__calculateWristToFingerTipDistance(self.__FINGER_INDEX)
        if fingerTipToWristDistance > fingerCenterToWristDistance: return False

        fingerTipToWristDistance, fingerCenterToWristDistance = self.__calculateWristToFingerTipDistance(self.__FINGER_MIDDLE)
        if fingerTipToWristDistance > fingerCenterToWristDistance: return False

        fingerTipToWristDistance, fingerCenterToWristDistance = self.__calculateWristToFingerTipDistance(self.__FINGER_RING)
        if fingerTipToWristDistance > fingerCenterToWristDistance: return False

        fingerTipToWristDistance, fingerCenterToWristDistance = self.__calculateWristToFingerTipDistance(self.__FINGER_LITTLE)
        if fingerTipToWristDistance > fingerCenterToWristDistance: return False

        finger_lenght, thumb_index_finger_distance = self.__calculateThumbToIndexFingerDistance()
        return thumb_index_finger_distance >= finger_lenght / self.__THUMB_DISTANCE_TO_INDEX_FINGER_RATIO