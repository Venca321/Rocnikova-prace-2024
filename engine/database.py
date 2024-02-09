
class UserStatusEnums:
    CONNECTED = 0
    READY = 1
    PLAYING = 2
    SUBMITED = 3
    WINNER = 4
    LOSER = 5
    TIED = 6
    
    def decode(status:int) -> str:
        """
        Decode status enum to string
        """
        if status == UserStatusEnums.CONNECTED: return 'Dejte gesto "palec nahoru"'
        elif status == UserStatusEnums.READY: return "Připraven"
        elif status == UserStatusEnums.PLAYING: return "Probíhá hra..."
        elif status == UserStatusEnums.SUBMITED: return "Vyhodnocoání..."
        elif status == UserStatusEnums.WINNER: return "Vítěz"
        elif status == UserStatusEnums.LOSER: return "Poražen"
        elif status == UserStatusEnums.TIED: return "Remíza"
        raise NotImplementedError