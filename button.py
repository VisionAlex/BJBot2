import cv2 as cv

class Button:
    turbo = cv.imread('img/turbo.bmp')
    repariere = cv.imread('img/repariere.bmp')
    hit = cv.imread('img/hit.bmp')
    split = cv.imread('img/split.bmp')
    double = cv.imread('img/double.bmp')
    stand = cv.imread('img/stand.bmp')
    insurance =cv.imread('img/insurance.bmp')
    even_money = cv.imread('img/even.bmp')
    ok = cv.imread('img/ok.bmp')
    continua = cv.imread('img/continua.bmp')


class Screen:
    player = (369, 284, 118, 184)
    dealer = (369, 73, 119, 106)
    split1 = (512, 288, 79, 132)
    split2 = (272, 282, 127, 160)

