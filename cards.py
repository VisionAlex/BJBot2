import cv2 as cv

BUST_CARDS = ["22Bust", "23", "24", "25", "26"]

class Cards:
    five =cv.imread('img/cards/5.bmp')
    six =cv.imread('img/cards/6.bmp')
    seven =cv.imread('img/cards/7.bmp')
    eight =cv.imread('img/cards/8.bmp')

    ten =cv.imread('img/cards/10.bmp')
    eleven =cv.imread('img/cards/11.bmp')
    twelve =cv.imread('img/cards/12.bmp')
    thirteen =cv.imread('img/cards/13.bmp')
    fourteen =cv.imread('img/cards/14.bmp')
    fifteen =cv.imread('img/cards/15.bmp')
    sixteen =cv.imread('img/cards/16.bmp')
    seventeen =cv.imread('img/cards/17.bmp')
    eighteen =cv.imread('img/cards/18.bmp')
    nineteen =cv.imread('img/cards/19.bmp')
    twenty = cv.imread('img/cards/20.bmp')
    twentyone = cv.imread('img/cards/21.bmp')
    twentytwo = cv.imread('img/cards/22.bmp')
    twentythree = cv.imread('img/cards/23.bmp')
    twentyfour = cv.imread('img/cards/24.bmp')
    twentyfive = cv.imread('img/cards/25.bmp')

    a4 = cv.imread('img/cards/a4.bmp')
    a8 = cv.imread('img/cards/a8.bmp')


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