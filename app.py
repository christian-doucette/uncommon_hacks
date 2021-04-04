from flask import Flask, request, render_template
from flask_socketio import SocketIO #, join_room, leave_room, send

import time
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

# global variable set containing all connections currently connected through sockets
# I know global variables like this are bad practice, but its a hackathon, not a best-practiceathon
all_connections = set()




@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('message sent: ' + str(json))
    socketio.emit('my response', json)



@socketio.on('connect')
def on_connect(methods=['GET', 'POST']):
    print('New user connected!')

    # increments num players
    global all_connections
    all_connections.add(request.sid)
    print(f"connections: {all_connections}")



@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected!')

    # decrements num players

    global all_connections
    all_connections.discard(request.sid)
    print(f"all_connections: {all_connections}")




@socketio.on('game start')
def on_game_start(methods=['GET', 'POST']):
    global all_connections
    all_players = list(all_connections.copy()) + ['bot']
    random_player_ordering = random.sample(all_players, k=len(all_players))
    random_player_names    = {player_name: f'Player {index}' for index, player_name in enumerate(random_player_ordering)}

    print('received game start event')
    print(f'Players: {random_player_names}')

    # creates model here
    socketio.emit('game started', random_player_names)
    time.sleep(10)
    socketio.emit('voting started')
    time.sleep(10)
    socketio.emit('voting ended')
    time.sleep(5)
    socketio.emit('back to start')



# won't allow players to end game, does it based off time limit
#@socketio.on('game end')
#def on_game_end(methods=['GET', 'POST']):
#    print('received game end event')
#    socketio.emit('game end')

"""
@socketio.on('join')
def on_join(data):
    print('JOIN REQUEST RECIEVED!')
    username = data['username']
    room = data['room']
    print(f'{username} has entered {room}')

    join_room(room)
    send(username + ' has entered the room.', room=room)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)
"""


@app.route('/')
def home_page():
    return render_template("home.html")


@app.route('/looking_for_game')
def looking_for_game():
    return render_template("looking_for_game.html")


@app.route('/rules')
def rules():
    return render_template("rules.html")


@app.route('/game', methods=['GET', 'POST'])
def game():
    return render_template("game.html")




if __name__ == '__app__':
    socketio.run(app, debug=True)
