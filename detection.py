import cv2 as cv
from screen import Screen
from threading import Thread, Lock

class Detection:
    stopped = True
    lock = None
    screenshot = None
    hasScreenshot = False
    w = None
    h = None
    offset_x = 0
    offset_y = 0
    object = None
    objectDetected = False
    objectPosition = None

    def __init__(self,offset_x, offset_y):
        self.lock = Lock()
        self.threshold = 0.95
        self. offset_x = offset_x
        self. offset_y = offset_y
    
    def update(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.hasScreenShot = True
        self.lock.release()
    
    def set_object(self,object):
        self.lock.acquire()
        self.object = object
        self.w = object.shape[1]
        self.h = object.shape[0]
        self.lock.release()
    
    def find(self):
        result = cv.matchTemplate(self.screenshot, self.object,method=cv.TM_CCOEFF_NORMED)
        _, max_val, __, max_loc = cv.minMaxLoc(result)
        if max_val > self.threshold:
            return max_loc
        else:
            return None
    
    def find_center(self,object, top_left):
        image_width = object.shape[1]
        image_height = object.shape[0]

        center_x = top_left[0] + int(image_width/2)
        center_y = top_left[1] + int(image_height/2)

        point = (center_x, center_y)

        return point
    
    def find_position(self, point):
        return (point[0]+ self.offset_x, point[1] + self.offset_y)

    
    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()
    
    def stop(self):
        self.stopped = True
    
    def run(self):
        while not self.stopped:
            if not self.screenshot is None:
                if not self.object is None:
                        point = self.find()
                        if point is not None:
                            position = self.find_position(self.find_center(self.object, point))
                            self.lock.acquire()
                            self.objectDetected = True
                            self.objectPosition = position
                            self.lock.release()
                        else:
                            self.lock.acquire()
                            self.objectDetected = False
                            self.objectPosition = False
                            self.lock.release()
                    


        
    


