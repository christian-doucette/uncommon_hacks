from flask import Flask, request, render_template
from flask_socketio import SocketIO

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

if __name__ == '__main__':
    socketio.run(app, debug=True)

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
