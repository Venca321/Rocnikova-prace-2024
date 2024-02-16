
from engine.engine import HandRecognition, GestureRecognition, GestureEnums, UserStatusEnums, GameEngine
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import numpy as np
import cv2, base64, os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

hand_recognizer = HandRecognition()
gesture_recognizer = GestureRecognition()
game_engine = GameEngine()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'images/favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/settings")
def settings():
    return render_template('settings.html')

@app.route("/game")
def game():
    return render_template('game.html')

@socketio.on('image_navigation')
def handle_image_navigation(data):
    flip = data['flip'] == "true"

    img_data = data['image']
    img_data = base64.b64decode(img_data.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    input_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if flip: input_img = cv2.flip(input_img, 1)

    cursor, click = None, None
    try:
        landmark, image = hand_recognizer.getLandmark(input_img)
        if landmark.index_finger.finger_tip[0] is not None and landmark.thumb.finger_tip[0] is not None:
            cursor = gesture_recognizer.calculate_middle_point(landmark.index_finger.finger_tip, landmark.thumb.finger_tip)
            click = gesture_recognizer.is_clicked(landmark)

        _, buffer = cv2.imencode('.png', image)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        emit('response', {"status": "ok", "cursor": cursor, "click": click, "image": f"data:image/png;base64,{img_base64}"})
    except Exception as e:
        print(e)
        emit('response', {"status": "error"})

@socketio.on('image')
def handle_image(data):
    flip = data['flip'] == "true"
    user_status = int(data["user_status"])
    gesture = int(data["gesture"])

    img_data = data['image']
    img_data = base64.b64decode(img_data.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    input_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if flip: input_img = cv2.flip(input_img, 1)

    try:
        landmark, image = hand_recognizer.getLandmark(input_img)
        recognition_game_status = [UserStatusEnums.CONNECTED, UserStatusEnums.PLAYING]
        if user_status in recognition_game_status:
            gesture = gesture_recognizer.detectGesture(landmark)
            if (
                user_status == UserStatusEnums.CONNECTED 
                and gesture_recognizer.isHandLike(landmark)
                ):
                gesture = GestureEnums.LIKE

        user_status = game_engine.process(gesture, user_status)

        _, buffer = cv2.imencode('.png', image)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        emit('response', {
            "status": "ok", "gesture": gesture, "gesture_text": GestureEnums.decode(gesture), 
            "user_status": user_status, "user_status_text": UserStatusEnums.decode(user_status),
            "image": f"data:image/png;base64,{img_base64}"
        })
    except Exception as e:
        print(e)
        emit('response', {"status": "error"})

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0")
