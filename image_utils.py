import pyautogui
import cv2  # Needed for confidence argument. Comes from opencv-python package.
import time
import os

import mouse_utils


class ImageUtils:
    """
    Provides the utility functions needed to perform mouse-related actions.

    Attributes
    ----------
    window_left (int, optional): The top left corner of the region for image matching. Defaults to None.

    window_top (int, optional): The top right corner of the region for image matching. Defaults to None.

    window_width (int, optional): The bottom left corner of the region for image matching. Defaults to None.

    window_height (int, optional): The bottom right corner of the region for image matching. Defaults to None.

    debug_mode (bool, optional): Optional flag to print debug messages related to this class. Defaults to True.

    Methods
    -------
    find_button(button_name, confirm_location_check, tries, sleep_time):
        Find the location of the specified button.

    confirm_location(location_name, tries, sleep_time):
        Confirm the bot's position by searching for the header image.
    """

    def __init__(self, window_left: int = None, window_top: int = None, window_width: int = None, window_height: int = None, debug_mode: bool = False):
        super().__init__()

        self.window_left = window_left
        self.window_top = window_top
        self.window_width = window_width
        self.window_height = window_height
        self.debug_mode = debug_mode
        self.mouse_tools = mouse_utils.MouseUtils(debug_mode=self.debug_mode)

        # The amount of time to pause after each call to pyautogui.
        pyautogui.PAUSE = 1.0

    def find_button(self, button_name: str, custom_confidence: float = 0.9, grayscale_check: bool = False, confirm_location_check: bool = False, tries: int = 10, sleep_time: int = 1):
        """Find the location of the specified button.

        Args:
            button_name (str): Name of the button image file in the images/buttons/ folder.
            custom_confidence (float, optional): Accuracy threshold for matching. Defaults to 0.9.
            grayscale_check (bool, optional): Match by converting screenshots to grayscale. This may lead to inaccuracies however. Defaults to False.
            confirm_location_check (bool, optional): Check to see if the location is correct. Defaults to False.
            tries (int, optional): Number of tries before failing. Defaults to 10.
            sleep_time (int, optional): Number of seconds for execution to pause for in cases of image match fail. Defaults to 1.

        Returns:
            location (int, int): Tuple of coordinates of where the center of the button is located if image matching was successful. Otherwise, return None.
        """
        if(self.debug_mode):
            print(
                f"\n[DEBUG] Now attempting to find the {button_name.upper()} Button from current position...")

        location = None

        # Loop until location is found or return None if image matching failed.
        while (location == None):
            if(self.window_left != None or self.window_top != None or self.window_width != None or self.window_height != None):
                location = pyautogui.locateCenterOnScreen(f"images/buttons/{button_name.lower()}.png", confidence=custom_confidence, grayscale=grayscale_check, region=(
                    self.window_left, self.window_top, self.window_width, self.window_height))
            else:
                location = pyautogui.locateCenterOnScreen(
                    f"images/buttons/{button_name.lower()}.png", confidence=custom_confidence, grayscale=grayscale_check)

            if (location == None):
                tries -= 1
                if (tries <= 0):
                    print(
                        f"[ERROR] Failed to find the {button_name.upper()} Button.")
                    return None

                if(self.debug_mode):
                    print(
                        f"[DEBUG] Could not locate the {button_name.upper()} Button. Trying again in {sleep_time} seconds...")

                time.sleep(sleep_time)

        if(self.debug_mode):
            print(
                f"[SUCCESS] Found the {button_name.upper()} Button at {location}.")

        if (confirm_location_check):
            self.confirm_location(button_name)

        return location

    def find_summon(self, summon_name: str, home_button_x: int, home_button_y: int, custom_confidence: float = 0.9, grayscale_check: bool = False, tries: int = 3, sleep_time: int = 1):
        """Find the location of the specified summon. Will attempt to scroll the screen down to see more Summons if the initial screen position yielded no matches.

        Args:
            summon_name (str): Name of the summon image file in the images/summons/ folder.
            home_button_x (int): X coordinate of where the center of the Home Button is.
            home_button_y (int): Y coordinate of where the center of the Home Button is.
            custom_confidence (float, optional): Accuracy threshold for matching. Defaults to 0.9.
            grayscale_check (bool, optional): Match by converting screenshots to grayscale. This may lead to inaccuracies however. Defaults to False.
            tries (int, optional): Number of tries before failing. Defaults to 3.
            sleep_time (int, optional): Number of seconds for execution to pause for in cases of image match fail. Defaults to 1.

        Returns:
            summon_location (int, int): Tuple of coordinates of where the center of the summon is located if image matching was successful. Otherwise, return None.
        """
        if(self.debug_mode):
            print(
                f"\n[DEBUG] Now attempting to find {summon_name.upper()} Summon...")

        summon_location = None

        while (summon_location == None):
            summon_location = pyautogui.locateCenterOnScreen(f"images/summons/{summon_name.lower()}.png", confidence=custom_confidence, grayscale=grayscale_check, region=(
                self.window_left, self.window_top, self.window_width, self.window_height))
            if (summon_location == None):
                if(self.debug_mode):
                    print(
                        f"[DEBUG] Could not locate the {summon_name.upper()} Summon. Trying again in {sleep_time} seconds...")

                tries -= 1
                if (tries == 0):
                    print(
                        f"[ERROR] Could not find {summon_name.upper()} Summon.")
                    return None

                # If matching failed, scroll the screen down to see more Summons.
                self.mouse_tools.scroll_screen(
                    home_button_x, home_button_y - 50, -400)

                time.sleep(sleep_time)

        if(self.debug_mode):
            print(
                f"[SUCCESS] Found the {summon_name.upper()} Summon at {summon_location}.")

        return summon_location

    def find_dialog(self, dialog_name: str, attack_button_x: int, attack_button_y: int, custom_confidence: float = 0.9, grayscale_check: bool = False, tries: int = 10, sleep_time: int = 1):
        """Attempt to find the specified dialog window.

        Args:
            dialog_name (str): The name of the image file's name of the dialog window.
            attack_button_x (int): X coordinate of where the center of the Attack Button is.
            attack_button_y (int): Y coordinate of where the center of the Attack Button is.
            custom_confidence (float, optional): Accuracy threshold for matching. Defaults to 0.9.
            grayscale_check (bool, optional): Match by converting screenshots to grayscale. This may lead to inaccuracies however. Defaults to False.
            tries (int, optional): Number of tries before failing. Defaults to 10.
            sleep_time (int, optional): Number of seconds for execution to pause for in cases of image match fail. Defaults to 1.

        Returns:
            dialog_location (int, int): Tuple of coordinates on the screen for where the match's center was found. Otherwise, return None.
        """
        dialog_location = None

        while (dialog_location == None):
            dialog_location = pyautogui.locateCenterOnScreen(f"images/dialogs/{dialog_name.lower()}.png", confidence=custom_confidence, grayscale=grayscale_check, region=(
                attack_button_x - 350, attack_button_y + 28, attack_button_x - 264, attack_button_y + 50))

            if (dialog_location == None):
                tries -= 1
                if (tries <= 0):
                    return None

                if(self.debug_mode):
                    print(
                        f"[DEBUG] Locating {dialog_name.upper()} Dialog failed. Trying again in {sleep_time} seconds...")

                time.sleep(sleep_time)

        if(self.debug_mode):
            print(
                f"[SUCCESS] Found the {dialog_name.upper()} Dialog at {dialog_location}.")

        return dialog_location

    def confirm_location(self, location_name: str, custom_confidence: float = 0.9, grayscale_check: bool = False, tries: int = 10, sleep_time: int = 1):
        """Confirm the bot's position by searching for the header image.

        Args:
            location_name (str): Name of the header image file in the images/headers/ folder.
            custom_confidence (float, optional): Accuracy threshold for matching. Defaults to 0.9.
            grayscale_check (bool, optional): Match by converting screenshots to grayscale. This may lead to inaccuracies however. Defaults to False.
            tries (int, optional): Number of tries before failing. Defaults to 10.
            sleep_time (int, optional): Number of seconds for execution to pause for in cases of image match fail. Defaults to 1.

        Returns:
            (bool): True if current location is confirmed. Otherwise, False.
        """
        if(self.debug_mode):
            print(
                f"\n[DEBUG] Now attempting to confirm the bot's location at the {location_name.upper()} Screen...")

        location = None

        # Loop until location is found or return False if image matching failed.
        while (location == None):
            if(self.window_left != None or self.window_top != None or self.window_width != None or self.window_height != None):
                location = pyautogui.locateCenterOnScreen(f"images/headers/{location_name}Header.png", confidence=custom_confidence, grayscale=grayscale_check, region=(
                    self.window_left, self.window_top, self.window_width, self.window_height))
            else:
                location = pyautogui.locateCenterOnScreen(
                    f"images/headers/{location_name}Header.png", confidence=custom_confidence, grayscale=grayscale_check)

            if (location == None):
                tries -= 1
                if (tries == 0):
                    print(
                        f"[ERROR] Failed to confirm the bot's location at the {location_name.upper()} Screen.")
                    return False

                if(self.debug_mode):
                    print(
                        f"[DEBUG] Could not confirm the bot's location at the {location_name.upper()} Screen. Trying again in {sleep_time} seconds...")

                time.sleep(sleep_time)

        if(self.debug_mode):
            print(
                f"[SUCCESS] Bot's location is at {location_name.upper()} Screen.")

        return True

    def find_all(self, image_name: str, custom_region: tuple[int, int, int, int] = None, custom_confidence: float = 0.9, grayscale_check: bool = False):
        """Find the specified image file by searching through all subfolders and locating all occurrences on the screen.

        Args:
            image_name (str): Name of the image file in the /images/ folder.
            custom_region (tuple[int, int, int, int]): Region tuple of integers to look for a occurrence in. Defaults to None.
            custom_confidence (float, optional): Accuracy threshold for matching. Defaults to 0.9.
            grayscale_check (bool, optional): Match by converting screenshots to grayscale. This may lead to inaccuracies however. Defaults to False.

        Returns:
            locations (list[Box]): List of Boxes where each occurrence is found on the screen. If no occurrence was found, return a empty list. Or if the file does not exist, return None.
        """
        # Find file by searching subfolders.
        dir_path = os.path.dirname(os.path.realpath(__file__))
        for root, dirs, files in os.walk(f"{dir_path}/images/"):
            for file in files:
                file_name = os.path.splitext(str(file))[0]
                if (file_name.lower() == image_name.lower()):
                    if(self.window_left != None or self.window_top != None or self.window_width != None or self.window_height != None and custom_region == None):
                        locations = list(pyautogui.locateAllOnScreen(
                            f"{root}/{image_name}.png", confidence=custom_confidence, grayscale=grayscale_check, region=(
                                self.window_left, self.window_top, self.window_width, self.window_height)))
                    elif(self.window_left != None or self.window_top != None or self.window_width != None or self.window_height != None and custom_region != None):
                        locations = list(pyautogui.locateAllOnScreen(
                            f"{root}/{image_name}.png", confidence=custom_confidence, grayscale=grayscale_check, region=custom_region))
                    else:
                        locations = list(pyautogui.locateAllOnScreen(
                            f"{root}/{image_name}.png", confidence=custom_confidence, grayscale=grayscale_check))

                    if (self.debug_mode and len(locations) != 0):
                        for location in locations:
                            print("[INFO] Occurrence found at: ", location)

                    return locations

        print(
            f"[ERROR] Given file name does not exist in /images/ folder.")

        return None
