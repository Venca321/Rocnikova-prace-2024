
from engine.engine import HandRecognition, GestureRecognition, GestureEnums
from engine.database import Database, UserStatusEnums
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

def get_user_status_screen_info(user_status) -> str:
    if user_status == UserStatusEnums.WAITING: return "Čekání na protihráče"
    elif user_status == UserStatusEnums.READY: return "Připraven"
    elif user_status == UserStatusEnums.PLAYING: return "Probíhá hra"
    elif user_status == UserStatusEnums.WINNER: return "Vítěz"
    elif user_status == UserStatusEnums.LOSER: return "Poražený"
    elif user_status == UserStatusEnums.TIED: return "Remíza"
    else: return "Error"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    db.remove_old_users()
    db.remove_old_sessions()
    user = db.create_user(request.json['username'], GestureEnums.NONE)
    return jsonify({"user_id": user.id})

@app.route('/find-session')
def find_session():
    return render_template('find-session.html')

"""
user = db.get_user(request.json['user_id'])
session_id = request.json['session_id']

if session_id == "None":
    if request.json['host'] == "true":
        session = db.create_session(user.id, "Not yet")
    else:
        session = db.connect_session(user.id)
else:
    session = db.connect_session(user.id, session_id)

return jsonify({"session_id": session.id})
"""

@app.route('/find-random-session', methods=['POST'])
def find__random_session_post():
    user = db.get_user(request.json['user_id'])
    session = db.connect_random_session(user.id)
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
    
    #Engine code

    session = db.get_session(user.id)
    if session.user1_id == user.id:
        user_status = session.user1_status
        opponent = db.get_user(session.user2_id)
    else:
        user_status = session.user2_status
        opponent = db.get_user(session.user1_id)

    gesture_name, gesture_image = get_gesture_screen_info(gesture)
    user_status_text = get_user_status_screen_info(user_status)
    emit('response', {"opponent": opponent.username, "status": user_status_text, "gesture_image": gesture_image, "gesture_name": gesture_name, "id_status": "Correct"})

if __name__ == '__main__':
    #serve(app, host="0.0.0.0", port=5000)
    socketio.run(app, host="0.0.0.0")


