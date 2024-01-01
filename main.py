
from engine.engine import HandRecognition, GestureRecognition, GestureEnums, GameEngine
import cv2, time


DEBUG_MODE = True


class GameStateEnums:
    LOADING = 0
    WAITING_FOR_PLAYERS = 1
    RUNNING = 2
    RESULTS_SCREEN = 3

class GameUI:
    def __init__(self, hand_recognizer:HandRecognition):
        self.hand_recognizer = hand_recognizer

    def __checkIfTerminated(self):
        if cv2.waitKey(1) == ord('q'): #if "q" is pressed
            self.hand_recognizer.stop()
            exit()

    def getGestureSreenText(self, gesture):
        if gesture == GestureEnums.ROCK: return "Kamen"
        elif gesture == GestureEnums.PAPER: return "Papir"
        elif gesture == GestureEnums.SCISSORS: return "Nuzky"
        elif gesture == GestureEnums.LIKE: return "Like"
        else: return "-----"

    def showUiScreen(self, text_left:str, text_right:str, image):
        image = cv2.putText(image, text_left, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
        image = cv2.putText(image, text_right, (int(image.shape[1]/2)+10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.line(image, (int(image.shape[1]/2), 0), (int(image.shape[1]/2), image.shape[0]), (0, 0, 255), 2) #draw center line
        cv2.imshow("Output", image)
        self.__checkIfTerminated()


if __name__ == "__main__":
    hand_recognizer = HandRecognition()
    gesture_recognizer = GestureRecognition()
    game_state = GameStateEnums.LOADING
    last_timer_update = time.time()

    while True:
        while game_state == GameStateEnums.LOADING:
            print("Loading...")
            game_ui = GameUI(hand_recognizer)
            game_engine = GameEngine()
            game_state = GameStateEnums.WAITING_FOR_PLAYERS

        while game_state == GameStateEnums.WAITING_FOR_PLAYERS:
            landmarks = hand_recognizer.getLandmarks(DEBUG_MODE)
            left_gesture = gesture_recognizer.detectGesture(landmarks.left_landmark)
            right_gesture = gesture_recognizer.detectGesture(landmarks.right_landmark)

            game_engine.checkPlayersReadiness(left_gesture, right_gesture)
            if game_engine.arePlayersReady(): game_state = GameStateEnums.RUNNING

            if game_engine.player_left_ready: gesture_text_left = "Ready"
            else: gesture_text_left = game_ui.getGestureSreenText(left_gesture)
            if game_engine.player_right_ready: gesture_text_right = "Ready"
            else: gesture_text_right = game_ui.getGestureSreenText(right_gesture)
            game_ui.showUiScreen(gesture_text_left, gesture_text_right, hand_recognizer.image)

        while game_state == GameStateEnums.RUNNING:
            landmarks = hand_recognizer.getLandmarks(DEBUG_MODE)
            left_gesture = gesture_recognizer.detectGesture(landmarks.left_landmark)
            right_gesture = gesture_recognizer.detectGesture(landmarks.right_landmark)

            if game_engine.seconds_to_start > 0 and (time.time() - last_timer_update) >= 1:
                print(game_engine.seconds_to_start)
                game_engine.seconds_to_start -= 1
                last_timer_update = time.time()
            elif game_engine.seconds_to_start <= 0:
                print("NOW!")
                submited_left_gesture = left_gesture
                submited_right_gesture = right_gesture
                game_state = GameStateEnums.RESULTS_SCREEN

            game_ui.showUiScreen("...", "...", hand_recognizer.image)

        while game_state == GameStateEnums.RESULTS_SCREEN:
            game_state = GameStateEnums.LOADING
            print("Results")
            print(f"Player left: {submited_left_gesture}")
            print(f"Player right: {submited_right_gesture}")
            game_ui.showUiScreen("...", "...", hand_recognizer.image)