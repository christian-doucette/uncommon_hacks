from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template("home.html")


@app.route('/looking_for_game')
def looking_for_game():
    return render_template("looking_for_game.html")


@app.route('/rules')
def rules():
    return render_template("rules.html")
