
from engine.HandRecognition import HandRecognition
from engine.HandProcessor import HandProcessor
import cv2

DEBUG_MODE = True

Hand_recognition = HandRecognition()

detected_gesture = 0
last_gestures = []

game_running = False
player1_ready = False
player2_ready = True

while True:
    results = Hand_recognition.processImage()

    if results == []: detected_gesture = 0
    for handMap in results:
        hand_processor = HandProcessor(handMap, Hand_recognition.image)
        gesture = hand_processor.process()

        if last_gestures.count(gesture) >= 5:
            if gesture == 1: detected_gesture = 1
            elif gesture == 2: detected_gesture = 2
            elif gesture == 3: detected_gesture = 3
            elif gesture == 4: detected_gesture = 4
            else: detected_gesture = 0

        last_gestures.append(gesture)
        if len(last_gestures) > 5: last_gestures.pop(0)
        
        if DEBUG_MODE: Hand_recognition.drawHandLandmarks(handMap)

    if not player1_ready and not game_running:
        if detected_gesture == 4: player1_ready = True
        else: print("Like to run game")
    
    if player1_ready and player1_ready: 
        game_running = True
        player1_ready = False
        #player2_ready = False

    if game_running:
        print("Running...")
        game_running = False

    if detected_gesture == 1: detected_gesture_text = "Kamen"
    elif detected_gesture == 2: detected_gesture_text = "Papir"
    elif detected_gesture == 3: detected_gesture_text = "Nuzky"
    elif detected_gesture == 4: detected_gesture_text = "Like"
    else: detected_gesture_text = "-----"

    Hand_recognition.image = cv2.putText(Hand_recognition.image, detected_gesture_text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)

    cv2.imshow("Output", Hand_recognition.image)
    if cv2.waitKey(1) == ord('q'): break

Hand_recognition.stop()