import win32gui
import win32ui
import win32con
import numpy as np


class GrabScreen:
    def __init__(self):
        self.hdesktop = win32gui.GetDesktopWindow()
        self.hwnd_dc = win32gui.GetWindowDC(self.hdesktop)
        self.img_dc = win32ui.CreateDCFromHandle(self.hwnd_dc)

    def capture_window_screenshot(self):
        self.active_window_handle = win32gui.GetForegroundWindow()
        rect = win32gui.GetWindowRect(self.active_window_handle)
        self.left, self.top, self.right, self.bottom = rect
        self.width, self.height = self.right - self.left, self.bottom - self.top
        mem_dc = self.img_dc.CreateCompatibleDC()
        screenshot = win32ui.CreateBitmap()
        screenshot.CreateCompatibleBitmap(self.img_dc, self.width, self.height)
        mem_dc.SelectObject(screenshot)

        mem_dc.BitBlt((0, 0), (self.width, self.height), self.img_dc, (self.left, self.top), win32con.SRCCOPY)
        buffer = screenshot.GetBitmapBits(True)
        frame = np.frombuffer(buffer, dtype=np.uint8).reshape((self.height, self.width, 4))
        win32gui.DeleteObject(screenshot.GetHandle())
        mem_dc.DeleteDC()
        return frame, self.left, self.top
