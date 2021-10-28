from detection import Detection
from windowcapture import Window
import cv2 as cv
from time import time, sleep
import pyautogui
from button import Button


def drawMarker(screenshot,point):
    cv.drawMarker(screenshot, point, (255,0,255),cv.MARKER_CROSS)


loop_time = time()
if __name__ == '__main__':
    window = Window()
    detector = Detection(window.offset_x, window.offset_y)

    window.start()
    detector.start()
    
    movedMouse = False
    while True:
        if window.screenshot is None:
            continue
        detector.update(window.screenshot)
        detector.set_object(Button.turbo)
        
        if detector.objectDetected:
            print(detector.objectPosition)
            if not movedMouse:
                pyautogui.moveTo(detector.objectPosition[0], detector.objectPosition[1])
                movedMouse = True
                sleep(10)

        else:
            print('Object not detected')

       

        
        
        # print('FPS {}'.format(1 / (time() - loop_time)))
        # print(pyautogui.position())
        loop_time = time()
        cv.imshow("BJ", window.screenshot)
        if cv.waitKey(1) == ord('q'):
            window.stop()
            detector.stop()
            cv.destroyAllWindows()
            break