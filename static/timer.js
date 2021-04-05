// Timer code

// timeLeft is set to various numbers at the different stages
var timeLeft = 0;
//var elem = document.getElementById('timer');

var timerId = setInterval(countdown, 1000);

function countdown() {
  if (timeLeft >= 0) {
    //elem.innerHTML = timeLeft + ' seconds remaining for this stage';
    $("div.timer").text(timeLeft + ' seconds remaining for this stage');
    //$("div.timer").text("TEST IF THIS WORKS");

    timeLeft--;
  }
}
