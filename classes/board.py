from .deck import Deck, Card
from .settings import *
import math

def set_direction(direction):
    if direction == -1:#-2
        return (0,-1)
    if direction == 2:#-1
        return (-1,0)
    if direction == 1:#1
        return (0,1)
    if direction == -2:#-2
        return (1,0)

dim = 19

class Board:
    start_x = 5
    start_y = 9    
    crystal_count = 0
    #NUM_CELLS = dim * dim
    #PAD_NUM = '{0:0'+str(len(str(NUM_CELLS - 1)))+'d}' 
    #cells = []
    #startLabel = "104" #starts at 0

    def __init__(self):
        self.reset_visited()
        self.board = [[None for i in range(dim)] for i in range(dim)]
        self.available = []
        self.stairs = []
        self.place_initial_cards()
        self.crystal_count = 0

    def reset_visited(self):
        visit = {-2: False, -1: False, 1: False, 2: False, 6: False}
        self.visited = [[dict(visit) for i in range(dim)] for i in range(dim)]

    def place_initial_cards(self):
        setup_deck = Deck('classes/paths.json','setup-cards')
        card = setup_deck.draw()
        self.add_card(card, self.start_x, self.start_y)        
        setup_deck.shuffle()        
        goals = [[self.start_x + 2, self.start_y + 8],
                 [self.start_x - 2, self.start_y + 8],
                 [self.start_x, self.start_y + 8]]
        for coords in goals:
            card = setup_deck.draw()
            if card.name == 'goal-00':
                self.goal_coords = [coords[0], coords[1]] 
            self.add_card(card, coords[0], coords[1])    

    def remove_card(self, x, y):
        self.crystal_count -= self.board[x][y].crystal
        print(self.board[x][y])
        self.board[x][y] = None
        self.available = []
        self.reset_visited()
        self.find_available_spots(self.start_x, self.start_y, 6)

    def add_card(self, card, x, y):
        print('card placed')
        self.crystal_count += card.crystal
        self.board[x][y] = card
        if card.has_stairs:
            self.stairs.append([x, y])
        if [x, y] in self.available:
            self.available.remove([x, y])
        if not card.name.startswith('goal'):
            self.available = []
            self.reset_visited()
            self.find_available_spots(self.start_x, self.start_y, 6)
            for stair in self.stairs:
                x = stair[0]
                y = stair[1]
                if True not in self.visited[x][y].values():
                    self.find_available_spots(x, y, 6)
        print(self.available)

    def mark_available(self, x, y):
        if [x, y] not in self.available:
            self.available.append([x, y])

    def add_card_check(self, card, x, y):
        if self.check_position(card, x, y):
            self.add_card(card, x, y)
            return True
        return False

    def check_position(self, card, x, y):
        print(self.available)
        print([x,y])
        if [x,y] in self.available:
            print("in available")
            return self.check_adjacent(x, y, card.required)
        return False

    def check_adjacent(self, x, y, required):
        for direction in [-2, -1, 1, 2]:
            (nx,ny) = set_direction(direction)
            nx += x
            ny += y
            other = self.board[nx][ny]            
            if other is not None:  
                print("other coords", nx,ny)
                print("direction", direction)
                print("other",other.required)
                print(other.name)
                print("this", required)              
                if (-direction in other.required) != (direction in required):
                    return False
        return True

    def check_visited(self, x, y, direction):
        return self.visited[x][y][direction] 

    def find_available_spots(self, x, y, direction,
    px = None, py = None, door = None):       
        flag = True
        if door is not None and hasattr(self.board[x][y], door):
            flag = self.board[x][y].door == door
        if flag:
            if not self.check_visited(x, y, direction):
                self.visited[x][y][direction] = True            
                for d in self.board[x][y].connections[direction]:
                    if d < 4:
                        (nx,ny) = set_direction(d)                
                        nx += x
                        ny += y
                        other = self.board[nx][ny]
                        if other is None:
                            self.mark_available(nx,ny)
                        else:
                            self.find_available_spots(nx, ny, -d, x, y, door)

    def check_end(self):
        coords = self.goal_coords
        return True in self.visited[coords[0]][coords[1]].values()
    
    def getBoardData(self):
        cell = 0
        data = {}
        for row in self.board:
            for col in row:
                cell +=1
                if (col is not None):
                    if(col.name.startswith( 'goal' )):
                        data[str(cell)]= "goal-back" if(True not in self.visited[cell//dim][(cell-1) % dim].values()) else col.name 
                    else:
                        data[str(cell)]= col.name if not col.rotated else col.name+".rotate"
            cell += GRID_UI - len(row)
        return data
    
    def getRevealCard(self, x, y):
        print (self.goal_coords[0],":",self.goal_coords[1])
        return "gold" if (int(self.goal_coords[0]) ==  int(x)) and (int(self.goal_coords[1]) ==  int(y)) else "none"



####################################################################################


    #def find_path(self, start, end, path=[]):
    #    path = path + [start]
    #    if start == end:
    #        return path
    #    if start not in self.graph.vertices:
    #        return None
    #    for node in self.graph.vertices[start]:
    #        if node not in path:
    #            newpath = self.find_path(node, end, path)
    #            if newpath: return newpath
    #    return None
#
    #def cellAtNord(self, n): # check top edge
    #    return -1 if n < dim else n - dim
#
    #def cellAtSud(self, n): # check bottom edge
    #    return -1 if n > (self.NUM_CELLS - dim) else n + dim
#
    #def cellAtEast(self, n): # check right edge
    #    return -1 if n % dim == 0 else n + 1
#
    #def cellAtWest(self, n): # check left edge
    #    return -1 if ((n + 1) % dim == 0) else n - 1
#
    #def nToLabel(self, n):
    #    return self.PAD_NUM.format(n)
#
    #def coordToPos(self, x, y):
    #    n = y + dim * x #n = x + dim * y
    #    return self.nToLabel(n)
#
    #def posToCoord(self, label):
    #    i = int(label)
    #    x = i % dim
    #    y = i // dim
    #    return (x,y)
#
    #def addGraphCard(self, card, label): # add card no checks, previously done by other methods
    #    index = int(label)
    #    print(index)
    #    start = self.cells[index]
    #    coords = self.posToCoord(label)
    #    addedCard = self.board[coords[1]][coords[0]]
    #    print(addedCard.connections)
    #    if(len(addedCard.connections[-2]) > 0):
    #        #for conne in addedCard.connections.keys():
    #        #    addedCard.connections[conne]
    #        self.graph.add_edge(start,self.cells[self.cellAtSud(index)])
    #    if(len(addedCard.connections[2]) > 0):
    #        self.graph.add_edge(start,self.cells[self.cellAtNord(index)])
    #    if(len(addedCard.connections[-1]) > 0):
    #        self.graph.add_edge(start,self.cells[self.cellAtWest(index)])
    #    if(len(addedCard.connections[1]) > 0):
    #        self.graph.add_edge(start,self.cells[self.cellAtEast(index)])
    #    if(self.find_path(self.startLabel,label)):
    #        print("path-found")
    #        neighbours = self.nearCells(index, addedCard.connections)
    #        for node in neighbours:
    #            if self.board[node[1]][node[0]] is None:
    #                self.mark_available(node[1],node[0])
    #    print(str(self.graph.adjacencyList()))
#
    #def nearCells(self, index, connects):
    #    neighbours = []
    #    if(len(connects[-2]) > 0):
    #        neighbours.append(self.posToCoord(self.cells[self.cellAtSud(index)].name))
    #    if(len(connects[2]) > 0):
    #        neighbours.append(self.posToCoord(self.cells[self.cellAtNord(index)].name))
    #    if(len(connects[-1]) > 0):    
    #        neighbours.append(self.posToCoord(self.cells[self.cellAtWest(index)].name))
    #    if(len(connects[1]) > 0):
    #        neighbours.append(self.posToCoord(self.cells[self.cellAtEast(index)].name))
    #    return neighbours

####################################################################################
#def fuTestBoard():
    #testBoard = Board()
    #testDeck = Deck('classes/paths.json','path-cards')
    #card = testDeck.cards[0]
    #testBoard.add_card_check(card, 6, 10)
    #testBoard.add_card_check(card, 5, 11)
    #testDeck.shuffle()
    #card = testDeck.draw()

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