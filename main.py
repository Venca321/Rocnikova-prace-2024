
from engine.engine import HandRecognition, GestureRecognition, GestureEnums, GameEngine
from engine.database import Database, UserStatusEnums
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import numpy as np
import cv2, base64, os


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
    if user_status == UserStatusEnums.WAITING: return "Čekání na protihráče..."
    elif user_status == UserStatusEnums.CONNECTED: return "Dejte like pro spuštění hry"
    elif user_status == UserStatusEnums.READY: return "Připraven"
    elif user_status == UserStatusEnums.PLAYING: return "Probíhá hra..."
    elif user_status == UserStatusEnums.SUBMITED: return "Čekání na vyhodnocení..."
    elif user_status == UserStatusEnums.WINNER: return "Vítěz!"
    elif user_status == UserStatusEnums.LOSER: return "Poražený"
    elif user_status == UserStatusEnums.TIED: return "Remíza"
    else: return "Error"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'images/favicon.ico', mimetype='image/vnd.microsoft.icon')

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

@app.route('/find-random-session', methods=['POST'])
def find_random_session_post():
    session = db.connect_random_session(request.json['user_id'])
    return jsonify({"session_id": session.id})

@app.route('/friend-game')
def friend_game():
    return render_template('friend-game.html')

@app.route('/create-friend-game')
def create_friend_game():
    return render_template('create-friend-game.html')

@app.route('/create-friend-game', methods=['POST'])
def create_friend_game_post():
    session = db.create_session(request.json['user_id'])
    return jsonify({"status": "ok", "session_id": session.id})

@app.route('/connect-friend-game')
def connect_friend_game():
    return render_template('connect-friend-game.html')

@app.route('/connect-friend-game', methods=['POST'])
def connect_friend_game_post():
    db.connect_session(request.json['user_id'], request.json['session_id'])
    return jsonify({"status": "ok"})

@app.route('/connect-bot', methods=['POST'])
def connect_bot_post():
    db.connect_bot_to_session(request.json["session_id"])
    return jsonify({"status": "ok"})

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
    status = data['status']

    try: user = db.get_user(user_id)
    except: emit('response', {"session_id": "", "opponent": "", "status": "Error", "gesture_image": "", "gesture_name": GestureEnums.NONE})
    session = db.get_session(user.id)

    if status == "submited": 
        db.update_session(user.id, UserStatusEnums.SUBMITED)
    elif status == "ready_to_replay":
        db.update_session(user.id, UserStatusEnums.CONNECTED)

    img_data = base64.b64decode(img_data.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    banned_status = [UserStatusEnums.SUBMITED, UserStatusEnums.WINNER, UserStatusEnums.LOSER, UserStatusEnums.TIED]
    if (user_id == session.user1_id and session.user1_status not in banned_status) or (user_id == session.user2_id and session.user2_status not in banned_status):
        try:
            landmark = hand_recognizer.getLandmark(img)
            gesture = gesture_recognizer.detectGesture(landmark)
        except Exception:
            gesture = GestureEnums.NONE

        if gesture != GestureEnums.NONE: db.update_user(user, gesture)

    session, user_status, opponent = GameEngine.process(db, session, user)
    gesture_name, gesture_image = get_gesture_screen_info(user.gesture)
    user_status_text = get_user_status_screen_info(user_status)
    emit('response', {"session_id": session.id, "opponent": opponent.username, "status": user_status_text, "gesture_image": gesture_image, "message": gesture_name})

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0")


