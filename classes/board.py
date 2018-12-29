from graphUndirected import Graph, Vertex
from deck import Deck, Card

import math

class Board:
    DIMENSION = 10#100
    NUM_CELLS = DIMENSION * DIMENSION
    # node labels formatting
    PAD_NUM = '{0:0'+str(len(str(NUM_CELLS - 1)))+'d}' 
    # start card certer row & 1/4th column
    START_IDX = ((DIMENSION // 2) * DIMENSION) + math.floor(DIMENSION* 0.25)

    def __init__(self):
        self.occupated = {} # dict of cells occupated by cards
        self.cells = [] # all the Vertex references of the board
        self.graph = Graph()
        for n in range(0, self.NUM_CELLS):
            self.cells.append(Vertex(self.nToLabel(n)))
        self.graph.add_vertices(self.cells)
        self.initialEdges()
    
    def initialEdges(self):
        setupDeck = Deck('paths.json','setup-cards')
        GOAL_IDX_COL =  self.START_IDX + 7
        startCard = setupDeck.draw()
        self.addCard(startCard, self.nToLabel(GOAL_IDX_COL))
        startCard = setupDeck.draw() # testing randomly adding setup cards
        self.addCard(startCard, self.nToLabel(GOAL_IDX_COL - self.DIMENSION))
        startCard = setupDeck.draw()
        self.addCard(startCard, self.nToLabel(GOAL_IDX_COL + self.DIMENSION))
        startCard = setupDeck.draw()
        self.addCard(startCard, self.nToLabel(self.START_IDX))
        return ""

    
    def graphPrint(self):
        #return(str(self.graph.adjacencyList()) + '\n' + '\n' + str(self.graph.adjacencyMatrix()))
        return(str(self.graph.adjacencyList()))
    
    def cellAtNord(self, n):
        # check top edge
        return -1 if n < self.DIMENSION else n - self.DIMENSION

    def cellAtSud(self, n):
        # check bottom edge
        return -1 if n > (self.NUM_CELLS - self.DIMENSION) else n + self.DIMENSION

    def cellAtEast(self, n):
        # check right edge
        return -1 if n % self.DIMENSION == 0 else n + 1

    def cellAtWest(self, n):
        # check left edge
        return -1 if ((n + 1) % self.DIMENSION == 0) else n - 1
    
    def checkPosition(self, card, label):
        return True

    def addCard(self, card, label):
        # add card no checks
        self.occupated[label] = card.name
        index = int(label)
        start = self.cells[index]
        self.graph.add_edge(start,self.cells[self.cellAtSud(index)])
        self.graph.add_edge(start,self.cells[self.cellAtNord(index)])
        self.graph.add_edge(start,self.cells[self.cellAtWest(index)])
        self.graph.add_edge(start,self.cells[self.cellAtEast(index)])
        print (self.occupated)
        return "toDo"

    def nToLabel(self, n):
        return self.PAD_NUM.format(n)

    def findAdjacentNodes(self, card, label):
        for key in card.connections.keys:
            card.connections[key]#to-Do

    def find_path(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if start not in self.graph.vertices:
            return None
        for node in self.graph.vertices[start]:
            if node not in path:
                newpath = self.find_path(node, end, path)
                if newpath: return newpath
        return None

###################################################################################
def fuTestBoard():
    testBoard = Board()   
    testDeck = Deck('paths.json','path-cards')  
    testDeck.shuffle()
    card = testDeck.draw()
    testBoard.addCard(card,"16")                   
    print(testBoard.graphPrint())
    print(testBoard.graph.vertices)
    print(testBoard.find_path("52","53"))

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