from threading import Lock, Thread
from enum import Enum, auto
from time import sleep
from button import Screen
from strategy import strategy
import winsound

import pyautogui

STRATEGY = strategy.get_strategy()
INSURANCE = (449, 744)


class HandState(Enum):
    INITIAL = auto()
    DEALT_CARDS = auto()
    SPLIT_HAND = auto()
    SECOND_SPLIT_HAND = auto()
    FINISHED = auto()


class Bot:
    stopped = True
    lock = None

    screen = None
    state = HandState.DEALT_CARDS
    hands = 0
    bet = 0

    repariere = None
    atentie = None
    continua = None

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

    def get_decision(self, dealer_card, player_cards):
        if not dealer_card or not player_cards:
            return None
        if player_cards == "Bust":
            print(f'{self.state}: Bust')
            return None
        decision = STRATEGY[player_cards][dealer_card]
        print(self.state)
        print(f"{player_cards} vs {dealer_card} : {decision}")
        return decision

    def update_repariere(self, repariere):
        self.lock.acquire()
        self.repariere = repariere
        self.lock.release()

    def update_attention_warning(self, atentie):
        self.lock.acquire()
        self.atentie = atentie
        self.lock.release()

    def update_activity_warning(self, continua):
        self.lock.acquire()
        self.continua = continua
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

    def update_screen(self, screen):
        self.lock.acquire()
        self.screen = screen
        self.lock.release()

    def press_button(self, action):
        if action in self.actions:
            if self.actions[action] is not None:
                pyautogui.click(*self.actions[action])
                if action == "D" or action == "P":
                    self.bet += 1
                return True
            else:
                return False

    def start(self):
        self.stopped = False
        t1 = Thread(target=self.run)
        t1.start()

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            if self.atentie is not None:
                pyautogui.click(*self.atentie)
                self.atentie = None

            if self.continua is not None:
                pyautogui.click(*self.continua)
                self.continua = None

            if self.repariere is not None:
                pyautogui.click(*self.repariere)
                self.lock.acquire()
                self.state = HandState.DEALT_CARDS
                self.hands += 1
                self.bet += 1
                self.lock.release()
                print(f'----- Hand {self.hands} -----')

                self.previous_player_total = None
                sleep(1)

            if self.insurance:
                pyautogui.click(*INSURANCE)
                continue

            if self.state == HandState.DEALT_CARDS:
                if self.previous_player_total is not None and self.previous_player_total == self.player_cards:
                    print('Same card as previous')
                    sleep(0.5)
                    continue

                if self.actions['H'] is None:
                    sleep(0.5)
                    continue

                if self.player_cards == "6" and self.actions['P'] is not None:
                    self.player_cards = "33"
                if self.player_cards == "8" and self.actions['P'] is not None:
                    self.player_cards = "44"
                if self.player_cards == "12" and self.actions['P'] is not None:
                    self.player_cards = "66"
                if self.player_cards == "14" and self.actions['P'] is not None:
                    self.player_cards = "77"
                if self.player_cards == "16" and self.actions['P'] is not None:
                    self.player_cards = "88"
                if self.player_cards == "18" and self.actions['P'] is not None:
                    self.player_cards = "99"

                self.previous_player_total = self.player_cards
                decision = self.get_decision(
                    self.dealer_card, self.player_cards)

                if decision:
                    self.lock.acquire()
                    if decision == "S":
                        is_pressed = self.press_button(decision)
                        if not is_pressed:
                            continue
                        self.state = HandState.FINISHED
                    elif decision == "H":
                        is_pressed = self.press_button(decision)
                        if not is_pressed:
                            continue
                    elif decision == "D":
                        if self.actions['D'] is not None:
                            is_pressed = self.press_button(decision)
                            if not is_pressed:
                                continue
                            self.state = HandState.FINISHED
                        else:
                            is_pressed = self.press_button("H")
                            if not is_pressed:
                                continue

                    elif decision == "Ds":
                        if self.actions['D'] is not None:
                            is_pressed = self.press_button("D")
                        else:
                            is_pressed = self.press_button("S")
                            if not is_pressed:
                                continue
                        self.state = HandState.FINISHED
                    elif decision == "P":
                        if self.player_cards == "AA":
                            is_pressed = self.press_button(decision)
                            if not is_pressed:
                                continue
                            self.state = HandState.FINISHED
                        else:
                            winsound.Beep(1440, 1000)
                            is_pressed = self.press_button(decision)

                            if not is_pressed:
                                continue

                            self.state = HandState.SPLIT_HAND
                            self.previous_player_total = None
                            sleep(4)
                    self.lock.release()
                    sleep(2)
                # else:
                    # print(
                    # f" No hand: {self.player_cards} vs {self.dealer_card}")
                continue

            if self.state == HandState.SPLIT_HAND:
                if self.screen != Screen.split1:
                    sleep(0.5)
                    continue
                if self.actions['H'] is None:
                    sleep(0.5)
                    continue
                if self.player_cards is None:
                    sleep(0.5)
                    continue
                if self.previous_player_total is not None and self.previous_player_total == self.player_cards:
                    print('Same card as previous')
                    continue

                if self.player_cards == "Bust" and self.previous_player_total is not None:
                    self.lock.acquire()
                    self.state = HandState.SECOND_SPLIT_HAND
                    self.previous_player_total = None
                    self.lock.release()

                if self.player_cards == "22":
                    self.player_cards = "4"
                self.previous_player_total = self.player_cards
                decision = self.get_decision(
                    self.dealer_card, self.player_cards)
                print(
                    f"SPLIT1: {self.player_cards} vs {self.dealer_card}: {decision}")

                if decision:
                    self.lock.acquire()
                    if decision == "S":
                        is_pressed = self.press_button("S")
                        if not is_pressed:
                            continue
                        self.player_cards = None
                        self.previous_player_total = None
                        self.state = HandState.SECOND_SPLIT_HAND
                    elif decision == "D":
                        if self.actions['D'] is not None:
                            is_pressed = self.press_button(decision)
                            if not is_pressed:
                                continue
                            self.player_cards = None
                            self.previous_player_total = None
                            self.state = HandState.SECOND_SPLIT_HAND
                        else:
                            is_pressed = self.press_button('H')
                            if not is_pressed:
                                continue
                    elif decision == "Ds":
                        if self.actions['D'] is not None:
                            is_pressed = self.press_button("D")
                            if not is_pressed:
                                continue
                        else:
                            is_pressed = self.press_button("S")
                            if not is_pressed:
                                continue
                        self.player_cards = None
                        self.previous_player_total = None
                        self.state = HandState.SECOND_SPLIT_HAND
                    elif decision == "H":
                        is_pressed = self.press_button(decision)
                        if not is_pressed:
                            continue
                    self.lock.release()
                    sleep(2)
                continue

            if self.state == HandState.SECOND_SPLIT_HAND:
                if self.screen != Screen.split2:
                    continue
                if self.actions['H'] is None:
                    continue
                if self.player_cards is None:
                    continue

                if self.previous_player_total is not None and self.previous_player_total == self.player_cards:
                    print('Previous player total is the same as current total')
                    self.player_cards = None
                    self.previous_player_total = None
                    continue

                if self.player_cards == "Bust":
                    self.lock.acquire()
                    self.state = HandState.FINISHED
                    self.lock.release()

                if self.player_cards == "22":
                    self.player_cards = "4"

                self.previous_player_total = self.player_cards
                decision = self.get_decision(
                    self.dealer_card, self.player_cards)
                print(
                    f"SPLIT2: {self.player_cards} vs {self.dealer_card}: {decision}")

                if decision:
                    self.lock.acquire()
                    if decision == "S":
                        is_pressed = self.press_button("S")
                        if not is_pressed:
                            continue
                        self.state = HandState.FINISHED
                    elif decision == "D":
                        if self.actions['D'] is not None:
                            is_pressed = self.press_button(decision)
                            if not is_pressed:
                                continue
                            self.state = HandState.FINISHED
                        else:
                            is_pressed = self.press_button('H')
                            if not is_pressed:
                                continue
                    elif decision == "Ds":
                        if self.actions['D'] is not None:
                            is_pressed = self.press_button("D")
                            if not is_pressed:
                                continue
                        else:
                            is_pressed = self.press_button("S")
                            if not is_pressed:
                                continue
                        self.state = HandState.FINISHED
                    elif decision == "H":
                        is_pressed = self.press_button(decision)
                        if not is_pressed:
                            continue
                    self.lock.release()
                else:
                    print(
                        f'no decision: {self.player_cards, self.dealer_card}')
                sleep(1.5)
                continue

            if self.state == HandState.FINISHED:
                self.previous_player_total = None
