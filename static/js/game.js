
var testData = {hand: ["path-01","path-02","path-03","path-19","path-20"], role:"path-03", 
board:{"203":"path-03","8":"path-02","208":"path-01","408":"path-01"}, 
players:["Game Opponent 1","Game Opponent 2","Game Opponent 3","Game Opponent 4"]};

function setUpGameUI(testData){

    testData.hand.forEach(function(name) {
        var cardNode = document.createElement("DIV");  
        cardNode.className= "card sprite " + name;
        document.getElementById("hand").appendChild(cardNode);
    });
    var roleNode = document.createElement("DIV"); 
    roleNode.className= "card sprite " + testData.role;
    document.getElementById("player-role").appendChild(roleNode);

    Object.keys(testData.board).forEach(function(key) {
        console.log(key, testData.board[key]);
        document.getElementById("square-"+key).className+=" sprite "+key;
    });

    testData.players.forEach(function(name) {
        var opponentNode = `<div class="col-sm-3">
        <div class="game-opponent well well-sm" style="min-height: 100px;">
            <div class="icon">
                 <i class="glyphicon glyphicon-user"></i>
            </div>
            <div class="text">
                <label class="text-muted">${name}</label>
            </div>
        </div>
        </div>`;
        
        document.getElementById("opponents").innerHTML += (opponentNode);
    });
}

window.onload = function() {
    var squarewidth = 120; 
    var squareheight= 195; 
    var divMain = document.getElementById('grid');
    var size = 100;
    var count = 0;
    for (var j = 0; j < size; j++) {
        for (var i = 0; i < size; i++) {
            var sqr = document.createElement('div'), 
            coord = {"x":i,"y":j} 
            sqr.className = 'square'; 
            count++;
            sqr.id ="square-"+count;
            sqr.style.width = squarewidth + 'px'; 
            sqr.style.height = squareheight + 'px'; 
            sqr.style.left = (coord.x * squarewidth) + 'px'; 
            sqr.style.top = (coord.y * squareheight) + 'px';
            sqr.addEventListener('click', function(evt) { 
                console.log(this); 
            }); 
            divMain.appendChild(sqr); 
        }
    }
    setUpGameUI(testData);
};