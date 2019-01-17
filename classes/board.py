from .deck import Deck, Card
from .settings import *
from .graphUndirected import Graph, Vertex
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
    NUM_CELLS = dim * dim
    PAD_NUM = '{0:0'+str(len(str(NUM_CELLS - 1)))+'d}' 
    cells = {}
    startLabel = "104" #starts at 0
    OFFSET = {"N":0, "E":1,"S":2,"W":3, " " : 0}
    DIRECTIONS = dict([(2, "N"), (1, "E"),(-2, "S"), (-1, "W")])
    
    def __init__(self):
        self.reset_visited()
        self.board = [[None for i in range(dim)] for i in range(dim)]
        self.available = []
        self.stairs = []
        self.graph = Graph()
        print(self.cells)
        self.occupied = []
        self.graph.add_vertices(self.cells)
        self.place_initial_cards()
        self.crystal_count = 0

    def reset_visited(self):
        self.visited = [[False for i in range(dim)] for i in range(dim)]

    def place_initial_cards(self):
        setup_deck = Deck('classes/paths.json','setup-cards')
        card = setup_deck.draw()
        self.add_card(card, self.start_x, self.start_y)   
        self.addGraphCard(card, self.coordToPos(self.start_x,self.start_y))     
        setup_deck.shuffle()        
        self.goals = [[self.start_x + 2, self.start_y + 8],
                 [self.start_x - 2, self.start_y + 8],
                 [self.start_x, self.start_y + 8]]
        for coords in self.goals:
            card = setup_deck.draw()
            if card.name == 'goal-00':
                self.goal_coords = [coords[0], coords[1]] 
            self.add_card(card, coords[0], coords[1]) 
            self.addGraphCard(card, self.coordToPos( coords[0], coords[1]))       

    def remove_card(self, x, y):
        self.crystal_count -= self.board[x][y].crystal
        print(self.board[x][y])
        self.board[x][y] = None
        self.find_available_spots(self.start_x, self.start_y, 6)

    def add_card(self, card, x, y):
        print('card placed')
        self.crystal_count += card.crystal
        self.board[x][y] = card
        self.occupied.append(self.coordToPos(x,y))
        if card.has_stairs:
            self.stairs.append([x, y])
        if [x, y] in self.available:
            self.available.remove([x, y])
        if not card.name.startswith('goal'):
            #self.available = []
            #self.reset_visited()
            self.find_available_spots(self.start_x, self.start_y, 6)
            for stair in self.stairs:
                x = stair[0]
                y = stair[1]
                if not self.visited[x][y]:
                    self.find_available_spots(x, y, 6)
        print(self.available)

    def mark_available(self, x, y):
        if [x, y] not in self.available:
            self.available.append([x, y])

    def add_card_check(self, card, x, y):
        if self.check_position(card, x, y):
            self.add_card(card, x, y)
            for key, value in card.connections.items():
                if len(value) > 0:
                    self.find_available_spots(x, y, key)
            self.addGraphCard(card, self.coordToPos( x, y))  
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

    def check_visited(self, x1, y1, x2, y2):
        if x2 is not None:
            return self.visited[x1][y1] and self.visited[x2][y2]
        return False

    def find_available_spots(self, x, y, direction,
    px = None, py = None, door = None):       
        flag = True
        if door is not None and hasattr(self.board[x][y], door):
            flag = self.board[x][y].door == door
        if flag:
            if not self.check_visited(x, y, px, py):
                self.visited[x][y] = True            
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
        return self.visited[self.goal_coords[0]][self.goal_coords[1]]
    
    def getBoardData(self):
        cell = 0
        data = {}
        for row in self.board:
            for col in row:
                cell +=1
                if (col is not None):
                    if(col.name.startswith( 'goal' )):
                        # actually just need to check if someone connected to it, without all this
                        data[str(cell)]= "goal-back" if(self.brute_find_path(self.startLabel,self.nToLabel(cell)) is None) else col.name 
                    else:
                        data[str(cell)]= col.name if not col.rotated else col.name+".rotate"
            cell += GRID_UI - len(row) #and not self.destination_revealed(row,col)
        return data
    
    def getRevealCard(self, x, y):
        print (self.goal_coords[0],":",self.goal_coords[1])
        return "gold" if (int(self.goal_coords[0]) ==  int(x)) and (int(self.goal_coords[1]) ==  int(y)) else "none"

    def destination_revealed(self, x, y): #it's a goal and it's visited
        print(x,y)
        return any([a,b] == [x,y] for a,b in self.goals) and self.visited[x][y]
####################################################################################


    def find_path(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if start not in self.graph.vertices:
            return None
        if start[:-1] not in self.occupied:
            return None
        for node in self.graph.vertices[start]:
            if node not in path:
                newpath = self.find_path(node, end, path)
                if newpath: return newpath
        return None

    def brute_find_path(self, start, end):
        for keyStart in ["N","S","W","E"]:
            for keyEnd in ["N","S","W","E"]:
                path = self.find_path(start + keyStart, end + keyEnd)
                if path is not None:
                    return path
        return None
 
    def vertex_cell_at(self, direction, n):
        cellSwitcher = {
            "N": self.cellAtNord,
            "E": self.cellAtEast,
            "S": self.cellAtSouth,
            "W": self.cellAtWest,
            " ": lambda x: x
        }
        fu = cellSwitcher.get(direction, "nothing")
        return self.get_cell(fu(n) + self.OFFSET[direction])

    def cellAtNord(self, n): # check top edge
        n = int(n) // 4
        cell = -1 if n < dim else n - dim
        return cell * 4 # fix later, no time

    def cellAtSouth(self, n): # check bottom edge
        n = int(n) // 4
        cell = -1 if n > (self.NUM_CELLS - dim) else n + dim
        return cell * 4

    def cellAtEast(self, n): # check right edge
        n = int(n) // 4
        cell = -1 if n % dim == 0 else n + 1
        return cell * 4

    def cellAtWest(self, n): # check left edge
        n = int(n) // 4
        cell = -1 if ((n + 1) % dim == 0) else n - 1
        return cell * 4

    def nToLabel(self, n):
        return self.PAD_NUM.format(n)

    def coordToPos(self, x, y):
        n = y + dim * x #n = x + dim * y
        return self.nToLabel(n)

    def posToCoord(self, label):
        i = int(label)
        x = i % dim
        y = i // dim
        return (x,y)

    def addGraphCard(self, card, label): # add card no checks, previously done by other methods
        index = int(label)*4
        print(index) # 
        #start = self.get_cell(index)
        coords = self.posToCoord(label)
        addedCard = self.board[coords[1]][coords[0]]
        self.add_card_vertex(index)
        print(addedCard.connections)
        for key, archs in addedCard.connections.items():
            if key < 3: #taking out 5 and 6 temp
                for item in [a for a in archs if not a > 2]: # temporary test
                    inStart = self.get_cell(index + self.OFFSET[self.DIRECTIONS[key]])
                    inEnd = self.get_cell(index + self.OFFSET[self.DIRECTIONS[item]])
                    self.graph.add_edge(inStart, inEnd)
        if(len(addedCard.connections[-2]) > 0):# and addedCard.connections[-2] != [5]:
            self.graph.add_edge(self.get_cell(index+self.OFFSET["S"]),self.get_cell(self.cellAtSouth(index)+self.OFFSET["N"]))
            
        if(len(addedCard.connections[2]) > 0):
            self.graph.add_edge(self.get_cell(index+self.OFFSET["N"]),self.get_cell(self.cellAtNord(index)+self.OFFSET["S"]))

        if(len(addedCard.connections[-1]) > 0):
            self.graph.add_edge(self.get_cell(index+self.OFFSET["W"]),self.get_cell(self.cellAtWest(index)+self.OFFSET["E"]))

        if(len(addedCard.connections[1]) > 0):
            self.graph.add_edge(self.get_cell(index+self.OFFSET["E"]),self.get_cell(self.cellAtEast(index)+self.OFFSET["W"]))
        #if(self.brute_find_path(self.startLabel,label)):
        #    print("path-found")
        print(str(self.graph.adjacencyList()))

    def get_cell(self, index):
        if str(index) not in self.cells:
            self.add_card_vertex(index) 
            print(index)
        return self.cells[str(index)]

    def add_card_vertex(self, n):
        posLabel = self.nToLabel(n//4)
        if n in self.cells:
            return 
        idx1 =n + self.OFFSET["N"]
        idx2 =n + self.OFFSET["E"]
        idx3 =n + self.OFFSET["S"]
        idx4 =n + self.OFFSET["W"]
        self.cells.update({str(idx1): Vertex(posLabel+"N"), str(idx2): Vertex(posLabel+"E"),str(idx3): Vertex(posLabel+"S"),str(idx4):Vertex(posLabel+"W")})

###################################################################################
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