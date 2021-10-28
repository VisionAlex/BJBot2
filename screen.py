import cv2 as cv

class Screen:
    speed_screen = (460, 300, 124, 94)
    decisions_screen = (73, 387, 428, 76)

    @staticmethod
    def offset_point(point,screen):
        return (point[0] + screen[0], point[1]+ screen[1])
