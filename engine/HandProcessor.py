
class HandProcessor:
    """
    Code for processing hand map and gestions recognition
    """
    def __init__(self, handMap, Hand_recognition_image):
        self.handMap = handMap
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

        if self.isHandRock(): return 1
        if self.isHandPaper(): return 2
        if self.isHandScissors(): return 3

        return 0

    def isHandRock(self) -> bool:
        """
        Returns True if the gesture is rock
        """
        raise NotImplementedError

    def isHandPaper(self) -> bool:
        """
        Returns True if the gesture is paper
        """
        raise NotImplementedError

    def isHandScissors(self) -> bool:
        """
        Returns True if the gesture is scissors
        """
        raise NotImplementedError