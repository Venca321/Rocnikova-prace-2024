
from engine.HandRecognition import HandRecognition
from engine.HandProcessor import HandProcessor
import cv2

DEBUG_MODE = True

Hand_recognition = HandRecognition()

while True:
    results = Hand_recognition.processImage()

    for handMap in results:
        hand_processor = HandProcessor(handMap, Hand_recognition.image)
        gesture = hand_processor.process()
        print(gesture)

        """for point_number, hand_point in enumerate(handMap.landmark):
            img_h, img_w, img_c = Hand_recognition.image.shape
            point_x, point_y = int(hand_point.x * img_w), int(hand_point.y * img_h)
            if point_number == 4:
                cv2.circle(Hand_recognition.image, (point_x, point_y), 25, (255, 0, 255), cv2.FILLED)
        """

        if DEBUG_MODE: Hand_recognition.drawHandLandmarks(handMap)

    cv2.imshow("Output", Hand_recognition.image)
    if cv2.waitKey(1) == ord('q'): break

Hand_recognition.stop()