import cv2 as cv
from bot import HandState
from button import Button, Screen
from cards import Cards, Dealer
from threading import Thread, Lock


class Detection:
    stopped = True
    lock = None
    screenshot = None
    w = None
    h = None
    offset_x = 0
    offset_y = 0

    repariere = None
    atentie = None
    continua = None
    hand_state = HandState.DEALT_CARDS   
    screen = Screen.player
    cropped = None

    player_cards = None
    dealer_card = None
    actions = {
        "H": None,
        "S": None,
        "D": None,
        "P": None,
    }

    def __init__(self, offset_x, offset_y):
        self.lock = Lock()
        self. offset_x = offset_x
        self. offset_y = offset_y

    def update(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def update_hand_state(self, state: HandState):
        self.lock.acquire()
        self.hand_state = state
        self.lock.release()

    def get_rectangle(self, object):
        point = self.find(object)
        return (point[0], point[1], object.shape[1], object.shape[0])

    def find(self, object, threshold=0.95):
        result = cv.matchTemplate(
            self.screenshot, object, method=cv.TM_CCOEFF_NORMED)
        _, max_val, __, max_loc = cv.minMaxLoc(result)
        if max_val > threshold:
            return max_loc
        else:
            return None

    def find_player_cards(self, object, threshold=0.83):
        if self.screen == Screen.split1 and self.hand_state != HandState.SPLIT_HAND:
            return None
        if self.screen == Screen.split2 and self.hand_state != HandState.SECOND_SPLIT_HAND:
            return None

        x, y, w, h = self.screen
        cropped = self.screenshot[y:y+h, x:x+w]
        grayed_cropped = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY)
        
        result = cv.matchTemplate(grayed_cropped, object, method=cv.TM_CCOEFF_NORMED)
        
        _, max_val, __, ___ = cv.minMaxLoc(result)
        if max_val > threshold:
            return max_val
        else:
            return None

    def find_dealer_cards(self, object, threshold=0.85):
        gray_screenshot = cv.cvtColor(self.screenshot, cv.COLOR_BGR2GRAY)
        x, y, w, h = Screen.dealer
        cropped = gray_screenshot[y:y+h, x:x+w]
        result = cv.matchTemplate(cropped, object, method=cv.TM_CCOEFF_NORMED)
        _, max_val, __, max_loc = cv.minMaxLoc(result)
        if max_val > threshold:
            return max_loc
        else:
            return None

    def find_center(self, object, top_left):
        image_width = object.shape[1]
        image_height = object.shape[0]

        center_x = top_left[0] + int(image_width/2)
        center_y = top_left[1] + int(image_height/2)

        point = (center_x, center_y)

        return point

    def find_position(self, point):
        return (point[0] + self.offset_x, point[1] + self.offset_y)

    def check_insurance(self):
        insurance = self.find(Button.insurance)
        even_money = self.find(Button.even_money)
        if insurance or even_money:
            return True
        return False

    def check_attention_warning(self):
        atentie = self.find(Button.ok)
        if atentie:
            return self.find_position(self.find_center(Button.ok, atentie))
        return None

    def check_activity_warning(self):
        continua = self.find(Button.continua)
        if continua:
            return self.find_position(self.find_center(Button.continua, continua))

    def check_is_game_in_progress(self):
        point = self.find(Button.repariere)
        if not point:
            return None

        center = self.find_center(Button.repariere, point)
        return self.find_position(center)

    def get_player_cards(self):
        coeff = 0
        card = None

        if self.hand_state == HandState.SECOND_SPLIT_HAND and self.screen != Screen.split2:
            return None
        if self.hand_state == HandState.SPLIT_HAND and self.screen != Screen.split1:
            return None

        if self.actions['H'] is None:
            return None
        twenty = self.find_player_cards(Cards.twenty)
        if twenty:
            if twenty > coeff:
                coeff = twenty
                card = "20"
        thirteen = self.find_player_cards(Cards.thirteen)
        if thirteen:
            if thirteen > coeff:
                coeff = thirteen
                card = "13"

        twelve = self.find_player_cards(Cards.twelve)
        if twelve:
            if twelve > coeff:
                coeff = thirteen
                card = "12"

        fourteen = self.find_player_cards(Cards.fourteen)
        if fourteen:
            if fourteen > coeff:
                coeff = fourteen
                card = "14"

        fifteen = self.find_player_cards(Cards.fifteen)
        if fifteen:
            if fifteen > coeff:
                coeff = fifteen
                card = "15"

        sixteen = self.find_player_cards(Cards.sixteen)
        if sixteen:
            if sixteen > coeff:
                coeff = sixteen
                card = "16"

        seventeen = self.find_player_cards(Cards.seventeen)
        if seventeen:
            if seventeen > coeff:
                coeff = seventeen
                card = "17"

        eighteen = self.find_player_cards(Cards.eighteen)
        if eighteen:
            if eighteen > coeff:
                coeff = eighteen
                card = "18"

        nineteen = self.find_player_cards(Cards.nineteen)
        if nineteen:
            if nineteen > coeff:
                coeff = nineteen
                card = "19"

        twentyone = self.find_player_cards(Cards.twentyone)
        if twentyone:
            if twentyone > coeff:
                coeff = twentyone
                card = "21"

        eleven = self.find_player_cards(Cards.eleven)
        if eleven:
            if eleven > coeff:
                coeff = eleven
                card = "11"

        ten = self.find_player_cards(Cards.ten)
        if ten:
            if ten > coeff:
                coeff = ten
                card = "10"

        nine = self.find_player_cards(Cards.nine)
        if nine:
            if nine > coeff:
                coeff = nine
                card = "9"

        eight = self.find_player_cards(Cards.eight)
        if eight:
            if eight > coeff:
                coeff = eight
                card = "8"

        seven = self.find_player_cards(Cards.seven)
        if seven:
            if seven > coeff:
                coeff = seven
                card = "7"

        six = self.find_player_cards(Cards.six)
        if six:
            if six > coeff:
                coeff = six
                card = "6"

        five = self.find_player_cards(Cards.five)
        if five:
            if five > coeff:
                coeff = five
                card = "5"

        a2 = self.find_player_cards(Cards.a2)
        if a2:
            if a2 > coeff:
                coeff = a2
                card = "A2"

        a3 = self.find_player_cards(Cards.a3)
        if a3:
            if a3 > coeff:
                coeff = a3
                card = "A3"

        a4 = self.find_player_cards(Cards.a4)
        if a4:
            if a4 > coeff:
                coeff = a4
                card = "A4"

        a5 = self.find_player_cards(Cards.a5)
        if a5:
            if a5 > coeff:
                coeff = a5
                card = "A5"

        a6 = self.find_player_cards(Cards.a6)
        if a6:
            if a6 > coeff:
                coeff = a6
                card = "A6"

        a7 = self.find_player_cards(Cards.a7)
        if a7:
            if a7 > coeff:
                coeff = a7
                card = "A7"

        a8 = self.find_player_cards(Cards.a8)
        if a8:
            if a8 > coeff:
                coeff = a8
                card = "A8"

        a9 = self.find_player_cards(Cards.a9)
        if a9:
            if a9 > coeff:
                coeff = a9
                card = "A9"

        aa = self.find_player_cards(Cards.aa)
        if aa:
            if aa > coeff:
                coeff = aa
                card = "AA"

        twentytwo = self.find_player_cards(Cards.twentytwo)
        if twentytwo:
            return "Bust"

        twentythree = self.find_player_cards(Cards.twentythree)
        if twentythree:
            return "Bust"

        twentyfour = self.find_player_cards(Cards.twentyfour)
        if twentyfour:
            return "Bust"

        twentyfive = self.find_player_cards(Cards.twentyfive)
        if twentyfive:
            return "Bust"

        busted = self.find_player_cards(Cards.busted)
        if busted:
            return "Bust"

        four = self.find_player_cards(Cards.four)
        if four:
            if four > coeff:
                coeff = four
                card = "22"
        # print(card,coeff)
        return card

    def get_dealer_card(self):
        two = self.find_dealer_cards(Dealer.two)
        if two:
            return "Two"

        three = self.find_dealer_cards(Dealer.three)
        if three:
            return "Three"

        four = self.find_dealer_cards(Dealer.four)
        if four:
            return "Four"

        five = self.find_dealer_cards(Dealer.five)
        if five:
            return "Five"

        six = self.find_dealer_cards(Dealer.six)
        if six:
            return "Six"

        seven = self.find_dealer_cards(Dealer.seven)
        if seven:
            return "Seven"

        eight = self.find_dealer_cards(Dealer.eight)
        if eight:
            return "Eight"

        nine = self.find_dealer_cards(Dealer.nine)
        if nine:
            return "Nine"

        ten = self.find_dealer_cards(Dealer.ten)
        if ten:
            return "Ten"

        jack = self.find_dealer_cards(Dealer.jack)
        if jack:
            return "Ten"

        queen = self.find_dealer_cards(Dealer.queen)
        if queen:
            return "Ten"

        king = self.find_dealer_cards(Dealer.king)
        if king:
            return "Ten"

        ace = self.find_dealer_cards(Dealer.ace)
        if ace:
            return "Ace"

    def get_actions(self):
        actions = {
            "H": None,
            "S": None,
            "D": None,
            "P": None,
        }

        hit = self.find(Button.hit)
        if hit:
            actions["H"] = self.find_position(
                self.find_center(Button.hit, hit))
        stand = self.find(Button.stand)
        if stand:
            actions["S"] = self.find_position(
                self.find_center(Button.stand, stand))
        double = self.find(Button.double)
        if double:
            actions['D'] = self.find_position(
                self.find_center(Button.double, double))
        split = self.find(Button.split)
        if split:
            actions['P'] = self.find_position(
                self.find_center(Button.split, split))

        return actions

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            if not self.screenshot is None:

                self.lock.acquire()
                if self.hand_state == HandState.SPLIT_HAND:
                    self.screen = Screen.split1
                elif self.hand_state == HandState.SECOND_SPLIT_HAND:
                    self.screen = Screen.split2
                else:
                    self.screen = Screen.player
                self.lock.release()

                atentie = self.check_attention_warning()
                self.lock.acquire()
                self.atentie = atentie
                self.lock.release()

                continua = self.check_activity_warning()
                self.lock.acquire()
                self.continua = continua
                self.lock.release()

                repariere = self.check_is_game_in_progress()
                self.lock.acquire()
                self.repariere = repariere
                self.lock.release()

                if not repariere:
                    actions = self.get_actions()
                    self.lock.acquire()
                    self.actions = actions
                    self.lock.release()

                    player_cards = self.get_player_cards()
                    dealer_card = self.get_dealer_card()
                    self.lock.acquire()
                    self.player_cards = player_cards
                    self.dealer_card = dealer_card
                    self.lock.release()
