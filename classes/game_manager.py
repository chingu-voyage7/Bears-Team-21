from .player import Player
from .deck import Deck, ActionCard, DoorCard, PathCard, RoleCard, ToolCard
from .board import Board

class GameManager():
    def __init__(self,room,player_list):
        self.room = room
        self.prev_state = ''
        self.state = 'start_game'
        self.players = [Player(name) for name in player_list]
        self.start_game() #testing
        self.start_round()    
        #self.state_listener()

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
        self.deck = Deck('classes\paths.json','path-cards')
        self.deck.concat(Deck('classes\paths.json', 'action-cards'))
        self.roles = Deck('classes\paths.json', 'role-cards')
        self.deck.shuffle()
        self.roles.shuffle()
        #deal roles and cards
        for player in self.players:
            player.set_role(self.roles.draw().type)
        remove_cards = 10
        for i in range(remove_cards):
            self.deck.draw()
        self.cards_in_play = len(self.deck.cards)
        start_cards = 6        
        for i in range(start_cards):
            for player in self.players:
                player.draw_card(self.deck.draw())
        #set up map and player divs
        self.board = Board()
        self.current_player = 0
        self.state = 'wait_for_move'    
        #self.handle_move() #test only    

    def handle_move(self, card, x=None, y=None, target=None):
        #handle move logic
        result = False # could be used positive or negative outcome of move
        print("handle move logic",card,x,y,target)
        player = self.players[self.current_player]
        if isinstance(card, list):
            if len(card) == 2 and target is not None:
                if target == "trapped":
                    player.release()
                else:
                    self.discard_repair(player, card, target)
            else:
                print ("discard(",card,")")
                self.discard(player, card)
        else:
            card_obj = player.cards[card] 
            if isinstance(card_obj, (PathCard, DoorCard)):
                self.path_played(player, 
                card, x, y)
            elif isinstance(card_obj, (ActionCard, ToolCard)):
                result = self.action_played(player, 
                card, target)
        round_over = self.board.check_end() or self.cards_in_play == 0
        if round_over:
            self.state = 'round_over'
        else:
            self.current_player += 1 
            self.current_player %= len(self.players)
            self.state = 'wait_for_move'
        print(self.state)
        return result
    
    def discard(self, player, cards):
        for card in sorted(cards, reverse=True):
            player.play_card(card)
            self.cards_in_play -= 1
        for card in cards:
            if len(self.deck.cards): 
                player.draw_card(self.deck.draw())

    def discard_repair(self, player, cards, tool):
        for card in cards:
            player.play_card(card)
            self.cards_in_play -= 1
        if len(self.deck.cards): # only draw 1 card, effectively reduce hand
            player.draw_card(self.deck.draw())
        print(tool)
        player.repair_tool(tool)   

    def path_played(self, player, card, x, y):
        if player.is_ready():
            card = player.play_card(card)
            self.cards_in_play -= 1
            if len(self.deck.cards):
                player.draw_card(self.deck.draw())
            return self.board.add_card_check(card, x, y)

    def action_played(self, player, card, target=None):        
        card = player.play_card(card)
        self.cards_in_play -= 1
        print("action card",card.type)
        if card.type == 'reveal': #show goal card
            #emit signal for showing the goal card
            print("action_reveal",target)
            return self.board.getRevealCard(target[0],target[1])

        elif card.type == 'remove':
            target_card = self.board.board[target[0]][target[1]]
            if isinstance(target_card, (PathCard, DoorCard)):
                self.board.remove_card(target[0], target[1])

        elif card.type == 'repair':
            t_player = self.players[target]            
            for tool in card.tools:
                t_player.repair_tool(tool)                

        elif card.type == 'damage':
            t_player = self.players[target]           
            for tool in card.tools:
                t_player.break_tool(tool)                

        elif card.type == 'theft':
            player.steal = True

        elif card.type == 'handsoff':
            t_player = self.players[target]
            target.steal = False

        elif card.type == 'swaphats':
            #change role
            player.set_role(self.roles.draw().type)

        elif card.type == 'trapped':
            t_player = self.players[target] 
            t_player.imprison()

        elif card.type == 'swaphand': #modify this to ID
            t_player = self.players[target] 
            (player.cards, t_player.cards) = (t_player.cards, player.cards)
            #other draws card

        elif card.type == 'inspection':
            #show player role card
            t_player = self.players[target] 
            return t_player.role

        elif card.type == 'free':
            t_player = self.players[target]
            t_player.release()   

        if len(self.deck.cards):
                player.draw_card(self.deck.draw())
        return True #placeholder

    def round_over(self):
        #split winnings
        self.board.reset_visited()
        self.board.find_available_spots(self.board.start_x, 
        self.board.start_y, 6, door='blue')
        blue_connected = self.board.check_end()

        self.board.reset_visited()
        self.board.find_available_spots(self.board.start_x, 
        self.board.start_y, 6, door='green')
        green_connected = self.board.check_end()

        last_player = self.players[self.current_player].role
        #blue won
        if last_player in ['bluedigger', 'theboss', 'geologist', 'profiteer']:
            blue_won = blue_connected
        elif last_player == 'greendigger':
            blue_won = not green_connected
        #green won
        if last_player in ['greendigger', 'theboss', 'geologist', 'profiteer']:
            green_won = green_connected
        elif last_player == 'bluedigger':
            green_won = not blue_connected

        boss_won = blue_won or green_won
        saboteur_won = not boss_won
        geologist_gold = self.board.crystal_count

        winners_count = 0
        for player in self.players:
            if player.role == 'bluedigger':
                winners_count += blue_won
            elif player.role == 'greendigger':
                winners_count += green_won
            elif player.role == 'theboss':
                winners_count += boss_won
            elif player.role == 'profiteer':
                winners_count += 1
            elif player.role == 'saboteur':
                winners_count += saboteur_won

        winnings = 6 - winners_count
        if winnings < 1:
            winnings = 1
        
        for player in self.players:
            if player.role == 'bluedigger' and blue_won:
                player.receive_gold(winnings)
            elif player.role == 'greendigger' and green_won:
                player.receive_gold(winnings)
            elif player.role == 'theboss' and boss_won:
                player.receive_gold(winnings - 1)
            elif player.role == 'profiteer':
                player.receive_gold(winnings - 2)
            elif player.role == 'saboteur':
                player.receive_gold(winnings)
            elif player.role == 'geologist':
                player.receive_gold(geologist_gold)

        for player in self.players:
            player.reset()
        self.rounds += 1
        if self.rounds == 3:
            self.state = 'game_over'
        else:
            self.state = 'start_round'
        print(self.state)
    
    def game_over(self):
        winners = []
        max_gold = max(self.players).gold
        for player in self.players:
            if player.gold == max_gold:
                winners.append(player)
        print('winners =', winners)
        #show buttons
        print(self.state)

    def players_list(self):
        listPlayers = []
        for player in self.players:
            listPlayers.append(player.name)
        return listPlayers
    
    def player_hand_list(self, name):
        cardsList = []
        for player in self.players:
            if player.name == name:
                for card in player.cards:
                    cardsList.append(card.__dict__)
        return cardsList
    
    def get_player_role(self, name):
        for player in self.players:
            if player.name == name:
                return player.role
        return ""