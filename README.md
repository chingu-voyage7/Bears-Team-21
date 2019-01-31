# Bears-Team-21
Multiplayer Board Game - Saboteur | Voyage-7 | https://chingu.io/

![Image description](https://cf.geekdo-images.com/itemrep/img/aoCM1KdOmd7w56bQr4JSKWdDpaE=/fit-in/246x300/pic3989824.jpg)

## Chingu-Voyage Project Idea

Develop a turn based board game, using JavaScript/socket.io for the front-end and Python/Flask for the back-end. The general idea it’s to build a Tile Game inspired by Saboteur, a game by **Frederic Moyersoen** published by [Amigo](https://www.amigo-spiele.de/). The web client interface should allow the users to join different rooms and join a Game, each game should allow a minimum of 2 players up to 10.


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

⚠️ This Project is an online multiplayer version of the board game Saboteur 2 published by **AMIGO**, built for educational purposes only. Rules of the game might have been  changed and be updated accordingly.

### Goal

Get as many gold nuggets as possible during the three rounds of the game. In order to do so,
- if you are a **Gold Digger** (*Green Team* or *Blue Team*), you must,  build a path from the **Start** card to the treasure card, among the three **End** cards.
- if you are **The Boss**, you win whenever the *Green or the Blue Team* wins, but always gets one Gold Piece less than them.
- if you are **The Profiteer**, you win when the gold-diggers (*Green or Blue*) win, and also when *The Saboteurs* win. However, two Gold Pieces less. 
- if you are **The Geologist** for each visible crystal, you receive 1 Gold Piece.
- if you are a **Saboteur**, you must, in association with other saboteurs, prevent the *gold diggers* from getting to the treasure. 

Your role will be randomly selected at the start of each round.

### Rules summary

On your turn, you must click on a card from your hand to select it, then play this card or discard it. You can also rotate a **Path** card before playing it by double clicking it.

The cards are of several types:
- **Path** card: you can play this card to extend the maze, provided it is compatible with the cards already in place.
- **Sabotage** card: you can break another player's tool of the type indicated. A player with a broken tool cannot play a Path card.
- **Repair** card: you can repair your, or another player's, broken tool of the type indicated.
- **Map** card: you can play this card on any **End** card to discover whether or not the treasure lies there. 
- **Rock fall** card: this card lets you remove any **Path** card of the maze. Just click on the card you want to remove. 
- **Inspection**: If you play this, you may look at the dwarf card of any one other player.
- **Swap Your Hand**: The player who plays this card chooses one other player and exchanges hands with them.
- **Theft**: You play this on yourself. At the end of the round, you will steal 1 Gold Piece from the player with most gold. You cannot use this card if you are trapped.
- **Hands Off**: If you play this card, you can remove one Theft card from in front of any player. 
- **Swap Your Hats**: Choose one player who has to discard their current Dwarf Card.
- **Trapped!** Play this on another player. This player is trapped and cannot play any more path cards. When the round ends, they don‘t get any treasure.
- **Free at last!**: If you play this card, remove the **Trapped!** status from any player. 

### Cards in play

- 70 **Path** cards
- 47 **Action** cards
- 15 **Role** cards
 
### The Dwarf Cards And Their Victory Conditions:

#### Blue and Green Gold-Diggers

Both teams try to tunnel their way towards the treasure, but they are in competition.
*A team wins* if:
* a dwarf from that team creates the connection to the treasure and the way there isn‘t blocked by a door of the other color
* a dwarf from the other team creates the connection to the treasure, but the way there for his or her own team is blocked by a door of the wrong color
* *Both teams win* (along with all other “non-Saboteurs”) if *The Boss*, *The Geologist* or *The Profiteer* creates the connection to the gold and the way there isn‘t blocked by a door of the other color.

#### The Boss

The Boss builds tunnels for both the *Green and the Blue Team* and wins if there's a path to the treasure. When the treasure is split, The Boss always gets one Gold
Piece less than the other winners.

#### The Profiteer

*The Profiteer* always wins, no matter if The Gold-Diggers or The Saboteurs are successful. However, when the treasure is divided, *The Profiteer* gets two fewer Gold Pieces than the others.

#### The Geologist

*The Geologist* dig at their own expense, so to speak. They aren‘t particularly interested in gold. When the treasure is split, a *Geologist* gets as many Gold Pieces as there are crystals visible in the maze of tunnels. If both *Geologists* are in play, they split the Gold Pieces (rounded down).

#### The Saboteur

*The saboteurs* have won the round if the goal card with the treasure wasn't reached.

## Playing the Game

When it is your turn, you have to take one of the four following actions:
* Place a path card in the tunnel maze.
* Play an action card.
* Discard two cards from your hand to remove a card in front of you.
* Pass and discard 1-3 face-down cards from your hand.

Then your turn is over and it‘s the next player‘s turn.

## Built With

* [Flask](http://flask.pocoo.org/docs/1.0/) - The web framework used
* [Socket.IO](https://socket.io/docs/) - Library for browser and server communication

## Authors

* **Salvatore Ventrone** - [Ventrosky](https://github.com/Ventrosky)
* **Mihajlo Krsmanović** - [rektix](https://github.com/rektix)

See also the list of [contributors](https://github.com/chingu-voyage7/Bears-Team-21/graphs/contributors) who participated in this project.

## License

This project is licensed under the GNU GPLv3 - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* The original [Saboteur](https://boardgamegeek.com/boardgame/9220/saboteur)
* Inspiration [Board Game Arena](https://en.boardgamearena.com)
* Game Designer: **Fréderic Moyersoen**
* Artists: **Andrea Boekhoff**, **Fréderic Moyersoen**
* Publisher: **AMIGO**
