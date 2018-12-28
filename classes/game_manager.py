from classes.player import Player

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
        #deal roles and cards
        #set up map and player divs
        self.current_player = 0
        self.state = 'wait_for_move'    
        self.handle_move() #test only    

    def handle_move(self):
        #handle move logic
        round_over = True #placeholder
        if round_over:
            self.state = 'round_over'
        else:
            self.current_player += 1 
            self.current_player %= len(self.players)
            self.state = 'wait_for_move'
        print(self.state)
    
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