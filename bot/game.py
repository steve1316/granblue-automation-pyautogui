import datetime
import multiprocessing
import random
import time
import traceback
from configparser import ConfigParser
from timeit import default_timer as timer
from typing import Iterable

import pyautogui

from bot.combat_mode import CombatMode
from bot.map_selection import MapSelection
from utils.image_utils import ImageUtils
from utils.mouse_utils import MouseUtils
from utils.twitter_room_finder import TwitterRoomFinder


class Game:
    """
    Main driver for bot activity and navigation for the web browser bot, Granblue Fantasy.

    Attributes
    ----------
    queue (multiprocessing.Queue): Queue to keep track of logging messages to share between backend and frontend.

    is_bot_running (int): Flag in shared memory that signals the frontend that the bot has finished/exited.

    combat_script (str, optional): The file path to the combat script to use for Combat Mode. Defaults to empty string.

    debug_mode (bool, optional): Optional flag to print debug messages related to this class. Defaults to False.

    """

    def __init__(self, queue: multiprocessing.Queue, is_bot_running: int, combat_script: str = "", debug_mode: bool = False):
        super().__init__()

        # ################## config.ini ###################
        # Grab the Twitter API keys and tokens from config.ini. The list order is: [consumer key, consumer secret key, access token, access secret token].
        config = ConfigParser()
        config.read("config.ini")

        # #### twitter ####
        keys_tokens = [config.get("twitter", "api_key"), config.get("twitter", "api_key_secret"), config.get("twitter", "access_token"), config.get("twitter", "access_token_secret")]
        # #### end of twitter ####

        # #### refill ####
        self._use_full_elixir = config.getboolean("refill", "refill_using_full_elixir")
        self._use_soul_balm = config.getboolean("refill", "refill_using_soul_balms")
        # #### end of refill ####

        # #### configuration ####
        custom_mouse_speed = float(config.get("configuration", "mouse_speed"))

        enable_bezier_curve_mouse_movement = config.getboolean("configuration", "enable_bezier_curve_mouse_movement")

        self._enable_delay_between_runs = config.getboolean("configuration", "enable_delay_between_runs")
        self._delay_in_seconds = config.getint("configuration", "delay_in_seconds")
        self._enable_randomized_delay_between_runs = config.getboolean("configuration", "enable_randomized_delay_between_runs")
        self._delay_in_seconds_lower_bound = config.getint("configuration", "delay_in_seconds_lower_bound")
        self._delay_in_seconds_upper_bound = config.getint("configuration", "delay_in_seconds_upper_bound")

        self._idle_seconds_after_skill = config.getint("configuration", "idle_seconds_after_skill")
        self._idle_seconds_after_summon = config.getint("configuration", "idle_seconds_after_summon")
        # #### end of configuration ####

        # #### dimensional_halo ####
        self._enable_dimensional_halo = config.getboolean("dimensional_halo", "enable_dimensional_halo")
        self._dimensional_halo_combat_script = config.get("dimensional_halo", "dimensional_halo_combat_script")

        self._dimensional_halo_summon_list = config.get("dimensional_halo", "dimensional_halo_summon_list").replace(" ", "_").split(",")
        if len(self._dimensional_halo_summon_list) == 1 and self._dimensional_halo_summon_list[0] == "":
            self._dimensional_halo_summon_list.clear()

        self._dimensional_halo_summon_element_list = config.get("dimensional_halo", "dimensional_halo_summon_element_list").replace(" ", "_").split(",")
        if len(self._dimensional_halo_summon_element_list) == 1 and self._dimensional_halo_summon_element_list[0] == "":
            self._dimensional_halo_summon_element_list.clear()

        self._dimensional_halo_group_number = config.getint("dimensional_halo", "dimensional_halo_group_number")
        self._dimensional_halo_party_number = config.getint("dimensional_halo", "dimensional_halo_party_number")
        self._dimensional_halo_amount = 0
        # #### end of dimensional_halo ####

        # #### event ####
        self._enable_event_nightmare = config.getboolean("event", "enable_event_nightmare")
        self._event_nightmare_combat_script = config.get("event", "event_nightmare_combat_script")

        self._event_nightmare_summon_list = config.get("event", "event_nightmare_summon_list").replace(" ", "_").split(",")
        if len(self._event_nightmare_summon_list) == 1 and self._event_nightmare_summon_list[0] == "":
            self._event_nightmare_summon_list.clear()

        self._event_nightmare_summon_element_list = config.get("event", "event_nightmare_summon_element_list").replace(" ", "_").split(",")
        if len(self._event_nightmare_summon_element_list) == 1 and self._event_nightmare_summon_element_list[0] == "":
            self._event_nightmare_summon_element_list.clear()

        self._event_nightmare_group_number = config.getint("event", "event_nightmare_group_number")
        self._event_nightmare_party_number = config.getint("event", "event_nightmare_party_number")
        # #### end of event ####

        # #### rise_of_the_beasts ####
        self._enable_rotb_extreme_plus = config.getboolean("rise_of_the_beasts", "enable_rotb_extreme_plus")
        self._rotb_extreme_plus_combat_script = config.get("rise_of_the_beasts", "rotb_extreme_plus_combat_script")

        self._rotb_extreme_plus_summon_list = config.get("rise_of_the_beasts", "rotb_extreme_plus_summon_list").replace(" ", "_").split(",")
        if len(self._rotb_extreme_plus_summon_list) == 1 and self._rotb_extreme_plus_summon_list[0] == "":
            self._rotb_extreme_plus_summon_list.clear()

        self._rotb_extreme_plus_summon_element_list = config.get("rise_of_the_beasts", "rotb_extreme_plus_summon_element_list").replace(" ", "_").split(",")
        if len(self._rotb_extreme_plus_summon_element_list) == 1 and self._rotb_extreme_plus_summon_element_list[0] == "":
            self._rotb_extreme_plus_summon_element_list.clear()

        self._rotb_extreme_plus_group_number = config.getint("rise_of_the_beasts", "rotb_extreme_plus_group_number")
        self._rotb_extreme_plus_party_number = config.getint("rise_of_the_beasts", "rotb_extreme_plus_party_number")
        self._rotb_extreme_plus_amount = 0
        # #### end of rise_of_the_beasts ####

        # #### dread_barrage ####
        self._enable_unparalleled_foe = config.getboolean("dread_barrage", "enable_unparalleled_foe")
        self._enable_unparalleled_foe_level_95 = config.getboolean("dread_barrage", "enable_unparalleled_foe_level_95")
        self._enable_unparalleled_foe_level_175 = config.getboolean("dread_barrage", "enable_unparalleled_foe_level_175")
        self.unparalleled_foe_combat_script = config.get("dread_barrage", "unparalleled_foe_combat_script")

        self._unparalleled_foe_summon_list = config.get("dread_barrage", "unparalleled_foe_summon_list").replace(" ", "_").split(",")
        if len(self._unparalleled_foe_summon_list) == 1 and self._unparalleled_foe_summon_list[0] == "":
            self._unparalleled_foe_summon_list.clear()

        self._unparalleled_foe_summon_element_list = config.get("dread_barrage", "unparalleled_foe_summon_element_list").replace(" ", "_").split(",")
        if len(self._unparalleled_foe_summon_element_list) == 1 and self._unparalleled_foe_summon_element_list[0] == "":
            self._unparalleled_foe_summon_element_list.clear()

        self._unparalleled_foe_group_number = config.getint("dread_barrage", "unparalleled_foe_group_number")
        self._unparalleled_foe_party_number = config.getint("dread_barrage", "unparalleled_foe_party_number")
        # #### end of dread_barrage ####
        # ################## end of config.ini ###################

        # Start a timer signaling bot start in order to keep track of elapsed time and create a Queue to share logging messages between backend and frontend.
        self._starting_time = timer()
        self._queue = queue

        # Keep track of a bot running status flag shared in memory. Value of 0 means the bot is currently running and a value of 1 means that the bot has stopped.
        self._is_bot_running = is_bot_running

        # Set a debug flag to determine whether or not to print debugging messages.
        self._debug_mode = debug_mode

        # Initialize the objects of helper classes.
        self.combat_mode = CombatMode(self, self._idle_seconds_after_skill, self._idle_seconds_after_summon, is_bot_running, debug_mode = self._debug_mode)
        self._map_selection = MapSelection(self, is_bot_running)
        self.room_finder = TwitterRoomFinder(self, keys_tokens[0], keys_tokens[1], keys_tokens[2], keys_tokens[3], debug_mode = self._debug_mode)
        self.image_tools = ImageUtils(self, debug_mode = self._debug_mode)
        self.mouse_tools = MouseUtils(self, enable_bezier_curve = enable_bezier_curve_mouse_movement, mouse_speed = custom_mouse_speed, debug_mode = self._debug_mode)

        # Save the locations of the "Home", "Attack", and "Back" buttons for use in other classes.
        self.home_button_location = None
        self._attack_button_location = None
        self._back_button_location = None

        # Keep track of the following for Combat Mode.
        self._combat_script = combat_script
        self._retreat_check = False

        # Keep track of the following for Farming Mode.
        self._item_name = ""
        self._item_amount_to_farm = 0
        self._item_amount_farmed = 0
        self.farming_mode = ""
        self._mission_name = ""
        self._summon_element_list = []
        self._summon_list = []
        self._group_number = 0
        self._party_number = 0
        self._amount_of_runs_finished = 0
        self._coop_first_run = True

        # Enable checking for Skyscope mission popups.
        self.enable_skyscope = True

        # Calibrate the dimensions of the bot window on bot launch.
        self.go_back_home(confirm_location_check = True, display_info_check = True)

    def _print_time(self):
        """Formats the time since the bot started into a readable, printable HH:MM:SS format using timedelta.

        Returns:
            str: A formatted string that displays the elapsed time since the bot started.
        """
        return str(datetime.timedelta(seconds = (timer() - self._starting_time))).split('.')[0]

    def print_and_save(self, message: str):
        """Saves the logging message into the Queue to be shared with the frontend and then prints it to console.

        Args:
            message (str): A logging message containing various information.

        Returns:
            None
        """
        if message.startswith("\n"):
            new_message = "\n" + self._print_time() + " " + message[len("\n"):]
        else:
            new_message = self._print_time() + " " + message

        self._queue.put(new_message)
        print(new_message)
        return None

    def _calibrate_game_window(self, display_info_check: bool = False):
        """Recalibrate the dimensions of the bot window for fast and accurate image matching.

        Args:
            display_info_check (bool, optional): Displays the screen size and the dimensions of the bot window. Defaults to False.

        Returns:
            None
        """
        if self._debug_mode:
            self.print_and_save("\n[DEBUG] Recalibrating the dimensions of the bot window...")

        # Save the location of the "Home" button at the bottom of the bot window.
        self.home_button_location = self.image_tools.find_button("home")

        # Set the dimensions of the bot window and save it in ImageUtils so that future operations do not go out of bounds.
        home_news_button = self.image_tools.find_button("home_news")
        home_menu_button = self.image_tools.find_button("home_menu")

        # Use the locations of the "News" and "Menu" buttons on the Home screen to calculate the dimensions of the bot window in the following
        # format:
        window_left = home_news_button[0] - 35  # The x-coordinate of the left edge.
        window_top = home_menu_button[1] - 24  # The y-coordinate of the top edge.
        window_width = window_left + 410  # The width of the region.
        window_height = (self.home_button_location[1] + 24) - window_top  # The height of the region.

        self.image_tools.update_window_dimensions(window_left, window_top, window_width, window_height)

        if self._debug_mode:
            self.print_and_save("[SUCCESS] Dimensions of the bot window has been successfully recalibrated.")

        if display_info_check:
            window_dimensions = self.image_tools.get_window_dimensions()
            self.print_and_save("\n********************************************************************************")
            self.print_and_save("********************************************************************************")
            self.print_and_save(f"[INFO] Screen Size: {pyautogui.size()}")
            self.print_and_save(f"[INFO] Game Window Dimensions: Region({window_dimensions[0]}, {window_dimensions[1]}, {window_dimensions[2]}, {window_dimensions[3]})")
            self.print_and_save("********************************************************************************")
            self.print_and_save("********************************************************************************")

        return None

    def go_back_home(self, confirm_location_check: bool = False, display_info_check: bool = False):
        """Go back to the Home screen to reset the position of the bot. Also able to recalibrate the region dimensions of the bot window if
        display_info_check is True.

        Args:
            confirm_location_check (bool, optional): Check to see if the current location is confirmed to be at the Home screen. Defaults to False.
            display_info_check (bool, optional): Recalibrate the bot window dimensions and displays the info. Defaults to False.

        Returns:
            None
        """
        if not self.image_tools.confirm_location("home"):
            self.print_and_save("\n[INFO] Moving back to the Home screen...")
            self.find_and_click_button("home")
        else:
            self.print_and_save("[INFO] Bot is at the Home screen.")

        # Recalibrate the dimensions of the bot window.
        if display_info_check:
            self._calibrate_game_window(display_info_check = True)

        if confirm_location_check:
            self.image_tools.confirm_location("home")

        return None

    @staticmethod
    def wait(seconds: int = 3):
        """Wait the specified seconds to account for ping or loading.

        Args:
            seconds (int, optional): Number of seconds for the execution to wait for. Defaults to 3.

        Returns:
            None
        """
        time.sleep(seconds)
        return None

    def find_and_click_button(self, button_name: str, clicks: int = 1, tries: int = 2, suppress_error: bool = False):
        """Find the center point of a button image and click it.

        Args:
            button_name (str): Name of the button image file in the /images/buttons/ folder.
            clicks (int): Number of mouse clicks when clicking the button image location. Defaults to 1.
            tries (int): Number of tries to attempt to find the specified button image. Defaults to 2.
            suppress_error (bool): Suppresses template matching error depending on boolean. Defaults to False.

        Returns:
            (bool): Return True if the button was found and clicked. Otherwise, return False.
        """
        if self._debug_mode:
            self.print_and_save(f"[DEBUG] Attempting to find and click the button: \"{button_name}\".")

        if button_name.lower() == "quest":
            temp_location = self.image_tools.find_button("quest_blue", tries = tries, suppress_error = suppress_error)
            if temp_location is None:
                temp_location = self.image_tools.find_button("quest_red", tries = tries, suppress_error = suppress_error)
            if temp_location is None:
                temp_location = self.image_tools.find_button("quest_blue_strike_time", tries = tries, suppress_error = suppress_error)
            if temp_location is None:
                temp_location = self.image_tools.find_button("quest_red_strike_time", tries = tries, suppress_error = suppress_error)

            if temp_location is not None:
                self.mouse_tools.move_and_click_point(temp_location[0], temp_location[1], "quest_blue", mouse_clicks = clicks)
                return True
        elif button_name.lower() == "raid":
            temp_location = self.image_tools.find_button("raid_flat", tries = tries, suppress_error = suppress_error)
            if temp_location is None:
                temp_location = self.image_tools.find_button("raid_bouncing", tries = tries, suppress_error = suppress_error)

            if temp_location is not None:
                self.mouse_tools.move_and_click_point(temp_location[0], temp_location[1], "raid_flat", mouse_clicks = clicks)
                return True
        elif button_name.lower() == "coop_start":
            temp_location = self.image_tools.find_button("coop_start_flat", tries = tries, suppress_error = suppress_error)
            if temp_location is None:
                temp_location = self.image_tools.find_button("coop_start_faded", tries = tries, suppress_error = suppress_error)

            if temp_location is not None:
                self.mouse_tools.move_and_click_point(temp_location[0], temp_location[1], "coop_start_flat", mouse_clicks = clicks)
                return True
        elif button_name.lower() == "event_special_quest":
            temp_location = self.image_tools.find_button("event_special_quest", tries = tries, suppress_error = suppress_error)
            if temp_location is None:
                temp_location = self.image_tools.find_button("event_special_quest_flat", tries = tries, suppress_error = suppress_error)
            if temp_location is None:
                temp_location = self.image_tools.find_button("event_special_quest_bouncing", tries = tries, suppress_error = suppress_error)

            if temp_location is not None:
                self.mouse_tools.move_and_click_point(temp_location[0], temp_location[1], "event_special_quest", mouse_clicks = clicks)
                return True
        else:
            temp_location = self.image_tools.find_button(button_name.lower(), tries = tries, suppress_error = suppress_error)
            if temp_location is not None:
                self.mouse_tools.move_and_click_point(temp_location[0], temp_location[1], button_name, mouse_clicks = clicks)
                return True

        return False

    def check_for_captcha(self):
        """Checks for CAPTCHA right after selecting a Summon and if detected, alert the user and then stop the bot.

        Returns:
            None
        """
        try:
            self.wait(2)
            if self.image_tools.confirm_location("captcha", tries = 1):
                raise RuntimeError("CAPTCHA DETECTED!")
            else:
                self.print_and_save("\n[CAPTCHA] CAPTCHA not detected. Moving on to Party Selection...")

            return None
        except RuntimeError:
            self.print_and_save(f"\n[ERROR] Bot encountered exception while checking for CAPTCHA: \n{traceback.format_exc()}")
            self.image_tools.generate_alert_for_captcha()
            self._is_bot_running.value = 1
            self.wait(1)

    def _delay_between_runs(self):
        """Execute a delay after every run completed based on user settings from config.ini.

        Returns:
            None
        """
        if self._enable_delay_between_runs:
            # Check if the provided delay is valid.
            if int(self._delay_in_seconds) < 0:
                self.print_and_save("\n[INFO] Provided delay in seconds for the resting period is not valid. Defaulting to 15 seconds.")
                self._delay_in_seconds = 15

            self.print_and_save(f"\n[INFO] Now waiting for {self._delay_in_seconds} seconds as the resting period. Please do not navigate from the current screen.")

            self.wait(int(self._delay_in_seconds))
        elif not self._enable_delay_between_runs and self._enable_randomized_delay_between_runs:
            # Check if the lower and upper bounds are valid.
            if int(self._delay_in_seconds_lower_bound) < 0 or int(self._delay_in_seconds_lower_bound) > int(self._delay_in_seconds_upper_bound):
                self.print_and_save("\n[INFO] Provided lower bound delay in seconds for the resting period is not valid. Defaulting to 15 seconds.")
                self._delay_in_seconds_lower_bound = 15
            if int(self._delay_in_seconds_upper_bound) < 0 or int(self._delay_in_seconds_upper_bound) < int(self._delay_in_seconds_lower_bound):
                self.print_and_save("\n[INFO] Provided upper bound delay in seconds for the resting period is not valid. Defaulting to 60 seconds.")
                self._delay_in_seconds_upper_bound = 60

            new_seconds = random.randrange(int(self._delay_in_seconds_lower_bound), int(self._delay_in_seconds_upper_bound))
            self.print_and_save(
                f"\n[INFO] Given the bounds of ({self._delay_in_seconds_lower_bound}, {self._delay_in_seconds_upper_bound}), bot will now wait for {new_seconds} seconds as a resting period. Please do not navigate from the current screen.")

            self.wait(new_seconds)

        self.print_and_save("\n[INFO] Resting period complete.")
        return None

    def _select_summon(self, summon_list: Iterable[str], summon_element_list: Iterable[str]):
        """Finds and selects the specified Summon based on the current index on the Summon Selection screen and then checks for CAPTCHA right
        afterwards.

        Args:
            summon_list (Iterable[str]): List of names of the Summon image's file name in /images/summons/ folder.
            summon_element_list (Iterable[str]): List of names of the Summon element image file in the /images/buttons/ folder.

        Returns:
            (bool): True if the Summon was found and clicked. Otherwise, return False.
        """
        # Format the Summon name and Summon element name strings.
        for idx, summon in enumerate(summon_list):
            summon_list[idx] = summon.lower().replace(" ", "_")
        for idx, summon_ele in enumerate(summon_element_list):
            summon_element_list[idx] = summon_ele.lower()

        summon_location = self.image_tools.find_summon(summon_list, summon_element_list, self.home_button_location[0], self.home_button_location[1])
        if summon_location is not None:
            self.mouse_tools.move_and_click_point(summon_location[0], summon_location[1], "template_support_summon")

            # Check for CAPTCHA here. If detected, stop the bot and alert the user.
            self.check_for_captcha()

            return True
        else:
            # If a Summon is not found, start a Trial Battle to refresh Summons.
            self._reset_summons()
            return False

    def _reset_summons(self):
        """Reset the Summons available by starting and then retreating from a Old Lignoid Trial Battle.

        Returns:
            None
        """
        self.print_and_save("\n[INFO] Now refreshing Summons...")
        self.go_back_home(confirm_location_check = True)

        # Scroll down the screen to see the "Gameplay Extra" button on smaller screen sizes.
        self.mouse_tools.scroll_screen_from_home_button(-600)

        if self.find_and_click_button("gameplay_extras"):
            # If the bot cannot find the "Trial Battles" button, keep scrolling down until it does. It should not take more than 2 loops to see it for any reasonable screen size.
            while self.find_and_click_button("trial_battles") is False:
                self.mouse_tools.scroll_screen_from_home_button(-300)

            if self.image_tools.confirm_location("trial_battles"):
                # Click on the "Old Lignoid" button.
                self.find_and_click_button("trial_battles_old_lignoid")

                # Select any detected "Play" button.
                self.find_and_click_button("play_round_button")

                # Now select the first Summon.
                choose_a_summon_location = self.image_tools.find_button("choose_a_summon")
                self.mouse_tools.move_and_click_point(choose_a_summon_location[0], choose_a_summon_location[1] + 187, "choose_a_summon")

                # Now start the Old Lignoid Trial Battle right away and then wait a few seconds.
                self.find_and_click_button("party_selection_ok")
                self.wait(3)

                # Close the popup and then retreat from this Trial Battle.
                if self.image_tools.confirm_location("trial_battles_description"):
                    self.find_and_click_button("close")

                    self.find_and_click_button("menu")
                    self.find_and_click_button("retreat")
                    self.find_and_click_button("retreat_confirmation")
                    self.find_and_click_button("next")

        if self.image_tools.confirm_location("trial_battles"):
            self.print_and_save("[SUCCESS] Summons have now been refreshed.")

        return None

    def _find_party_and_start_mission(self, group_number: int, party_number: int, tries: int = 3):
        """Select the specified Group and Party. It will then start the mission.

        Args:
            group_number (int): The Group that the specified Party in in.
            party_number (int): The specified Party to start the mission with.
            tries (int, optional): Number of tries to select a Set before failing. Defaults to 3.

        Returns:
            (bool): Returns False if it detects the "Raid is full/Raid is already done" dialog. Otherwise, return True.
        """
        # Find the Group that the Party is in first. If the specified Group number is less than 8, it is in Set A. Otherwise, it is in Set B. If failed, alternate searching for Set A / Set B until
        # found or tries are depleted.
        set_location = None
        if group_number < 8:
            while set_location is None:
                set_location = self.image_tools.find_button("party_set_a", tries = 1)
                if set_location is None:
                    tries -= 1
                    if tries <= 0:
                        raise Exception("Could not find Set A.")

                    # See if the user had Set B active instead of Set A if matching failed.
                    set_location = self.image_tools.find_button("party_set_b", tries = 1)
        else:
            while set_location is None:
                set_location = self.image_tools.find_button("party_set_b", tries = 1)
                if set_location is None:
                    tries -= 1
                    if tries <= 0:
                        raise Exception("Could not find Set B.")

                    # See if the user had Set A active instead of Set B if matching failed.
                    set_location = self.image_tools.find_button("party_set_a", tries = 1)

        # Center the mouse on the "Set A" / "Set B" button and then click the correct Group tab.
        if self._debug_mode:
            self.print_and_save(f"\n[DEBUG] Successfully selected the correct Set. Now selecting Group {group_number}...")

        if group_number == 1:
            x = set_location[0] - 350
        elif group_number == 2:
            x = set_location[0] - 290
        elif group_number == 3:
            x = set_location[0] - 230
        elif group_number == 4:
            x = set_location[0] - 170
        elif group_number == 5:
            x = set_location[0] - 110
        elif group_number == 6:
            x = set_location[0] - 50
        else:
            x = set_location[0] + 10

        y = set_location[1] + 50
        self.mouse_tools.move_and_click_point(x, y, "template_group", mouse_clicks = 2)

        # Now select the correct Party.
        if self._debug_mode:
            self.print_and_save(f"[DEBUG] Successfully selected Group {group_number}. Now selecting Party {party_number}...")

        if party_number == 1:
            x = set_location[0] - 309
        elif party_number == 2:
            x = set_location[0] - 252
        elif party_number == 3:
            x = set_location[0] - 195
        elif party_number == 4:
            x = set_location[0] - 138
        elif party_number == 5:
            x = set_location[0] - 81
        elif party_number == 6:
            x = set_location[0] - 24

        y = set_location[1] + 325
        self.mouse_tools.move_and_click_point(x, y, "template_party", mouse_clicks = 2)

        if self._debug_mode:
            self.print_and_save(f"[DEBUG] Successfully selected Party {party_number}. Now starting the mission.")

        # Find and click the "OK" button to start the mission.
        self.find_and_click_button("ok")

        # If a popup appears and says "This raid battle has already ended. The Home screen will now appear.", return False.
        if self.farming_mode.lower() == "raid" and self.image_tools.confirm_location("raid_just_ended_home_redirect"):
            self.print_and_save("\n[WARNING] Raid unfortunately just ended. Backing out now...")
            self.find_and_click_button("ok")
            return False

        return True

    def check_for_ap(self):
        """Check if the user encountered the "Not Enough AP" popup and it will refill using either Half or Full Elixir.

        Returns:
            None
        """
        # Loop until the user gets to the Summon Selection screen.
        while (self.farming_mode.lower() != "coop" and not self.image_tools.confirm_location("select_summon", tries = 2)) or (
                self.farming_mode.lower() == "coop" and not self.image_tools.confirm_location("coop_without_support_summon", tries = 2)):
            if self.image_tools.confirm_location("not_enough_ap", tries = 2):
                # If the bot detects that the user has run out of AP, it will refill using either Half Elixir or Full Elixir.
                if self._use_full_elixir is False:
                    self.print_and_save("\n[INFO] AP ran out! Using Half Elixir...")
                    half_ap_location = self.image_tools.find_button("refill_half_ap")
                    self.mouse_tools.move_and_click_point(half_ap_location[0], half_ap_location[1] + 175, "use")
                else:
                    self.print_and_save("\n[INFO] AP ran out! Using Full Elixir...")
                    full_ap_location = self.image_tools.find_button("refill_full_ap")
                    self.mouse_tools.move_and_click_point(full_ap_location[0], full_ap_location[1] + 175, "use")

                # Press the "OK" button to move to the Summon Selection screen.
                self.wait(1)
                self.find_and_click_button("ok")
                return None
            elif self.farming_mode.lower() == "coop" and not self._coop_first_run and self.image_tools.find_button("attack"):
                break
            else:
                self.wait(1)

        self.print_and_save("[INFO] AP is available. Continuing...")
        return None

    def check_for_ep(self):
        """Check if the user encountered the "Not Enough EP" popup and it will refill using either Soul Berry or Soul Balm.

        Returns:
            None
        """
        if self.farming_mode.lower() == "raid" and self.image_tools.confirm_location("not_enough_ep", tries = 2):
            # If the bot detects that the user has run out of EP, it will refill using either Soul Berry or Soul Balm.
            if self._use_soul_balm is False:
                self.print_and_save("\n[INFO] EP ran out! Using Soul Berries...")
                half_ep_location = self.image_tools.find_button("refill_soul_berry")
                self.mouse_tools.move_and_click_point(half_ep_location[0], half_ep_location[1] + 175, "use")
            else:
                self.print_and_save("\n[INFO] EP ran out! Using Soul Balm...")
                full_ep_location = self.image_tools.find_button("refill_soul_balm")
                self.mouse_tools.move_and_click_point(full_ep_location[0], full_ep_location[1] + 175, "use")

            # Press the "OK" button to move to the Summon Selection screen.
            self.wait(1)
            self.find_and_click_button("ok")
        else:
            self.print_and_save("[INFO] EP is available. Continuing...")

        return None

    def collect_loot(self, is_pending_battle: bool = False, is_event_nightmare: bool = False):
        """Collect the loot from the Results screen while clicking away any dialog popups. Primarily for raids.
        
        Args:
            is_pending_battle (bool): Skip the incrementation of runs attempted if this was a Pending Battle. Defaults to False.
            is_event_nightmare (bool): Skip the incrementation of runs attempted if this was a Event Nightmare. Defaults to False.

        Returns:
            None
        """
        temp_amount = 0

        # Click away the "EXP Gained" popup and any other popups until the bot reaches the Loot Collected screen.
        if not self._retreat_check and self.image_tools.confirm_location("exp_gained"):
            while not self.image_tools.confirm_location("loot_collected", tries = 1):
                self.find_and_click_button("close", tries = 1, suppress_error = True)
                self.find_and_click_button("cancel", tries = 1, suppress_error = True)
                self.find_and_click_button("ok", tries = 1, suppress_error = True)

                # Search for and click on the "Extended Mastery" popup.
                self.find_and_click_button("new_extended_mastery_level", tries = 1, suppress_error = True)

            # Now that the bot is at the Loot Collected screen, detect any user-specified items.
            if not is_pending_battle and not is_event_nightmare:
                self.print_and_save("\n[INFO] Detecting if any user-specified loot dropped this run...")
                if self._item_name != "EXP" and self._item_name != "Angel Halo Weapons" and self._item_name != "Repeated Runs":
                    temp_amount = self.image_tools.find_farmed_items([self._item_name])[0]
                else:
                    temp_amount = 1

                self._item_amount_farmed += temp_amount
                self._amount_of_runs_finished += 1
        else:
            # If the bot reached here, that means the raid ended without the bot being able to take action so no loot
            # dropped.
            temp_amount = 0

        if not is_pending_battle and not is_event_nightmare:
            if self._item_name != "EXP" and self._item_name != "Angel Halo Weapons" and self._item_name != "Repeated Runs":
                self.print_and_save("\n\n********************************************************************************")
                self.print_and_save("********************************************************************************")
                self.print_and_save(f"[FARM] Farming Mode: {self.farming_mode}")
                self.print_and_save(f"[FARM] Mission: {self._mission_name}")
                self.print_and_save(f"[FARM] Summons: {self._summon_list}")
                self.print_and_save(f"[FARM] Amount of {self._item_name} gained this run: {temp_amount}")
                self.print_and_save(f"[FARM] Amount of {self._item_name} gained in total: {self._item_amount_farmed} / {self._item_amount_to_farm}")
                self.print_and_save(f"[FARM] Amount of runs completed: {self._amount_of_runs_finished}")
                self.print_and_save("********************************************************************************")
                self.print_and_save("********************************************************************************\n")
            else:
                self.print_and_save("\n\n********************************************************************************")
                self.print_and_save("********************************************************************************")
                self.print_and_save(f"[FARM] Farming Mode: {self.farming_mode}")
                self.print_and_save(f"[FARM] Mission: {self._mission_name}")
                self.print_and_save(f"[FARM] Summons: {self._summon_list}")
                self.print_and_save(f"[FARM] Amount of runs completed: {self._amount_of_runs_finished} / {self._item_amount_to_farm}")
                self.print_and_save("********************************************************************************")
                self.print_and_save("********************************************************************************\n")

        return None

    def check_for_friend_request(self):
        """Detect any "Friend Request" popups and click them away.

        Returns:
            None
        """
        if self.image_tools.confirm_location("friend_request", tries = 1):
            self.print_and_save("\n[INFO] Detected \"Friend Request\" popup. Closing it now...")
            self.find_and_click_button("cancel")

        return None

    def _check_for_event_nightmare(self):
        """Checks for Event Nightmare and if it appears and the user enabled it in config.ini, start it.

        Returns:
            (bool): Return True if Event Nightmare was detected and successfully completed. Otherwise, return False.
        """
        if self._enable_event_nightmare and self.image_tools.confirm_location("limited_time_quests"):
            # First check if the Event Nightmare is skippable.
            event_claim_loot_location = self.image_tools.find_button("event_claim_loot", tries = 1, suppress_error = True)
            if event_claim_loot_location is not None:
                self.print_and_save("\n[EVENT] Skippable Event Nightmare detected. Claiming it now...")
                self.mouse_tools.move_and_click_point(event_claim_loot_location[0], event_claim_loot_location[1], "event_claim_loot")
                self.collect_loot(is_event_nightmare = True)
                return True
            else:
                self.print_and_save("\n[EVENT] Detected Event Nightmare. Starting it now...")

                self.print_and_save("\n\n********************************************************************************")
                self.print_and_save("********************************************************************************")
                self.print_and_save("[EVENT] Event Nightmare")
                self.print_and_save("[EVENT] Event Nightmare Summon Elements: {self._event_nightmare_summon_element_list}")
                self.print_and_save("[EVENT] Event Nightmare Summons: {self._event_nightmare_summon_list}")
                self.print_and_save("[EVENT] Event Nightmare Group Number: {self._event_nightmare_group_number}")
                self.print_and_save("[EVENT] Event Nightmare Party Number: {self._event_nightmare_party_number}")
                self.print_and_save("[EVENT] Event Nightmare Combat Script: {self._event_nightmare_combat_script}")
                self.print_and_save("********************************************************************************")
                self.print_and_save("********************************************************************************\n")

                self.find_and_click_button("play_next")

                # Once the bot is at the Summon Selection screen, select your Summon and Party and start the mission.
                self.wait(1)
                if self.image_tools.confirm_location("select_summon"):
                    self._select_summon(self._event_nightmare_summon_list, self._event_nightmare_summon_element_list)
                    start_check = self._find_party_and_start_mission(self._event_nightmare_group_number, self._event_nightmare_party_number)

                    # Once preparations are completed, start Combat Mode.
                    if start_check and self.combat_mode.start_combat_mode(self._event_nightmare_combat_script, is_nightmare = True):
                        self.collect_loot(is_event_nightmare = True)
                        return True

        elif not self._enable_event_nightmare and self.image_tools.confirm_location("limited_time_quests"):
            # First check if the Event Nightmare is skippable.
            event_claim_loot_location = self.image_tools.find_button("event_claim_loot", tries = 1, suppress_error = True)
            if event_claim_loot_location is not None:
                self.print_and_save("\n[EVENT] Skippable Event Nightmare detected but user opted to not run it. Claiming it regardless...")
                self.mouse_tools.move_and_click_point(event_claim_loot_location[0], event_claim_loot_location[1], "event_claim_loot")
                self.collect_loot(is_event_nightmare = True)
                return True
            else:
                self.print_and_save("\n[EVENT] Event Nightmare detected but user opted to not run it. Moving on...")
                self.find_and_click_button("close")
        else:
            self.print_and_save("\n[EVENT] No Event Nightmare detected. Moving on...")

        return False

    def _check_for_dimensional_halo(self):
        """Checks for Dimensional Halo and if it appears and the user enabled it in config.ini, start it.

        Returns:
            (bool): Return True if Dimensional Halo was detected and successfully completed. Otherwise, return False.
        """
        if self._enable_dimensional_halo and self.image_tools.confirm_location("limited_time_quests", tries = 1):
            self.print_and_save("\n[D.HALO] Detected Dimensional Halo. Starting it now...")
            self._dimensional_halo_amount += 1

            self.print_and_save("\n\n********************************************************************************")
            self.print_and_save("********************************************************************************")
            self.print_and_save(f"[D.HALO] Dimensional Halo")
            self.print_and_save(f"[D.HALO] Dimensional Halo Summon Elements: {self._dimensional_halo_summon_element_list}")
            self.print_and_save(f"[D.HALO] Dimensional Halo Summons: {self._dimensional_halo_summon_list}")
            self.print_and_save(f"[D.HALO] Dimensional Halo Group Number: {self._dimensional_halo_group_number}")
            self.print_and_save(f"[D.HALO] Dimensional Halo Party Number: {self._dimensional_halo_party_number}")
            self.print_and_save(f"[D.HALO] Dimensional Halo Combat Script: {self._dimensional_halo_combat_script}")
            self.print_and_save(f"[D.HALO] Amount of Dimensional Halos encountered: {self._dimensional_halo_amount}")
            self.print_and_save("********************************************************************************")
            self.print_and_save("********************************************************************************\n")

            self.find_and_click_button("play_next")

            # Once the bot is at the Summon Selection screen, select your Summon and Party and start the mission.
            self.wait(1)
            if self.image_tools.confirm_location("select_summon"):
                self._select_summon(self._dimensional_halo_summon_list, self._dimensional_halo_summon_element_list)
                start_check = self._find_party_and_start_mission(self._dimensional_halo_group_number, self._dimensional_halo_party_number)

                # Once preparations are completed, start Combat Mode.
                if start_check and self.combat_mode.start_combat_mode(self._dimensional_halo_combat_script, is_nightmare = True):
                    self.collect_loot()
                    return True

        elif not self._enable_dimensional_halo and self.image_tools.confirm_location("limited_time_quests", tries = 1):
            self.print_and_save("\n[D.HALO] Dimensional Halo detected but user opted to not run it. Moving on...")
            self.find_and_click_button("close")
        else:
            self.print_and_save("\n[D.HALO] No Dimensional Halo detected. Moving on...")

        return False

    def _check_for_rotb_extreme_plus(self):
        """Checks for Extreme+ for Rise of the Beasts and if it appears and the user enabled it in config.ini, start it.

        Returns:
            (bool): Return True if Extreme+ was detected and successfully completed. Otherwise, return False.
        """
        if self._enable_rotb_extreme_plus and self.image_tools.confirm_location("rotb_extreme_plus", tries = 2):
            self.print_and_save("\n[ROTB] Detected Extreme+. Starting it now...")

            self.print_and_save("\n\n********************************************************************************")
            self.print_and_save("********************************************************************************")
            self.print_and_save(f"[ROTB] Rise of the Beasts Extreme+")
            self.print_and_save(f"[ROTB] Rise of the Beasts Extreme+ Summon Elements: {self._rotb_extreme_plus_summon_element_list}")
            self.print_and_save(f"[ROTB] Rise of the Beasts Extreme+ Summons: {self._rotb_extreme_plus_summon_list}")
            self.print_and_save(f"[ROTB] Rise of the Beasts Extreme+ Group Number: {self._rotb_extreme_plus_group_number}")
            self.print_and_save(f"[ROTB] Rise of the Beasts Extreme+ Party Number: {self._rotb_extreme_plus_party_number}")
            self.print_and_save(f"[ROTB] Rise of the Beasts Extreme+ Combat Script: {self._rotb_extreme_plus_combat_script}")
            self.print_and_save(f"[ROTB] Amount of Rise of the Beasts Extreme+ encountered: {self._rotb_extreme_plus_amount}")
            self.print_and_save("********************************************************************************")
            self.print_and_save("********************************************************************************\n")

            self.find_and_click_button("play_next")

            # Once the bot is at the Summon Selection screen, select your Summon and Party and start the mission.
            self.wait(1)
            if self.image_tools.confirm_location("select_summon"):
                self._select_summon(self._rotb_extreme_plus_summon_list, self._rotb_extreme_plus_summon_element_list)
                start_check = self._find_party_and_start_mission(self._rotb_extreme_plus_group_number, self._rotb_extreme_plus_party_number)

                # Once preparations are completed, start Combat mode.
                if start_check and self.combat_mode.start_combat_mode(self._rotb_extreme_plus_combat_script, is_nightmare = True):
                    self.collect_loot()
                    return True

        elif not self._enable_rotb_extreme_plus and self.image_tools.confirm_location("rotb_extreme_plus", tries = 2):
            self.print_and_save("\n[ROTB] Rise of the Beasts Extreme+ detected but user opted to not run it. Moving on...")
            self.find_and_click_button("close")
        else:
            self.print_and_save("\n[ROTB] No Rise of the Beasts Extreme+ detected. Moving on...")

        return False

    def start_farming_mode(self, item_name: str, item_amount_to_farm: int, farming_mode: str, location_name: str, mission_name: str,
                           summon_element_list: Iterable[str], summon_list: Iterable[str], group_number: int, party_number: int):
        """Start the Farming Mode using the given parameters.

        Args:
            item_name (str): Name of the item to farm.
            item_amount_to_farm (int): Amount of the item to farm.
            farming_mode (str): Mode to look for the specified item and map in.
            location_name (str): Name of the map to look for the specified mission in.
            mission_name (str): Name of the mission to farm the item in.
            summon_element_list (Iterable[str]): List of names of the Summon element image file in the /images/buttons/ folder.
            summon_list (Iterable[str]): List of names of the Summon image's file name in /images/summons/ folder.
            group_number (int): The Group that the specified Party in in.
            party_number (int): The specified Party to start the mission with.
        
        Returns:
            None
        """
        try:
            if item_name != "EXP":
                self.print_and_save("\n\n################################################################################")
                self.print_and_save("################################################################################")
                self.print_and_save(f"[FARM] Starting Farming Mode for {farming_mode}.")
                self.print_and_save(f"[FARM] Farming {item_amount_to_farm}x {item_name} at {mission_name}.")
                self.print_and_save("################################################################################")
                self.print_and_save("################################################################################\n")
            else:
                self.print_and_save("\n\n################################################################################")

                self.print_and_save("################################################################################")
                self.print_and_save(f"[FARM] Starting Farming Mode for {farming_mode}.")
                self.print_and_save(f"[FARM] Doing {item_amount_to_farm}x runs for {item_name} at {mission_name}.")
                self.print_and_save("################################################################################")
                self.print_and_save("################################################################################\n")

            # Parse the difficulty for the chosen mission.
            difficulty = ""
            if farming_mode.lower() == "special" or farming_mode.lower() == "event" or farming_mode.lower() == "event (token drawboxes)" or farming_mode.lower() == "rise of the beasts":
                if mission_name.find("N ") == 0:
                    difficulty = "Normal"
                elif mission_name.find("H ") == 0:
                    difficulty = "Hard"
                elif mission_name.find("VH ") == 0:
                    difficulty = "Very Hard"
                elif mission_name.find("EX ") == 0:
                    difficulty = "Extreme"
                elif mission_name.find("IM ") == 0:
                    difficulty = "Impossible"
            elif farming_mode.lower() == "dread barrage":
                if mission_name.find("1 Star") == 0:
                    difficulty = "1 Star"
                elif mission_name.find("2 Star") == 0:
                    difficulty = "2 Star"
                elif mission_name.find("3 Star") == 0:
                    difficulty = "3 Star"
                elif mission_name.find("4 Star") == 0:
                    difficulty = "4 Star"
                elif mission_name.find("5 Star") == 0:
                    difficulty = "5 Star"

            self._item_amount_farmed = 0
            self._amount_of_runs_finished = 0
            start_check = False
            summon_check = False

            # Save the following information to share between the Game class and the MapSelection class.
            self._item_name = item_name
            self._item_amount_to_farm = item_amount_to_farm
            self.farming_mode = farming_mode
            self._mission_name = mission_name
            self._summon_element_list = summon_element_list
            self._summon_list = summon_list
            self._group_number = group_number
            self._party_number = party_number

            # If Dimensional Halo is enabled, save settings for it based on conditions.
            if self.farming_mode.lower() == "special" and self._mission_name == "VH Angel Halo" and self._enable_dimensional_halo and (
                    self._item_name == "EXP" or self._item_name == "Angel Halo Weapons"):
                self.print_and_save("\n[INFO] Initializing settings for Dimensional Halo...")

                if self._dimensional_halo_combat_script == "":
                    self.print_and_save("[INFO] Combat Script for Dimensional Halo will reuse the one for Farming Mode.")
                    self._dimensional_halo_combat_script = self._combat_script

                if len(self._dimensional_halo_summon_element_list) == 0:
                    self.print_and_save("[INFO] Summon Elements for Dimensional Halo will reuse the ones for Farming Mode.")
                    self._dimensional_halo_summon_element_list = self._summon_element_list

                if len(self._dimensional_halo_summon_list) == 0:
                    self.print_and_save("[INFO] Summons for Dimensional Halo will reuse the ones for Farming Mode.")
                    self._dimensional_halo_summon_list = self._summon_list

                if self._dimensional_halo_group_number == "":
                    self.print_and_save("[INFO] Group Number for Dimensional Halo will reuse the one for Farming Mode.")
                    self._dimensional_halo_group_number = self._group_number
                else:
                    self._dimensional_halo_group_number = int(self._dimensional_halo_group_number)

                if self._dimensional_halo_party_number == "":
                    self.print_and_save("[INFO] Party Number for Dimensional Halo will reuse the one for Farming Mode.")
                    self._dimensional_halo_party_number = self._party_number
                else:
                    self._dimensional_halo_party_number = int(self._dimensional_halo_party_number)

                self.print_and_save("[INFO] Settings initialized for Dimensional Halo...")
            elif self._item_name == "Repeated Runs" and self._enable_event_nightmare:
                # Do the same for Event Nightmare if enabled.
                self.print_and_save("\n[INFO] Initializing settings for Event...")

                if self._event_nightmare_combat_script == "":
                    self.print_and_save("[INFO] Combat Script for Event will reuse the one for Farming Mode.")
                    self._event_nightmare_combat_script = self._combat_script

                if len(self._event_nightmare_summon_element_list) == 0:
                    self.print_and_save("[INFO] Summon Elements for Event will reuse the ones for Farming Mode.")
                    self._event_nightmare_summon_element_list = self._summon_element_list

                if len(self._event_nightmare_summon_list) == 0:
                    self.print_and_save("[INFO] Summons for Event will reuse the ones for Farming Mode.")
                    self._event_nightmare_summon_list = self._summon_list

                if self._event_nightmare_group_number == "":
                    self.print_and_save("[INFO] Group Number for Event will reuse the one for Farming Mode.")
                    self._event_nightmare_group_number = self._group_number
                else:
                    self._event_nightmare_group_number = int(self._event_nightmare_group_number)

                if self._event_nightmare_party_number == "":
                    self.print_and_save("[INFO] Party Number for Event will reuse the one for Farming Mode.")
                    self._event_nightmare_party_number = self._party_number
                else:
                    self._event_nightmare_party_number = int(self._event_nightmare_party_number)

                self.print_and_save("[INFO] Settings initialized for Event...")
            elif self._item_name == "Repeated Runs" and self._enable_rotb_extreme_plus:
                # Do the same for Rise of the Beasts Extreme+ if enabled.
                self.print_and_save("\n[INFO] Initializing settings for Rise of the Beasts Extreme+...")

                if self._rotb_extreme_plus_combat_script == "":
                    self.print_and_save("[INFO] Combat Script for Rise of the Beasts Extreme+ will reuse the one for Farming Mode.")
                    self._event_nightmare_combat_script = self._combat_script

                if len(self._rotb_extreme_plus_summon_element_list) == 0:
                    self.print_and_save("[INFO] Summon Elements for Rise of the Beasts Extreme+ will reuse the ones for Farming Mode.")
                    self._rotb_extreme_plus_summon_element_list = self._summon_element_list

                if len(self._rotb_extreme_plus_summon_list) == 0:
                    self.print_and_save("[INFO] Summons for Rise of the Beasts Extreme+ will reuse the ones for Farming Mode.")
                    self._rotb_extreme_plus_summon_list = self._summon_list

                if self._rotb_extreme_plus_group_number == "":
                    self.print_and_save("[INFO] Group Number for Rise of the Beasts Extreme+ will reuse the one for Farming Mode.")
                    self._rotb_extreme_plus_group_number = self._group_number
                else:
                    self._rotb_extreme_plus_group_number = int(self._rotb_extreme_plus_group_number)

                if self._rotb_extreme_plus_party_number == "":
                    self.print_and_save("[INFO] Party Number for Rise of the Beasts Extreme+ will reuse the one for Farming Mode.")
                    self._rotb_extreme_plus_party_number = self._party_number
                else:
                    self._rotb_extreme_plus_party_number = int(self._rotb_extreme_plus_party_number)

                self.print_and_save("[INFO] Settings initialized for Rise of the Beasts Extreme+...")
            elif self._item_name == "Repeated Runs" and self._enable_unparalleled_foe:
                # Do the same for Dread Barrage Unparalleled Foes if enabled.
                self.print_and_save("\n[INFO] Initializing settings for Dread Barrage Unparalleled Foes...")

                if self.unparalleled_foe_combat_script == "":
                    self.print_and_save("[INFO] Combat Script for Dread Barrage Unparalleled Foes will reuse the one for Farming Mode.")
                    self.unparalleled_foe_combat_script = self._combat_script

                if len(self._unparalleled_foe_summon_element_list) == 0:
                    self.print_and_save("[INFO] Summon Elements for Dread Barrage Unparalleled Foes will reuse the ones for Farming Mode.")
                    self._unparalleled_foe_summon_element_list = self._summon_element_list

                if len(self._unparalleled_foe_summon_list) == 0:
                    self.print_and_save("[INFO] Summons for Dread Barrage Unparalleled Foes will reuse the ones for Farming Mode.")
                    self._unparalleled_foe_summon_list = self._summon_list

                if self._unparalleled_foe_group_number == "":
                    self.print_and_save("[INFO] Group Number for Dread Barrage Unparalleled Foes will reuse the one for Farming Mode.")
                    self._unparalleled_foe_group_number = self._group_number
                else:
                    self._unparalleled_foe_group_number = int(self._unparalleled_foe_group_number)

                if self._unparalleled_foe_party_number == "":
                    self.print_and_save("[INFO] Party Number for Dread Barrage Unparalleled Foes will reuse the one for Farming Mode.")
                    self._unparalleled_foe_party_number = self._party_number
                else:
                    self._unparalleled_foe_party_number = int(self._unparalleled_foe_party_number)

                self.print_and_save("[INFO] Settings initialized for Dread Barrage Unparalleled Foes...")

            # Main workflow for Farming Mode.
            if (farming_mode.lower() != "raid" and self._map_selection.select_map(farming_mode, location_name, mission_name, difficulty)) or (
                    farming_mode.lower() == "raid" and self._map_selection.join_raid(mission_name)):
                while self._item_amount_farmed < self._item_amount_to_farm:
                    # Loop until the specified Summon has been selected successfully.
                    self.print_and_save("\n[INFO] Selecting Summon before starting mission for Farming Mode...")
                    while summon_check is False and farming_mode.lower() != "coop":
                        # Select the Summon element and the Summon itself.
                        summon_check = self._select_summon(summon_list, summon_element_list)

                        # If the Summons were reset, select the mission again.
                        if summon_check is False:
                            if farming_mode.lower() != "raid":
                                self.print_and_save("\n[INFO] Selecting mission again after resetting Summons...")
                                self._map_selection.select_map(farming_mode, location_name, mission_name, difficulty)
                            else:
                                self.print_and_save("\n[INFO] Joining raids again after resetting Summons...")
                                self._map_selection.join_raid(mission_name)

                    # Select the specified Party and then start the mission.
                    if farming_mode.lower() != "coop":
                        start_check = self._find_party_and_start_mission(group_number, party_number)
                    else:
                        # Only select the Party for this Coop mission once. After that, subsequent runs always has that Party selected.
                        if self._coop_first_run:
                            start_check = self._find_party_and_start_mission(group_number, party_number)
                            self._coop_first_run = False
                            self.find_and_click_button("coop_start")

                        self.print_and_save("[INFO] Starting Coop mission.")

                    # After Party has been successfully selected, start Combat Mode.
                    if start_check and farming_mode.lower() != "raid":
                        # Check for the "Items Picked Up" popup that appears after starting a Quest mission.
                        self.wait(2)
                        if farming_mode.lower() == "quest" and self.image_tools.confirm_location("items_picked_up", tries = 5):
                            self.find_and_click_button("ok")

                        # Start Combat Mode for this mission.
                        if self.combat_mode.start_combat_mode(self._combat_script):
                            # If Combat Mode finished successfully without retreating or exiting prematurely, start loot detection.
                            self.collect_loot()

                            if self._item_amount_farmed < self._item_amount_to_farm:
                                # Click the Play Again button or the Room button if its Coop.
                                if farming_mode.lower() != "coop":
                                    # Generate a resting period if the user enabled it.
                                    self._delay_between_runs()

                                    if not self.find_and_click_button("play_again"):
                                        # Clear away any Pending Battles.
                                        self._map_selection.check_for_pending(farming_mode)

                                        # Start the mission again.
                                        self._map_selection.select_map(farming_mode, location_name, mission_name, difficulty)
                                else:
                                    # Generate a resting period if the user enabled it.
                                    self._delay_between_runs()

                                    self.find_and_click_button("coop_room")
                                    self.wait(1)

                                    # Check for the "Daily Missions" popup for Coop.
                                    if self.image_tools.confirm_location("coop_daily_missions", tries = 1):
                                        self.find_and_click_button("close")

                                    # Now click the "Start" button.
                                    self.find_and_click_button("coop_start")

                                # Check for "Missions" popup for Dread Barrage.
                                if farming_mode.lower() == "dread barrage" and self.image_tools.confirm_location("dread_barrage_missions", tries = 1):
                                    self.print_and_save("[INFO] Found \"Missions\" popup for Dread Barrage. Closing it now...")
                                    self.find_and_click_button("close")

                                # If the user wants to fight Unparalleled Foes during Dread Barrage, then start it.
                                if farming_mode.lower() == "dread barrage" and self.image_tools.confirm_location("dread_barrage_unparalleled_foe", tries = 1):
                                    # Find the locations of the "AP 0" text underneath each Unparalleled Foe.
                                    ap_0_locations = self.image_tools.find_all("ap_0")

                                    if self._enable_unparalleled_foe_level_95 and not self._enable_unparalleled_foe_level_175:
                                        # Start the Level 95 Unparalleled Foe.
                                        self.print_and_save("\n[INFO] Starting Level 95 Unparalleled Foe...")
                                        self.mouse_tools.move_and_click_point(ap_0_locations[0][0], ap_0_locations[0][1], "ap_0")
                                    elif self._enable_unparalleled_foe_level_175 and not self._enable_unparalleled_foe_level_95:
                                        # Start the Level 175 Unparalleled Foe.
                                        self.print_and_save("\n[INFO] Starting Level 175 Unparalleled Foe...")
                                        self.mouse_tools.move_and_click_point(ap_0_locations[1][0], ap_0_locations[1][1], "ap_0")
                                    elif not self._enable_unparalleled_foe_level_95 and not self._enable_unparalleled_foe_level_175:
                                        # Close the popup.
                                        self.print_and_save("\n[INFO] Closing Dread Barrage Unparalleled Foes popup...")
                                        self.find_and_click_button("close")
                                    else:
                                        # Every other case will default to the Level 95 Unparalleled Foe.
                                        self.print_and_save("\n[INFO] Defaulting to Level 95 Unparalleled Foe. Starting it now...")
                                        self.mouse_tools.move_and_click_point(ap_0_locations[0][0], ap_0_locations[0][1], "ap_0")

                                # Check for "Trophy Achieved" popup.
                                if self.image_tools.confirm_location("trophy_achieved", tries = 1):
                                    self.print_and_save("[INFO] Detected \"Trophy Achieved\" popup. Closing it now...")
                                    self.find_and_click_button("close")

                                # Check for any Skyscope popups.
                                if self.enable_skyscope and self.image_tools.confirm_location("skyscope", tries = 1):
                                    self.find_and_click_button("close")

                                # Check for "Daily Missions" popup for Rise of the Beasts.
                                if farming_mode.lower() == "rise of the beasts" and self.image_tools.confirm_location("event_daily_missions", tries = 1):
                                    self.find_and_click_button("close")

                                # Check for "Friend Request" popup.
                                self.check_for_friend_request()

                                # Check for "Proud Solo Quest" popup for Rise of the Beasts.
                                if farming_mode.lower() == "rise of the beasts" and self.image_tools.confirm_location("proud_solo_quest", tries = 1):
                                    # Scroll down the screen a little bit because the popup itself is too long for screen sizes around 1080p.
                                    self.mouse_tools.scroll_screen_from_home_button(-400)
                                    self.find_and_click_button("close")

                                # Check for "Extreme+" popup for Rise of the Beasts.
                                if farming_mode.lower() == "rise of the beasts":
                                    if self._check_for_rotb_extreme_plus():
                                        # Make sure the bot goes back to the Home screen when completing a Extreme+ so that the "Play Again"
                                        # functionality comes back.
                                        self._map_selection.select_map(farming_mode, location_name, mission_name, difficulty)

                                # Check for Dimensional Halo and Event Nightmare.
                                if self.farming_mode.lower() == "special" and self._mission_name == "VH Angel Halo" and (self._item_name == "EXP" or self._item_name == "Angel Halo Weapons"):
                                    if self._check_for_dimensional_halo():
                                        # Make sure the bot goes back to the Home screen when completing a Dimensional Halo so that the "Play Again"
                                        # functionality comes back.
                                        self._map_selection.select_map(farming_mode, location_name, mission_name, difficulty)
                                elif self.farming_mode.lower() == "event" or self.farming_mode.lower() == "event (token drawboxes)":
                                    if self._check_for_event_nightmare():
                                        # Make sure the bot goes back to the Home screen when completing a Event Nightmare so that the "Play Again"
                                        # functionality comes back.
                                        self._map_selection.select_map(farming_mode, location_name, mission_name, difficulty)

                                # Check for any Skyscope popups.
                                if self.enable_skyscope and self.image_tools.confirm_location("skyscope", tries = 1):
                                    self.find_and_click_button("close")

                                # Check for available AP and then reset the Summon check flag.
                                self.check_for_ap()
                                summon_check = False

                                # If the bot tried to repeat a Extreme/Impossible difficulty Event Raid and it lacked the treasures to host it, go
                                # back to select_map().
                                if self.farming_mode.lower() == "event (token drawboxes)" and self.image_tools.confirm_location("not_enough_treasure"):
                                    self.find_and_click_button("ok")

                                    self._map_selection.select_map(farming_mode, location_name, mission_name, difficulty)
                        else:
                            # Start the mission again if the Party wiped or exited prematurely during Combat Mode.
                            self.print_and_save("\n[INFO] Selecting mission again due to retreating...")
                            self._map_selection.select_map(farming_mode, location_name, mission_name, difficulty)

                    elif start_check and farming_mode.lower() == "raid":
                        # Cover the occasional case where joining the raid after selecting the Summon and Party led to the Quest Results screen with
                        # no loot to collect.
                        if self.image_tools.confirm_location("no_loot"):
                            self.print_and_save("\n[INFO] Seems that the raid just ended. Moving back to the Home screen and joining another raid...")
                            self.go_back_home(confirm_location_check = True)
                            summon_check = False
                        else:
                            # Start Combat Mode for this Raid.
                            if self.combat_mode.start_combat_mode(self._combat_script):
                                # If Combat Mode finished successfully without retreating or exiting prematurely, start loot detection.
                                self.collect_loot()

                                if self._item_amount_farmed < self._item_amount_to_farm:
                                    # Generate a resting period if the user enabled it.
                                    self._delay_between_runs()

                                    # Clear away any Pending Battles.
                                    self._map_selection.check_for_pending(farming_mode)

                                    # Join a new raid.
                                    self._map_selection.join_raid(mission_name)
                                    summon_check = False
                            else:
                                # Join a new raid.
                                self._map_selection.join_raid(mission_name)
                                summon_check = False
                    elif not start_check and farming_mode.lower() == "raid":
                        # If the bot reached here, it means that the Raid ended before the bot could start the mission after selecting the Summon and Party.
                        self.print_and_save("[INFO] Seems that the raid ended before the bot was able to join. Now looking for another raid to join...")
                        self._map_selection.join_raid(mission_name)
                        summon_check = False
            else:
                raise RuntimeError("Confirming the location of the Summon Selection screen after selecting the mission returned False.")
        except RuntimeError:
            self.print_and_save(f"\n[ERROR] Bot encountered exception in Farming Mode: \n{traceback.format_exc()}")

        self.print_and_save("\n################################################################################")
        self.print_and_save("################################################################################")
        self.print_and_save("[FARM] Ending Farming Mode.")
        self.print_and_save("################################################################################")
        self.print_and_save("################################################################################\n")

        self._is_bot_running.value = 1
        return None
