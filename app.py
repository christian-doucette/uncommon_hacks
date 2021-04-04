from flask import Flask, request, render_template
from flask_socketio import SocketIO #, join_room, leave_room, send

import time
import random
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

# global variable set containing all connections currently connected through sockets
# I know global variables like this are bad practice, but its a hackathon, not a best-practiceathon
all_connections = set()
name_encoder    = dict()
votes           = dict()




@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    json['user_name'] = name_encoder[request.sid]
    print('message sent: ' + str(json))
    socketio.emit('my response', json)



@socketio.on('new_connect')
def on_connect(methods=['GET', 'POST']):
    print('New user connected!')

    # increments num players
    global all_connections
    all_connections.add(request.sid)

    socketio.emit('update num players', len(all_connections))

    print(f"connections: {all_connections}")



@socketio.on('start bot')
def start_bot():
    print('Bot started!')
    choice = random.choice([True, False])

    # 1/2 chance of messaging
    if choice:
        print('Bot actually ran!')
        r = requests.post(
        "https://api.deepai.org/api/text-generator",
        data={
            'text': 'how are you? ',
        },
        headers={'api-key': '8fdab04e-b922-4165-9a0d-25ae9b58017b'}
        )
        output_text = r.json().get('output', 'Im not a bot!')
        outlist = output_text.split()[3:13]
        outlist_text = ' '.join(outlist)

        socketio.emit('my response', {'message' : outlist_text, 'user_name': name_encoder['bot']})



@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected!')

    # decrements num players

    global all_connections
    all_connections.discard(request.sid)
    socketio.emit('update num players', len(all_connections))

    print(f"all_connections: {all_connections}")


@socketio.on('record vote')
def record_vote(vote):
    print('Going to record vote, using global variable!')
    print(f'{request.sid} voted for {vote}')


    global votes
    votes[request.sid] = vote



@socketio.on('game start')
def on_game_start(methods=['GET', 'POST']):
    global all_connections
    global name_encoder

    all_players = list(all_connections.copy()) + ['bot']
    random_player_ordering = random.sample(all_players, k=len(all_players))
    name_encoder           = {player_sid: f'Player {index}' for index, player_sid in enumerate(random_player_ordering)}

    print('received game start event')
    print(f'Players: {name_encoder}')

    # creates model here
    socketio.emit('game started')
    time.sleep(60)
    socketio.emit('voting started', len(all_connections) + 1)
    time.sleep(10)
    socketio.emit('tallying votes')
    time.sleep(5)
    print(votes)

    # calculate scores here
    name_decoder = {val: key for key, val in name_encoder.items()}

    scores = {conn: 0 for conn in all_connections}
    for conn in all_connections:
        if votes[conn] == name_encoder['bot']:
            scores[conn] += 5
        else:
            scores[name_decoder[votes[conn]]] += 1

    # gets names
    scores_with_names = {name_encoder[conn]: score for conn, score in scores.items()}

    socketio.emit('voting ended', scores_with_names)
    time.sleep(5)
    socketio.emit('back to start')





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

@app.route('/About_Us')
def About_Us():
    return render_template("About_Us.html")


if __name__ == '__app__':
    socketio.run(app, debug=True)
