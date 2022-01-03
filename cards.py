import cv2 as cv

BUST_CARDS = ["22Bust", "23", "24", "25", "26"]

class Cards:
    four =cv.imread('img/cards/4.bmp',cv.IMREAD_GRAYSCALE)
    five =cv.imread('img/cards/5.bmp',cv.IMREAD_GRAYSCALE)
    six =cv.imread('img/cards/6.bmp',cv.IMREAD_GRAYSCALE)
    seven =cv.imread('img/cards/7.bmp',cv.IMREAD_GRAYSCALE)
    eight =cv.imread('img/cards/8.bmp',cv.IMREAD_GRAYSCALE)
    nine =cv.imread('img/cards/9.bmp',cv.IMREAD_GRAYSCALE)
    ten =cv.imread('img/cards/10.bmp',cv.IMREAD_GRAYSCALE)
    eleven =cv.imread('img/cards/11.bmp',cv.IMREAD_GRAYSCALE)
    twelve =cv.imread('img/cards/12.bmp',cv.IMREAD_GRAYSCALE)
    thirteen =cv.imread('img/cards/13.bmp',cv.IMREAD_GRAYSCALE)
    fourteen =cv.imread('img/cards/14.bmp',cv.IMREAD_GRAYSCALE)
    fifteen =cv.imread('img/cards/15.bmp',cv.IMREAD_GRAYSCALE)
    sixteen =cv.imread('img/cards/16.bmp',cv.IMREAD_GRAYSCALE)
    seventeen =cv.imread('img/cards/17.bmp',cv.IMREAD_GRAYSCALE)
    eighteen =cv.imread('img/cards/18.bmp',cv.IMREAD_GRAYSCALE)
    nineteen =cv.imread('img/cards/19.bmp',cv.IMREAD_GRAYSCALE)
    twenty = cv.imread('img/cards/20.bmp',cv.IMREAD_GRAYSCALE)
    twentyone = cv.imread('img/cards/21.bmp',cv.IMREAD_GRAYSCALE)
    twentytwo = cv.imread('img/cards/22.bmp',cv.IMREAD_GRAYSCALE)
    twentythree = cv.imread('img/cards/23.bmp',cv.IMREAD_GRAYSCALE)
    twentyfour = cv.imread('img/cards/24.bmp',cv.IMREAD_GRAYSCALE)
    twentyfive = cv.imread('img/cards/25.bmp',cv.IMREAD_GRAYSCALE)

    a2 = cv.imread('img/cards/a2.bmp',cv.IMREAD_GRAYSCALE)
    a3 = cv.imread('img/cards/a3.bmp',cv.IMREAD_GRAYSCALE)
    a4 = cv.imread('img/cards/a4.bmp',cv.IMREAD_GRAYSCALE)
    a5 = cv.imread('img/cards/a5.bmp',cv.IMREAD_GRAYSCALE)
    a6 = cv.imread('img/cards/a6.bmp',cv.IMREAD_GRAYSCALE)
    a7 = cv.imread('img/cards/a7.bmp',cv.IMREAD_GRAYSCALE)
    a8 = cv.imread('img/cards/a8.bmp',cv.IMREAD_GRAYSCALE)
    a9 = cv.imread('img/cards/a9.bmp',cv.IMREAD_GRAYSCALE)
    aa = cv.imread('img/cards/aa.bmp',cv.IMREAD_GRAYSCALE)

    busted = cv.imread('img/cards/busted.bmp',cv.IMREAD_GRAYSCALE)


class Dealer:
    two = cv.imread('img/dealer_cards/2.bmp',cv.IMREAD_GRAYSCALE)
    three = cv.imread('img/dealer_cards/3.bmp',cv.IMREAD_GRAYSCALE)
    four = cv.imread('img/dealer_cards/4.bmp',cv.IMREAD_GRAYSCALE)
    five = cv.imread('img/dealer_cards/5.bmp',cv.IMREAD_GRAYSCALE)
    six = cv.imread('img/dealer_cards/6.bmp',cv.IMREAD_GRAYSCALE)
    seven = cv.imread('img/dealer_cards/7.bmp',cv.IMREAD_GRAYSCALE)
    eight = cv.imread('img/dealer_cards/8.bmp',cv.IMREAD_GRAYSCALE)
    nine = cv.imread('img/dealer_cards/9.bmp',cv.IMREAD_GRAYSCALE)
    ten = cv.imread('img/dealer_cards/10.bmp',cv.IMREAD_GRAYSCALE)
    jack = cv.imread('img/dealer_cards/J.bmp',cv.IMREAD_GRAYSCALE)
    queen = cv.imread('img/dealer_cards/Q.bmp',cv.IMREAD_GRAYSCALE)
    king = cv.imread('img/dealer_cards/K.bmp',cv.IMREAD_GRAYSCALE)
    ace = cv.imread('img/dealer_cards/A.bmp',cv.IMREAD_GRAYSCALE)


class DetectorScreen:
    dealer = cv.imread('img/screens/dealer.bmp')
    player = cv.imread('img/screens/player.bmp')
    split1 = cv.imread('img/screens/split1.bmp')
    split2 = cv.imread('img/screens/split2.bmp')