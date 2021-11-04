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
    hand_state = HandState.INITIAL
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
    
    def __init__(self,offset_x, offset_y):
        self.lock = Lock()
        self.threshold = 0.95
        self. offset_x = offset_x
        self. offset_y = offset_y
    
    def update(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()
    
    def update_hand_state(self,state: HandState):
        self.lock.acquire()
        self.hand_state = state
        self.lock.release()
    
    def get_rectangle(self,object):
        point = self.find(object)
        return (point[0],point[1], object.shape[1], object.shape[0])
    

    def find(self,object, threshold= 0.95):
        result = cv.matchTemplate(self.screenshot, object,method=cv.TM_CCOEFF_NORMED)
        _, max_val, __, max_loc = cv.minMaxLoc(result)
        if max_val > threshold:
            return max_loc
        else:
            return None
    
    def find_player_cards(self,object, threshold=0.95):
        if self.hand_state == HandState.SPLIT_HAND or self.hand_state == HandState.SECOND_SPLIT_HAND:
            threshold = 0.9

        x,y,w,h = self.screen
        cropped = self.screenshot[y:y+h,x:x+w]
        
        result = cv.matchTemplate(cropped, object,method=cv.TM_CCOEFF_NORMED)
        _, max_val, __, max_loc = cv.minMaxLoc(result)
        if max_val > threshold:
            return max_loc
        else:
            return None
    
    
    def find_dealer_cards(self,object,threshold=0.85):
        gray_screenshot = cv.cvtColor(self.screenshot,cv.COLOR_BGR2GRAY)
        x,y,w,h = Screen.dealer
        cropped = gray_screenshot[y:y+h, x:x+w]
        result = cv.matchTemplate(cropped,object,method=cv.TM_CCOEFF_NORMED)
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
    
    def check_insurance(self):
        insurance = self.find(Button.insurance)
        even_money = self.find(Button.even_money)
        if insurance or even_money:
            return True
        return False
    
    def check_attention_warning(self):
        atentie = self.find(Button.ok)
        if atentie:
            return self.find_position(self.find_center(Button.ok,atentie))
        return None
    
    def check_activity_warning(self):
        continua = self.find(Button.continua)
        if continua:
            return self.find_position(self.find_center(Button.continua,continua))


    def check_is_game_in_progress(self):
        point = self.find(Button.repariere)
        if not point:
            return None

        center = self.find_center(Button.repariere,point)
        return self.find_position(center)
    
    def get_player_cards(self):
        isSplit = self.hand_state == HandState.SPLIT_HAND or self.hand_state == HandState.SECOND_SPLIT_HAND
        
        if self.actions['H'] is None:
            return None
        twenty = self.find_player_cards(Cards.twenty)
        if twenty:
            return "20"
        
        thirteen = self.find_player_cards(Cards.thirteen)
        if thirteen:
            return "13"
        
        twelve = self.find_player_cards(Cards.twelve)
        if twelve:
            if self.actions['P'] is not None:
                return "66"
            return "12"
        
        fourteen = self.find_player_cards(Cards.fourteen)
        if fourteen:
            if not isSplit and self.actions['P'] is not None:
                return "77"
            return "14"
        
        fifteen = self.find_player_cards(Cards.fifteen)
        if fifteen:
            return "15"
        
        sixteen = self.find_player_cards(Cards.sixteen)
        if sixteen:
            if not isSplit and self.actions['P'] is not None:
                return "88"
            return "16"
        
        seventeen = self.find_player_cards(Cards.seventeen)
        if seventeen:
            return "17"
        
        eighteen = self.find_player_cards(Cards.eighteen)
        if eighteen:
            if not isSplit and self.actions['P'] is not None:
                return "99"
            return "18"
        
        nineteen = self.find_player_cards(Cards.nineteen)
        if nineteen:
            return "19"
        
        twentyone = self.find_player_cards(Cards.twentyone)
        if twentyone:
            return "21"
        
        eleven = self.find_player_cards(Cards.eleven)
        if eleven:
            return "11"
        
        ten = self.find_player_cards(Cards.ten)
        if ten:
            return "10"
        
        nine = self.find_player_cards(Cards.nine)
        if nine:
            return "9"
        
        eight = self.find_player_cards(Cards.eight)
        if eight:
            if not isSplit and self.actions['P'] is not None:
                return "44"
            return "8"

        seven = self.find_player_cards(Cards.seven)
        if seven:
            return "7"

        six = self.find_player_cards(Cards.six)
        if six:
            if  not isSplit and self.actions['P'] is not None:
                return "33"
            return "6"

        five = self.find_player_cards(Cards.five)
        if five:
            return "5"
        
        a2 = self.find_player_cards(Cards.a2)
        if a2:
            return "A2"

        a3 = self.find_player_cards(Cards.a3)
        if a3:
            return "A3"

        a4 = self.find_player_cards(Cards.a4)
        if a4:
            return "A4"
        
        a5 = self.find_player_cards(Cards.a5)
        if a5:
            return "A5"

        a6 = self.find_player_cards(Cards.a6)
        if a6:
            return "A6"
        
        a7 = self.find_player_cards(Cards.a7)
        if a7:
            return "A7"


        a8 = self.find_player_cards(Cards.a8)
        if a8:
            return "A8"
        
        a9 = self.find_player_cards(Cards.a9)
        if a9:
            return "A9"
        
        aa = self.find_player_cards(Cards.aa)
        if aa:
            return "AA"
        
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
        
        four = self.find_player_cards(Cards.four)
        if four:
            return "22"

        return None

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
                       
                    

