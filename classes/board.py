from .deck import Deck, Card

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
    start_x = 5
    start_y = 9    

    def __init__(self):
        self.visited = [[False for i in range(dim)] for i in range(dim)]
        self.board = [[None for i in range(dim)] for i in range(dim)]
        self.available = []
        self.place_initial_cards()

    def place_initial_cards(self):
        setup_deck = Deck('classes/paths.json','setup-cards')
        card = setup_deck.draw()
        self.add_card(card, self.start_x, self.start_y + 8)
        card = setup_deck.draw()
        self.add_card(card, self.start_x + 2, self.start_y + 8)
        card = setup_deck.draw()
        self.add_card(card, self.start_x - 2, self.start_y + 8)
        card = setup_deck.draw()
        self.add_card(card, self.start_x, self.start_y)

    def remove_card(self, x, y):
        self.board[x][y] = None
        self.find_available_spots(self.start_x, self.start_y, 1)
        self.find_available_spots(self.start_x, self.start_y, 2)

    def add_card(self, card, x, y):
        print('card placed')
        self.board[x][y] = card
        if [x, y] in self.available:
            self.available.remove([x, y])
        if not card.name.startswith('goal'):
            self.available = []
            self.visited = [[False for i in range(dim)] for i in range(dim)]
            self.find_available_spots(self.start_x, self.start_y, 1)
            self.find_available_spots(self.start_x, self.start_y, 2)
        print(self.available)

    def mark_available(self, x, y):
        if [x, y] not in self.available:
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
            if other is not None:
                if not -direction in other.required:
                    return False
        return True

    def check_visited(self, x1, y1, x2, y2):
        if x2 is not None:
            return self.visited[x1][y1] and self.visited[x2][y2]
        return False

    def find_available_spots(self, x, y, direction, px = None, py = None):       
        if not self.check_visited(x, y, px, py):
            for d in self.board[x][y].connections[direction]:
                (nx,ny) = set_direction(d)
                nx += x
                ny += y
                other = self.board[nx][ny]
                if other is None:
                    self.mark_available(nx,ny)
                else:
                    self.find_available_spots(nx, ny, -d, x, y)
        self.visited[x][y] = True

###################################################################################
def fuTestBoard():
    testBoard = Board()
    testDeck = Deck('classes/paths.json','path-cards')
    card = testDeck.cards[0]
    testBoard.add_card_check(card, 6, 10)
    testBoard.add_card_check(card, 5, 11)
    #testDeck.shuffle()
    #card = testDeck.draw()

fuTestBoard()

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