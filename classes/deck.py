import json, random
from pprint import pprint   

def loadCardsData(path):    
    with open(path) as f:
        data = json.load(f)
    return list(data['path-cards'])

class Deck:

    def __init__(self, path):
        self.data = loadCardsData(path)

    def getData(self):
        return self.data

    def shffule(self):
        random.shuffle(self.data)

    def remove(self,card):
        self.data.remove(card)

    def draw(self):
        return self.data.pop()
    
    def cards_remaining(self):
        return len(self.data)

def fuTest():
    testDeck = Deck('paths.json')
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