
from engine.engine import HandRecognition, GestureRecognition, GestureEnums
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

import numpy as np
import cv2, base64


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

hand_recognizer = HandRecognition()
gesture_recognizer = GestureRecognition()

def getGestureSreenText(gesture) -> str:
    if gesture == GestureEnums.ROCK: return "Kámen 🪨"
    elif gesture == GestureEnums.PAPER: return "Papír 📜"
    elif gesture == GestureEnums.SCISSORS: return "Nůžky ✂️"
    elif gesture == GestureEnums.LIKE: return "Like 👍"
    else: return "-----"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def index():
    return render_template('game.html')

@app.route('/pick-camera-device')
def pick_camera_device():
    return render_template('pick-camera-device.html')

@socketio.on('image')
def handle_image(data):
    img_data = base64.b64decode(data.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    try:
        landmark = hand_recognizer.getLandmark(img)
        gesture = gesture_recognizer.detectGesture(landmark)
    except Exception:
        gesture = 0

    emit('response', {"message": getGestureSreenText(gesture)})

if __name__ == '__main__':
    #serve(app, host="0.0.0.0", port=5000)
    socketio.run(app, host="0.0.0.0")


