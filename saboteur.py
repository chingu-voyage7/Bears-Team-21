import os

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from socket_module import GameRoomNamespace


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SABOTEUR_SECRET_KEY")

socketio = SocketIO(app)

game_rooms = {}

@app.route("/", methods=["POST", "GET"])
def index():
    return jsonify(game_rooms)

@socketio.on('create room')
def on_create(data):
    # create game room, query game-manager.py for new game room
    room_entry = {STUFF: "TO-BE DEFINED", gameState: "GAMEMANAGER To be used to generate new game listing", roomId:"generate", players: []}
    roomId = room_entry.roomId
    newGame = room_entry
    game_rooms[roomId] = gameState
    join_room(roomId)
    emit('join_room', {'game_roomId': roomId})

@socketio.on('join_room')
def on_join(data):
    # join a game room
    roomId = data['game_roomId']
    if roomId in game_rooms:
        game_rooms[players].append(data['userId')
        join_room(roomId)
        send(game_rooms[roomId].to_json(), roomId=roomId)
        socketio.on_namespace(GameRoomNamespace(roomId))

@socketio.on("leave")
def on_leave(roomId):
    leave_room(roomId)
    emit("leave game room", room=roomId)

if __name__ == '__main__':
    socketio.run(app)