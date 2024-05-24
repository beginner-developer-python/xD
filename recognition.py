import cv2
import pyautogui
import mss
import numpy as np
import os
import time
import keyboard
import random
import pydirectinput
import win32com.client
from colorama import Fore
shell = win32com.client.Dispatch("WScript.Shell")


def focus_pokw():
    win = []
    winNum = 0
    for x in pyautogui.getAllWindows():
        win.append(x.title)
        winNum = winNum+1
    for q in range(winNum):
        if len(win[q]) == 7:
            print(win[q])
            shell.AppActivate(win[q])
            break


path = os.path.dirname(os.path.dirname(__file__))
img_path = os.path.join(path, 'PokeMMO\img')


def Template_Match(needle, haystack):
    img = cv2.imread(os.path.join(img_path, needle), cv2.COLOR_BGR2GRAY)

    result_try = cv2.matchTemplate(haystack, img, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result_try)
    print(max_loc, max_val)
    return (max_loc, max_val)


def Click_Location(x, y, wait=0):
    pydirectinput.moveTo(x, y)
    pydirectinput.mouseDown()
    time.sleep(wait)
    pydirectinput.mouseUp()


def Screen_Shot(left=0, top=0, width=1920, height=1080):
    stc = mss.mss()
    scr = stc.grab({
        'left': left,
        'top': top,
        'width': width,
        'height': height
    })

    img = np.array(scr)
    img = cv2.cvtColor(img, cv2.IMREAD_COLOR)

    return img


def Quit():
    print(Fore.GREEN + "PokeMMOBot Closed\n")
    os._exit(os.EX_OK)


shell = win32com.client.Dispatch("WScript.Shell")

def find_loc(start_loc, end_loc):
    print(f"Input: start={start_loc}, end={end_loc}")
    start = start_loc
    end = end_loc

    scale_factor = 1920 / 1080
    print(f"scale_factor={scale_factor}")
    
    if start[0] % 2 == 0:
        print(f"start[0]={start[0]} is even")
        pass
    else:
        print(f"start[0]={start[0]} is odd, subtracting 1")
        start = (start[0] - 1, start[1])
    if end[0] % 2 == 0:
        print(f"end[0]={end[0]} is even")
        pass
    else:
        print(f"end[0]={end[0]} is odd, subtracting 1")
        end = (end[0] - 1, end[1])
        
    start = (start[0], int(start[1] / scale_factor))
    end = (end[0], int(end[1]/scale_factor))
    
    print(f"Output: start={start}, end={end}")
    return start, end


def focus_pokw():
    win = []
    winNum = 0
    for x in pyautogui.getAllWindows():
        win.append(x.title)
        winNum = winNum+1
    for q in range(winNum):
        if len(win[q]) == 7:
            print(win[q])
            shell.AppActivate(win[q])
            break


def Template_Match(needle, haystack):
    img = cv2.imread(os.path.join(img_path, needle), cv2.COLOR_BGR2GRAY)

    result_try = cv2.matchTemplate(haystack, img, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result_try)
    print(max_loc, max_val)
    return (max_loc, max_val)


def locate_image(image, path):
    img = os.path.join(path, image)
    start = pyautogui.locateCenterOnScreen(img, region=(
        0, 0, 1920, 1080), grayscale=True, confidence=0.80)
    return start

def Click_Location(x, y, wait=0):
    pydirectinput.moveTo(x, y)
    pydirectinput.mouseDown()
    time.sleep(wait)
    pydirectinput.mouseUp()


def Screen_Shot(left=0, top=0, width=1920, height=1080):
    stc = mss.mss()
    scr = stc.grab({
        'left': left,
        'top': top,
        'width': width,
        'height': height
    })

    img = np.array(scr)
    img = cv2.cvtColor(img, cv2.IMREAD_COLOR)

    return img


def Quit():
    print(Fore.GREEN + "PokeMMOBot Closed\n")
    os._exit(os.EX_OK)


# keyboard.add_hotkey("B", Quit)
