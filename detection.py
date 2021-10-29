import cv2 as cv
from button import Button
from cards import Cards, Dealer
from screen import Screen
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
    player_cards = None
    dealer_card = None
    actions = {
        "H": None,
        "S": None,
        "D": None,
        "P": None,
    }
    def __init__(self,offset_x, offset_y):
        self.lock = Lock()
        self.threshold = 0.95
        self. offset_x = offset_x
        self. offset_y = offset_y
    
    def update(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()
    
    def set_object(self,object):
        self.lock.acquire()
        self.object = object
        self.w = object.shape[1]
        self.h = object.shape[0]
        self.lock.release()
    

    def find(self, object, threshold= 0.95):
        result = cv.matchTemplate(self.screenshot, object,method=cv.TM_CCOEFF_NORMED)
        _, max_val, __, max_loc = cv.minMaxLoc(result)
        if max_val > threshold:
            return max_loc
        else:
            return None
    
    def find_gray(self,object,threshold=0.9):
        gray_screenshot = cv.cvtColor(self.screenshot,cv.COLOR_BGR2GRAY)
        result = cv.matchTemplate(gray_screenshot,object,method=cv.TM_CCOEFF_NORMED)
        _, max_val, __, max_loc = cv.minMaxLoc(result)
        if max_val > threshold:
            return max_loc
        else:
            return None

    
    def find_center(self,object, top_left):
        image_width = object.shape[1]
        image_height = object.shape[0]

        center_x = top_left[0] + int(image_width/2)
        center_y = top_left[1] + int(image_height/2)

        point = (center_x, center_y)

        return point
    
    def find_position(self, point):
        return (point[0]+ self.offset_x, point[1] + self.offset_y)

    def check_is_game_in_progress(self):
        point = self.find(Button.repariere)
        if not point:
            return None

        center = self.find_center(Button.repariere,point)
        return self.find_position(center)
    
    def get_player_cards(self):
        twenty = self.find(Cards.twenty)
        if twenty:
            return "20"
        
        thirteen = self.find(Cards.thirteen)
        if thirteen:
            return "13"
        
        twelve = self.find(Cards.twelve)
        if twelve:
            if self.actions['P'] is not None:
                return "66"
            return "12"
        
        fourteen = self.find(Cards.fourteen)
        if fourteen:
            if self.actions['P'] is not None:
                return "77"
            return "14"
        
        fifteen = self.find(Cards.fifteen)
        if fifteen:
            return "15"
        
        sixteen = self.find(Cards.sixteen)
        if sixteen:
            if self.actions['P'] is not None:
                return "88"
            return "16"
        
        seventeen = self.find(Cards.seventeen)
        if seventeen:
            return "17"
        
        eighteen = self.find(Cards.eighteen)
        if eighteen:
            if self.actions['P'] is not None:
                return "99"
            return "18"
        
        nineteen = self.find(Cards.nineteen)
        if nineteen:
            return "19"
        
        twentyone = self.find(Cards.twentyone)
        if twentyone:
            return "21"
        
        eleven = self.find(Cards.eleven)
        if eleven:
            return "11"
        
        ten = self.find(Cards.ten)
        if ten:
            return "10"
        
        #Nine
        eight = self.find(Cards.eight)
        if eight:
            if self.actions['P'] is not None:
                return "44"
            return "8"

        seven = self.find(Cards.seven)
        if seven:
            return "7"

        six = self.find(Cards.six)
        if six:
            if self.actions['P'] is not None:
                return "33"
            return "6"

        
        a4 = self.find(Cards.a4)
        
        if a4:
            return "A4"
        
        a8 = self.find(Cards.a8)
        if a8:
            return "A8"
        
        twentytwo = self.find(Cards.twentytwo)
        if twentytwo:
            return "22Bust"
        
        twentythree = self.find(Cards.twentythree)
        if twentythree:
            return "23"

        twentyfour = self.find(Cards.twentyfour)
        if twentyfour:
            return "24"

        twentyfive = self.find(Cards.twentyfive)
        if twentyfive:
            return "25"

        return None

    def get_dealer_card(self):
        two = self.find_gray(Dealer.two)
        if two:
            return "Two"

        three = self.find_gray(Dealer.three)
        if three:
            return "Three"

        four = self.find_gray(Dealer.four)
        if four:
            return "Four"

        five = self.find_gray(Dealer.five)
        if five:
            return "Five"
        
        six = self.find_gray(Dealer.six)
        if six:
            return "Six"

        seven = self.find_gray(Dealer.seven)
        if seven:
            return "Seven"
        
        eight = self.find_gray(Dealer.eight)
        if eight:
            return "Eight"
        
        nine = self.find_gray(Dealer.nine)
        if nine:
            return "Nine"

        ten = self.find_gray(Dealer.ten)
        if ten:
            return "Ten"

        jack = self.find_gray(Dealer.jack)
        if jack:
            return "Ten"
        
        queen = self.find_gray(Dealer.queen)
        if queen:
            return "Ten"

        king = self.find_gray(Dealer.king)
        if king:
            return "Ten"

        ace = self.find_gray(Dealer.ace)
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
            actions["H"]= self.find_position(self.find_center(Button.hit,hit))
        stand = self.find(Button.stand)
        if stand:
            actions["S"] =self.find_position(self.find_center(Button.stand, stand))
        double = self.find(Button.double)
        if double:
            actions['D'] = self.find_position(self.find_center(Button.double, double))
        split = self.find(Button.split)
        if split:
            actions['P'] = self.find_position(self.find_center(Button.split,split))

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
                       
                    

