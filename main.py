
from engine.HandRecognition import HandRecognition
from engine.HandProcessor import HandProcessor
import cv2

DEBUG_MODE = True
LIMIT = 3

Hand_recognition = HandRecognition()

detected_gesture0 = 0
detected_gesture1 = 0
last_gestures0 = []
last_gestures1 = []

game_running = False
player0_ready = False
player1_ready = False

while True:
    results = Hand_recognition.processImage()

    if results[0] == []: detected_gesture0 = 0
    if results[1] == []: detected_gesture1 = 0

    for handMap in results[0]:
        hand_processor = HandProcessor(handMap, Hand_recognition.image0)
        gesture = hand_processor.process()

        if last_gestures0.count(gesture) >= LIMIT:
            if gesture == 1: detected_gesture0 = 1
            elif gesture == 2: detected_gesture0 = 2
            elif gesture == 3: detected_gesture0 = 3
            elif gesture == 4: detected_gesture0 = 4
            else: detected_gesture0 = 0

        last_gestures0.append(gesture)
        if len(last_gestures0) > LIMIT: last_gestures0.pop(0)
        
        if DEBUG_MODE: Hand_recognition.drawHandLandmarks(handMap, Hand_recognition.image0)

    for handMap in results[1]:
        hand_processor = HandProcessor(handMap, Hand_recognition.image1)
        gesture = hand_processor.process()

        if last_gestures1.count(gesture) >= LIMIT:
            if gesture == 1: detected_gesture1 = 1
            elif gesture == 2: detected_gesture1 = 2
            elif gesture == 3: detected_gesture1 = 3
            elif gesture == 4: detected_gesture1 = 4
            else: detected_gesture1 = 0

        last_gestures1.append(gesture)
        if len(last_gestures1) > LIMIT: last_gestures1.pop(0)
        
        if DEBUG_MODE: Hand_recognition.drawHandLandmarks(handMap, Hand_recognition.image1)

    if not player0_ready and not game_running:
        if detected_gesture0 == 4: player0_ready = True

    if not player1_ready and not game_running:
        if detected_gesture1 == 4: player1_ready = True
    
    if player0_ready and player1_ready: 
        game_running = True
        player0_ready = False
        player1_ready = False

    if game_running:
        print("Running...")
        game_running = False

    if detected_gesture0 == 1: detected_gesture_text0 = "Kamen"
    elif detected_gesture0 == 2: detected_gesture_text0 = "Papir"
    elif detected_gesture0 == 3: detected_gesture_text0 = "Nuzky"
    elif detected_gesture0 == 4: detected_gesture_text0 = "Like"
    else: detected_gesture_text0 = "-----"
    Hand_recognition.image = cv2.putText(Hand_recognition.image, detected_gesture_text0, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
    
    if detected_gesture1 == 1: detected_gesture_text1 = "Kamen"
    elif detected_gesture1 == 2: detected_gesture_text1 = "Papir"
    elif detected_gesture1 == 3: detected_gesture_text1 = "Nuzky"
    elif detected_gesture1 == 4: detected_gesture_text1 = "Like"
    else: detected_gesture_text1 = "-----"
    Hand_recognition.image = cv2.putText(Hand_recognition.image, detected_gesture_text1, (int(Hand_recognition.image.shape[1]/2)+10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
    
    cv2.line(Hand_recognition.image, (int(Hand_recognition.image.shape[1]/2), 0), (int(Hand_recognition.image.shape[1]/2), Hand_recognition.image.shape[0]), (0, 0, 255), 2)

    cv2.imshow("Output", Hand_recognition.image)
    if cv2.waitKey(1) == ord('q'): break

Hand_recognition.stop()