import threading
import time
import win32api
import win32con
from win32api import mouse_event
import simple_pid as pid
from Grab_screen import GrabScreen
from final_bbox import FindBoxes
import cv2
import keyboard

grabber = GrabScreen()
findboxer = FindBoxes()
aim_flag = 1
time.sleep(3)

def monitor_caps_lock():
    global aim_flag
    while True:
        if keyboard.is_pressed('caps lock') and aim_flag == 0:
            aim_flag = 1
            print("aim is on")
        elif keyboard.is_pressed('caps lock') and aim_flag == 1:
            aim_flag = 0
            print("aim is off")
        time.sleep(0.1)


# 创建并启动一个线程来监听大写键状态
monitor_thread = threading.Thread(target=monitor_caps_lock)
monitor_thread.daemon = True  # 设置为守护线程，在主线程退出时自动退出
monitor_thread.start()

while True:
    # print("6")
    try:
        frame, left, top = grabber.capture_window_screenshot()
    except Exception as e:
        break

    frame, point_x, point_y = findboxer.process(frame, left, top)
    if point_x and point_y is not None:
        pid_x = pid.PID(2.5, 0.0, 0.00, setpoint=point_x)
        pid_y = pid.PID(2.5, 0.0, 0.00, setpoint=point_y)
        mouse_x, mouse_y = win32api.GetCursorPos()

        move_x, move_y = int(pid_x(mouse_x)), int(pid_y(mouse_y))
        # print("pid_x,y:", move_x, " ", move_y)
        if aim_flag:
            mouse_event(win32con.MOUSEEVENTF_MOVE, move_x, move_y)
            # if (move_x**2+move_y**2)**1/2<300:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    cv2.imshow('2', frame)
    cv2.waitKey(1)
print("over!")
