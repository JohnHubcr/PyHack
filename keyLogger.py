from ctypes import *
import pythoncom
import pyHook
import win32clipboard

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
currentWindow = None

def getCurrentProcess():
    hwnd = uer32.GetForegroundWindow()

    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))

    processId = "%d" % pid.value

    executable = create_string_buffer("\x00" * 512)
    hProcess = kernel32.OpenProcess(0x400 | 0x10, False, pid)
    psapi.GetModuleBaseNameA(hProcess, None, byref(executable), 512)

    windowTitle = create_string_buffer("\x00" * 512)
    length = user32.GetWindowTextA(hwnd, byref(windowTitle), 512)

    print
    print "[ PID: %s - %s - %s]" % (processId, executable.value, windowTitle.value)
    print

    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(hProcess)
