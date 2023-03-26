import cv2 as cv
import numpy as np
import pyautogui

from utils.image_utils import ImageUtils
from bot.window import Window

def check_image_utils():
    print(sorted(ImageUtils.find_all("home", hide_info=True)))
    print(sorted(ImageUtils.find_all("home_back")))

def check_window():
    Window.calibrate_window(display_info_check=True)

# stwh = tuple of start, top , width , height
def visualize(list_of_stwh):
    frame = pyautogui.screenshot(region=(0,0,1920,1080))
    img = cv.cvtColor(np.array(frame), cv.COLOR_BGR2RGB)
    color = (255, 0, 0)
    for stwh in list_of_stwh:
        s, t, w, h = stwh
        img = cv.rectangle(img, (s,t), (s+w,t+h), color, 2)
    # Window name in which image is displayed
    img = cv.resize(img, (1280, 720))

    cv.imshow("debug", img)
    cv.waitKey(0)
    
    # closing all open windows
    cv.destroyAllWindows()

def test_calibrate() :
    check_window()
    stwhs = [(Window.start, Window.top, Window.width, Window.height),
             (Window.start+160, Window.top-55, 10, 10)
             ]
    if Window.sub_start != None:
        stwhs.append(
            (Window.sub_start, Window.sub_top, Window.sub_width, Window.sub_height)
        )
    visualize(stwhs)

test_calibrate()