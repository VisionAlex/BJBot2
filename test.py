import cv2

screen = cv2.imread('screen.bmp',cv2.IMREAD_GRAYSCALE)
card1 = cv2.imread('img/cards/9.bmp', cv2.IMREAD_GRAYSCALE)
result1 = cv2.matchTemplate(screen,card1, method=cv2.TM_CCORR_NORMED)
_, max_val1, _, max_loc2 = cv2.minMaxLoc(result1)
print('maxVal 10:', max_val1)
while True:
    cv2.imshow('detect',screen)
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break