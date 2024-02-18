
import mediapipe as mp
import numpy as np
from dataclasses import dataclass


class GestureEnums:
    NONE = 0
    ROCK = 1
    PAPER = 2
    SCISSORS = 3
    LIKE = 4

    def decode(gesture:int) -> str:
        """
        Decode gesture enum to string
        """
        if gesture == GestureEnums.ROCK: return "Kámen"
        elif gesture == GestureEnums.PAPER: return "Papír"
        elif gesture == GestureEnums.SCISSORS: return "Nůžky"
        elif gesture == GestureEnums.LIKE: return "Palec nahoru"
        else: return "Neznámé"

@dataclass
class ThumbLandmark:
    finger_cmc: list[float | None, float | None, float | None]
    finger_mcp: list[float | None, float | None, float | None]
    finger_ip: list[float | None, float | None, float | None]
    finger_tip: list[float | None, float | None, float | None]

@dataclass
class FingerLandmark:
    finger_mcp: list[float | None, float | None, float | None]
    finger_pip: list[float | None, float | None, float | None]
    finger_dip: list[float | None, float | None, float | None]
    finger_tip: list[float | None, float | None, float | None]

class HandLandmark:
    def __init__(self, raw_landmark:list):
        self.wrist = raw_landmark[0]
        self.thumb = ThumbLandmark(
            raw_landmark[1], raw_landmark[2], 
            raw_landmark[3], raw_landmark[4]
        )
        self.index_finger = FingerLandmark(
            raw_landmark[5], raw_landmark[6], 
            raw_landmark[7], raw_landmark[8]
        )
        self.middle_finger = FingerLandmark(
            raw_landmark[9], raw_landmark[10], 
            raw_landmark[11], raw_landmark[12]
        )
        self.ring_finger = FingerLandmark(
            raw_landmark[13], raw_landmark[14], 
            raw_landmark[15], raw_landmark[16]
        )
        self.pinky = FingerLandmark(
            raw_landmark[17], raw_landmark[18], 
            raw_landmark[19], raw_landmark[20]
        )

class HandRecognition:
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(False, 1, 1, 0.5, 0.5) #mode, maxHands, modelComplex, detectionCon, trackCon

    def getLandmark(self, image) -> HandLandmark | None:
        black_image = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
        results = self.hands.process(image).multi_hand_landmarks

        if not results: return HandLandmark([[None, None, None] for _ in range(21)]), black_image

        mpDraw = mp.solutions.drawing_utils
        mpDraw.draw_landmarks(black_image, results[0], self.mpHands.HAND_CONNECTIONS)

        # remap landmarks to list of points and calculate their position in image
        hand_landmarks = []
        for hand_point in results[0].landmark:
            image_height, image_width, _ = image.shape
            point_x, point_y = int(hand_point.x * image_width), int(hand_point.y * image_height)
            hand_landmarks.append([point_x, point_y, hand_point.z])

        return HandLandmark(hand_landmarks), black_image

class GestureRecognition:
    def __calculate_points_distance(self, point1:list, point2:list) -> float:
        return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5
    
    def __is_tip_to_wrist_longer_than_pip_to_wrist(
            self, finger:FingerLandmark, wrist) -> bool:
        return (
            self.__calculate_points_distance(finger.finger_tip, wrist)
            > self.__calculate_points_distance(finger.finger_pip, wrist)
        )
 
    def __calculate_thumb_length(self, thumb:ThumbLandmark) -> float:
        return (
            self.__calculate_points_distance(thumb.finger_cmc, thumb.finger_mcp)
            + self.__calculate_points_distance(thumb.finger_mcp, thumb.finger_ip)
            + self.__calculate_points_distance(thumb.finger_ip, thumb.finger_tip)
        )

    def __is_thumb_to_index_finger_distance_shorter_than_thumb_lenght(
            self, thumb:ThumbLandmark, index_finger:FingerLandmark
        ) -> bool:
        __THUMB_DISTANCE_TO_INDEX_FINGER_RATIO = 2
        return (
            self.__calculate_points_distance(thumb.finger_ip, index_finger.finger_pip)
            < (self.__calculate_thumb_length(thumb) 
               / __THUMB_DISTANCE_TO_INDEX_FINGER_RATIO)
        )
    
    def calculate_middle_point(self, point1, point2) -> tuple[int, int]:
        return (int((point1[0] + point2[0]) / 2), int((point1[1] + point2[1]) / 2))
    
    def is_clicked(self, hand_landmark:HandLandmark) -> bool:
        finger_tips_distance = self.__calculate_points_distance(
            hand_landmark.index_finger.finger_tip,
            hand_landmark.thumb.finger_tip
        )
        index_finger_tip_to_dip_distance = self.__calculate_points_distance(
            hand_landmark.index_finger.finger_tip,
            hand_landmark.index_finger.finger_dip
        )
        return finger_tips_distance < index_finger_tip_to_dip_distance

    def detectGesture(self, hand_landmark:HandLandmark) -> int:
        try:
            index_finger_up = self.__is_tip_to_wrist_longer_than_pip_to_wrist(hand_landmark.index_finger, hand_landmark.wrist)
            middle_finger_up = self.__is_tip_to_wrist_longer_than_pip_to_wrist(hand_landmark.middle_finger, hand_landmark.wrist)
            if not index_finger_up and not middle_finger_up:
                return GestureEnums.ROCK
            
            ring_finger_up = self.__is_tip_to_wrist_longer_than_pip_to_wrist(hand_landmark.ring_finger, hand_landmark.wrist)
            pinky_finger_up = self.__is_tip_to_wrist_longer_than_pip_to_wrist(hand_landmark.pinky, hand_landmark.wrist)
            if ring_finger_up and pinky_finger_up:
                return GestureEnums.PAPER
            
            return GestureEnums.SCISSORS
        
        except Exception: None
        return GestureEnums.NONE

    def isHandLike(self, hand_landmark:HandLandmark) -> bool:
        try:
            index_finger_up = self.__is_tip_to_wrist_longer_than_pip_to_wrist(hand_landmark.index_finger, hand_landmark.wrist)
            middle_finger_up = self.__is_tip_to_wrist_longer_than_pip_to_wrist(hand_landmark.middle_finger, hand_landmark.wrist)
            ring_finger_up = self.__is_tip_to_wrist_longer_than_pip_to_wrist(hand_landmark.ring_finger, hand_landmark.wrist)
            pinky_finger_up = self.__is_tip_to_wrist_longer_than_pip_to_wrist(hand_landmark.pinky, hand_landmark.wrist)
            thumb_near_palm = self.__is_thumb_to_index_finger_distance_shorter_than_thumb_lenght(hand_landmark.thumb, hand_landmark.index_finger)
            
            if index_finger_up: return False
            if middle_finger_up: return False
            if ring_finger_up: return False
            if pinky_finger_up: return False
            if thumb_near_palm: return False
            return True
        except Exception: 
            return False
