import ctypes
import threading
import time

def auto_close_msgbox_win(title, text, timeout=3):
    """Windows 原生弹窗，自动关闭"""
    def close_msgbox():
        time.sleep(timeout)
        # 找到弹窗并发送关闭信号
        hwnd = ctypes.windll.user32.FindWindowW(None, title)
        if hwnd:
            ctypes.windll.user32.PostMessageW(hwnd, 0x0010, 0, 0)  # 0x0010 = WM_CLOSE

    threading.Thread(target=close_msgbox).start()
    ctypes.windll.user32.MessageBoxW(0, text, title, 0x40)  # 0x40 = 信息图标

# 示例
auto_close_msgbox_win("提示", "3秒后关闭", timeout=3)