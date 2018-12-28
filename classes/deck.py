import json, random
from pprint import pprint   

def load_cards_data(path):    
    with open(path) as f:
        data = list(json.load(f)['path-cards'])
    return data

class Card:

    def __init__(self, name, edges):
        self.name = name
        self.connections = {-2: [], -1: [], 1: [], 2: []}
        for edge in edges:
            if edge[0] < 3:
                self.connections[edge[0]].append(edge[1])
            if edge[1] < 3:
                self.connections[edge[1]].append(edge[0])

    def rotate(self):
        c = self.connections
        (c[-2], c[2]) = (c[2], c[-2])
        (c[-1], c[1]) = (c[1], c[-1])
            

class Deck:

    def __init__(self, path):
        cards = load_cards_data(path)
        self.cards = []
        for card in cards:
            self.cards.append(Card(card['name'], card['edges']))

    def getData(self):
        return self.cards

    def shffule(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()
    
    def cards_remaining(self):
        return len(self.cards)

def fuTest():
    testDeck = Deck('paths.json')
    testDeck.shffule()
    pprint(testDeck.getData())
    print(testDeck.cards_remaining())
    testDeck.draw()
    testDeck.draw()
    testDeck.draw()
    print(testDeck.cards_remaining())
    pprint(testDeck.getData())

#fuTest()