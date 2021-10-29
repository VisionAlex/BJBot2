from threading import Lock, Thread
from enum import Enum
from time import sleep
from cards import BUST_CARDS
from strategy import strategy

import pyautogui

STRATEGY = strategy.get_strategy()

def get_decision(dealer_card, player_cards):
    if not dealer_card or not player_cards:
        return None
    if player_cards in BUST_CARDS:
        return None 
    return STRATEGY[player_cards][dealer_card]

class HandState(Enum):
    INITIAL = 0
    NEW_HAND = 2
    DEALT_CARDS = 2
    MORE_THAN_TWO = 3
    SPLIT_HAND = 4
    FINISHED = 5

class Bot:
    stopped = True
    lock = None

    state = HandState.INITIAL
    repariere = None
    player_cards = None
    dealer_card = None
    actions = {
        "H": None,
        "S": None,
        "D": None,
        "P": None,
    }


    def __init__(self):
        self.lock = Lock()
    
    def update_repariere(self, repariere):
        self.lock.acquire()
        self.repariere = repariere
        self.lock.release()
    
    def update_dealer_card(self, dealer_card):
        self.lock.acquire()
        self.dealer_card = dealer_card
        self.lock.release()
    
    def update_player_cards(self, player_cards):
        self.lock.acquire()
        self.player_cards = player_cards
        self.lock.release()
    
    def update_actions(self, actions):
        self.lock.acquire()
        self.actions = actions
        self.lock.release()
    
    def press_button(self,action):
        if action in self.actions:
            if self.actions[action]:
                pyautogui.moveTo(*self.actions[action])
                pyautogui.click(*self.actions[action])



    def start(self):
        self.stopped = False
        t1 = Thread(target=self.run)
        t1.start()
    
    def stop(self):
        self.stopped = True
    
    def run(self):
        while not self.stopped:
                if self.repariere is not None:
                    pyautogui.moveTo(*self.repariere)
                    pyautogui.click(*self.repariere)
                    self.state = HandState.NEW_HAND
                    sleep(2)
                
                if self.player_cards and self.dealer_card and self.actions['H'] is not None:
                    self.state = HandState.DEALT_CARDS

                if self.state == HandState.DEALT_CARDS:
                    decision = get_decision(self.dealer_card,self.player_cards)
                    if decision:
                        print(f"{self.player_cards} vs {self.dealer_card}: {decision}")
                        if decision == "S":
                            self.press_button(decision)
                            self.state = HandState.FINISHED
                        elif decision == "H":
                            self.press_button(decision)
                            self.state = HandState.MORE_THAN_TWO
                        elif decision == "D":
                            if self.actions['D'] is not None:
                                self.press_button(decision)
                                self.state = HandState.FINISHED
                            else:
                                self.press_button("H")
                                self.state = HandState.MORE_THAN_TWO
                        elif decision == "Ds":
                            if self.actions['D'] is not None:
                                self.press_button(decision)
                            else:
                                self.press_button("S")
                            self.state = HandState.FINISHED
                        elif decision == "P":
                            self.state = HandState.SPLIT_HAND
                            self.press_button("P")
                            sleep(1)
                        sleep(1)
                    else:
                        print(f" No hand: {self.player_cards} vs {self.dealer_card}")
                
                if self.state == HandState.MORE_THAN_TWO:
                    if self.player_cards in ["22Bust", "23", "24", "25", "26"]:
                        self.state = HandState.FINISHED
                    else:
                        decision = get_decision(self.dealer_card,self.player_cards)
                        if decision:
                            if decision == "S":
                                self.press_button(decision)
                                self.state = HandState.FINISHED
                            elif decision == "H":
                                if self.dealer_card == "Ten" and self.player_cards == "16":
                                    self.press_button("S")
                                else:
                                    self.press_button(decision)
                            elif decision == "D":
                                    self.press_button("H")
                            elif decision == "Ds":
                                    self.press_button("S")
                                    self.state = HandState.FINISHED
                            
                        else:
                            print(f" No hand: {self.player_cards} vs {self.dealer_card}")
                        sleep(1)

                        

                
                if self.state == HandState.SPLIT_HAND:
                    pass
                
                if self.state == HandState.FINISHED:
                    if self.repariere is None:
                        continue
