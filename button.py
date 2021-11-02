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
    player = (299, 202, 109, 45)
    dealer = (266, 54, 89, 81)
    split1 = (326, 206, 83, 87)
    split2 = (205, 203, 80, 88)

