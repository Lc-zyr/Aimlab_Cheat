import win32api
from Grab_screen import GrabScreen
import cv2

import numpy as np

class FindBoxes:
    def __init__(self):
        self.create_windows()

    def create_windows(self):
        cv2.namedWindow( '1', cv2.WINDOW_NORMAL)

    def process(self, frame, left, top):
        frame = frame. copy()
        hsv = cv2. cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([82,199, 118])
        upper_blue = np.array([97, 255,255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        result_frame = cv2. bitwise_and(frame, frame, mask=mask)
        edges = cv2.Canny(result_frame, 80, 255)
        contours, _ =cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        all_box = []
        distance=[]
        point_x=None
        point_y=None
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
            all_box.append((x, y, w, h))
        if len(all_box)!=0:
            mouse_x, mouse_y = win32api.GetCursorPos()
            all_point = [(int((x+w/2)+left),int((y+h/2)+top)) for x,y,w,h in all_box]
            for k in all_point:
                move_x, move_y = (k[0] - mouse_x),(k[1] - mouse_y)
                distance.append((move_x**2)+(move_y**2))
            min_index = np.argmin(distance)
            point_x, point_y = all_point[min_index][0],all_point[min_index][1]
        return frame,point_x,point_y