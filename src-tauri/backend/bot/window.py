import cv2
from PIL import Image
from typing import List, Tuple
from utils.settings import Settings
from pyautogui import size as get_screen_size, hold, screenshot, click , press
import pyautogui as pya
from utils.message_log import MessageLog as Log
from utils.mouse_utils import MouseUtils as mouse
from time import sleep
from pyperclip import paste, copy
import numpy as np

class Window():

    start: int = None
    top: int = None
    width: int = None
    height: int = None

    sub_start: int = None
    sub_top: int = None
    sub_width: int = None
    sub_height: int = None

    BROWSER_TOP_COLOR = (53, 54, 58)
    calibration_complete: bool = False
    additional_calibration_required: bool = False
    party_selection_first_run: bool = True
    


    @staticmethod
    def goto(url: str, is_sub: bool = False, pattern:str = "_") -> None:
        """
        Args:
            is_sub: if use sub window
            pattern: if match, will not go to the url
        """
        if is_sub:
            mouse.move_to(Window.sub_start+160, Window.sub_top-55)
        else:
            mouse.move_to(Window.start+160, Window.top-55)
        click()
        sleep(.03)
        with hold('ctrl'):
            press(['a', 'c'])
        if paste() != url and not paste().startswith(pattern):
            copy(url)
            pya.hotkey('ctrl', 'v')
            sleep(.03)
            press('enter')

    @staticmethod
    def sub_prepare_loot() -> None:
        """ prepare the support window to be ready to claim loot
        """
        Window.goto("https://game.granbluefantasy.jp/#quest/index",
                    is_sub=True)

    @staticmethod
    def reload(is_sub: bool = False, is_focus: bool = True) -> None:
        if not is_focus:
            if is_sub:
                mouse.move_to(Window.sub_start+160, Window.sub_top-55)
            elif not is_focus:
                mouse.move_to(Window.start+160, Window.top-55)
            click()

        pya.keyDown('f5')
        sleep(np.random.uniform(0.04,0.15))
        pya.keyUp('f5')

    @staticmethod
    def calibrate(display_info_check: bool = False) -> None:
        """Calibrate the game window for fast and accurate image matching.

        Args:
            display_info_check: Displays the screen size and the dimensions of the bot window.
        """
        from utils.image_utils import ImageUtils

        Log.print_message("\n[INFO] Calibrating the dimensions of the window...")
        # sort coordinate from left to right
        home_bttn_coords = sorted(ImageUtils.find_all("home", hide_info=True))
        calibration_left = sorted(ImageUtils.find_all("calibration_left", hide_info=True))
        calibration_right = sorted(ImageUtils.find_all("calibration_right", hide_info=True))
        
        if len(calibration_right) != len(calibration_left):
            raise RuntimeError(
                "Calibration of window dimensions failed. Some window is partially visible")
        if len(calibration_right) == 0:
            raise RuntimeError(
                "Calibration of window dimensions failed. Is the Home button on the bottom bar visible?")
        if len(calibration_left) == 0:
            raise RuntimeError(
                "Calibration of window dimensions failed. Is the back button visible on the screen?")
        if len(calibration_right) > 2:
            raise RuntimeError(
                "Calibration of window dimensions failed. maximum window is 2")
        # Save the location of the "Home" button at the bottom of the bot window.
        Settings.home_button_location = home_bttn_coords[0]
        screen_w, screen_h = get_screen_size()

        if not Settings.static_window:
            Log.print_message("[WARNING] V2 must use static window, ignoring settings and proceding...")
        
        calibraion_window = list(zip(calibration_left, calibration_right))

        img = screenshot(region=(0,0, screen_w, screen_h))

        left_width, bar_height = ImageUtils.get_button_dimensions("calibration_left")
        right_width, _ = ImageUtils.get_button_dimensions("calibration_right")
        for win_idx, win in enumerate(calibraion_window):
            # get back the top right coordinates
            (left_x, left_y), (right_x, _) = win
            left_x -= left_width//2
            left_y -= bar_height//2
            right_x -= right_width//2
            # serach up to find color
            for j in range (left_y, 3, -1):
                # check if there are 3 consecutive pixel that match the color of browser top
                if img.getpixel((left_x+2, j)) == img.getpixel((left_x+2, j-1))\
                    == img.getpixel((left_x+2, j-2)) == Window.BROWSER_TOP_COLOR:

                    if win_idx==0:
                        Window.start = left_x
                        Window.top = j+1
                        Window.width = right_x + right_width - Window.start
                        Window.height = left_y + bar_height - Window.top
                    else:
                        Window.sub_start = left_x 
                        Window.sub_top = j+1
                        Window.sub_width = right_x + right_width - Window.sub_start
                        Window.sub_height = left_y + bar_height - Window.sub_top
                    break
            else:
                raise RuntimeError("Cannot find consecutive color pixels on the top of browser!")
            

        ImageUtils.update_window_dimensions(
            Window.start,
            Window.top,
            Window.width,
            Window.height)
        
        if Window.start != None and Window.top != None and \
            Window.width != None and Window.height != None:
            Log.print_message("[SUCCESS] Dimensions of the first window has been successfully recalibrated.")
        else:
            raise RuntimeError("Calibration of window dimensions failed")
        if Window.sub_start != None and Window.sub_top != None and \
            Window.sub_width != None and Window.sub_height != None:
            Log.print_message("[SUCCESS] Dimensions of the second window has been successfully recalibrated.")
        else:
            Log.print_message("[INFO] Second Window is not presented")

        
        if display_info_check:
            Log.print_message("\n**********************************************************************")
            Log.print_message("**********************************************************************")
            Log.print_message(f"[INFO] Screen Size: {get_screen_size()}")
            Log.print_message(f"[INFO] Game Window Dimensions: Region({Window.start}, {Window.top}, {Window.width}, {Window.height})")
            Log.print_message(f"[INFO] Game Sub-Window Dimensions: Region({Window.sub_start}, {Window.sub_top}, {Window.sub_width}, {Window.sub_height})")
            Log.print_message("**********************************************************************")
            Log.print_message("**********************************************************************")