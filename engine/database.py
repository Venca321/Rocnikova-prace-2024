
import sqlite3, uuid, random

class User:
    def __init__(self, id:str, username:str, gesture:int):
        self.id = id
        self.username = username
        self.gesture = gesture

class Session:
    def __init__(self, id:str, user1_id:str, user_1_status:int, user2_id:str, user_2_status:int):
        self.id = id
        self.user1_id = user1_id
        self.user1_status = user_1_status
        self.user2_id = user2_id
        self.user2_status = user_2_status

class UserStatusEnums:
    WAITING = 0
    READY = 1
    PLAYING = 2
    WINNER = 3
    LOSER = 4
    TIED = 5

class Database:
    def __init__(self, file_location:str="database.db"):
        self.connection = sqlite3.connect(file_location)
        self.cursor = self.connection.cursor()

    def push(self):
        """
        Push changes to database
        """
        try: self.cursor.execute("create table users (id text, username text, gesture integer, updated_at timestamp  NOT NULL  DEFAULT current_timestamp ON UPDATE current_timestamp -- trigger -- soft delete)")
        except: None
        try: self.cursor.execute("create table sessions (id text, user1_id text, user1_status integer, user2_id text, user2_status integer, updated_at timestamp  NOT NULL  DEFAULT current_timestamp ON UPDATE current_timestamp -- trigger -- soft delete)")
        except: None

    def create_user(self, username:str, gesture:int) -> User:
        """
        Create user from username
        """
        try:
            user_id = uuid.uuid4()
            self.cursor.execute("insert into users (id, username, gesture) values (?, ?, ?)", (user_id, username, gesture))
            return User(user_id, username, gesture)
        except Exception: return None

    def get_user(self, user_id:str) -> User:
        """
        Get user from id
        """
        try:
            self.cursor.execute("select * from users where id=:id", {"id": user_id})
            user = self.cursor.fetchall()
            return User(user[0], user[1], user[2])
        except Exception: return None

    def update_user(self, user:User, gesture:int) -> User:
        """
        Update users gesture
        """
        try:
            self.cursor.execute("update users set gesture=:gesture where id=:id", {"gesture": gesture, "id": user.id})
            return User(user.id, user.username, gesture)
        except Exception: return None

    def remove_old_users(self):
        """
        Remove users that are not connected anymore
        """
        pass

    def create_session(self, user1_id, user2_id) -> Session:
        """
        Create session
        """
        try:
            session_id = str(random.randint(100000, 9999999))
            self.cursor.execute("insert into sessions (id, user1_id, user1_status, user2_id, user2_status) values (?, ?, ?, ?, ?)", (session_id, user1_id, UserStatusEnums.WAITING, user2_id, UserStatusEnums.WAITING))
            return Session(session_id, user2_id, UserStatusEnums.WAITING, user2_id, UserStatusEnums.WAITING)
        except Exception: return None

    def get_session(self, session_id:str) -> Session:
        """
        Get session from id
        """
        try:
            self.cursor.execute("select * from sessions where id=:id", {"id": session_id})
            session = self.cursor.fetchall()
            return Session(session[0], session[1], session[2], session[3], session[4])
        except Exception: return None

    def update_session(self, session:Session, user1_status:int, user2_status:int) -> Session:
        """
        Update session
        """
        try:
            self.cursor.execute("update sessions set user1_status=:user1_status, user2_status=:user2_status where id=:id", {"user1_status": user1_status, "user2_status": user2_status, "id": session.id})
            return Session(session.id, session.user1_id, user1_status, session.user2_id, user2_status)
        except Exception: return None

    def remove_old_sessions(self):
        """
        Remove sessions that are not connected anymore
        """
        pass
