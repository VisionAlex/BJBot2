import cv2 as cv
from screen import Screen

class Detection:
    def find(self,screenshot, image, threshold=0.95, method=cv.TM_CCOEFF_NORMED):
        result = cv.matchTemplate(screenshot, image, method)
        _, max_val, __, max_loc = cv.minMaxLoc(result)

        if max_val > threshold:
            return max_loc
    def findButton(self,screenshot,image, threshold=0.95):
        point = self.find(screenshot,image, threshold)
        if point is not None:
            return self.find_center(image,point)
    
    def draw_rectangle(self,screenshot, image):
        image_width = image.shape[1]
        image_height = image.shape[0]

        top_left = self.find(screenshot,image)
        if not top_left:
            print('Item not found.')
            return None

        bottom_right = (top_left[0] + image_width, top_left[1] + image_height)
        cv.rectangle(screenshot,top_left, bottom_right, color=(0,255,0), thickness=1, lineType=cv.LINE_4)
        return screenshot
        

    def find_center(self,image, top_left):
        image_width = image.shape[1]
        image_height = image.shape[0]

        center_x = top_left[0] + int(image_width/2)
        center_y = top_left[1] + int(image_height/2)

        point = (center_x, center_y)
        return point

    def find_and_crop_image(self,screenshot,image):
        point = self.find(screenshot,image)
        if not point:
            return None
        x,y = point
        width = image.shape[1]
        height = image.shape[0]
        print(x,y,width,height)
        return self.crop_image(screenshot,(x,y,width,height))
    
    def crop_image(self,image,screen:Screen):
        x,y,width,height = screen
        return image[y:y + height, x:x + width]

        
    


