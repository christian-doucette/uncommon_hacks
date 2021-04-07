# Spot the Bot
*Spot the Bot* was built by Christian, Jake, Mason and Kevin in a 24 hour period for Uncommon Hacks 2021. Our web app is live [here](https://spot-the-bot-hackathon.herokuapp.com/)!


## The Idea
*Spot the Bot* is a web-based game where players chat with other players and one bot. After a minute of chatting, players make a guess of who the bot is. Each player gets points for correctly guessing the bot, and by misleading other players into thinking that they are the bot. For this, we were inspired by the idea of Turing Tests, as well as imposter games such as *Among Us*.


## Challenges
The main technical challenge was building a web-based interactive multiplayer game. While we had experience with web applications and Flask, building the level of interactivity needed for an online chat-based game required the use of sockets, which we had not used before. We used flask_socketio, Flask's socket library.

We also had some trouble with the chatbot. While we tried to use a pretrained chatbot model for this, hosting our web app with the file size required for a good chatbot model was difficult. To get around this, we switched to instead use a text generation API from DeepAI.
