from threading import Lock, Thread
from enum import Enum
from time import sleep
from strategy import strategy

import pyautogui

STRATEGY = strategy.get_strategy()
INSURANCE = (361,591)

def get_decision(dealer_card, player_cards):
    if not dealer_card or not player_cards:
        return None
    if player_cards == "Bust":
        return None 
    return STRATEGY[player_cards][dealer_card]

class HandState(Enum):
    INITIAL = 0
    NEW_HAND = 1
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
    insurance = False
    previous_player_total = None

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
    
    def update_insurance(self, insurance):
        self.lock.acquire()
        self.insurance = insurance
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
                    sleep(1)
                
                if self.insurance:
                    pyautogui.moveTo(*INSURANCE)
                    pyautogui.click(*INSURANCE)
                
                if self.player_cards and self.dealer_card and self.actions['H'] is not None:
                    self.lock.acquire()
                    self.state = HandState.DEALT_CARDS
                    self.lock.release()

                if self.state == HandState.DEALT_CARDS:
                    if self.previous_player_total == self.player_cards:
                        continue

                    if self.actions['H'] is None:
                        continue

                    self.previous_player_total = self.player_cards
                    decision = get_decision(self.dealer_card,self.player_cards)
                    print(f"{self.player_cards} vs {self.dealer_card}: {decision}")
                    if decision:
                        self.lock.acquire()
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
                                self.press_button("D")
                            else:
                                self.press_button("S")
                            self.state = HandState.FINISHED
                        elif decision == "P":
                            if self.player_cards == "AA":
                                self.press_button(decision)
                                self.state = HandState.FINISHED
                            else:
                                self.press_button(decision)
                                self.state = HandState.SPLIT_HAND
                        self.lock.release()
                        sleep(1)
                    else:
                        print(f" No hand: {self.player_cards} vs {self.dealer_card}")
                
                if self.state == HandState.MORE_THAN_TWO:
                    if self.previous_player_total == self.player_cards:
                        continue
                    if self.actions['H'] is None:
                        continue


                    if self.player_cards  == "Bust":
                        self.lock.acquire()
                        self.state = HandState.FINISHED
                        self.lock.release()
                    else:
                        self.previous_player_total = self.player_cards
                        decision = get_decision(self.dealer_card,self.player_cards)
                        if decision:
                            self.lock.acquire()
                            if decision == "S":
                                self.press_button(decision)
                                self.state = HandState.FINISHED
                            elif decision == "H":
                                if self.dealer_card == "Ten" and self.player_cards == "16":
                                    self.press_button("S")
                                    print('Changed decision to S for 16 vs 10')
                                    self.state = HandState.FINISHED
                                else:
                                    self.press_button(decision)
                            elif decision == "D":
                                    self.press_button("H")
                            elif decision == "Ds":
                                    self.press_button("S")
                                    self.state = HandState.FINISHED
                            self.lock.release()  
                        else:
                            print(f" No hand: {self.player_cards} vs {self.dealer_card}")

                
                if self.state == HandState.SPLIT_HAND:
                    pass
                
                if self.state == HandState.FINISHED:
                    self.previous_player_total = None
                    sleep(0.5)
