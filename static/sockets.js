// Hides navbar, doing this because we want to leave the navbar in base.html but don't want it on this page
$("nav.navbar").hide();




// Socket code
var socket = io.connect('https://' + document.domain + ':' + location.port);

socket.on('connect', function() {
    console.log("Connected");
    socket.emit('new_connect');
    var form = $('form').on('submit', function(e) {
        e.preventDefault()
        let user_input = $('input.message').val()
        socket.emit('my event', {
            message : user_input
        } )
        socket.emit('start bot')
      $('input.message').val('').focus()
    } )
} )


// Updates number of players in lobby when someone enters or leaves
socket.on('update num players', function(new_num) {
    console.log('got update number players message')
    $("p.num_players").text(`Number of players: ${new_num}`);
})

socket.on('my response', function(msg) {
    console.log("Response")
    console.log(msg)
    if(typeof msg.user_name !== 'undefined') {
        $('h3').remove()
        $('div.message_holder').append('<div><b style="color: #000">'+msg.user_name+'</b> '+msg.message+'</div>')
    }
})

socket.on('game started', function() {
    console.log("Game started!");
    $("div.before_start").hide();
    timeLeft = 60;
    $("div.game").show();
})

socket.on('voting started', function(num_options) {
    for (var i = 0; i < num_options; i++) {
      $("select.bot_guess").append(`<option value="Player ${i}">Player ${i}</option>`)
    };

    console.log("Voting started!");
    $("div.game").hide();
    timeLeft = 10;
    $("div.voting").show()
})

socket.on('tallying votes', function() {
    console.log("Tallying votes!");
    let bot_guess = $('select.bot_guess').val()
    socket.emit("record vote", bot_guess)

    $("div.voting").hide();
    timeLeft = 5;
    $("div.tallying").show()

})

socket.on('voting ended', function(scores) {
    Object.keys(scores).forEach(function(key) {
      $("ol.scoreboard").append(`<li>Player: ${key}, score: ${scores[key]}</li>`)
    })
    $("div.tallying").hide();
    timeLeft = 5;
    $("div.score").show();
})



socket.on('back to start', function() {
    console.log("Back to start!");

    // Removes all messages, score, and vote options from the previous game
    $('div.message_holder').empty();
    $("ol.scoreboard").empty();
    $("select.bot_guess").empty();

    $("div.score").hide();
    $("div.before_start").show();
})
