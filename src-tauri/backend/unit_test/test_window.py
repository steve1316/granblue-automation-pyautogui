import cv2 as cv
import numpy as np
import pyautogui

from utils.image_utils_v2 import ImageUtils
from bot.window import Window
from bot.game import Game
from utils.settings import Settings
from utils.mouse_utils import MouseUtils as mouse
from bot.combat_mode_v2 import CombatMode as combat

def test_find_all():
    print(sorted(ImageUtils.find_all("home", hide_info=True)))
    print(sorted(ImageUtils.find_all("home_back")))

# stwh = tuple of start, top , width , height
def visualize(list_of_stwh):
    frame = pyautogui.screenshot(region=(0,0,1920,1080))
    img = cv.cvtColor(np.array(frame), cv.COLOR_BGR2RGB)
    color = (255, 0, 0)
    for stwh in list_of_stwh:
        s, t, w, h = stwh
        img = cv.rectangle(img, (s,t), (s+w,t+h), color, 2)

    img = cv.resize(img, (1280, 720))

    cv.imshow("debug", img)
    cv.waitKey(0)
    
    # closing all open windows
    cv.destroyAllWindows()

def test_find_summon():

    s,t=ImageUtils.find_summon(Settings.summon_list, Settings.summon_element_list)
    w,h=mouse._randomize_point(s,t, image_name="template_support_summon")
    
    visualize([(s,t,w,h)])

def test_calibrate():
    stwh = [(Window.start, Window.top, Window.width, Window.height)]
    if Window.sub_start != None:
        stwh.append(
            (Window.sub_start, Window.sub_top, Window.sub_width, Window.sub_height)
        )
    visualize(stwh)

def test_find_button() :
    
    stwh = []
    s,t=ImageUtils.find_button("ok")
    w,h=mouse._randomize_point(s,t,"ok")
    if None not in (s,t):
        stwh.append(
            (s,t ,w-s, h-t)
        )
    visualize(stwh)

def test_character_selector():

    stwh = []
    w,h = ImageUtils.get_button_dimensions("template_character")
    for i in range(1,5):
        x,y = combat._select_char(i-1)
        stwh.append(
            (x,y,w,h)
        )
    visualize(stwh)

def test_skill_selector():

    # stwh = []
    # w,h = ImageUtils.get_button_dimensions("template_skill")
    for i in range(1,2):
        # x,y = combat._select_character(1,[1,2,3,4])
        combat._select_character(0,[1,2,3,4])
        # stwh.append(
        #     (x,y,w,h)
        # )
    # visualize(stwh)


Window.calibrate(display_info_check=True)
# test_calibrate()
Window.goto("https://www.google.com")