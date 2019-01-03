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
        for player in self.players:
            player.set_role(self.roles.draw().type)

        #set up map and player divs
        self.board = Board()
        self.current_player = 0
        self.state = 'wait_for_move'    
        #self.handle_move() #test only    

    def handle_move(self, player, card, x=None, y=None, target=None):
        #handle move logic
        if isinstance(card, (PathCard, DoorCard)):
            move_end = self.path_played(card, player, x, y)
        elif isinstance(card, (ActionCard, ToolCard)):
            move_end = self.action_played(player, card, target)
        round_over = True #placeholder
        if move_end:
            if round_over:
                self.state = 'round_over'
            else:
                self.current_player += 1 
                self.current_player %= len(self.players)
                self.state = 'wait_for_move'
            print(self.state)
    
    def path_played(self, player, card, x, y):
        if player.is_ready():
            return self.board.add_card_check(card, x, y)

    def action_played(self, player, card, target=None):
        if card.type == 'reveal': #show goal card
            #emit signal for showing the goal card
            pass

        elif card.type == 'remove':
            target_card = self.board.board[target[0]][target[1]]
            if isinstance(target_card, (PathCard, DoorCard)):
                self.board.remove_card(target[0], target[1])

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
            player.steal_count += 1

        elif card.type == 'handsoff':
            player.steal_count -= 1

        elif card.type == 'swaphats':
            #change role
            player = self.players[self.current_player]
            player.set_role(self.roles.draw().type)

        elif card.type == 'trapped':
            target.imprison()

        elif card.type == 'swaphand':
            (player.cards, target.cards) = (target.cards, player.cards)
            #other draws card

        elif card.type == 'inspection':
            #show player role card
            player = self.players[target]
            return player.role

        elif card.type == 'free':
            target.release()            

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