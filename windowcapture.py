import win32gui
import numpy as np
import cv2 as cv
from PIL import ImageGrab
from screen import Screen
from threading import  Thread , Lock

class Window:
    stopped = True
    lock = None
    screenshot = None


    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0
    def __init__(self) -> None:
        self.lock = Lock()

        # self.hwnd = win32gui.FindWindow(None,'Maxbet Casino | Jocuri online: Lux Blackjack - Google Chrome')
        self.hwnd = win32gui.FindWindow(None,'Jocuri de Noroc | Pacanele Online Gratis: Lux Blackjack - Google Chrome')
        if not self.hwnd:
            raise Exception(f'Window not found')
        self.resize()

         # get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        # account for the window border and titlebar and cut them off
        border_left = 100
        border_right = 11
        titlebar_pixels = 250
        bottom_border = 50
        self.w = self.w - (border_left + border_right)
        self.h = self.h -bottom_border
        self.cropped_x = border_left
        self.cropped_y = titlebar_pixels

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y




    def resize(self):
        win32gui.MoveWindow(self.hwnd,0,0,800,800, True)
    
    def get_screenshot(self, code=cv.COLOR_RGB2BGR):
        small_rect= (self.offset_x,self.offset_y,self.w,self.h)
        image = ImageGrab.grab(small_rect)
        opencvImage = cv.cvtColor(np.array(image), code)            
        return opencvImage
    
    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)
    
    def crop_image(self,image,screen:Screen):
        x,y,width,height = screen
        return image[y:y + height, x:x + width]
    

    def start(self):
        self.stopped = False
        t = Thread(target = self.run)
        t.start()
    
    def stop(self):
        self.stopped = True
    
    def run(self):
        while not self.stopped:
            screenshot = self.get_screenshot()
            self.lock.acquire()
            self.screenshot = screenshot
            self.lock.release()