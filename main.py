from bot import Bot, HandState
from cards import Cards
from detection import Detection
from windowcapture import Window
import cv2 as cv
from time import time
import pyautogui
from button import Button, Screen


def drawMarker(screenshot, point):
    cv.drawMarker(screenshot, point, (255, 0, 255), markerSize=10,
                  markerType=cv.MARKER_CROSS, thickness=2)


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
        detector.update_hand_state(bot.state)

        # img = cv.imread('img/screens/player.bmp')
        # rect = detector.get_rectangle(img)
        # print(rect)

        bot.update_repariere(detector.repariere)
        bot.update_screen(detector.screen)
        bot.update_attention_warning(detector.atentie)
        bot.update_activity_warning(detector.continua)

        bot.update_actions(detector.actions)
        bot.update_dealer_card(detector.dealer_card)
        bot.update_player_cards(detector.player_cards)

        if detector.dealer_card == "Ace":
            insurance = detector.check_insurance()
            bot.update_insurance(insurance)

        # print(f"{detector.player_cards} vs {detector.dealer_card}")
        # print(f"{detector.actions}")
        # print('FPS {}'.format(1 / (time() - loop_time)))

        # img = cv.imread('img/screens/player.bmp')
        # rect = detector.get_rectangle(img)
        # print(rect)
        # x, y, w, h = detector.screen
        # print(pyautogui.position())
        # loop_time = time()
        # cv.drawMarker(window.screenshot,center,(0,0,255))
        # cv.rectangle(window.screenshot,(x,y),(x+w,y+h),color=(0,255,0),thickness=1)
        cv.imshow("BJ", detector.screenshot)
        if cv.waitKey(1) == ord("q"):
            print('----------------------------')
            print(f'HANDS: {bot.hands}')
            print(f'Wagered: {bot.bet * 200}')
            print(f'Time: {int(time() - loop_time)}s')
            print('----------------------------')
            window.stop()
            detector.stop()
            bot.stop()
            cv.destroyAllWindows()
            break
