from .player import Player
from .deck import Deck, ActionCard, DoorCard, PathCard, RoleCard, ToolCard
from .board import Board
from .utility import sub_one
from threading import Thread, Event
from .timer_thread import TimerThread
import time

class GameManager():
    timerThread = None
    
    def __init__(self,room,player_list):
        self.room = room
        self.prev_state = ''
        self.state = 'start_game'
        self.players = [Player(name) for name in player_list]
        self.start_game() #testing
        self.start_round()    
        self.round_scores = {}
        self.winners = []
        self.log_message = 'Starting Game!'
        #self.state_listener()

    def state_listener(self):
        #while True:          
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
        self.round_scores = {}
        print('move to start_round')
        self.state = 'start_round'
        
    def start_round(self):
        self.log_message = 'Round started!'
        #create decks
        if self.timerThread is not None:
            self.timerThread.resume()
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

    def handle_move(self, card, x=None, y=None, target=None, timeOut = False):
        #handle move logic
        result = False # could be used positive or negative outcome of move
        print("handle move logic",card,x,y,target)
        player = self.players[self.current_player]
        try:
            if isinstance(card, list):
                if len(card) == 2:
                    if not player.free:
                        self.discard_release(player, card)                 
                    else:
                        self.discard_repair(player, card, target)
                else:
                    print ("discard(",card,")")
                    self.discard(player, card)
                self.log_message = player.name + " discards cards"
                result = True
            else:
                card_obj = player.cards[card] 
                if isinstance(card_obj, (PathCard, DoorCard)):
                    result = self.path_played(player, 
                    card, x, y)
                elif isinstance(card_obj, (ActionCard, ToolCard)):
                    result = self.action_played(player, 
                    card, target)
            if result:
                if not timeOut:
                    self.timerThread.pause()
                round_over = self.board.check_end() or self.cards_in_play == 0        
                if round_over:
                    self.state = 'round_over'
                else:
                    self.current_player += 1 
                    self.current_player %= len(self.players)
                    self.state = 'wait_for_move'
                    print("set event")
                    if not timeOut:
                        self.timerThread.resume()
                print(self.state)   
            return result  
        except Exception as exception:
            print(exception)
            return False    
        
    
    def discard(self, player, cards):
        for card in sorted(cards, reverse=True):
            player.play_card(card)
            self.cards_in_play -= 1
        for card in cards:
            if len(self.deck.cards): 
                player.draw_card(self.deck.draw())

    def discard_repair(self, player, cards, tool):
        for card in sorted(cards, reverse=True):
            player.play_card(card)
            self.cards_in_play -= 1
        if len(self.deck.cards): # only draw 1 card, effectively reduce hand
            player.draw_card(self.deck.draw())
        for tool, status in player.tools.items():
            if not status:
                player.repair_tool(tool)
                return True  #try repair a tool 
        if len(self.deck.cards): # draw second card since nothing repaired
            player.draw_card(self.deck.draw())
        return False

    def discard_release(self, player, cards):
        for card in sorted(cards, reverse=True):
            player.play_card(card)
            self.cards_in_play -= 1
        player.release() 
        if len(self.deck.cards): 
            player.draw_card(self.deck.draw())  

    def path_played(self, player, card, x, y):
        print ("path_played(",x,y,")")
        if player.is_ready():
            print("ready")
            if self.board.add_card_check(player.cards[card], int(x), int(y)):
                print("check")
                card = player.play_card(card)
                self.cards_in_play -= 1
                if len(self.deck.cards):
                    player.draw_card(self.deck.draw())
                self.log_message = player.name + " plays a path card"
                return True
        return False

    def action_played(self, player, card, target=None):        
        card = player.play_card(card)
        self.cards_in_play -= 1
        if len(self.deck.cards):
                player.draw_card(self.deck.draw())
        print("action card",card.type)
        if card.type == 'reveal': #show goal card
            #emit signal for showing the goal card
            print("action_reveal",target)
            result = self.board.getRevealCard(target[0],target[1])
            print(result)
            self.log_message = player.name + " reveals a destination "
            return result

        elif card.type == 'remove':
            target_card = self.board.board[target[0]][target[1]]
            print("remove", target_card.name)
            if isinstance(target_card, (PathCard, DoorCard)):
                self.board.remove_card(target[0], target[1])
                self.log_message = player.name + " removes a 'Path Card'"
                return True
            return False

        elif card.type == 'repair':
            t_player = self.players[target]            
            for tool in card.tools:
                if not t_player.tools[tool]:
                    t_player.repair_tool(tool)  
                    self.log_message = player.name + " plays 'Repair' on " + tool +" tool"
                    return True              
        #either one of the tools shown, but not both. 
        elif card.type == 'damage':
            t_player = self.players[target]          
            for tool in card.tools:
                if t_player.tools[tool]:
                    t_player.break_tool(tool)    
                    self.log_message = player.name + " 'Break' on " + t_player.name +"'s "+ tool +"tool"
                    return True            

        elif card.type == 'theft':
            if player.free:
                player.steal = True
                self.log_message = player.name + " plays 'Theft' on self"

        elif card.type == 'handsoff':
            t_player = self.players[target]
            t_player.steal = False
            self.log_message = player.name + " plays 'Hands Off' on " + t_player.name

        elif card.type == 'swaphats':
            t_player = self.players[target]
            t_player.set_role(self.roles.draw().type)
            self.log_message = player.name + " plays 'Swap Your Hats' on " + t_player.name

        elif card.type == 'trapped':
            t_player = self.players[target] 
            t_player.imprison()
            self.log_message = player.name + " plays 'Trapped!' on " + t_player.name

        elif card.type == 'swaphand': #modify this to ID
            if not self.current_player == target:
                t_player = self.players[target] 
                (player.cards, t_player.cards) = (t_player.cards, player.cards)
                t_player.draw_card(self.deck.draw())
                self.log_message = player.name + " plays 'Swap Your Hats' on " + t_player.name

        elif card.type == 'inspection':
            #show player role card
            t_player = self.players[target]
            print(t_player.role) 
            self.log_message = player.name + " plays 'Inspection' on " + t_player.name
            return t_player.role

        elif card.type == 'free':
            t_player = self.players[target]
            t_player.release()   
            self.log_message = player.name + " plays 'Free at last!' on " + t_player.name
            
        return True #placeholder

    def round_over(self):
        #split winnings
        # If there is a path with a blue and green door, 
        # the boss is the only player who can win through this path
        boss_won = self.board.check_end()
        
        self.board.reset_visited()
        self.board.find_available_spots(self.board.start_x, 
        self.board.start_y, 6, door='blue')
        blue_connected = self.board.check_end()

        self.board.reset_visited()
        self.board.find_available_spots(self.board.start_x, 
        self.board.start_y, 6, door='green')
        green_connected = self.board.check_end()

        last_player = self.players[self.current_player].role
        blue_won = False
        green_won = False
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

        #boss_won = blue_won or green_won #boss wins if there's a path, even if no gold-diggers receive gold
        saboteur_won = not boss_won
        geologist_gold = self.board.crystal_count

        winners_count = 0
        for player in self.players:
            if player.role == 'bluedigger':
                winners_count += int(blue_won)
            elif player.role == 'greendigger':
                winners_count += int(green_won)
            elif player.role == 'theboss':
                winners_count += int(boss_won)
            elif player.role == 'profiteer':
                winners_count += 1
            elif player.role == 'saboteur':
                winners_count += int(saboteur_won)

        winnings = sub_one(6,winners_count)

        self.round_scores = {}

        for player in self.players:
            if player.role == 'bluedigger' and blue_won:
                player.receive_gold(winnings)
                self.round_scores[player.name] = winnings
            elif player.role == 'greendigger' and green_won:
                player.receive_gold(winnings)
                self.round_scores[player.name] = winnings
            elif player.role == 'theboss' and boss_won:
                player.receive_gold(sub_one(winnings,1))
                self.round_scores[player.name] = sub_one(winnings,1)
            elif player.role == 'profiteer':
                player.receive_gold(sub_one(winnings, 2))
                self.round_scores[player.name] = sub_one(winnings,2)
            elif player.role == 'saboteur':
                player.receive_gold(winnings)
                self.round_scores[player.name] = winnings
            elif player.role == 'geologist':
                player.receive_gold(geologist_gold)
                self.round_scores[player.name] = geologist_gold

        for player in sorted(self.players, key=self.get_gold):
            if player.free and player.steal: # from poorest steal to richest
                player.receive_gold(self.next_rich_player(player).lose_gold())

        for player in self.players:
            player.reset()
        self.rounds += 1
        if self.rounds == 3:
            self.state = 'game_over'
        else:
            self.state = 'start_round'
        print(self.state)
        self.log_message = "Round Scores: " + ', '.join(" %s: %s, " % tup for tup in sorted(self.round_scores.items(), key=lambda kv: kv[1], reverse = True))
        return(self.round_scores)
    
    def get_gold(self, player):
        return player.gold

    def next_rich_player(self, notMe):
        for player in sorted(self.players, key=self.get_gold, reverse = True):
            if player.name != notMe.name:
                return player
        return notMe

    def game_over(self):
        #self.timerThread.pause()
        self.winners = []
        max_gold = max(self.players).gold
        for player in self.players:
            if player.gold == max_gold:
                self.winners.append(player.name)
        print('winners =', self.winners)
        self.log_message = "Game Winners: " + ', '.join(self.winners)
        print(self.state)

    def players_list(self):
        listPlayers = {}
        for player in self.players:
            icons = []
            icons.append("pickaxe_on" if(player.tools['pickaxe']) else "pickaxe_off")
            icons.append("light_on" if(player.tools['light']) else "light_off")
            icons.append("cart_on" if(player.tools['cart']) else "cart_off")
            icons.append("trapped_on" if(player.free) else "trapped_off")
            icons.append("theft_on" if(player.steal) else "theft_off")
            icons.append("Gold Nudgets:  " + str(player.gold))
            icons.append("Cards in Hand: " + str(len(player.cards)))
            listPlayers[player.name] = icons
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
        
    def player_rotate_card(self, name, card):
        for player in self.players:
            if player.name == name:
                print(name,"rotates",card)
                return player.cards[card].rotate()
        return ""

    def set_player_sid(self, name, sid):
        for player in self.players:
            if player.name == name:
                print(name,"->",sid)
                player.disconnect = False
                return player.set_sid(sid)
        return ""
    
    def get_current_player(self):
        turn_pl = self.players[self.current_player]
        return [turn_pl.sid, turn_pl.name]

    def player_disconnected(self, name):
        for player in self.players:
            if player.name == name:
                player.disconnect = True
                return True
        return False