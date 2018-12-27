import json, random
from pprint import pprint   

def loadCardsData():
    data = []
    with open('data.json') as f:
        data = json.load(f)
    return data['path-cards']

class Deck:

    def __init__(self):
        self.data = loadCardsData()

    def getData(self):
        return self.data

    def shffule(self):
        random.shuffle(self.data)

    def remove(self,card):
        self.data.remove(card)
    
    def cardremaining(self):
        return self.data

def fuTest():
    testDeck = Deck()
    testDeck.shffule()
    pprint(testDeck.getData())
    testDeck.remove({'edges': [[0, 2]], 'name': 'path-01'})
    testDeck.remove({'edges': [[0, 1], [1, 3], [3, 0]], 'name': 'path-30'})
    testDeck.remove({'edges': [[0, 1], [1, 3], [3, 0]], 'name': 'path-31'})
    testDeck.remove({'edges': [[0, 1], [1, 3], [3, 0]], 'name': 'path-32'})
    testDeck.remove({'edges': [[0, 1], [1, 3], [3, 0]], 'name': 'path-33'})
    testDeck.remove({'edges': [[0, 1], [1, 3], [3, 0]], 'name': 'path-34'})
    pprint(testDeck.getData())

#fuTest()