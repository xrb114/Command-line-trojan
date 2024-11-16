#截图模块
import win32gui
from PyQt5.QtWidgets import QApplication
import sys

hwnd_title = dict()

def get_all_hwnd():
    """获取所有窗口句柄和标题"""
    def callback(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title[hwnd] = win32gui.GetWindowText(hwnd)

    win32gui.EnumWindows(callback, 0)
    return hwnd_title

def print_all_windows():
    """打印所有窗口句柄和标题"""
    windows = get_all_hwnd()
    for hwnd, title in windows.items():
        if title:
            print(hwnd, title)

def find_window_by_title(title):
    """根据窗口标题查找窗口句柄"""
    return win32gui.FindWindow(None, title)

def capture_window(hwnd, save_path="screenshot.jpg"):
    """对指定窗口进行截图并保存"""
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()
    img.save(save_path)
    app.quit()
    print(f"截图已保存为 {save_path}")
