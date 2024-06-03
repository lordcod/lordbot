import time
import pyautogui
import random

pos = ()
time_place = 0

while True:
    np = pyautogui.position()
    if np == pos:
        time_place += 1
    if time_place >= 15:
        width, height = pyautogui.size()
        posx, posy = random.randint(0, width), random.randint(0, height)
        pyautogui.moveTo(posx, posy, duration=1)
        pyautogui.click()
        time_place = 0
    pos = np
    time.sleep(1)
