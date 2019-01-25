import json, random
from pprint import pprint   

def load_cards_data(path, name_set):    
    with open(path) as f:
        data = list(json.load(f)[name_set])
    return data

class Card:

    def __init__(self, name, tooltip):
        self.name = name
        self.rotated = False
        self.tooltip = tooltip
    def rotate(self):
        self.rotated = not self.rotated
        
class PathCard(Card):

    def __init__(self, name, tooltip, edges, crystal):
        super().__init__(name, tooltip)
        self.has_stairs = False
        self.connections = {-2: [], -1: [], 1: [], 2: [], 6:[]}
        self.edges = edges
        for edge in edges:
            if edge[0] < 3:
                self.connections[edge[0]].append(edge[1])
            if edge[1] < 3:
                self.connections[edge[1]].append(edge[0])
            if edge[1] == 6:                
                self.has_stairs = True
                self.connections[6].append(edge[0])
        self.crystal = int(crystal)
        self.set_required()

    def rotate(self):
        super().rotate()
        c = self.connections
        (c[-2], c[2]) = (c[2], c[-2])
        (c[-1], c[1]) = (c[1], c[-1])
        for key, value in c.items():
            c[key] = list(map(self.rotateConnecs, c[key]))
        self.set_required()

    def rotateConnecs(self,n):
        return n*-1 if -2 <= n <= 2 else n

    def set_required(self):
        self.required = []
        for c in self.connections:
            if self.connections[c] and c != 6:
                self.required.append(c)
        print(self.required)
                
class DoorCard(PathCard):

    def __init__(self, name, tooltip, edges, door):
        super().__init__(name, tooltip, edges, False)
        self.door = door

class ActionCard(Card):

    def __init__(self, name, tooltip, type):
        super().__init__(name, tooltip)
        self.type = type

class ToolCard(ActionCard):

    def __init__(self, name, tooltip, type, tools):

        super().__init__(name, tooltip, type)
        self.tools = tools

class RoleCard(Card):

    def __init__(self, name, tooltip, type):

        super().__init__(name, tooltip)
        self.type = type

class Deck:

    def __init__(self, path, name_set):
        cards = load_cards_data(path, name_set)
        self.cards = []
        for card in cards:
            name = card['name']    
            tooltip = card['tooltip']        
            if name.startswith('path') or name.startswith('goal'):                
                edges = card['edges']
                door = ['path-49','path-50','path-51',
                        'path-52','path-53','path-54'] 
                if name in door: 
                    self.cards.append(DoorCard(name, tooltip, edges, card['door']))
                else:
                    crystal = 'crystal' in card
                    self.cards.append(PathCard(name, tooltip, edges, crystal))
            if name.startswith('action'):
                type = card['type']
                if 'tools' in card:
                    self.cards.append(ToolCard(name, tooltip, type, card['tools']))
                else:
                    self.cards.append(ActionCard(name, tooltip, type))
            if name.startswith('role'):
                self.cards.append(RoleCard(name, tooltip, card['type']))

    def getData(self):
        return self.cards

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()
    
    def cards_remaining(self):
        return len(self.cards)

    def concat(self, other):
        self.cards += other.cards

#def fuTest():
#    testDeck = Deck('paths.json','path-cards')
#    testDeck.shuffle()
#    pprint(testDeck.getData())
#    print(testDeck.cards_remaining())
#    testDeck.draw()
#    testDeck.draw()
#    testDeck.draw()
#    print(testDeck.cards_remaining())
#    pprint(testDeck.getData())

#fuTest()