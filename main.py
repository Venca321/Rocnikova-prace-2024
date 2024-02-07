
from engine.engine import HandRecognition, GestureRecognition, GestureEnums, UserStatusEnums
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import numpy as np
import cv2, base64, os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

hand_recognizer = HandRecognition()
gesture_recognizer = GestureRecognition()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'images/favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('image_navigation')
def handle_image(data):
    img_data = base64.b64decode(img_data.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Do something with the image

    emit('response', {"status": "ok"})

@socketio.on('image')
def handle_image(data):
    #img_data = data['image']
    #user_id = data['user_id']
    #status = data['status']

    img_data = base64.b64decode(img_data.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    try:
        landmark = hand_recognizer.getLandmark(img)
        gesture = gesture_recognizer.detectGesture(landmark)
    except Exception:
        gesture = GestureEnums.NONE

    emit('response', {"status": ""})

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0")


