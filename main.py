
from engine.engine import *
import cv2

DEBUG_MODE = True
LIMIT = 3

handRecognition = HandRecognition()

gameRunning = False
playerLeftReady = False
playerRightReady = False

while True:
    results = handRecognition.processImage()

    if results[0] == []: gestureLeft = 0
    if results[1] == []: gestureRight = 0

    for handMap in results[0]:
        hand_processor = Hands.HandProcessor(handMap, handRecognition.imageLeft)
        gestureLeft = hand_processor.process()
        
        if DEBUG_MODE: handRecognition.drawHandLandmarks(handMap, handRecognition.imageLeft)

    for handMap in results[1]:
        hand_processor = Hands.HandProcessor(handMap, handRecognition.imageRight)
        gestureRight = hand_processor.process()

        if DEBUG_MODE: handRecognition.drawHandLandmarks(handMap, handRecognition.imageRight)

    if not playerLeftReady and not gameRunning and gestureLeft == 4:
        playerLeftReady = True

    if not playerRightReady and not gameRunning and gestureRight == 4:
        playerRightReady = True
    
    if playerLeftReady and playerRightReady: 
        gameRunning = True
        playerLeftReady = False
        playerRightReady = False

    if gameRunning:
        print("Running...")
        gameRunning = False

    if gestureLeft == 1: detectedGestureLeftText = "Kamen"
    elif gestureLeft == 2: detectedGestureLeftText = "Papir"
    elif gestureLeft == 3: detectedGestureLeftText = "Nuzky"
    elif gestureLeft == 4: detectedGestureLeftText = "Like"
    else: detectedGestureLeftText = "-----"
    handRecognition.image = cv2.putText(handRecognition.image, detectedGestureLeftText, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
    
    if gestureRight == 1: detectedGestureRightText = "Kamen"
    elif gestureRight == 2: detectedGestureRightText = "Papir"
    elif gestureRight == 3: detectedGestureRightText = "Nuzky"
    elif gestureRight == 4: detectedGestureRightText = "Like"
    else: detectedGestureRightText = "-----"
    handRecognition.image = cv2.putText(handRecognition.image, detectedGestureRightText, (int(handRecognition.image.shape[1]/2)+10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
    
    cv2.line(handRecognition.image, (int(handRecognition.image.shape[1]/2), 0), (int(handRecognition.image.shape[1]/2), handRecognition.image.shape[0]), (0, 0, 255), 2)

    cv2.imshow("Output", handRecognition.image)
    if cv2.waitKey(1) == ord('q'): break

handRecognition.stop()