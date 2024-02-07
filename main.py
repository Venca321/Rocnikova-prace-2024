
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
def handle_image_navigation(data):
    flip = bool(data['flip'])

    img_data = data['image']
    img_data = base64.b64decode(img_data.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    input_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if flip: input_img = cv2.flip(input_img, 1)

    cursor, click = None, None
    try:
        # TODO: downsite the image if needed

        landmark, image = hand_recognizer.getLandmark(input_img)
        if landmark.index_finger.finger_tip[0] is not None and landmark.thumb.finger_tip[0] is not None:
            cursor = gesture_recognizer.calculate_middle_point(landmark.index_finger.finger_tip, landmark.thumb.finger_tip)
            click = gesture_recognizer.is_clicked(landmark)

        # TODO: get data from the landmark

        _, buffer = cv2.imencode('.png', image)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        emit('response', {"status": "ok", "cursor": cursor, "click": click, "image": f"data:image/png;base64,{img_base64}"})
    except Exception as e:
        print(e)
        emit('response', {"status": "error"})

@socketio.on('image')
def handle_image(data):
    #user_id = data['user_id']
    #status = data['status']

    img_data = data['image']
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


