from classes.graphUndirected import Graph, Vertex

class Board:
    START_IDX = 500

    def __init__(self):
        self.cells = []
        self.graph = Graph()
        for n in range(0,1000):
            self.cells.append(Vertex(f'{n:03}'))
        self.graph.add_vertices(self.cells)
        self.initialEdges()
        print(self.graphPrint())
    
    def initialEdges(self):
        start = self.cells[self.START_IDX]
        self.graph.add_edge(start,self.cells[self.cellAtNord(self.START_IDX)])
        self.graph.add_edge(start,self.cells[self.cellAtSud(self.START_IDX)])
        self.graph.add_edge(start,self.cells[501])
        self.graph.add_edge(start,self.cells[499])
        return ""
     
    def graphPrint(self):
        #return(str(self.graph.adjacencyList()) + '\n' + '\n' + str(self.graph.adjacencyMatrix()))
        return(str(self.graph.adjacencyList()))
    
    def cellAtNord(self, n):
        return -1 if n < 100 else n-100

    def cellAtSud(self, n):
        return -1 if n > 900 else n+100

    def cellAtEast(self, n):
        return n # toDO
    def cellAtWest(self, n):
        return n # toDO
    
    def addCard(self, card):
        return "toDo"

testBoard = Board()                        

###################################################################################
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