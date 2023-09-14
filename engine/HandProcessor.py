
class HandProcessor:
    """
    Code for processing hand map and gestions recognition
    """
    def __init__(self, handMap, Hand_recognition_image):
        self.handMap = handMap
        self.handData = {}
        self.hand_recognition_image = Hand_recognition_image

    def process(self) -> int:
        """
        Returns:
            0: if the gesture is not recognized
            1: if the gesture is rock
            2: if the gesture is paper
            3: if the gesture is scissors
        """
        data = {}
        for point_number, hand_point in enumerate(self.handMap.landmark):
            img_h, img_w, _ = self.hand_recognition_image.shape
            point_x, point_y = int(hand_point.x * img_w), int(hand_point.y * img_h)
            data[point_number] = [point_x, point_y, hand_point.z]

        self.handData = data

        if self.isHandRock(): return 1
        if self.isHandPaper(): return 2
        if self.isHandScissors(): return 3

        return 0

    def isHandRock(self) -> bool:
        """
        Returns True if the gesture is rock
        """
        #ukazovacek
        finger_tip_to_wrist = (abs(self.handData[8][0] - self.handData[0][0]) + abs(self.handData[8][1] - self.handData[0][1]))
        finger_center_to_wrist = (abs(self.handData[6][0] - self.handData[0][0]) + abs(self.handData[6][1] - self.handData[0][1])) * 1.1
        if finger_tip_to_wrist > finger_center_to_wrist: return False

        #prostrednicek
        finger_tip_to_wrist = (abs(self.handData[12][0] - self.handData[0][0]) + abs(self.handData[12][1] - self.handData[0][1]))
        finger_center_to_wrist = (abs(self.handData[10][0] - self.handData[0][0]) + abs(self.handData[10][1] - self.handData[0][1])) * 1.1
        if finger_tip_to_wrist > finger_center_to_wrist: return False

        #prstenicek
        finger_tip_to_wrist = (abs(self.handData[16][0] - self.handData[0][0]) + abs(self.handData[16][1] - self.handData[0][1]))
        finger_center_to_wrist = (abs(self.handData[14][0] - self.handData[0][0]) + abs(self.handData[14][1] - self.handData[0][1])) * 1.1
        if finger_tip_to_wrist > finger_center_to_wrist: return False

        #malicek
        finger_tip_to_wrist = (abs(self.handData[20][0] - self.handData[0][0]) + abs(self.handData[20][1] - self.handData[0][1]))
        finger_center_to_wrist = (abs(self.handData[18][0] - self.handData[0][0]) + abs(self.handData[18][1] - self.handData[0][1])) * 1.1
        if finger_tip_to_wrist > finger_center_to_wrist: return False

        #palec
        finger_lenght = (abs(self.handData[4][0] - self.handData[3][0]) + abs(self.handData[4][1] - self.handData[3][1])) ** 0.5
        finger_lenght += (abs(self.handData[3][0] - self.handData[2][0]) + abs(self.handData[3][1] - self.handData[2][1])) ** 0.5
        finger_lenght += (abs(self.handData[2][0] - self.handData[1][0]) + abs(self.handData[2][1] - self.handData[1][1])) ** 0.5
        thumb_index_finger_distance = (abs(self.handData[6][0] - self.handData[3][0]) + abs(self.handData[6][1] - self.handData[3][1])) ** 0.5
        if thumb_index_finger_distance > finger_lenght / 2.5: return False

        return True

    def isHandPaper(self) -> bool:
        """
        Returns True if the gesture is paper
        """
        finger_tip_to_wrist = (abs(self.handData[8][0] - self.handData[0][0]) + abs(self.handData[8][1] - self.handData[0][1]))
        finger_center_to_wrist = (abs(self.handData[6][0] - self.handData[0][0]) + abs(self.handData[6][1] - self.handData[0][1])) * 1.1
        if finger_tip_to_wrist < finger_center_to_wrist: return False

        finger_tip_to_wrist = (abs(self.handData[12][0] - self.handData[0][0]) + abs(self.handData[12][1] - self.handData[0][1]))
        finger_center_to_wrist = (abs(self.handData[10][0] - self.handData[0][0]) + abs(self.handData[10][1] - self.handData[0][1])) * 1.1
        if finger_tip_to_wrist < finger_center_to_wrist: return False

        finger_tip_to_wrist = (abs(self.handData[16][0] - self.handData[0][0]) + abs(self.handData[16][1] - self.handData[0][1]))
        finger_center_to_wrist = (abs(self.handData[14][0] - self.handData[0][0]) + abs(self.handData[14][1] - self.handData[0][1])) * 1.1
        if finger_tip_to_wrist < finger_center_to_wrist: return False

        finger_tip_to_wrist = (abs(self.handData[20][0] - self.handData[0][0]) + abs(self.handData[20][1] - self.handData[0][1]))
        finger_center_to_wrist = (abs(self.handData[18][0] - self.handData[0][0]) + abs(self.handData[18][1] - self.handData[0][1])) * 1.1
        if finger_tip_to_wrist < finger_center_to_wrist: return False

        return True

    def isHandScissors(self) -> bool:
        """
        Returns True if the gesture is scissors
        """
        finger_tip_to_wrist = (abs(self.handData[8][0] - self.handData[0][0]) + abs(self.handData[8][1] - self.handData[0][1]))
        finger_center_to_wrist = (abs(self.handData[6][0] - self.handData[0][0]) + abs(self.handData[6][1] - self.handData[0][1])) * 1.1
        if finger_tip_to_wrist < finger_center_to_wrist: return False

        finger_tip_to_wrist = (abs(self.handData[12][0] - self.handData[0][0]) + abs(self.handData[12][1] - self.handData[0][1]))
        finger_center_to_wrist = (abs(self.handData[10][0] - self.handData[0][0]) + abs(self.handData[10][1] - self.handData[0][1])) * 1.1
        if finger_tip_to_wrist < finger_center_to_wrist: return False

        finger_tip_to_wrist = (abs(self.handData[16][0] - self.handData[0][0]) + abs(self.handData[16][1] - self.handData[0][1]))
        finger_center_to_wrist = (abs(self.handData[14][0] - self.handData[0][0]) + abs(self.handData[14][1] - self.handData[0][1])) * 1.1
        if finger_tip_to_wrist > finger_center_to_wrist: return False

        finger_tip_to_wrist = (abs(self.handData[20][0] - self.handData[0][0]) + abs(self.handData[20][1] - self.handData[0][1]))
        finger_center_to_wrist = (abs(self.handData[18][0] - self.handData[0][0]) + abs(self.handData[18][1] - self.handData[0][1])) * 1.1
        if finger_tip_to_wrist > finger_center_to_wrist: return False

        #palec
        finger_lenght = (abs(self.handData[4][0] - self.handData[3][0]) + abs(self.handData[4][1] - self.handData[3][1])) ** 0.5
        finger_lenght += (abs(self.handData[3][0] - self.handData[2][0]) + abs(self.handData[3][1] - self.handData[2][1])) ** 0.5
        finger_lenght += (abs(self.handData[2][0] - self.handData[1][0]) + abs(self.handData[2][1] - self.handData[1][1])) ** 0.5
        thumb_index_finger_distance = (abs(self.handData[6][0] - self.handData[3][0]) + abs(self.handData[6][1] - self.handData[3][1])) ** 0.5
        if thumb_index_finger_distance > finger_lenght / 2: return False

        return True