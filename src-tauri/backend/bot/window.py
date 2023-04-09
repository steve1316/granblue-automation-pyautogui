import cv2
from PIL import Image
from typing import List, Tuple
from utils.settings import Settings
from pyautogui import size as get_screen_size, hold, screenshot, click, write, press
import pyautogui as pya
from utils.message_log import MessageLog as Log
from utils.mouse_utils import MouseUtils as mouse
from time import sleep
from pyperclip import paste, copy

class Window():

    start: int = None
    top: int = None
    width: int = None
    height: int = None

    sub_start: int = None
    sub_top: int = None
    sub_width: int = None
    sub_height: int = None

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
    def reload(is_sub: bool = False) -> None:
        if is_sub:
            mouse.move_to(Window.sub_start+160, Window.sub_top-55)
        else:
            mouse.move_to(Window.start+160, Window.top-55)
        click()
        press('f5')

    @staticmethod
    def calibrate(display_info_check: bool = False) -> None:
        """Calibrate the game window for fast and accurate image matching.

        Args:
            display_info_check: Displays the screen size and the dimensions of the bot window.
        """
        from utils.image_utils import ImageUtils

        # Save the location of the "Home" button at the bottom of the bot window.

        Log.print_message("\n[INFO] Calibrating the dimensions of the window...")
        # sort coordinate from left to right
        home_bttn_coords = sorted(ImageUtils.find_all("home", hide_info=True))
        back_bttn_coords = sorted(ImageUtils.find_all("home_back", hide_info=True))
        
        if len(home_bttn_coords) != len(back_bttn_coords):
            raise RuntimeError(
                "Calibration of window dimensions failed. Some window is partially visible")
        if len(home_bttn_coords) == 0:
            raise RuntimeError(
                "Calibration of window dimensions failed. Is the Home button on the bottom bar visible?")
        if len(back_bttn_coords) == 0:
            raise RuntimeError(
                "Calibration of window dimensions failed. Is the back button visible on the screen?")
        if len(home_bttn_coords) > 2:
            raise RuntimeError(
                "Calibration of window dimensions failed. maximum window is 2")

        screen_w, screen_h = get_screen_size()

        if Settings.static_window:
            Log.print_message("[INFO] Using static window configuration...")
            
            # calibration base on the side bar
            img = screenshot(region=(0,0, screen_w, screen_h))
            for win, coord in enumerate(back_bttn_coords):
                for i in range (coord[0], 2, -1):
                    # search left to find 3 consecutive pixels which is the same as side bar
                    if img.getpixel((i, coord[1])) == img.getpixel((i-1, coord[1])) == \
                       img.getpixel((i-2, coord[1])) == (31,31,31):
                        # serach up until the color is different
                        for j in range (coord[1], 0, -1):
                            if img.getpixel((i, j)) != (31,31,31):
                                if win==0:
                                    Window.start = i+1
                                    Window.top = j+1
                                    Window.width = home_bttn_coords[win][0] - Window.start + 50
                                    Window.height = back_bttn_coords[win][1] - Window.top + 22
                                else:
                                    Window.sub_start = i+1
                                    Window.sub_top = j+1
                                    Window.sub_width = home_bttn_coords[win][0] - Window.sub_start + 50
                                    Window.sub_height = back_bttn_coords[win][1] - Window.sub_top + 22
                                break
                        break
        else:
            Window.start  = 0
            Window.top  = 0
            Window.width = screen_h
            Window.height = screen_w

            Window.sub_left = 0
            Window.sub_top = 0
            Window.sub_width = screen_h
            Window.sub_height = screen_w

        ImageUtils.update_window_dimensions(
            Window.start,
            Window.top,
            Window.width,
            Window.height)
        
        if Window.start != None and Window.top != None and \
            Window.width != None and Window.height != None:
            Log.print_message("[SUCCESS] Dimensions of the first window has been successfully recalibrated.")
        else:
            raise RuntimeError("Calibration of window dimensions failed, possbily due to side bar")
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