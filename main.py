from bot import Bot
from detection import Detection
from windowcapture import Window
import cv2 as cv
from time import time, sleep
import pyautogui
from button import Button


def drawMarker(screenshot,point):
    cv.drawMarker(screenshot, point, (255,0,255),markerSize=10,markerType=cv.MARKER_CROSS,thickness=2)


loop_time = time()
move = True
if __name__ == '__main__':
    window = Window()
    detector = Detection(window.offset_x, window.offset_y)
    bot = Bot()

    window.start()
    detector.start()
    bot.start()

    while True:
        if window.screenshot is None:
            continue

        detector.update(window.screenshot)
        bot.update_repariere(detector.repariere)
        bot.update_dealer_card(detector.dealer_card)
        bot.update_player_cards(detector.player_cards)
        bot.update_actions(detector.actions) 
        
        # print('FPS {}'.format(1 / (time() - loop_time)))
        # print(pyautogui.position())
        loop_time = time()
        cv.imshow("BJ", window.screenshot)
        if cv.waitKey(1) == ord('q'):
            window.stop()
            detector.stop()
            bot.stop()
            cv.destroyAllWindows()
            break