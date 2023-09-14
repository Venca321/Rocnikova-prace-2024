
from engine.HandRecognition import HandRecognition
from engine.HandProcessor import HandProcessor
import cv2

DEBUG_MODE = True

Hand_recognition = HandRecognition()

detected_gesture = ""
last_gestures = []
while True:
    results = Hand_recognition.processImage()

    for handMap in results:
        hand_processor = HandProcessor(handMap, Hand_recognition.image)
        gesture = hand_processor.process()

        if last_gestures.count(gesture) >= 3:
            if gesture == 1: detected_gesture = "Kamen"
            elif gesture == 2: detected_gesture = "Papir"
            elif gesture == 3: detected_gesture = "Nuzky"
            else: detected_gesture = "-----"

        last_gestures.append(gesture)
        if len(last_gestures) > 3: last_gestures.pop(0)

        Hand_recognition.image = cv2.putText(Hand_recognition.image, detected_gesture, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2, cv2.LINE_AA)

        """
        for point_number, hand_point in enumerate(handMap.landmark):
            img_h, img_w, img_c = Hand_recognition.image.shape
            point_x, point_y = int(hand_point.x * img_w), int(hand_point.y * img_h)
            if point_number == 8:
                cv2.circle(Hand_recognition.image, (point_x, point_y), 8, (0, 255, 0), cv2.FILLED)
        """

        if DEBUG_MODE: Hand_recognition.drawHandLandmarks(handMap)

    cv2.imshow("Output", Hand_recognition.image)
    if cv2.waitKey(1) == ord('q'): break

Hand_recognition.stop()