
from engine.HandRecognition import HandRecognition
import cv2

Hand_recognition = HandRecognition()

while True:
    results = Hand_recognition.processImage()

    print(results)

    for handLms in results: # working with each hand
        for id, lm in enumerate(handLms.landmark):
            h, w, c = Hand_recognition.image.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            if id == 4:
                cv2.circle(Hand_recognition.image, (cx, cy), 25, (255, 0, 255), cv2.FILLED)

        Hand_recognition.drawHandLandmarks(handLms)

    cv2.imshow("Output", Hand_recognition.image)
    if cv2.waitKey(1) == ord('q'): break

Hand_recognition.stop()