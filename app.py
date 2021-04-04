from flask import Flask, request, render_template
from flask_socketio import SocketIO #, join_room, leave_room, send
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")




def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)


@socketio.on('game start')
def on_game_start(methods=['GET', 'POST']):
    print('received game start event')
    socketio.emit('game started')
    time.sleep(5)
    socketio.emit('voting started')
    time.sleep(5)
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
