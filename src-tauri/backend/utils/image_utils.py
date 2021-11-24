import datetime
import os
import sys
import codecs
from datetime import date
from typing import List, Tuple

import PIL
import cv2
import easyocr
import numpy
import pyautogui
from PIL import Image as Image
from playsound import playsound

from utils.settings import Settings
from utils.message_log import MessageLog


class ImageUtils:
    """
    Provides the utility functions needed to perform image-related actions.
    """

    # Initialize the following for saving screenshots.
    _image_number: int = 0
    _new_folder_name: str = None

    # Used for skipping selecting the Summon Element every time on repeated runs.
    _summon_selection_first_run = True
    _summon_selection_same_element = False

    _match_method: int = cv2.TM_CCOEFF_NORMED
    _match_location: Tuple[int, int] = None

    # Check if the temp folder is created in the images folder.
    _current_dir: str = os.getcwd()
    _temp_dir: str = _current_dir + "/temp/"
    if not os.path.exists(_temp_dir):
        os.makedirs(_temp_dir)

    _reader: easyocr.Reader = None

    @staticmethod
    def update_window_dimensions(window_left: int, window_top: int, window_width: int, window_height: int, additional_calibration_required: bool = False):
        """Updates the window dimensions for PyAutoGUI to perform faster operations in.

        Args:
            window_left (int): The x-coordinate of the left edge of the region for image matching.
            window_top (int): The y-coordinate of the top edge of the region for image matching.
            window_width (int): The width of the region for image matching.
            window_height (int): The height of the region for image matching.
            additional_calibration_required (bool, optional): Flag that allows for compensation of x-coordinates of all matches to fit the right hand side of the computer screen.

        Returns:
            None
        """
        Settings.window_left = window_left
        Settings.window_top = window_top
        Settings.window_width = window_width
        Settings.window_height = window_height
        Settings.calibration_complete = True
        Settings.additional_calibration_required = additional_calibration_required
        return None

    @staticmethod
    def get_window_dimensions():
        """Get the window dimensions as a Tuple of 4 integers.

        Returns:
            (Tuple[int, int, int, int]): A Tuple of 4 integers consisting of (window_left, window_top, window_width, window_height).
        """
        return Settings.window_left, Settings.window_top, Settings.window_width, Settings.window_height

    @staticmethod
    def _match(template: numpy.ndarray, confidence: float = 0.8) -> bool:
        """Updates the window dimensions for PyAutoGUI to perform faster operations in.

        Args:
            template (numpy.ndarray): The template image array to match against in a source image.
            confidence (float, optional): Accuracy threshold for matching. Defaults to 0.8.

        Returns:
            (bool): True if the template was found inside the source image and False otherwise.
        """
        match_check = False
        if Settings.window_left is not None and Settings.window_top is not None and Settings.window_width is not None and Settings.window_height is not None:
            image: PIL.Image.Image = pyautogui.screenshot(region = (Settings.window_left, Settings.window_top, Settings.window_width, Settings.window_height))
        else:
            image: PIL.Image.Image = pyautogui.screenshot()

        image.save(f"temp/source.png")
        src: numpy.ndarray = cv2.imread(f"temp/source.png", 0)
        height, width = template.shape

        result: numpy.ndarray = cv2.matchTemplate(src, template, ImageUtils._match_method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if (ImageUtils._match_method == cv2.TM_SQDIFF or ImageUtils._match_method == cv2.TM_SQDIFF_NORMED) and min_val <= 1.0 - confidence:
            ImageUtils._match_location = min_loc
            match_check = True
        elif ImageUtils._match_method != cv2.TM_SQDIFF and ImageUtils._match_method != cv2.TM_SQDIFF_NORMED and max_val >= confidence:
            ImageUtils._match_location = max_loc
            match_check = True
        elif Settings.debug_mode:
            if ImageUtils._match_method == cv2.TM_SQDIFF or ImageUtils._match_method == cv2.TM_SQDIFF_NORMED:
                MessageLog.print_message(f"[WARNING] Match not found with {min_val} not <= {1.0 - confidence} at Point {min_loc}.")
            else:
                MessageLog.print_message(f"[WARNING] Match not found with {max_val} not >= {confidence} at Point {max_loc}.")

        if match_check:
            region = (ImageUtils._match_location[0] + width, ImageUtils._match_location[1] + height)
            cv2.rectangle(src, ImageUtils._match_location, region, 255, 5)

            if Settings.debug_mode:
                cv2.imwrite(f"temp/match.png", src)

            if Settings.additional_calibration_required is False:
                temp_location = list(ImageUtils._match_location)
                temp_location[0] += int(width / 2)
                temp_location[1] += int(height / 2)
            else:
                temp_location = list(ImageUtils._match_location)
                temp_location[0] += int(pyautogui.size()[0] - (pyautogui.size()[0] / 3)) + int(width / 2)
                temp_location[1] += int(height / 2)

            ImageUtils._match_location = tuple(temp_location)

            if ImageUtils._match_method == cv2.TM_SQDIFF or ImageUtils._match_method == cv2.TM_SQDIFF_NORMED:
                if Settings.debug_mode:
                    MessageLog.print_message(f"[DEBUG] Match found with {min_val} <= {confidence} at Point {ImageUtils._match_location}")
            else:
                if Settings.debug_mode:
                    MessageLog.print_message(f"[DEBUG] Match found with {max_val} >= {confidence} at Point {ImageUtils._match_location}")

        return match_check

    @staticmethod
    def _match_all(template: numpy.ndarray, confidence: float = 0.8) -> List[Tuple[int, ...]]:
        """Updates the window dimensions for PyAutoGUI to perform faster operations in.

        Args:
            template (numpy.ndarray): The template image array to match against in a source image.
            confidence (float, optional): Accuracy threshold for matching. Defaults to 0.8.

        Returns:
            (List[Tuple[int, ...]]): List of Tuples containing match locations.
        """
        if Settings.window_left is not None and Settings.window_top is not None and Settings.window_width is not None and Settings.window_height is not None:
            image: PIL.Image.Image = pyautogui.screenshot(region = (Settings.window_left, Settings.window_top, Settings.window_width, Settings.window_height))
        else:
            image: PIL.Image.Image = pyautogui.screenshot()

        image.save(f"temp/source.png")

        src: numpy.ndarray = cv2.imread(f"temp/source.png", 0)
        height, width = template.shape

        match_check = True
        match_locations = []

        while match_check:
            result: numpy.ndarray = cv2.matchTemplate(src, template, ImageUtils._match_method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if (ImageUtils._match_method == cv2.TM_SQDIFF or ImageUtils._match_method == cv2.TM_SQDIFF_NORMED) and min_val <= 1.0 - confidence:
                ImageUtils._match_location = min_loc
                match_check = True
            elif ImageUtils._match_method != cv2.TM_SQDIFF and ImageUtils._match_method != cv2.TM_SQDIFF_NORMED and max_val >= confidence:
                ImageUtils._match_location = max_loc
                match_check = True
            else:
                if Settings.debug_mode:
                    if ImageUtils._match_method == cv2.TM_SQDIFF or ImageUtils._match_method == cv2.TM_SQDIFF_NORMED:
                        MessageLog.print_message(f"[WARNING] Match not found with {min_val} not <= {1.0 - confidence} at Point {min_loc}.")
                    else:
                        MessageLog.print_message(f"[WARNING] Match not found with {max_val} not >= {confidence} at Point {max_loc}.")

                match_check = False

            if match_check:
                region = (ImageUtils._match_location[0] + width, ImageUtils._match_location[1] + height)
                cv2.rectangle(src, ImageUtils._match_location, region, 255, 5)

                if Settings.debug_mode:
                    cv2.imwrite(f"temp/matchAll.png", src)

                if Settings.additional_calibration_required is False:
                    temp_location = list(ImageUtils._match_location)
                    temp_location[0] += int(width / 2)
                    temp_location[1] += int(height / 2)
                else:
                    temp_location = list(ImageUtils._match_location)
                    temp_location[0] += int(pyautogui.size()[0] - (pyautogui.size()[0] / 3)) + int(width / 2)
                    temp_location[1] += int(height / 2)

                ImageUtils._match_location = tuple(temp_location)
                match_locations.append(ImageUtils._match_location)

                if ImageUtils._match_method == cv2.TM_SQDIFF or ImageUtils._match_method == cv2.TM_SQDIFF_NORMED:
                    if Settings.debug_mode:
                        MessageLog.print_message(f"[DEBUG] Match found with {min_val} <= {confidence} at Point {ImageUtils._match_location}")
                else:
                    if Settings.debug_mode:
                        MessageLog.print_message(f"[DEBUG] Match found with {max_val} >= {confidence} at Point {ImageUtils._match_location}")

        return match_locations

    @staticmethod
    def find_button(image_name: str, custom_confidence: float = 0.8, tries: int = 5, suppress_error: bool = False):
        """Find the location of the specified button.

        Args:
            image_name (str): Name of the button image file in the /images/buttons/ folder.
            custom_confidence (float, optional): Accuracy threshold for matching. Defaults to 0.8.
            tries (int, optional): Number of tries before failing. Defaults to 5.
            suppress_error (bool, optional): Suppresses template matching error if True. Defaults to False.

        Returns:
            (Tuple[int, int]): Tuple of coordinates of where the center of the button is located if image matching was successful. Otherwise, return None.
        """
        if Settings.debug_mode:
            MessageLog.print_message(f"\n[DEBUG] Starting process to find the {image_name.upper()} button image...")

        template: numpy.ndarray = cv2.imread(f"{ImageUtils._current_dir}/images/buttons/{image_name.lower()}.jpg", 0)

        while tries > 0:
            result_flag: bool = ImageUtils._match(template, custom_confidence)

            if result_flag is False:
                tries -= 1
                if tries <= 0:
                    if not suppress_error:
                        MessageLog.print_message(f"[WARNING] Failed to find the {image_name.upper()} button.")
                    return None
            else:
                return ImageUtils._match_location

        return None

    @staticmethod
    def confirm_location(image_name: str, custom_confidence: float = 0.8, tries: int = 5, suppress_error: bool = False):
        """Confirm the position of the bot by searching for the header image.

        Args:
            image_name (str): Name of the header image file in the /images/headers/ folder.
            custom_confidence (float, optional): Accuracy threshold for matching. Defaults to 0.8.
            tries (int, optional): Number of tries before failing. Defaults to 5.
            suppress_error (bool, optional): Suppresses template matching error if True. Defaults to False.

        Returns:
            (bool): True if current location is confirmed. Otherwise, False.
        """
        if Settings.debug_mode:
            MessageLog.print_message(f"\n[DEBUG] Starting process to find the {image_name.upper()} button image...")

        template: numpy.ndarray = cv2.imread(f"{ImageUtils._current_dir}/images/headers/{image_name.lower()}_header.jpg", 0)

        while tries > 0:
            result_flag: bool = ImageUtils._match(template, custom_confidence)

            if result_flag is False:
                tries -= 1
                if tries <= 0:
                    if not suppress_error:
                        MessageLog.print_message(f"[WARNING] Failed to confirm the bot's location at {image_name.upper()}.")
                    return False
            else:
                return True

        return False

    @staticmethod
    def find_summon(summon_list: List[str], summon_element_list: List[str], home_button_x: int, home_button_y: int, custom_confidence: float = 0.8, suppress_error: bool = False):
        """Find the location of the specified Summon. Will attempt to scroll the screen down to see more Summons if the initial screen position yielded no matches.

        Args:
            summon_list (List[str]): List of names of the Summon image's file name in /images/summons/ folder.
            summon_element_list (List[str]): List of names of the Summon element image file in the /images/buttons/ folder.
            home_button_x (int): X coordinate of where the center of the Home Button is.
            home_button_y (int): Y coordinate of where the center of the Home Button is.
            custom_confidence (float, optional): Accuracy threshold for matching. Defaults to 0.8.
            suppress_error (bool, optional): Suppresses template matching error if True. Defaults to False.

        Returns:
            (Tuple[int, int]): Tuple of coordinates of where the center of the Summon is located if image matching was successful. Otherwise, return None.
        """
        from bot.game import Game

        if Settings.debug_mode:
            MessageLog.print_message(f"[DEBUG] Received the following list of Summons to search for: {str(summon_list)}")
            MessageLog.print_message(f"[DEBUG] Received the following list of Elements: {str(summon_element_list)}")

        last_summon_element = ""
        summon_index = 0

        # Make sure that the bot is at the Summon Selection screen.
        tries = 10
        while not ImageUtils.confirm_location("select_a_summon"):
            Game.find_and_click_button('reload')
            tries -= 1
            if tries <= 0 and ImageUtils.confirm_location("select_a_summon", tries = 1) is False:
                raise Exception("Could not reach the Summon Selection screen.")

        # Determine if all the summon elements are the same or not. This will influence whether or not the bot needs to change elements in repeated runs.
        ImageUtils._summon_selection_same_element = all(element == summon_element_list[0] for element in summon_element_list)

        while True:
            # Perform first time setup by selecting the correct summon element.
            if ImageUtils._summon_selection_first_run or ImageUtils._summon_selection_same_element is False:
                current_summon_element: str = summon_element_list[summon_index]
                if current_summon_element != last_summon_element:
                    Game.find_and_click_button(f"summon_{current_summon_element}")
                    last_summon_element = current_summon_element

                ImageUtils._summon_selection_first_run = False

            summon_index = 0
            while summon_index < len(summon_list):
                # Now try and find the Summon at the current index.
                template: numpy.ndarray = cv2.imread(f"{ImageUtils._current_dir}/images/summons/{summon_list[summon_index]}.jpg", 0)

                # Crop the summon template image so that plus marks would not potentially obscure any match.
                height, width = template.shape
                template = template[0:height, 0:width - 40]

                result_flag: bool = ImageUtils._match(template, custom_confidence)

                if result_flag:
                    if Settings.debug_mode:
                        MessageLog.print_message(f"[SUCCESS] Found {summon_list[summon_index].upper()} Summon at {ImageUtils._match_location}.")

                    return ImageUtils._match_location
                else:
                    if suppress_error is False:
                        MessageLog.print_message(f"[WARNING] Could not locate {summon_list[summon_index].upper()} Summon.")

                    summon_index += 1

            # If the bot reached the bottom of the page, scroll back up to the top and start searching for the next Summon.
            if ImageUtils.find_button("bottom_of_summon_selection", tries = 1) is not None:
                MessageLog.print_message(f"[WARNING] Bot has reached the bottom of the page and found no suitable Summons. Resetting Summons now...")
                return None

            # If matching failed, scroll the screen down to see more Summons.
            from utils.mouse_utils import MouseUtils
            MouseUtils.scroll_screen(home_button_x, home_button_y - 50, -700)
            Game.wait(1.0)

    @staticmethod
    def find_all(image_name: str, is_item: bool = False, custom_confidence: float = 0.8, hide_info: bool = False) -> List[Tuple[int, ...]]:
        """Find the specified image file by locating all occurrences on the screen.

        Args:
            image_name (str): Name of the image file in the /images/buttons folder.
            is_item (bool, optional): Determines whether to search for the image file in the /images/buttons/ or /images/items/ folder. Defaults to False.
            custom_confidence (float, optional): Accuracy threshold for matching. Defaults to 0.8.
            hide_info (bool, optional): Whether or not to print the matches' locations. Defaults to False.

        Returns:
            (List[Tuple[int, ...]): List of occurrences found on the screen. If no occurrence was found, return a empty list.
        """
        if is_item:
            folder_name = "items"
        else:
            folder_name = "buttons"

        template: numpy.ndarray = cv2.imread(f"{ImageUtils._current_dir}/images/{folder_name}/{image_name}.jpg", 0)

        locations = ImageUtils._match_all(template, custom_confidence)
        filtered_locations: List[Tuple[int, ...]] = []
        same_y: int = 0
        sort_flag: bool = False

        if len(locations) != 0:
            for (index, location) in enumerate(locations):
                if index > 0:
                    # Filter out duplicate locations where they are 1 pixel away from each other.
                    if location[0] != (locations[index - 1][0] + 1) and location[1] != (locations[index - 1][1] + 1):
                        filtered_locations.append(location)
                        if same_y != location[1]:
                            same_y = location[1]
                            sort_flag = False
                        else:
                            sort_flag = True
                else:
                    filtered_locations.append(location)
                    same_y = location[1]
                    sort_flag = False

            # Sort the matched locations.
            def first(point):
                return point[0]

            def second(point):
                return point[1]

            if sort_flag:
                MessageLog.print_message(f"Sorting first")
                filtered_locations.sort(key = first)
            else:
                MessageLog.print_message(f"Sorting second")
                filtered_locations.sort(key = second)

            if not hide_info:
                MessageLog.print_message(f"[INFO] Occurrence for {image_name.upper()} found at: {filtered_locations}")
        else:
            if Settings.debug_mode:
                MessageLog.print_message(f"[DEBUG] Failed to detect any occurrences of {image_name.upper()} images.")

        return filtered_locations

    @staticmethod
    def find_farmed_items(item_name: str, take_screenshot: bool = True) -> int:
        """Detect amounts of items gained according to the desired items specified.

        Args:
            item_name (str): Item to be found.
            take_screenshot (bool, optional): Takes a screenshot whenever matches were detected. Defaults to True.

        Returns:
            (int): Amount gained for the item.
        """
        try:
            if not os.path.exists(ImageUtils._current_dir + "/backend/model/"):
                os.makedirs(ImageUtils._current_dir + "/backend/model/")

            MessageLog.print_message(f"\n[INFO] Initializing EasyOCR reader. This may take a few seconds...")
            ImageUtils._reader = easyocr.Reader(["en"], model_storage_directory = ImageUtils._current_dir + "/backend/model/", gpu = True)
            MessageLog.print_message(f"[INFO] EasyOCR reader initialized.")
        except UnicodeEncodeError:
            # Tauri spawns the Python process using encoding cp1252 and not utf-8. Need to do this hacky way to force stdout to be utf-8 to get through
            # EasyOCR initialization as it uses Unicode characters. This process is not needed after EasyOCR downloads the models to the /model/ folder.
            MessageLog.print_message(f"\n[INFO] Seems that the models for EasyOCR has not been downloaded yet. Downloading them now after setting stdout encoding from cp1252 to utf-8...\n\n")
            sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
            ImageUtils._reader = easyocr.Reader(["en"], model_storage_directory = ImageUtils._current_dir + "/backend/model/", gpu = True)
            MessageLog.print_message(f"\n[INFO] Models for EasyOCR has been downloaded successfully.\n\n")

        # List of items blacklisted from using the standard confidence and instead need a custom confidence to detect them.
        blacklisted_items = ["Fire Orb", "Water Orb", "Earth Orb", "Wind Orb", "Light Orb", "Dark Orb",
                             "Red Tome", "Blue Tome", "Brown Tome", "Green Tome", "White Tome", "Black Tome",
                             "Hellfire Scroll", "Flood Scroll", "Thunder Scroll", "Gale Scroll", "Skylight Scroll", "Chasm Scroll",
                             "Jasper Scale", "Crystal Spirit", "Luminous Judgment", "Sagittarius Rune", "Sunlight Quartz", "Shadow Silver",
                             "Ifrit Anima", "Cocytus Anima", "Vohu Manah Anima", "Sagittarius Anima", "Corow Anima", "Diablo Anima",
                             "Ifrit Omega Anima", "Cocytus Omega Anima", "Vohu Manah Omega Anima", "Sagittarius Omega Anima", "Corow Omega Anima", "Diablo Omega Anima",
                             "Ancient Ecke Sachs", "Ancient Auberon", "Ancient Perseus", "Ancient Nalakuvara", "Ancient Bow of Artemis", "Ancient Cortana",
                             "Ecke Sachs", "Auberon", "Perseus", "Nalakuvara", "Bow of Artemis", "Cortana"]

        lite_blacklisted_items = ["Infernal Garnet", "Frozen Hell Prism", "Evil Judge Crystal", "Horseman's Plate", "Halo Light Quartz", "Phantom Demon Jewel",
                                  "Tiamat Anima", "Colossus Anima", "Leviathan Anima", "Yggdrasil Anima", "Luminiera Anima", "Celeste Anima",
                                  "Tiamat Omega Anima", "Colossus Omega Anima", "Leviathan Omega Anima", "Yggdrasil Omega Anima", "Luminiera Omega Anima", "Celeste Omega Anima",
                                  "Shiva Anima", "Europa Anima", "Alexiel Anima", "Grimnir Anima", "Metatron Anima", "Avatar Anima",
                                  "Shiva Omega Anima", "Europa Omega Anima", "Alexiel Omega Anima", "Grimnir Omega Anima", "Metatron Omega Anima", "Avatar Omega Anima",
                                  "Twin Elements Anima", "Macula Marius Anima", "Medusa Anima", "Nezha Anima", "Apollo Anima", "Dark Angel Olivia Anima",
                                  "Twin Elements Omega Anima", "Macula Marius Omega Anima", "Medusa Omega Anima", "Nezha Omega Anima", "Apollo Omega Anima", "Dark Angel Olivia Omega Anima",
                                  "Athena Anima", "Grani Anima", "Baal Anima", "Garuda Anima", "Odin Anima", "Lich Anima",
                                  "Athena Omega Anima", "Grani Omega Anima", "Baal Omega Anima", "Garuda Omega Anima", "Odin Omega Anima", "Lich Omega Anima",
                                  "Prometheus Anima", "Ca Ong Anima", "Gilgamesh Anima", "Morrigna Anima", "Hector Anima", "Anubis Anima",
                                  "Prometheus Omega Anima", "Ca Ong Omega Anima", "Gilgamesh Omega Anima", "Morrigna Omega Anima", "Hector Omega Anima", "Anubis Omega Anima",
                                  "Huanglong Anima", "Huanglong Omega Anima", "Qilin Anima", "Qilin Omega Anima"]

        MessageLog.print_message(f"[INFO] Now detecting item rewards...")

        total_amount_farmed = 0

        # Detect amounts gained from each item on the Loot Collected screen. If the item is on the blacklist, use my method instead.
        if item_name in blacklisted_items:
            locations = ImageUtils.find_all(item_name, is_item = True, custom_confidence = 0.99)
        elif item_name in lite_blacklisted_items:
            locations = ImageUtils.find_all(item_name, is_item = True, custom_confidence = 0.85)
        else:
            locations = ImageUtils.find_all(item_name, is_item = True, custom_confidence = 0.80)

        for index, location in enumerate(locations):
            check = False

            # Filter out any duplicate locations that are 1 pixels from each other when the item is in either of the blacklists.
            if item_name in blacklisted_items or item_name in lite_blacklisted_items:
                for x in range(index):
                    if (abs(location[0] - locations[x][0]) <= 1 and location[1] == locations[x][1]) or (abs(location[1] - locations[x][1]) and location[0] == locations[x][0]) or (
                            abs(location[0] - locations[x][0]) and abs(location[1] - locations[x][1])):
                        check = True

            if not check:
                # Create a screenshot in the specified region named "test" and save it in the /temp/ folder. Then use EasyOCR to extract text from it into a list.
                # Adjust the width and height variables if EasyOCR cannot detect the numbers correctly.
                left = location[0] + 10
                top = location[1] - 5
                width = 30
                height = 25
                test_image = pyautogui.screenshot(f"temp/test.png", region = (left, top, width, height))
                # test_image.show() # Uncomment this line of code to see what the bot captured for the region of the detected text.
                result = ImageUtils._reader.readtext(f"temp/test.png", detail = 0)

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
                MessageLog.print_message(f"[INFO] Duplicate location detected. Removing it...")

        # If items were detected on the Quest Results screen, take a screenshot and save in the /results/ folder.    
        if take_screenshot and total_amount_farmed != 0:
            ImageUtils._take_screenshot()

        MessageLog.print_message(f"[INFO] Detection of item rewards finished.")
        return total_amount_farmed

    @staticmethod
    def wait_vanish(image_name: str, timeout: int = 10, suppress_error: bool = False) -> bool:
        """Check if the provided image vanishes from the screen after a certain amount of time.

        Args:
            image_name (str): Name of the image file in the /images/buttons/ folder.
            timeout (int, optional): Timeout in tries. Defaults to 10.
            suppress_error (bool, optional): Suppresses template matching error if True. Defaults to False.

        Returns:
            (bool): True if the image vanishes from the screen within the allotted time or False if timeout was reached.
        """
        MessageLog.print_message(f"\n[INFO] Now waiting for {image_name} to vanish from screen...")

        template: numpy.ndarray = cv2.imread(f"{ImageUtils._current_dir}/images/buttons/{image_name.lower()}.jpg", 0)

        for _ in range(timeout):
            if ImageUtils._match(template) is False:
                MessageLog.print_message(f"[SUCCESS] Image successfully vanished from screen...")
                return True

        if suppress_error is False:
            MessageLog.print_message(f"[WARNING] Image did not vanish from screen...")

        return False

    @staticmethod
    def get_button_dimensions(image_name: str) -> Tuple[int, int]:
        """Get the dimensions of a image in /images/buttons/ folder.

        Args:
            image_name (str): File name of the image in /images/buttons/ folder.

        Returns:
            (Tuple[int, int]): Tuple of the width and the height of the image.
        """
        image = Image.open(f"{ImageUtils._current_dir}/images/buttons/{image_name}.jpg")
        width, height = image.size
        image.close()
        return width, height

    @staticmethod
    def _take_screenshot():
        """Takes a screenshot of the Quest Results screen when called in find_farmed_items().

        Returns:
            None
        """
        MessageLog.print_message(f"[INFO] Taking a screenshot of the Quest Results screen...")

        # Construct the image file and folder name from the current date, time, and image number.
        current_time = datetime.datetime.now().strftime("%H-%M-%S")
        current_date = date.today()
        new_file_name = f"{current_date} {current_time} #{ImageUtils._image_number}"
        ImageUtils._image_number += 1
        if ImageUtils._new_folder_name is None:
            ImageUtils._new_folder_name = f"{current_date} {current_time}"

        # Take a screenshot using the calibrated window dimensions.
        new_image: PIL.Image.Image = pyautogui.screenshot(region = (Settings.window_left, Settings.window_top, Settings.window_width, Settings.window_height))

        # Create the /results/ directory if it does not already exist.
        current_dir = os.getcwd()
        results_dir = os.path.join(current_dir, r"results")
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        # Then create a new folder to hold this session's screenshots in.
        new_dir = os.path.join(current_dir, r"results", ImageUtils._new_folder_name)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)

        # Finally, save the new image into the results directory with its new file name.
        new_image.save(f"{ImageUtils._current_dir}/results/{ImageUtils._new_folder_name}/{new_file_name}.jpg")
        MessageLog.print_message(f"[INFO] Results image saved as \"{new_file_name}.jpg\" in \"{ImageUtils._new_folder_name}\" folder...")
        return None

    @staticmethod
    def _play_captcha_sound():
        """Plays the CAPTCHA.mp3 music file.

        Returns:
            None
        """
        playsound(f"{ImageUtils._current_dir}/backend/CAPTCHA.mp3", block = False)
        return None

    @staticmethod
    def generate_alert_for_captcha():
        """Displays a alert that will inform users that a CAPTCHA was detected.

        Returns:
            None
        """
        ImageUtils._play_captcha_sound()
        pyautogui.alert(
            text = "Stopping bot. Please enter the CAPTCHA yourself and play this mission manually to its completion. \n\nIt is now highly recommended that you take a break of several hours and "
                   "in the future, please reduce the amount of hours that you use this program consecutively without breaks in between.",
            title = "CAPTCHA Detected!", button = "OK")
        return None

    @staticmethod
    def generate_alert(message: str):
        """Displays a alert that will inform users about various user errors that may occur.

        Args:
            message (str): The message to be displayed.

        Returns:
            None
        """
        ImageUtils._play_captcha_sound()
        pyautogui.alert(text = message, title = "Exception Encountered", button = "OK")
        return None
