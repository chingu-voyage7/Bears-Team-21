class Player():
    def __init__(self, name):
        self.name = name
        self.tools = {'pickaxe': True,
                      'lamp': True,
                      'cart': True}
        self.cards = []
        self.role = ''
        self.gold = 0

    def __gt__(self, other):
        return self.gold > other.gold

    def set_role(self, role):
        self.role = role

    def draw_card(self, card):
        self.cards.append(card)

    def play_card(self, index):
        return self.cards.pop(index)

    def break_tool(self, tool):
        self.tools[tool] = False

    def repair_tool(self, tool):
        self.tools[tool] = True

    def receive_gold(self, amount):
        if amount > 0:
            self.gold += amount

    def reset(self):
        self.tools = {'pickaxe': True,
                      'lamp': True,
                      'cart': True}
        self.cards = []
        self.role = ''
        