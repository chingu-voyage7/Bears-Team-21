class Player():
    def __init__(self, name):
        self.name = name
        self.tools = {'pickaxe': True,
                      'light': True,
                      'cart': True}
        self.cards = []
        self.role = ''
        self.gold = 0
        self.free = True
        self.steal = False
        self.sid = ""

    def __gt__(self, other):
        return self.gold > other.gold

    def set_sid(self, sid):
        self.sid = sid

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

    def imprison(self):
        self.free = False

    def release(self):
        self.free = True

    def is_ready(self):
        if not self.free: 
            return False
        for tool in self.tools:
            if not self.tools[tool]:
                return False
        return True

    def reset(self):
        self.tools = {'pickaxe': True,
                      'light': True,
                      'cart': True}
        self.cards = []
        self.role = ''
        self.free = True
        self.steal = False