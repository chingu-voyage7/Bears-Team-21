# Bears-Team-21
Multiplayer Board Game - Saboteur | Voyage-7 | https://chingu.io/

![Image description](https://cf.geekdo-images.com/itemrep/img/aoCM1KdOmd7w56bQr4JSKWdDpaE=/fit-in/246x300/pic3989824.jpg)

## Chingu-Voyage Project Idea

Develop a turn based board game, using JavaScript/socket.io for the front-end and Python/Flask for the back-end. The general idea it’s to build a Tile Game inspired by Saboteur. The web client interface should allow the users to join different rooms and join a Game, each game should allow a minimum of 2 players up to 10. Also there should be the option to play against Bots AI. 

⚠️ This Project is still a work in progress.

### Prerequisites

Project dependencies

```
Werkzeug==0.14.1
Flask_SocketIO==3.1.0
Flask==1.0.2
Flask_Login==0.4.1
```

### Installing

Clone this repository

```
$ git clone https://github.com/chingu-voyage7/Bears-Team-21.git
```

It is suggested to make a virtual environment:

```
$ virtualenv venv
$ . venv/bin/activate
```

Install dependencies 

```
(venv) $ pip install -r requirements.txt
```

Run the server app

```
(venv) $ python app.py
```

Browse on your local machine 

```
http://127.0.0.1:5000/ 
```

## About Saboteur

⚠️ This Project is still a work in progress, rules of the game might be changed and be updated accordingly.

### Goal

Get as many gold nuggets as possible during the three rounds of the game. In order to do so,
- if you are a gold digger, you must, in association with other gold diggers, build a path from the 'Start' card to the treasure card which can be found among the three 'End' cards
- if you are a saboteur, you must, in association with other saboteurs, prevent the gold diggers from getting to the treasure. 

Your role (gold digger or saboteur) will be randomly selected at the start of each round.

### Rules summary

On your turn, you must click on a card from your hand to select it, then play this card or discard it. You can also rotate a 'Path' card before playing it by clicking the 'rotate' arrow that appears above the card.

The cards are of several types:
- 'Path' card: you can play this card to extend the maze, provided it is compatible with the cards already in place. To do this, click the location where you want to put the card.
- 'Sabotage' card: you can break another player's tool of the type indicated. To do this, click the corresponding tool in the target player's panel (under the score). A player with a broken tool cannot play a Path card.
- 'Repair' card: you can repair your, or another player's, broken tool of the type indicated. To do this, click the corresponding tool in the target player's panel (under the score), or click on the 'Sabotage' card in front of you.
- 'Map' card: you can play this card on any 'End' card to discover whether or not the treasure lies there (you alone will get the information, other players will see nothing). Just click on the 'End' card that you want to know. Then click on "I have seen it" button at the top.
- 'Rock fall' card: this card lets you remove any 'Path' card of the maze. Just click on the card you want to remove. 

### Cards in play

- 44 'Path' cards
- 9 'Sabotage' cards (three for each tool)
- 6 'Repair a tool' cards (two for each tool)
- 3 'Repair a tool among these two' cards (one for each combination of two tools)
- 5 'Map' cards (one less than in the box set, as requested by the game author)
- 3 'Rock fall' cards
- 28 'Gold' cards
- 16 with one gold nugget
- 8 with two gold nuggets
- 4 with three gold nuggets 
 
### Roles

Roles are randomly selected among a set that depends upon the number of players:
- with 3 players: 1 saboteur and 3 gold diggers
- with 4 players: 1 saboteur and 4 gold diggers
- with 5 players: 2 saboteurs and 4 gold diggers
- with 6 players: 2 saboteurs and 5 gold diggers
- with 7 players: 3 saboteurs and 5 gold diggers
- with 8 players: 3 saboteurs and 6 gold diggers
- with 9 players: 3 saboteurs and 7 gold diggers
- with 10 players: 4 saboteurs and 7 gold diggers 

## Built With

* [Flask](http://flask.pocoo.org/docs/1.0/) - The web framework used
* [Socket.IO](https://socket.io/docs/) - Library for browser and server communication

## Authors

* **[rektix](https://github.com/rektix)**
* **[Ventrosky](https://github.com/Ventrosky)**

See also the list of [contributors](https://github.com/chingu-voyage7/Bears-Team-21/graphs/contributors) who participated in this project.

## License

This project is licensed under the GNU GPLv3 - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* The original [Saboteur](https://boardgamegeek.com/boardgame/9220/saboteur)
* Inspiration [Board Game Arena](https://en.boardgamearena.com)
