
from engine.engine import HandRecognition, GestureRecognition, GestureEnums
from engine.database import Database
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import numpy as np
import cv2, base64


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

hand_recognizer = HandRecognition()
gesture_recognizer = GestureRecognition()
db = Database()

def get_gesture_screen_info(gesture) -> (str, str):
    if gesture == GestureEnums.ROCK: return "Kámen", "🪨"
    elif gesture == GestureEnums.PAPER: return "Papír", "📜"
    elif gesture == GestureEnums.SCISSORS: return "Nůžky", "✂️"
    elif gesture == GestureEnums.LIKE: return "Like", "👍"
    else: return "Neznámé", "❓"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    user = db.create_user(request.json['username'], GestureEnums.NONE)
    return jsonify({"user_id": user.id})

@app.route('/find-session')
def find_session():
    return render_template('find-session.html')

@app.route('/find-session', methods=['POST'])
def find_session_post():
    user = db.get_user(request.json['user_id'])
    session_id = request.json['session_id']
    host = request.json['host']

    if session_id == "None":
        if host == "true":
            session = db.create_session(user.id, "Not yet")
        else:
            session = db.connect_session(user.id)
    else:
        session = db.connect_session(user.id, session_id)
    
    return jsonify({"session_id": session.id})

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/pick-camera-device')
def pick_camera_device():
    return render_template('pick-camera-device.html')

@socketio.on('image')
def handle_image(data):
    img_data = data['image']
    user_id = data['user_id']

    try: user = db.get_user(user_id)
    except: emit('response', {"opponent": "None", "status": "None", "gesture_image": "", "gesture_name": GestureEnums.NONE, "id_status": "Error"})

    img_data = base64.b64decode(img_data.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    try:
        landmark = hand_recognizer.getLandmark(img)
        gesture = gesture_recognizer.detectGesture(landmark)
    except Exception:
        gesture = GestureEnums.NONE
    
    db.update_user(user, gesture)
    db.remove_old_users()

    gesture_name, gesture_image = get_gesture_screen_info(gesture)
    emit('response', {"opponent": "Bot1", "status": "Not implemented...", "gesture_image": gesture_image, "gesture_name": gesture_name, "id_status": "Correct"})

if __name__ == '__main__':
    #serve(app, host="0.0.0.0", port=5000)
    socketio.run(app, host="0.0.0.0")


