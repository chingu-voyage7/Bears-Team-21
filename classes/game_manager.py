from .player import Player
from .deck import Deck, PathCard, DoorCard, ActionCard, ToolCard, RoleCard
from .board import Board

class GameManager():
    def __init__(self,room,player_list):
        self.room = room
        self.prev_state = ''
        self.state = 'start_game'
        self.players = [Player(name) for name in player_list]
        self.state_listener()

    def state_listener(self):
        while True:          
            if self.prev_state != self.state:
                self.prev_state = self.state
                print('checking')
                if self.state == 'start_game':
                    self.start_game()
                elif self.state == 'start_round':
                    self.start_round()                
                elif self.state == 'round_over':
                    self.round_over()
                elif self.state == 'game_over':
                    self.game_over()                                             

    def start_game(self):
        self.rounds = 0
        print('move to start_round')
        self.state = 'start_round'
        
    def start_round(self):
        print('round started')
        #create decks
        self.deck = Deck('paths.json','path-cards')
        self.deck.concat(Deck('paths.json', 'action-cards'))
        self.roles = Deck('paths.json', 'role-cards')
        self.deck.shuffle()
        self.roles.shuffle()
        #deal roles and cards
        #set up map and player divs
        self.board = Board()
        self.current_player = 0
        self.state = 'wait_for_move'    
        self.handle_move() #test only    

    def handle_move(self, card, x=None, y=None):
        #handle move logic
        if isinstance(card, (PathCard, DoorCard)):
            move_end = path_played(card, x, y)
        elif isinstance(card, (ActionCard, ToolCard))
            move_end = action_played(card)
        round_over = True #placeholder
        if move_end:
            if round_over:
                self.state = 'round_over'
            else:
                self.current_player += 1 
                self.current_player %= len(self.players)
                self.state = 'wait_for_move'
            print(self.state)
    
    def path_played(self, card, x, y):
        return self.board.add_card_check(card, x, y)

    def action_played(card, target):
        if card.type == 'reveal':
            pass
        elif card.type == 'remove':
            pass
        elif card.type == 'repair':
            if isinstance(target, Player):
                for tool in card.tools:
                    target.repair_tool(tool)
                return True
            return False
        elif card.type == 'damage':
            if isinstance(target, Player):
                for tool in card.tools:
                    target.break_tool(tool)
                return True
            return False
        elif card.type == 'theft':
            pass
        elif card.type == 'handsoff':
            pass
        elif card.type == 'swaphats':
            pass
        elif card.type == 'trapped':
            pass
        elif card.type == 'swaphand':
            pass
        elif card.type == 'inspection':
            pass
        elif card.type == 'free':
            pass
        elif card.type == 'remove':
            pass
        return True #placeholder

    def round_over(self):
        #split winnings
        for player in self.players:
            player.reset()
        self.rounds += 1
        if self.rounds == 3:
            self.state = 'game_over'
        else:
            self.state = 'start_round'
        print(self.state)
    
    def game_over(self):
        print('winner = srs')
        #show buttons
        print(self.state)