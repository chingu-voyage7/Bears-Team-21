from classes.deck import Deck, Card

import math

def set_direction(direction):
    if direction == -2:
        return (0,-1)
    if direction == -1:
        return (-1,0)
    if direction == 2:
        return (0,1)
    if direction == 1:
        return (1,0)

dim = 19

class Board:
    board = [[None for i in range(dim)] for i in range(dim)]
    start_x = 5
    start_y = 9

    def __init__(self):
        self.place_initial_cards()
        self.available = []

    def place_initial_cards(self):
        setup_deck = Deck('paths.json','setup-cards')        
        card = setup_deck.draw()
        self.add_card(card, self.start_x, self.start_y)
        card = setup_deck.draw()
        self.add_card(card, self.start_x + 2, self.start_y + 8)
        card = setup_deck.draw()
        self.add_card(card, self.start_x - 2, self.start_y + 8)
        card = setup_deck.draw()
        self.add_card(card, self.start_x, self.start_y + 8)

    def add_card(self, card, x, y):
        self.board[x][y] = card
        if [x, y] in self.available:
            self.available.remove([x, y])
        if not card.name.startswith('goal'):
            self.available = []
            self.find_available_spots(self.start_x, self.start_y, 1)
            self.find_available_spots(self.start_x, self.start_y, 2)

    def mark_available(self, x, y):        
        self.available.append([x, y])
    
    def add_card_check(self, card, x, y):
        if self.check_position(card, x, y):
            self.add_card(card, x, y)

    def check_position(self, card, x, y):
        if [x,y] in self.available:
            return self.check_adjacent(x, y, card.required)
        return False

    def check_adjacent(self, x, y, required):
        for direction in required:
            (nx,ny) = set_direction(direction)
            nx += x
            ny += y
            other = self.board[nx][ny]
            if not -direction in other.required:
                return False            
        return True

    def find_available_spots(self, x, y, direction):        
        for d in self.board[x][y].connections[direction]:
            (nx,ny) = set_direction(d)
            nx += x
            ny += y
            other = self.board[x][y-1]
            if other is None:
                self.mark_available(x,y-1)
            else:
                self.find_available_spots(nx,ny, -d)

###################################################################################
def fuTestBoard():
    testBoard = Board()
    testDeck = Deck('paths.json','path-cards')
    testDeck.shuffle()
    card = testDeck.draw()    

#fuTestBoard()

#001      ...          099
#[[0. 1. 1. ... 0. 0. 0.]
# [1. 0. 1. ... 0. 0. 0.]
# [1. 1. 0. ... 0. 0. 0.]
# ...
# [0. 0. 0. ... 0. 0. 0.]
# [0. 0. 0. ... 0. 0. 0.]
# [0. 0. 0. ... 0. 0. 0.]]
#899      ...          999
#a = Vertex('A')
#b = Vertex('B')
#c = Vertex('C')
#d = Vertex('D')
#e = Vertex('E')
#
#a.add_neighbors([b,c,e])
#b.add_neighbors([a,c])
#c.add_neighbors([b,d,a,e])
#d.add_neighbor(c)
#e.add_neighbors([a,c])
#
#g = Graph()
#print(graph(g))
#print()
#g.add_vertices([a,b,c,d,e])
#g.add_edge(b,d)
#print(graph(g))