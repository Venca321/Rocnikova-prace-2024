
class UserStatusEnums:
    CONNECTED = 0
    PLAYING = 1
    SUBMITED = 2
    WINNER = 3
    LOSER = 4
    TIED = 5
    
    def decode(status:int) -> str:
        """
        Decode status enum to string
        """
        if status == UserStatusEnums.CONNECTED: return 'Dejte gesto "palec nahoru"'
        elif status == UserStatusEnums.PLAYING: return "Probíhá hra..."
        elif status == UserStatusEnums.SUBMITED: return "Vyhodnocování..."
        elif status == UserStatusEnums.WINNER: return "Vítěz"
        elif status == UserStatusEnums.LOSER: return "Poražen"
        elif status == UserStatusEnums.TIED: return "Remíza"
        raise NotImplementedError