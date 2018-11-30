
from flask_socketio import Namespace, emit

class GameRoomNamespace(Namespace):
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_play_turn(self, data):
        emit('game_update', data)

    def on_something_else(self, data):
        emit('game_update', data)





