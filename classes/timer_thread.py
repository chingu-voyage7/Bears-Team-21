from threading import Thread, Event
import threading
import time
import classes.settings as config

class TimerThread(Thread):

    def __init__(self, room, appCtx, sio, gm):
        self.appCtx = appCtx
        self.sio = sio
        self.room = room
        self.player = 0
        self.delay = config.TIMER_TURN
        self.number = 0
        self.can_run = Event()
        self.thing_done = Event()
        self.thing_done.set()
        self.can_run.set()   
        self.gm = gm
        super(TimerThread, self).__init__()

    def run(self):
        while True:
            self.can_run.wait()
            try:
                self.thing_done.clear()
                self.number += 1  #(0.1 sec)
                if self.number % (config.TIMER_TURN*10) == 0:    
                    with self.appCtx.app_context():
                        #self.sio.emit('time_out', {'number': self.number}, namespace=self.room)
                        self.number = 0
                        currentPl = self.gm.get_current_player()
                        self.gm.handle_move(card=[0], timeOut = True)
                        left = config.TIMER_TURN - (self.number//10)
                        self.sio.emit('seconds_left', {'number': left}, namespace=self.room) 
                        self.sio.emit("update_hand", self.gm.player_hand_list(currentPl[1]), namespace=self.room, room=currentPl[0])
                        self.gm.log_message = "Time Out Discard: "+currentPl[1]
                        self.sio.emit('game_message', {'message':self.gm.log_message}, namespace=self.room, broadcast=True)
                        self.sio.emit("wait_for_timer", {"active" : 0}, namespace=self.room, broadcast= True)
                elif self.number % 10 == 0:
                    with self.appCtx.app_context():
                        left = config.TIMER_TURN - (self.number//10)
                        self.sio.emit('seconds_left', {'number': left}, namespace=self.room)         
                time.sleep(0.1)
            finally:
                self.thing_done.set()

    def pause(self):
        self.can_run.clear()
        self.thing_done.wait()
        self.number = 0

    def resume(self):
        self.can_run.set()
    
