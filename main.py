
from engine.engine import HandRecognition, GestureRecognition, Gesture
from flask import Flask, render_template, request, Response, jsonify
from waitress import serve
import numpy as np
import cv2


app = Flask(__name__)

hand_recognizer = HandRecognition()
gesture_recognizer = GestureRecognition()

def getGestureSreenText(gesture) -> str:
    if gesture == Gesture.ROCK: return "Kámen"
    elif gesture == Gesture.PAPER: return "Papír"
    elif gesture == Gesture.SCISSORS: return "Nůžky"
    elif gesture == Gesture.LIKE: return "Like"
    else: return "-----"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'frame' not in request.files: return Response(status=400)
    
    file = request.files['frame']
    file_str = file.read()
    nparr = np.frombuffer(file_str, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    try:
        landmark = hand_recognizer.getLandmark(img)
        gesture = gesture_recognizer.detectGesture(landmark)
    except Exception:
        gesture = 0

    print(gesture)

    return jsonify({"message": getGestureSreenText(gesture)})

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)
