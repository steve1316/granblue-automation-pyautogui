import datetime
import multiprocessing
import os
import time
from datetime import date
from typing import List, Tuple

import easyocr
import pyautogui
from PIL import Image
from guibot.fileresolver import FileResolver
from guibot.guibot import GuiBot
from playsound import playsound


class ImageUtils:
    """
    Provides the utility functions needed to perform image-related actions. This utility will alternate between PyAutoGUI and GuiBot to find the template image.

    Attributes
    ----------
    game (bot.Game): The Game object.

    debug_mode (bool, optional): Optional flag to print debug messages related to this class. Defaults to False.

    """

    def __init__(self, game, debug_mode: bool = False):
        super().__init__()

        self._game = game
        self._debug_mode = debug_mode

        # The dimensions are set in calibrate_game_window() in Game class.
        self._window_left = None
        self._window_top = None
        self._window_width = None
        self._window_height = None

        # Initialize the following for saving screenshots.
        self._image_number = 0
        self._new_folder_name = None

        # Initialize GuiBot object for image matching.
        self._guibot = GuiBot()
        self._file_resolver = FileResolver()

        # Initialize EasyOCR for text detection.
        self._game.print_and_save(f"\n[INFO] Initializing EasyOCR reader. This may take a few seconds...")
        self._reader = easyocr.Reader(["en"], gpu = True)
        self._game.print_and_save(f"[INFO] EasyOCR reader initialized.")

        # Used for skipping selecting the Summon Element every time on repeated runs.
        self._summon_selection_first_run = True
        self._summon_selection_same_element = False

    def update_window_dimensions(self, window_left: int, window_top: int, window_width: int, window_height: int):
        """Updates the window dimensions for PyAutoGUI to perform faster operations in.

        Args:
            window_left (int): The x-coordinate of the left edge of the region for image matching.
            window_top (int): The y-coordinate of the top edge of the region for image matching.
            window_width (int): The width of the region for image matching.
            window_height (int): The height of the region for image matching.

        Returns:
            None
        """
        self._window_left = window_left
        self._window_top = window_top
        self._window_width = window_width
        self._window_height = window_height

        return None

    def get_window_dimensions(self):
        """Get the window dimensions as a Tuple of 4 integers.

        Returns:
            (int, int, int, int): A Tuple of 4 integers consisting of (window_left, window_top, window_width, window_height).
        """
        return self._window_left, self._window_top, self._window_width, self._window_height

    def _clear_memory_guibot(self):
        """Eliminates the memory leak caused by GuiBot by deleting the GuiBot object and reinitializing it. This is required before or after every single GuiBot operation, else you will run
        into cv::OutOfMemoryError.

        Returns:
            None
        """
        del self._guibot
        self._guibot = GuiBot()
        return None

    def find_button(self, button_name: str, custom_confidence: float = 0.9, grayscale_check: bool = False, confirm_location_check: bool = False, tries: int = 3, sleep_time: int = 1,
                    suppress_error: bool = False):
        """Find the location of the specified button.

        Args:
            button_name (str): Name of the button image file in the /images/buttons/ folder.
            custom_confidence (float, optional): Accuracy threshold for matching. Defaults to 0.9.
            grayscale_check (bool, optional): Match by converting screenshots to grayscale. This may lead to inaccuracies however. Defaults to False.
            confirm_location_check (bool, optional): Check to see if the location is correct. Defaults to False.
            tries (int, optional): Number of tries before failing. Defaults to 3.
            sleep_time (int, optional): Number of seconds for execution to pause for in cases of image match fail. Defaults to 1.
            suppress_error (bool, optional): Suppresses template matching error if True. Defaults to False.

        Returns:
            location (int, int): Tuple of coordinates of where the center of the button is located if image matching was successful. Otherwise, return None.
        """
        button_location = None
        guibot_check = False
        while button_location is None:
            if self._window_left is not None or self._window_top is not None or self._window_width is not None or self._window_height is not None:
                button_location = pyautogui.locateCenterOnScreen(f"images/buttons/{button_name.lower()}.png", confidence = custom_confidence, grayscale = grayscale_check,
                                                                 region = (self._window_left, self._window_top, self._window_width, self._window_height))
            else:
                button_location = pyautogui.locateCenterOnScreen(f"images/buttons/{button_name.lower()}.png", confidence = custom_confidence, grayscale = grayscale_check)

            if button_location is None:
                # Use GuiBot to template match if PyAutoGUI failed.    
                self._file_resolver.add_path("images/buttons/")
                self._clear_memory_guibot()
                button_location = self._guibot.exists(f"{button_name.lower()}")
                if button_location is None:
                    tries -= 1
                    if tries <= 0:
                        if not suppress_error:
                            self._game.print_and_save(f"[WARNING] Failed to find the {button_name.upper()} button.")
                        return None

                    if self._debug_mode:
                        self._game.print_and_save(f"[WARNING] Could not locate the {button_name.upper()} button. Trying again in {sleep_time} seconds...")

                    time.sleep(sleep_time)
                else:
                    guibot_check = True

        # If the location was successfully found using GuiBot, convert the Match object to a Location object.
        if guibot_check:
            button_location = (button_location.target.x, button_location.target.y)

        if self._debug_mode:
            self._game.print_and_save(f"[SUCCESS] Found the {button_name.upper()} button at {button_location}.")

        if confirm_location_check:
            self.confirm_location(button_name)

        return button_location

    def confirm_location(self, location_name: str, custom_confidence: float = 0.9, grayscale_check: bool = False, tries: int = 3, sleep_time: int = 1):
        """Confirm the position of the bot by searching for the header image.

        Args:
            location_name (str): Name of the header image file in the /images/headers/ folder.
            custom_confidence (float, optional): Accuracy threshold for matching. Defaults to 0.9.
            grayscale_check (bool, optional): Match by converting screenshots to grayscale. This may lead to inaccuracies however. Defaults to False.
            tries (int, optional): Number of tries before failing. Defaults to 3.
            sleep_time (int, optional): Number of seconds for execution to pause for in cases of image match fail. Defaults to 1.

        Returns:
            (bool): True if current location is confirmed. Otherwise, False.
        """
        header_location = None
        while header_location is None:
            if self._window_left is not None or self._window_top is not None or self._window_width is not None or self._window_height is not None:
                header_location = pyautogui.locateCenterOnScreen(f"images/headers/{location_name.lower()}_header.png", confidence = custom_confidence, grayscale = grayscale_check,
                                                                 region = (self._window_left, self._window_top, self._window_width, self._window_height))
            else:
                header_location = pyautogui.locateCenterOnScreen(f"images/headers/{location_name.lower()}_header.png", confidence = custom_confidence, grayscale = grayscale_check)

            if header_location is None:
                # Use GuiBot to template match if PyAutoGUI failed.
                self._file_resolver.add_path("images/headers/")
                self._clear_memory_guibot()
                header_location = self._guibot.exists(f"{location_name.lower()}_header")
                if header_location is None:
                    tries -= 1
                    if tries <= 0:
                        # If tries ran out, return False.
                        if self._debug_mode:
                            self._game.print_and_save(f"[WARNING] Failed to confirm the bot's location at {location_name.upper()}.")
                        return False

                    if self._debug_mode:
                        self._game.print_and_save(f"[WARNING] Could not confirm the bot's location at {location_name.upper()}. Trying again in {sleep_time} seconds...")

                    time.sleep(sleep_time)

        if self._debug_mode:
            self._game.print_and_save(f"[SUCCESS] Bot's current location is at {location_name.upper()}.")

        return True

    def find_summon(self, summon_list: List[str], summon_element_list: List[str], home_button_x: int, home_button_y: int, custom_confidence: float = 0.9, grayscale_check: bool = False,
                    suppress_error: bool = False):
        """Find the location of the specified Summon. Will attempt to scroll the screen down to see more Summons if the initial screen position yielded no matches.

        Args:
            summon_list (List[str]): List of names of the Summon image's file name in /images/summons/ folder.
            summon_element_list (List[str]): List of names of the Summon element image file in the /images/buttons/ folder.
            home_button_x (int): X coordinate of where the center of the Home Button is.
            home_button_y (int): Y coordinate of where the center of the Home Button is.
            custom_confidence (float, optional): Accuracy threshold for matching. Defaults to 0.9.
            grayscale_check (bool, optional): Match by converting screenshots to grayscale. This may lead to inaccuracies however. Defaults to False.
            suppress_error (bool, optional): Suppresses template matching error if True. Defaults to False.

        Returns:
            summon_location (int, int): Tuple of coordinates of where the center of the Summon is located if image matching was successful. Otherwise, return None.
        """
        if self._debug_mode:
            self._game.print_and_save(f"[DEBUG] Received the following list of Summons to search for: {str(summon_list)}")
            self._game.print_and_save(f"[DEBUG] Received the following list of Elements: {str(summon_element_list)}")

        last_summon_element = ""
        summon_location = None
        guibot_check = False
        summon_index = 0

        # Make sure that the bot is at the Summon Selection screen.
        tries = 3
        while not self.confirm_location("select_a_summon"):
            self._game.find_and_click_button('reload')
            tries -= 1
            if tries <= 0 and self.confirm_location("select_a_summon", tries = 1) is False:
                raise Exception("Could not reach the Summon Selection screen.")

        # Determine if all the summon elements are the same or not. This will influence whether or not the bot needs to change elements in repeated runs.
        self._summon_selection_same_element = all(element == summon_element_list[0] for element in summon_element_list)

        while summon_location is None:
            if self._summon_selection_first_run or self._summon_selection_same_element is False:
                current_summon_element = summon_element_list[summon_index]
                if current_summon_element != last_summon_element:
                    self._game.find_and_click_button(f"summon_{current_summon_element}")
                    last_summon_element = current_summon_element

                self._summon_selection_first_run = False

            summon_index = 0
            while summon_index <= len(summon_list):
                # Now try and find the Summon at the current index.
                if self._window_left is not None or self._window_top is not None or self._window_width is not None or self._window_height is not None:
                    summon_location = pyautogui.locateCenterOnScreen(f"images/summons/{summon_list[summon_index]}.png", confidence = custom_confidence, grayscale = grayscale_check,
                                                                     region = (self._window_left, self._window_top, self._window_width, self._window_height))
                else:
                    summon_location = pyautogui.locateCenterOnScreen(f"images/summons/{summon_list[summon_index]}.png", confidence = custom_confidence, grayscale = grayscale_check)

                if summon_location is None:
                    # Use GuiBot to template match if PyAutoGUI failed.
                    self._file_resolver.add_path("images/summons/")
                    self._clear_memory_guibot()
                    summon_location = self._guibot.exists(f"{summon_list[summon_index]}")

                    if summon_location is None:
                        if suppress_error is False:
                            self._game.print_and_save(f"[WARNING] Could not locate {summon_list[summon_index].upper()} Summon.")

                        if summon_index + 1 >= len(summon_list):
                            break
                        else:
                            summon_index += 1
                    else:
                        guibot_check = True
                        break
                else:
                    break

            # If the location was successfully found using GuiBot, convert the Match object to a Location object.
            if guibot_check:
                summon_location = (summon_location.target.x, summon_location.target.y)
                break
            elif summon_location is not None:
                break

            # If the bot reached the bottom of the page, scroll back up to the top and start searching for the next Summon.
            if self.find_button("bottom_of_summon_selection", tries = 1) is not None:
                self._game.print_and_save(f"[WARNING] Bot has reached the bottom of the page and found no suitable Summons. Resetting Summons now...")
                return None

            # If matching failed, scroll the screen down to see more Summons.
            self._game.mouse_tools.scroll_screen(home_button_x, home_button_y - 50, -700)

        self._game.print_and_save(f"[SUCCESS] Found {summon_list[summon_index].upper()} Summon at {summon_location}.")
        return summon_location

    def find_dialog(self, attack_button_x: int, attack_button_y: int, custom_confidence: float = 0.9, grayscale_check: bool = False, tries: int = 3, sleep_time: int = 1):
        """Attempt to find any Lyria/Vyrn dialog popups. Used during Combat Mode.

        Args:
            attack_button_x (int): X coordinate of where the center of the Attack Button is.
            attack_button_y (int): Y coordinate of where the center of the Attack Button is.
            custom_confidence (float, optional): Accuracy threshold for matching. Defaults to 0.9.
            grayscale_check (bool, optional): Match by converting screenshots to grayscale. This may lead to inaccuracies however. Defaults to False.
            tries (int, optional): Number of tries before failing. Defaults to 3.
            sleep_time (int, optional): Number of seconds for execution to pause for in cases of image match fail. Defaults to 1.

        Returns:
            (int, int): Tuple of coordinates on the screen for where the dialog popup's center was found. Otherwise, return None.
        """
        lyria_dialog_location = None
        vyrn_dialog_location = None
        guibot_check = False
        while lyria_dialog_location is None and vyrn_dialog_location is None:
            if self._window_left is not None or self._window_top is not None or self._window_width is not None or self._window_height is not None:
                lyria_dialog_location = pyautogui.locateCenterOnScreen(f"images/dialogs/dialog_lyria.png", confidence = custom_confidence, grayscale = grayscale_check,
                                                                       region = (attack_button_x - 350, attack_button_y + 28, attack_button_x - 264, attack_button_y + 50))
                vyrn_dialog_location = pyautogui.locateCenterOnScreen(f"images/dialogs/dialog_vyrn.png", confidence = custom_confidence, grayscale = grayscale_check,
                                                                      region = (attack_button_x - 350, attack_button_y + 28, attack_button_x - 264, attack_button_y + 50))
            else:
                lyria_dialog_location = pyautogui.locateCenterOnScreen(f"images/dialogs/dialog_lyria.png", confidence = custom_confidence, grayscale = grayscale_check)
                vyrn_dialog_location = pyautogui.locateCenterOnScreen(f"images/dialogs/dialog_vyrn.png", confidence = custom_confidence, grayscale = grayscale_check)

            if lyria_dialog_location is None and vyrn_dialog_location is None:
                # Use GuiBot to template match if PyAutoGUI failed.
                self._file_resolver.add_path("images/dialogs/")
                self._clear_memory_guibot()
                lyria_dialog_location = self._guibot.exists(f"dialog_lyria")
                self._clear_memory_guibot()
                vyrn_dialog_location = self._guibot.exists(f"dialog_vyrn")
                if lyria_dialog_location is None and vyrn_dialog_location is None:
                    tries -= 1
                    if tries <= 0:
                        if self._debug_mode:
                            self._game.print_and_save(f"[SUCCESS] There are no Lyria/Vyrn dialog popups detected.")
                        return None

                    if self._debug_mode:
                        self._game.print_and_save(f"[WARNING] Could not locate any Lyria/Vyrn dialog popups failed. Trying again in {sleep_time} seconds...")

                    time.sleep(sleep_time)
                else:
                    guibot_check = True

        # If the location was successfully found using GuiBot, convert the Match object to a Location object.
        if guibot_check:
            if lyria_dialog_location is not None:
                lyria_dialog_location = (lyria_dialog_location.target.x, lyria_dialog_location.target.y)
            else:
                vyrn_dialog_location = (vyrn_dialog_location.target.x, vyrn_dialog_location.target.y)

        if self._debug_mode:
            if lyria_dialog_location is not None:
                self._game.print_and_save(f"[SUCCESS] Found a Lyria dialog popup at {lyria_dialog_location}.")
            else:
                self._game.print_and_save(f"[SUCCESS] Found a Vyrn dialog popup at {vyrn_dialog_location}.")

        if lyria_dialog_location is not None:
            return lyria_dialog_location
        else:
            return vyrn_dialog_location

    def find_all(self, image_name: str, is_item: bool = False, custom_region: Tuple[int, int, int, int] = None, custom_confidence: float = 0.9, grayscale_check: bool = False, hide_info: bool = False):
        """Find the specified image file by locating all occurrences on the screen.

        Args:
            image_name (str): Name of the image file in the /images/buttons folder.
            is_item (bool, optional): Determines whether to search for the image file in the images/buttons/ or images/items/ folder. Defaults to False.
            custom_region (tuple[int, int, int, int], optional): Region tuple of integers to look for a occurrence in. Defaults to None.
            custom_confidence (float, optional): Accuracy threshold for matching. Defaults to 0.9.
            grayscale_check (bool, optional): Match by converting screenshots to grayscale. This may lead to inaccuracies however. Defaults to False.
            hide_info (bool, optional): Whether or not to print the matches' locations. Defaults to False.

        Returns:
            locations (list[Box]): List of Boxes where each occurrence is found on the screen. If no occurrence was found, return a empty list.
        """
        if is_item:
            folder_name = "items"
        else:
            folder_name = "buttons"

        if custom_region is None:
            locations = list(pyautogui.locateAllOnScreen(f"images/{folder_name}/{image_name}.png", confidence = custom_confidence, grayscale = grayscale_check))
        else:
            locations = list(pyautogui.locateAllOnScreen(f"images/{folder_name}/{image_name}.png", confidence = custom_confidence, grayscale = grayscale_check, region = custom_region))

        centered_locations = []
        if len(locations) != 0:
            for (index, location) in enumerate(locations):
                if index > 0:
                    # Filter out duplicate locations where they are 1 pixel away from each other.
                    if location[0] != (locations[index - 1][0] + 1) and location[1] != (locations[index - 1][1] + 1):
                        centered_locations.append(pyautogui.center(location))
                else:
                    centered_locations.append(pyautogui.center(location))

            if not hide_info:
                for location in centered_locations:
                    self._game.print_and_save(f"[INFO] Occurrence for {image_name.upper()} found at: " + str(location))
        else:
            if self._debug_mode:
                self._game.print_and_save(f"[DEBUG] Failed to detect any occurrences of {image_name.upper()} images.")

        return centered_locations

    def find_farmed_items(self, item_name: str, take_screenshot: bool = True):
        """Detect amounts of items gained according to the desired items specified.

        Args:
            item_name (str): Item to be found.
            take_screenshot (bool, optional): Takes a screenshot whenever matches were detected. Defaults to True.

        Returns:
            amount_farmed (int): Amount gained for the item.
        """
        self._file_resolver.add_path("images/items/")

        # List of items blacklisted from using GuiBot's built-in CV finder due to how similar looking they are. These items have to use my method using 
        # PyAutoGUI instead for the confidence argument from OpenCV as GuiBot does not have a confidence argument.
        blacklisted_items = ["Fire Orb", "Water Orb", "Earth Orb", "Wind Orb", "Light Orb", "Dark Orb",
                             "Red Tome", "Blue Tome", "Brown Tome", "Green Tome", "White Tome", "Black Tome",
                             "Hellfire Scroll", "Flood Scroll", "Thunder Scroll", "Gale Scroll", "Skylight Scroll", "Chasm Scroll",
                             "Jasper Scale", "Crystal Spirit", "Luminous Judgment", "Sagittarius Rune", "Sunlight Quartz",
                             "Shadow Silver", "Ifrit Anima", "Ifrit Omega Anima", "Cocytus Anima", "Cocytus Omega Anima",
                             "Vohu Manah Anima", "Vohu Manah Omega Anima", "Sagittarius Anima", "Sagittarius Omega Anima",
                             "Corow Anima", "Corow Omega Anima", "Diablo Anima", "Diablo Omega Anima", "Ancient Ecke Sachs",
                             "Ecke Sachs", "Ancient Auberon", "Auberon", "Ancient Perseus", "Perseus", "Ancient Nalakuvara",
                             "Nalakuvara", "Ancient Bow of Artemis", "Bow of Artemis", "Ancient Cortana", "Cortana"]

        lite_blacklisted_items = ["Infernal Garnet", "Frozen Hell Prism", "Evil Judge Crystal", "Horseman's Plate", "Halo Light Quartz",
                                  "Phantom Demon Jewel",
                                  "Tiamat Anima", "Tiamat Omega Anima", "Colossus Anima", "Colossus Omega Anima", "Leviathan Anima",
                                  "Leviathan Omega Anima",
                                  "Yggdrasil Anima", "Yggdrasil Omega Anima", "Luminiera Anima", "Luminiera Omega Anima", "Celeste Anima",
                                  "Celeste Omega Anima",
                                  "Shiva Anima", "Shiva Omega Anima", "Europa Anima", "Europa Omega Anima", "Alexiel Anima", "Alexiel Omega Anima",
                                  "Grimnir Anima",
                                  "Grimnir Omega Anima", "Metatron Anima", "Metatron Omega Anima", "Avatar Anima", "Avatar Omega Anima",
                                  "Nezha Anima", "Nezha Omega Anima",
                                  "Twin Elements Anima", "Twin Elements Omega Anima", "Macula Marius Anima", "Macula Marius Omega Anima",
                                  "Medusa Anima", "Medusa Omega Anima",
                                  "Apollo Anima", "Apollo Omega Anima", "Dark Angel Olivia Anima", "Dark Angel Olivia Omega Anima", "Garuda Anima",
                                  "Garuda Omega Anima",
                                  "Athena Anima", "Athena Omega Anima", "Grani Anima", "Grani Omega Anima", "Baal Anima", "Baal Omega Anima",
                                  "Odin Anima", "Odin Omega Anima",
                                  "Lich Anima", "Lich Omega Anima", "Morrigna Anima", "Morrigna Omega Anima", "Prometheus Anima",
                                  "Prometheus Omega Anima", "Ca Ong Anima",
                                  "Ca Ong Omega Anima", "Gilgamesh Anima", "Gilgamesh Omega Anima", "Hector Anima", "Hector Omega Anima",
                                  "Anubis Anima", "Anubis Omega Anima",
                                  "Huanglong Anima", "Huanglong Omega Anima", "Qilin Anima", "Qilin Omega Anima", "Tiamat Malice Anima",
                                  "Leviathan Malice Anima", "Phronesis Anima"]

        self._game.print_and_save(f"[INFO] Now detecting item rewards...")
        guibot_check = False

        total_amount_farmed = 0

        # Detect amounts gained from each item on the Loot Collected screen. If the item is on the blacklist, use my method instead.
        if item_name in blacklisted_items:
            locations = self.find_all(item_name, is_item = True, custom_confidence = 0.99)
        elif item_name in lite_blacklisted_items:
            locations = self.find_all(item_name, is_item = True, custom_confidence = 0.85)
        else:
            self._clear_memory_guibot()
            locations = self._guibot.find_all(item_name, timeout = 1, allow_zero = True)
            guibot_check = True

        for index, location in enumerate(locations):
            check = False

            # Filter out any duplicate locations that are 1 pixels from each other when the item is in either of the blacklists.
            if item_name in blacklisted_items or item_name in lite_blacklisted_items:
                for x in range(index):
                    if (abs(location[0] - locations[x][0]) <= 1 and location[1] == locations[x][1]) or (abs(location[1] - locations[x][1]) and location[0] == locations[x][0]) or (
                            abs(location[0] - locations[x][0]) and abs(location[1] - locations[x][1])):
                        check = True

            if not check:
                # Deconstruct the location object into coordinates if found using GuiBot.
                if item_name not in blacklisted_items and item_name not in lite_blacklisted_items:
                    location = (location.target.x, location.target.y)

                if guibot_check:
                    self._game.print_and_save(f"[INFO] Occurrence for {item_name.upper()} found at: {location} using GuiBot.")

                # Adjust the width and height variables if EasyOCR cannot detect the numbers correctly.
                left = location[0] + 10
                top = location[1] - 5
                width = 30
                height = 25

                # Create the /temp/ folder in the /images/ folder to house the taken screenshots.
                current_dir = os.getcwd()
                temp_dir = os.path.join(current_dir, r"images/temp")
                if not os.path.exists(temp_dir):
                    os.makedirs(temp_dir)

                # Create a screenshot in the specified region named "test" and save it in the /temp/ folder. Then use EasyOCR to extract text from it into a list.
                test_image = pyautogui.screenshot("images/temp/test.png", region = (left, top, width, height))
                # test_image.show() # Uncomment this line of code to see what the bot captured for the region of the detected text.
                result = self._reader.readtext("images/temp/test.png", detail = 0)

                # Split any unnecessary characters in the extracted text until only the number remains.
                result_cleaned = 0
                if len(result) != 0:
                    result_split = [char for char in result[0]]
                    for char in result_split:
                        try:
                            if int(char):
                                result_cleaned = int(char)
                        except ValueError:
                            continue
                else:
                    result_cleaned = 1

                total_amount_farmed += result_cleaned
            else:
                self._game.print_and_save(f"[INFO] Duplicate location detected. Removing it...")

        # If items were detected on the Quest Results screen, take a screenshot and save in the /results/ folder.    
        if take_screenshot and total_amount_farmed != 0:
            self._take_screenshot()

        self._game.print_and_save(f"[INFO] Detection of item rewards finished.")
        return total_amount_farmed

    def wait_vanish(self, image_name: str, timeout: int = 30, suppress_error: bool = False):
        """Use GuiBot to check if the provided image vanishes from the screen after a certain amount of time.

        Args:
            image_name (str): Name of the image file in the /images/buttons/ folder.
            timeout (int, optional): Timeout in seconds. Defaults to 30.
            suppress_error (bool, optional): Suppresses template matching error if True. Defaults to False.

        Returns:
            (bool): True if the image vanishes from the screen within the allotted time or False if timeout was reached.
        """
        self._game.print_and_save(f"\n[INFO] Now waiting for {image_name} to vanish from screen...")
        self._file_resolver.add_path("images/buttons/")
        self._clear_memory_guibot()
        try:
            self._guibot.wait_vanish(image_name, timeout = timeout)
            self._game.print_and_save(f"[SUCCESS] Image successfully vanished from screen...")
            return True
        except Exception:
            if suppress_error is False:
                self._game.print_and_save(f"[WARNING] Image did not vanish from screen...")
            return False

    @staticmethod
    def get_button_dimensions(image_name: str):
        """Get the dimensions of a image in images/buttons/ folder.

        Args:
            image_name (str): File name of the image in images/buttons/ folder.

        Returns:
            (int, int): Tuple of the width and the height.
        """
        image = Image.open(f"images/buttons/{image_name}.png")
        width, height = image.size
        image.close()
        return width, height

    def _take_screenshot(self):
        """Takes a screenshot of the Quest Results screen when called in find_farmed_items().

        Returns:
            None
        """
        self._game.print_and_save(f"[INFO] Taking a screenshot of the Quest Results screen...")

        # Construct the image file and folder name from the current date, time, and image number.
        current_time = datetime.datetime.now().strftime("%H-%M-%S")
        current_date = date.today()
        new_file_name = f"{current_date} {current_time} #{self._image_number}"
        self._image_number += 1
        if self._new_folder_name is None:
            self._new_folder_name = f"{current_date} {current_time}"

        # Take a screenshot using the calibrated window dimensions.
        new_image = pyautogui.screenshot(region = (self._window_left, self._window_top, self._window_width, self._window_height))

        # Create the /results/ directory if it does not already exist.
        current_dir = os.getcwd()
        results_dir = os.path.join(current_dir, r"results")
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        # Then create a new folder to hold this session's screenshots in.
        new_dir = os.path.join(current_dir, r"results", self._new_folder_name)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)

        # Finally, save the new image into the results directory with its new file name.
        new_image.save(f"./results/{self._new_folder_name}/{new_file_name}.jpg")
        self._game.print_and_save(f"[INFO] Results image saved as \"{new_file_name}.jpg\" in \"{self._new_folder_name}\" folder...")
        return None

    @staticmethod
    def _play_captcha_sound():
        playsound("CAPTCHA.mp3")
        return None

    @staticmethod
    def generate_alert_for_captcha():
        """Displays a alert that will inform users that a CAPTCHA was detected.

        Returns:
            None
        """
        # Play the CAPTCHA.mp3 using playsound.
        process = multiprocessing.Process(target = ImageUtils._play_captcha_sound)
        process.start()

        pyautogui.alert(
            text = "Stopping bot. Please enter the CAPTCHA yourself and play this mission manually to its completion. \n\nIt is now highly recommended that you take a break of several hours and "
                   "in the future, please reduce the amount of hours that you use this program consecutively without breaks in between.",
            title = "CAPTCHA Detected!", button = "OK")

        process.terminate()
        return None

    @staticmethod
    def generate_alert(message: str):
        """Displays a alert that will inform users about various user errors that may occur.

        Args:
            message (str): The message to be displayed.

        Returns:
            None
        """
        pyautogui.alert(text = message, button = "OK")
        return None
