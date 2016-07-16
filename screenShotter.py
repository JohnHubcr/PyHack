import win32gui
import win32ui
import win32con
import win32api

hDesktop = win32gui.GetDesktopWindow()

width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

desktopDC = win32gui.GetWindowDC(hDesktop)
imgDC = win32ui.CreateDCFromHandle(desktopDC)

memDC = imgDC.CreateCompatibleDC()

screenShot = win32ui.CreateBitmap()
screenShot.CreateCompatibleBitmap(imgDC, width, height)
memDC.SelectObject(screenShot)

memDC.BitBlt((0, 0), (width, height), imgDC, (left, top), win32con.SRCCOPY)

screenShot.SaveBitmapFile(memDC, "C:\\WINDOWS\\Temp\\screenShot.tmp")

memDC.DeleteDC()
win32gui.DeleteObject(screenShot.GetHandle())
