
from engine.engine import *
import cv2


DEBUG_MODE = True

class GameUI:
    def checkIfTerminated(handRecognition):
        if cv2.waitKey(1) == ord('q'): #if "q" is pressed
            handRecognition.stop()
            exit()

    def __getGestureSreenText(gesture):
        if gesture == 1: return "Kamen"
        elif gesture == 2: return "Papir"
        elif gesture == 3: return "Nuzky"
        elif gesture == 4: return "Like"
        else: return "-----"

    def showUiScreen(gestureLeft, gestureRight, image):
        detectedGestureLeftText = GameUI.__getGestureSreenText(gestureLeft)
        image = cv2.putText(image, detectedGestureLeftText, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
        
        detectedGestureRightText = GameUI.__getGestureSreenText(gestureRight)
        image = cv2.putText(image, detectedGestureRightText, (int(image.shape[1]/2)+10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
        
        cv2.line(image, (int(image.shape[1]/2), 0), (int(image.shape[1]/2), image.shape[0]), (0, 0, 255), 2) #draw center line
        cv2.imshow("Output", image)


class __GameStates:
    def __init__(self, handRecognition):
        self.handRecognition = handRecognition
        self.playerLeftReady = False
        self.playerRightReady = False

    def __processHandMapToGesture(self, results, handRecognition, image):
        for handMap in results:
            handProcessor = Hands.HandProcessor(handMap, image)
            gesture = handProcessor.process()
            if DEBUG_MODE: handRecognition.drawHandLandmarks(handMap, image)
            return gesture

    def __getGestures(self):
        results = handRecognition.processImage()
        gestureLeft = self.__processHandMapToGesture(results[0], handRecognition, handRecognition.imageLeft)
        gestureRight = self.__processHandMapToGesture(results[1], handRecognition, handRecognition.imageRight)
        return gestureLeft, gestureRight

    def notRuning(self):
        gestureLeft, gestureRight = self.__getGestures()

        if not self.playerLeftReady and gestureLeft == Hands.HandEnums.LIKE:
            self.playerLeftReady = True

        if not self.playerRightReady and gestureRight == Hands.HandEnums.LIKE:
            self.playerRightReady = True

        GameUI.showUiScreen(gestureLeft, gestureRight, self.handRecognition.image)
        GameUI.checkIfTerminated(self.handRecognition)
        
        if self.playerLeftReady and self.playerRightReady: return True
        return False

    def runing(self):
        gestureLeft, gestureRight = self.__getGestures()

        print("Running...")

        GameUI.showUiScreen(gestureLeft, gestureRight, self.handRecognition.image)
        GameUI.checkIfTerminated(self.handRecognition)
        return True

if __name__ == "__main__":
    handRecognition = HandRecognition()

    while True:
        gameState = __GameStates(handRecognition)
        gameRuning = False

        while not gameRuning:
            gameRuning = gameState.notRuning()

        while gameRuning:
            gameRuning = gameState.runing()
