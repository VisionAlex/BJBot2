from detection import Detection
from windowcapture import Window
import cv2 as cv
from time import time
import pyautogui
from screen import Screen
from button import Button


loop_time = time()
if __name__ == '__main__':
    window = Window()
    detector = Detection()
    while True:
        screenshot = window.get_screenshot()
        speed_screen = detector.crop_image(screenshot,Screen.speed_screen)
        decisions_screen = detector.crop_image(screenshot,Screen.decisions_screen)
        point = detector.findButton(decisions_screen,Button.hit)
        if point:
            offset_point = Screen.offset_point(point,Screen.decisions_screen)
            hit = window.get_screen_position(offset_point)
            pyautogui.moveTo(*hit)
            pyautogui.click(*hit)
            break

        
        
        # print('FPS {}'.format(1 / (time() - loop_time)))
        # print(pyautogui.position())
        # loop_time = time()
        cv.imshow("BJ", screenshot)
        # if speed_screen is not None:
        #     cv.imshow('Speed', speed_screen)
        if cv.waitKey(1) == ord('q'):
            break