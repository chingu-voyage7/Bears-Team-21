import json, random
from pprint import pprint   
from pathlib import Path
import os

def load_cards_data(path, name_set):    
    mypath = os.getcwd()
    print(mypath)
    with open(mypath+'\\'+path) as f:
        data = list(json.load(f)[name_set])
    return data

class Card:

    def __init__(self, name):
        self.name = name
        
class PathCard(Card):

    def __init__(self, name, edges, crystal):
        super().__init__(name)
        self.connections = {-2: [], -1: [], 1: [], 2: []}
        self.edges = edges
        for edge in edges:
            if edge[0] < 3:
                self.connections[edge[0]].append(edge[1])
            if edge[1] < 3:
                self.connections[edge[1]].append(edge[0])
        self.crystal = int(crystal)
        self.set_required()

    def rotate(self):
        c = self.connections
        (c[-2], c[2]) = (c[2], c[-2])
        (c[-1], c[1]) = (c[1], c[-1])
        self.set_required()

    def set_required(self):
        self.required = []
        for c in self.connections:
            if self.connections[c]:
                self.required.append(c)
                
class DoorCard(PathCard):

    def __init__(self, name, edges, door):
        super().__init__(name, edges)
        self.door = door

class ActionCard(Card):

    def __init__(self, name, type):
        super().__init__(name)
        self.type = type

class ToolCard(ActionCard):

    def __init__(self, name, type, tools):

        super().__init__(name, type)
        self.tools = tools

class RoleCard(Card):

    def __init__(self, name, type):

        super().__init__(name)
        self.type = type

class Deck:

    def __init__(self, path, name_set):
        cards = load_cards_data(path, name_set)
        self.cards = []
        for card in cards:
            name = card['name']            
            if name.startswith('path') or name.startswith('goal'):                
                edges = card['edges']
                print(name,edges)
                door = ['path-49','path-50','path-51',
                        'path-52','path-53','path-54'] 
                if name in door: 
                    self.cards.append(DoorCard(name, edges, card['door']))
                else:
                    crystal = 'crystal' in card
                    self.cards.append(PathCard(name, edges, crystal))
            if name.startswith('action'):
                type = card['type']
                if 'tools' in card:
                    self.cards.append(ToolCard(name, type, card['tools']))
                else:
                    self.cards.append(ActionCard(name, type))
            if name.startswith('role'):
                self.cards.append(RoleCard(name, card['type']))

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