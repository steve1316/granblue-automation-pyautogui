import datetime
import multiprocessing
import random
import time
import traceback
from configparser import ConfigParser
from timeit import default_timer as timer
from typing import List

import pyautogui

from bot.combat_mode import CombatMode
from bot.game_modes.arcarum import Arcarum
from bot.game_modes.coop import Coop
from bot.game_modes.dread_barrage import DreadBarrage
from bot.game_modes.event import Event
from bot.game_modes.guild_wars import GuildWars
from bot.game_modes.proving_grounds import ProvingGrounds
from bot.game_modes.quest import Quest
from bot.game_modes.raid import Raid
from bot.game_modes.rotb import RiseOfTheBeasts
from bot.game_modes.special import Special
from bot.game_modes.xeno_clash import XenoClash
from utils.image_utils import ImageUtils
from utils.mouse_utils import MouseUtils
from utils.twitter_room_finder import TwitterRoomFinder


class Game:
    """
    Main driver for bot activity and navigation for the web browser bot, Granblue Fantasy.

    Attributes
    ----------
    queue (multiprocessing.Queue): Queue to keep track of logging messages to share between backend and frontend.

    discord_queue (multiprocessing.Queue): Queue to keep track of status messages to inform the user via Discord DMs.

    is_bot_running (int): Flag in shared memory that signals the frontend that the bot has finished/exited.

    item_name (str): Name of the item to farm.

    item_amount_to_farm (int): Amount of the item to farm.

    farming_mode (str): Mode to look for the specified item and map in.

    map_name (str): Name of the map to look for the specified mission in.

    mission_name (str): Name of the mission to farm the item in.

    summon_element_list (List[str]): List of names of the Summon element image file in the /images/buttons/ folder.

    summon_list (List[str]): List of names of the Summon image's file name in /images/summons/ folder.

    group_number (int): The Group that the specified Party in in.

    party_number (int): The specified Party to start the mission with.

    combat_script (str, optional): The file path to the combat script to use for Combat Mode. Defaults to empty string.

    test_mode (bool, optional): Prevents the bot from automatically calibrating the window dimensions to facilitate easier testing.

    debug_mode (bool, optional): Optional flag to print debug messages related to this class. Defaults to False.

    """

    def __init__(self, queue: multiprocessing.Queue, discord_queue: multiprocessing.Queue, is_bot_running: int, item_name: str, item_amount_to_farm: int, farming_mode: str, map_name: str,
                 mission_name: str, summon_element_list: List[str], summon_list: List[str], group_number: int, party_number: int, combat_script: str = "", test_mode: bool = False,
                 debug_mode: bool = False):
        super().__init__()

        # Keep track of the following for Combat Mode.
        self.combat_script = combat_script

        # Keep track of the following for Farming Mode.
        self.item_name = item_name
        self.item_amount_to_farm = item_amount_to_farm
        self.item_amount_farmed = 0
        self.farming_mode = farming_mode
        self.map_name = map_name
        self.mission_name = mission_name
        self.difficulty = ""
        self.summon_element_list = summon_element_list
        self.summon_list = summon_list
        self.group_number = group_number
        self.party_number = party_number
        self._amount_of_runs_finished = 0
        self._party_selection_first_run = True

        # ################## config.ini ###################
        # Grab the Twitter API keys and tokens from config.ini. The list order is: [consumer key, consumer secret key, access token, access secret token].
        config = ConfigParser()
        config.read("config.ini")

        # #### discord ####
        self.discord_queue = discord_queue
        # #### end of discord ####

        # #### twitter ####
        keys_tokens = [config.get("twitter", "api_key"), config.get("twitter", "api_key_secret"), config.get("twitter", "access_token"), config.get("twitter", "access_token_secret")]
        # #### end of twitter ####

        # #### refill ####
        self._use_full_elixir = config.getboolean("refill", "refill_using_full_elixir")
        self._use_soul_balm = config.getboolean("refill", "refill_using_soul_balms")
        self._enabled_auto_restore = config.getboolean("refill", "enabled_auto_restore")
        # #### end of refill ####

        # #### configuration ####
        custom_mouse_speed = float(config.get("configuration", "mouse_speed"))

        enable_bezier_curve_mouse_movement = config.getboolean("configuration", "enable_bezier_curve_mouse_movement")

        self._enable_delay_between_runs = config.getboolean("configuration", "enable_delay_between_runs")
        self._delay_in_seconds = config.getint("configuration", "delay_in_seconds")
        self._enable_randomized_delay_between_runs = config.getboolean("configuration", "enable_randomized_delay_between_runs")
        self._delay_in_seconds_lower_bound = config.getint("configuration", "delay_in_seconds_lower_bound")
        self._delay_in_seconds_upper_bound = config.getint("configuration", "delay_in_seconds_upper_bound")
        # #### end of configuration ####
        # ################## end of config.ini ###################

        # Start a timer signaling bot start in order to keep track of elapsed time and create a Queue to share logging messages between backend and frontend.
        self._starting_time = timer()
        self._queue = queue

        # Keep track of a bot running status flag shared in memory. Value of 0 means the bot is currently running and a value of 1 means that the bot has stopped.
        self.is_bot_running = is_bot_running

        # Set a debug flag to determine whether or not to print debugging messages.
        self.debug_mode = debug_mode

        # Initialize the objects of helper classes.
        self.combat_mode = CombatMode(self, is_bot_running, debug_mode = self.debug_mode)
        self.room_finder = TwitterRoomFinder(self, keys_tokens[0], keys_tokens[1], keys_tokens[2], keys_tokens[3])
        self.image_tools = ImageUtils(self, debug_mode = self.debug_mode)
        self.mouse_tools = MouseUtils(self, enable_bezier_curve = enable_bezier_curve_mouse_movement, mouse_speed = custom_mouse_speed, debug_mode = self.debug_mode)

        # Save the locations of the "Home" button for use in other classes.
        self.home_button_location = None

        # Construct the object of the specified Farming Mode.
        if self.farming_mode == "Quest":
            self._quest = Quest(self, self.map_name, self.mission_name)
        elif self.farming_mode == "Special":
            self._special = Special(self, self.map_name, self.mission_name)
        elif self.farming_mode == "Coop":
            self._coop = Coop(self, self.mission_name)
        elif self.farming_mode == "Raid":
            self._raid = Raid(self, self.mission_name)
        elif self.farming_mode == "Event" or self.farming_mode == "Event (Token Drawboxes)":
            self._event = Event(self, self.mission_name)
        elif self.farming_mode == "Dread Barrage":
            self._dread_barrage = DreadBarrage(self, self.mission_name)
        elif self.farming_mode == "Rise of the Beasts":
            self._rise_of_the_beasts = RiseOfTheBeasts(self, self.mission_name)
        elif self.farming_mode == "Guild Wars":
            self._guild_wars = GuildWars(self, self.mission_name)
        elif self.farming_mode == "Proving Grounds":
            self._proving_grounds = ProvingGrounds(self, self.mission_name)
        elif self.farming_mode == "Xeno Clash":
            self._xeno_clash = XenoClash(self, self.mission_name)
        elif self.farming_mode == "Arcarum":
            self._arcarum = Arcarum(self, self.mission_name)

        try:
            if test_mode is False:
                # Calibrate the dimensions of the bot window on bot launch.
                self.go_back_home(confirm_location_check = True, display_info_check = True)
            else:
                self.home_button_location = self.image_tools.find_button("home")
                if self.home_button_location is None:
                    raise RuntimeError("Calibration of window dimensions failed. Is the Home button on the bottom bar visible?")
        except Exception as e:
            self.print_and_save(f"\n[ERROR] Bot encountered exception while setting up: \n{traceback.format_exc()}")
            self.discord_queue.put(f"> Bot encountered exception while setting up: \n{e}")
            self.image_tools.generate_alert(f"Bot encountered exception while setting up: \n{e}")
            self.is_bot_running.value = 1

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
        # Save the location of the "Home" button at the bottom of the bot window.
        self.home_button_location = self.image_tools.find_button("home")

        self.print_and_save("\n[INFO] Recalibrating the dimensions of the window...")

        if self.home_button_location is None:
            raise RuntimeError("Calibration of window dimensions failed. Is the Home button on the bottom bar visible?")

        # Set the dimensions of the bot window and save it in ImageUtils so that future operations do not go out of bounds.
        home_news_button = self.image_tools.find_button("home_news")
        home_menu_button = self.image_tools.find_button("home_menu")

        if home_news_button is None:
            raise RuntimeError("Calibration of window dimensions failed. Is the News button visible on the Home screen?")

        if home_menu_button is None:
            raise RuntimeError("Calibration of window dimensions failed. Is the Menu button visible on the Home screen?")

        width, height = pyautogui.size()
        additional_calibration_required = False
        # if self.home_button_location[0] < (width / 2):
        #     window_left = 0
        #     window_top = 0
        #     window_width = int(width / 3)
        #     window_height = height
        # elif self.home_button_location[0] > (width - (width / 2)):
        #     window_left = int(width - width / 3)
        #     window_top = 0
        #     window_width = int(width / 3)
        #     window_height = height
        #     additional_calibration_required = True
        # else:
        #     window_left = 0
        #     window_top = 0
        #     window_width = width
        #     window_height = height

        window_left = 0
        window_top = 0
        window_width = width
        window_height = height

        self.image_tools.update_window_dimensions(window_left, window_top, window_width, window_height, additional_calibration_required)

        self.print_and_save("[SUCCESS] Dimensions of the window has been successfully recalibrated.")

        if display_info_check:
            window_dimensions = self.image_tools.get_window_dimensions()
            self.print_and_save("\n**********************************************************************")
            self.print_and_save("**********************************************************************")
            self.print_and_save(f"[INFO] Screen Size: {pyautogui.size()}")
            self.print_and_save(f"[INFO] Game Window Dimensions: Region({window_dimensions[0]}, {window_dimensions[1]}, {window_dimensions[2]}, {window_dimensions[3]})")
            self.print_and_save("**********************************************************************")
            self.print_and_save("**********************************************************************")

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
            if self.find_and_click_button("home") is False:
                raise RuntimeError("Home button located on the bottom bar is not visible. Is the browser window properly visible?")
        else:
            self.print_and_save("[INFO] Bot is at the Home screen.")

        # Handle any misc popups on the Home screen.
        self.find_and_click_button("close", tries = 2)

        # Recalibrate the dimensions of the bot window.
        if display_info_check:
            self._calibrate_game_window(display_info_check = True)

        if confirm_location_check:
            self.image_tools.confirm_location("home")

        return None

    @staticmethod
    def wait(seconds: float = 3.0):
        """Wait the specified seconds to account for ping or loading.

        Args:
            seconds (float, optional): Number of seconds for the execution to wait for. Defaults to 3.0.

        Returns:
            None
        """
        time.sleep(seconds)
        return None

    def find_and_click_button(self, button_name: str, clicks: int = 1, tries: int = 0, suppress_error: bool = False):
        """Find the center point of a button image and click it.

        Args:
            button_name (str): Name of the button image file in the /images/buttons/ folder.
            clicks (int): Number of mouse clicks when clicking the button image location. Defaults to 1.
            tries (int): Number of tries to attempt to find the specified button image. Defaults to 0 which will use ImageUtil's default.
            suppress_error (bool): Suppresses template matching error depending on boolean. Defaults to False.

        Returns:
            (bool): Return True if the button was found and clicked. Otherwise, return False.
        """
        if self.debug_mode:
            self.print_and_save(f"[DEBUG] Attempting to find and click the button: \"{button_name}\".")

        if tries == 0:
            if button_name.lower() == "quest":
                temp_location = self.image_tools.find_button("quest_blue")
                if temp_location is None:
                    temp_location = self.image_tools.find_button("quest_red")

                if temp_location is not None:
                    self.mouse_tools.move_and_click_point(temp_location[0], temp_location[1], "quest_blue", mouse_clicks = clicks)
                    return True
            elif button_name.lower() == "raid":
                temp_location = self.image_tools.find_button("raid_flat")
                if temp_location is None:
                    temp_location = self.image_tools.find_button("raid_bouncing")

                if temp_location is not None:
                    self.mouse_tools.move_and_click_point(temp_location[0], temp_location[1], "raid_flat", mouse_clicks = clicks)
                    return True
            elif button_name.lower() == "coop_start":
                temp_location = self.image_tools.find_button("coop_start_flat")
                if temp_location is None:
                    temp_location = self.image_tools.find_button("coop_start_faded")

                if temp_location is not None:
                    self.mouse_tools.move_and_click_point(temp_location[0], temp_location[1], "coop_start_flat", mouse_clicks = clicks)
                    return True
            elif button_name.lower() == "event_special_quest":
                temp_location = self.image_tools.find_button("event_special_quest")
                if temp_location is None:
                    temp_location = self.image_tools.find_button("event_special_quest_flat")
                if temp_location is None:
                    temp_location = self.image_tools.find_button("event_special_quest_bouncing")

                if temp_location is not None:
                    self.mouse_tools.move_and_click_point(temp_location[0], temp_location[1], "event_special_quest", mouse_clicks = clicks)
                    return True
            else:
                temp_location = self.image_tools.find_button(button_name.lower())
                if temp_location is not None:
                    self.mouse_tools.move_and_click_point(temp_location[0], temp_location[1], button_name, mouse_clicks = clicks)
                    return True
        else:
            if button_name.lower() == "quest":
                temp_location = self.image_tools.find_button("quest_blue", tries = tries)
                if temp_location is None:
                    temp_location = self.image_tools.find_button("quest_red", tries = tries)

                if temp_location is not None:
                    self.mouse_tools.move_and_click_point(temp_location[0], temp_location[1], "quest_blue", mouse_clicks = clicks)
                    return True
            elif button_name.lower() == "raid":
                temp_location = self.image_tools.find_button("raid_flat", tries = tries)
                if temp_location is None:
                    temp_location = self.image_tools.find_button("raid_bouncing", tries = tries)

                if temp_location is not None:
                    self.mouse_tools.move_and_click_point(temp_location[0], temp_location[1], "raid_flat", mouse_clicks = clicks)
                    return True
            elif button_name.lower() == "coop_start":
                temp_location = self.image_tools.find_button("coop_start_flat", tries = tries)
                if temp_location is None:
                    temp_location = self.image_tools.find_button("coop_start_faded", tries = tries)

                if temp_location is not None:
                    self.mouse_tools.move_and_click_point(temp_location[0], temp_location[1], "coop_start_flat", mouse_clicks = clicks)
                    return True
            elif button_name.lower() == "event_special_quest":
                temp_location = self.image_tools.find_button("event_special_quest", tries = tries)
                if temp_location is None:
                    temp_location = self.image_tools.find_button("event_special_quest_flat", tries = tries)
                if temp_location is None:
                    temp_location = self.image_tools.find_button("event_special_quest_bouncing", tries = tries)

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
            if self.image_tools.confirm_location("captcha"):
                raise RuntimeError("CAPTCHA DETECTED!")
            else:
                self.print_and_save("\n[CAPTCHA] CAPTCHA not detected.")

            return None
        except RuntimeError:
            self.print_and_save(f"\n[ERROR] Bot encountered exception while checking for CAPTCHA: \n{traceback.format_exc()}")
            self.discord_queue.put(f"> Bot encountered exception while checking for CAPTCHA: \n{traceback.format_exc()}")
            self.image_tools.generate_alert_for_captcha()
            self.is_bot_running.value = 1
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

    def select_summon(self, summon_list: List[str], summon_element_list: List[str]):
        """Finds and selects the specified Summon based on the current index on the Summon Selection screen and then checks for CAPTCHA right
        afterwards.

        Args:
            summon_list (List[str]): List of names of the Summon image's file name in /images/summons/ folder.
            summon_element_list (List[str]): List of names of the Summon element image file in the /images/buttons/ folder.

        Returns:
            (bool): True if the Summon was found and clicked. Otherwise, return False.
        """
        self.print_and_save("\n[INFO] Starting process for Support Summon Selection...")

        # Format the Summon name and Summon element name strings.
        for idx, summon in enumerate(summon_list):
            summon_list[idx] = summon.lower().replace(" ", "_")
        for idx, summon_ele in enumerate(summon_element_list):
            summon_element_list[idx] = summon_ele.lower()

        summon_location = self.image_tools.find_summon(summon_list, summon_element_list, self.home_button_location[0], self.home_button_location[1])
        if summon_location is not None:
            self.mouse_tools.move_and_click_point(summon_location[0], summon_location[1], "template_support_summon", mouse_clicks = 2)

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
                if self.image_tools.confirm_location("trial_battles_description", tries = 10):
                    self.find_and_click_button("close", tries = 5)

                    self.find_and_click_button("menu", tries = 5)
                    self.find_and_click_button("retreat", tries = 5)
                    self.find_and_click_button("retreat_confirmation", tries = 5)
                    self.go_back_home()

                if self.image_tools.confirm_location("home"):
                    self.print_and_save("[SUCCESS] Summons have now been refreshed.")

        return None

    def find_party_and_start_mission(self, group_number: int, party_number: int, tries: int = 3):
        """Select the specified Group and Party. It will then start the mission.

        Args:
            group_number (int): The Group that the specified Party in in.
            party_number (int): The specified Party to start the mission with.
            tries (int, optional): Number of tries to select a Set before failing. Defaults to 3.

        Returns:
            (bool): Returns False if it detects the "Raid is full/Raid is already done" dialog. Otherwise, return True.
        """
        # Repeat runs already have the same party already selected.
        if self._party_selection_first_run:
            self.print_and_save(f"\n[INFO] Starting process to select Group {group_number}, Party {party_number}...")

            # Find the Group that the Party is in first. If the specified Group number is less than 8, it is in Set A. Otherwise, it is in Set B. If failed, alternate searching for Set A / Set B until
            # found or tries are depleted.
            set_location = None
            if group_number < 8:
                while set_location is None:
                    set_location = self.image_tools.find_button("party_set_a", tries = 1)
                    if set_location is None:
                        tries -= 1
                        if tries <= 0:
                            raise RuntimeError("Could not find Set A.")

                        # See if the user had Set B active instead of Set A if matching failed.
                        set_location = self.image_tools.find_button("party_set_b", tries = 1)
            else:
                while set_location is None:
                    set_location = self.image_tools.find_button("party_set_b", tries = 1)
                    if set_location is None:
                        tries -= 1
                        if tries <= 0:
                            raise RuntimeError("Could not find Set B.")

                        # See if the user had Set A active instead of Set B if matching failed.
                        set_location = self.image_tools.find_button("party_set_a", tries = 1)

            # Center the mouse on the "Set A" / "Set B" button and then click the correct Group tab.
            if self.debug_mode:
                self.print_and_save(f"[DEBUG] Successfully selected the correct Set. Now selecting Group {group_number}...")

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
            if self.debug_mode:
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

            self._party_selection_first_run = False

            self.print_and_save(f"[INFO] Successfully selected Group {group_number}, Party {party_number}. Now starting the mission.")
        else:
            self.print_and_save("\n[INFO] Reusing the same Party.")

        # Find and click the "OK" button to start the mission.
        self.find_and_click_button("ok")

        # If a popup appears and says "This raid battle has already ended. The Home screen will now appear.", return False.
        if self.farming_mode.lower() == "raid" and self.image_tools.confirm_location("raids"):
            self.print_and_save("\n[WARNING] Raid unfortunately just ended. Backing out now...")
            self.find_and_click_button("ok")
            return False

        return True

    def check_for_ap(self):
        """Check if the user encountered the "Not Enough AP" popup and it will refill using either Half or Full Elixir.

        Returns:
            None
        """
        if self._enabled_auto_restore is False:
            tries = 3

            self.wait(3)

            if self.image_tools.confirm_location("auto_ap_recovered", tries = 1) is False and self.image_tools.confirm_location("auto_ap_recovered2", tries = 1) is False:
                # Loop until the user gets to the Summon Selection screen.
                while (self.farming_mode.lower() != "coop" and not self.image_tools.confirm_location("select_a_summon", tries = 2)) or (
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
                    else:
                        self.wait(1)

                        tries -= 1
                        if tries <= 0:
                            break
            else:
                self.print_and_save("\n[INFO] AP auto recovered due to in-game settings. Closing the popup now...")
                self.find_and_click_button("ok")

            self.print_and_save("\n[INFO] AP is available. Continuing...")
        else:
            self.print_and_save("\n[INFO] AP was auto-restored according to your config.ini. Continuing...")

        return None

    def check_for_ep(self):
        """Check if the user encountered the "Not Enough EP" popup and it will refill using either Soul Berry or Soul Balm.

        Returns:
            None
        """
        if self._enabled_auto_restore is False:
            self.wait(3)

            if self.image_tools.confirm_location("auto_ep_recovered", tries = 1) is False:
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
                self.print_and_save("\n[INFO] EP auto recovered due to in-game settings. Closing the popup now...")
                self.find_and_click_button("ok")

            self.print_and_save("[INFO] EP is available. Continuing...")
        else:
            self.print_and_save("[INFO] EP was auto-restored according to your config.ini. Continuing...")

        return None

    def collect_loot(self, is_completed: bool, is_pending_battle: bool = False, is_event_nightmare: bool = False, skip_info: bool = False, skip_popup_check: bool = False):
        """Collect the loot from the Results screen while clicking away any dialog popups. Primarily for raids.
        
        Args:
            is_completed (bool): Allows incrementing of number of runs completed. This is for Farming Modes who have multi-part sections to them to prevent unnecessary incrementing of runs when it wasn't finished with 1 yet.
            is_pending_battle (bool): Skip the incrementation of runs attempted if this was a Pending Battle. Defaults to False.
            is_event_nightmare (bool): Skip the incrementation of runs attempted if this was a Event Nightmare. Defaults to False.
            skip_info (bool): Skip printing the information of the run. Defaults to False.
            skip_popup_check (bool): Skip checking for popups to get to the Loot Collected screen. Defaults to False.

        Returns:
            (int): Number of specified items dropped.
        """
        temp_amount = 0

        # Close all popups until the bot reaches the Loot Collected screen.
        if skip_popup_check is False:
            while not self.image_tools.confirm_location("loot_collected", tries = 1):
                self.find_and_click_button("ok", tries = 1, suppress_error = True)
                self.find_and_click_button("close", tries = 1, suppress_error = True)
                self.find_and_click_button("cancel", tries = 1, suppress_error = True)

                # Search for and click on the "Extended Mastery" popup.
                self.find_and_click_button("new_extended_mastery_level", tries = 1, suppress_error = True)

        # Now that the bot is at the Loot Collected screen, detect any user-specified items.
        if is_completed and not is_pending_battle and not is_event_nightmare:
            self.print_and_save("\n[INFO] Detecting if any user-specified loot dropped from this run...")
            if self.item_name != "EXP" and self.item_name != "Angel Halo Weapons" and self.item_name != "Repeated Runs":
                temp_amount = self.image_tools.find_farmed_items(self.item_name)
            else:
                temp_amount = 1

            self._amount_of_runs_finished += 1
        elif is_pending_battle:
            self.print_and_save("\n[INFO] Detecting if any user-specified loot dropped from this pending battle...")
            if self.item_name != "EXP" and self.item_name != "Angel Halo Weapons" and self.item_name != "Repeated Runs":
                temp_amount = self.image_tools.find_farmed_items(self.item_name)
            else:
                temp_amount = 0

            self.item_amount_farmed += temp_amount

        if is_completed and not is_pending_battle and not is_event_nightmare and not skip_info:
            if self.item_name != "EXP" and self.item_name != "Angel Halo Weapons" and self.item_name != "Repeated Runs":
                self.print_and_save("\n**********************************************************************")
                self.print_and_save("**********************************************************************")
                self.print_and_save(f"[FARM] Farming Mode: {self.farming_mode}")
                self.print_and_save(f"[FARM] Mission: {self.mission_name}")
                self.print_and_save(f"[FARM] Summons: {self.summon_list}")
                self.print_and_save(f"[FARM] Amount of {self.item_name} gained from this run: {temp_amount}")
                self.print_and_save(f"[FARM] Amount of {self.item_name} gained in total: {self.item_amount_farmed + temp_amount} / {self.item_amount_to_farm}")
                self.print_and_save(f"[FARM] Amount of runs completed: {self._amount_of_runs_finished}")
                self.print_and_save("**********************************************************************")
                self.print_and_save("**********************************************************************\n")

                if temp_amount != 0:
                    if self.item_amount_farmed >= self.item_amount_to_farm:
                        discord_string = f"> {temp_amount}x __{self.item_name}__ gained from this run: **[{self.item_amount_farmed} / {self.item_amount_to_farm}]** -> " \
                                         f"**[{self.item_amount_farmed + temp_amount} / {self.item_amount_to_farm}]** :white_check_mark:"
                    else:
                        discord_string = f"> {temp_amount}x __{self.item_name}__ gained from this run: **[{self.item_amount_farmed} / {self.item_amount_to_farm}]** -> " \
                                         f"**[{self.item_amount_farmed + temp_amount} / {self.item_amount_to_farm}]**"

                    self.discord_queue.put(discord_string)
            else:
                self.print_and_save("\n**********************************************************************")
                self.print_and_save("**********************************************************************")
                self.print_and_save(f"[FARM] Farming Mode: {self.farming_mode}")
                self.print_and_save(f"[FARM] Mission: {self.mission_name}")
                self.print_and_save(f"[FARM] Summons: {self.summon_list}")
                self.print_and_save(f"[FARM] Amount of runs completed: {self._amount_of_runs_finished} / {self.item_amount_to_farm}")
                self.print_and_save("**********************************************************************")
                self.print_and_save("**********************************************************************\n")

                if self._amount_of_runs_finished >= self.item_amount_to_farm:
                    discord_string = f"> Runs completed for __{self.mission_name}__: **[{self._amount_of_runs_finished - 1} / {self.item_amount_to_farm}]** -> " \
                                     f"**[{self._amount_of_runs_finished} / {self.item_amount_to_farm}]** :white_check_mark:"
                else:
                    discord_string = f"> Runs completed for __{self.mission_name}__: **[{self._amount_of_runs_finished - 1} / {self.item_amount_to_farm}]** -> " \
                                     f"**[{self._amount_of_runs_finished} / {self.item_amount_to_farm}]**"

                self.discord_queue.put(discord_string)
        elif is_pending_battle and temp_amount > 0 and not skip_info:
            if self.item_name != "EXP" and self.item_name != "Angel Halo Weapons" and self.item_name != "Repeated Runs":
                self.print_and_save("\n**********************************************************************")
                self.print_and_save("**********************************************************************")
                self.print_and_save(f"[FARM] Farming Mode: {self.farming_mode}")
                self.print_and_save(f"[FARM] Mission: {self.mission_name}")
                self.print_and_save(f"[FARM] Summons: {self.summon_list}")
                self.print_and_save(f"[FARM] Amount of {self.item_name} gained from this pending battle: {temp_amount}")
                self.print_and_save(f"[FARM] Amount of {self.item_name} gained in total: {self.item_amount_farmed} / {self.item_amount_to_farm}")
                self.print_and_save(f"[FARM] Amount of runs completed: {self._amount_of_runs_finished}")
                self.print_and_save("**********************************************************************")
                self.print_and_save("**********************************************************************\n")

                if temp_amount != 0:
                    if self.item_amount_farmed >= self.item_amount_to_farm:
                        discord_string = f"> {temp_amount}x __{self.item_name}__ gained from this pending battle: **[{self.item_amount_farmed} / {self.item_amount_to_farm}]** -> " \
                                         f"**[{self.item_amount_farmed + temp_amount} / {self.item_amount_to_farm}]** :white_check_mark:"
                    else:
                        discord_string = f"> {temp_amount}x __{self.item_name}__ gained from this pending battle: **[{self.item_amount_farmed} / {self.item_amount_to_farm}]** -> " \
                                         f"**[{self.item_amount_farmed + temp_amount} / {self.item_amount_to_farm}]**"

                    self.discord_queue.put(discord_string)

        return temp_amount

    def check_for_popups(self) -> bool:
        """Detect any popups and attempt to close them all with the final destination being the Summon Selection screen.

        Returns:
            (bool): True if there was a Nightmare mission detected or some other popup appeared that requires the navigation process to be restarted.
        """
        self.print_and_save(f"\n[INFO] Now beginning process to check for popups...")

        while self.image_tools.confirm_location("select_a_summon", tries = 1) is False:
            # Break out of the loop if the bot detected that a AP recovery item was automatically used and let check_for_ap() take care of it.
            if self.image_tools.confirm_location("auto_ap_recovered", tries = 1) or self.image_tools.confirm_location("auto_ap_recovered2", tries = 1):
                break

            # Break out of the loop if the bot detected the "Not Enough AP" popup.
            if self.image_tools.confirm_location("not_enough_ap", tries = 1):
                break

            if self.farming_mode == "Rise of the Beasts" and self.image_tools.confirm_location("proud_solo_quest", tries = 1):
                # Scroll down the screen a little bit because the popup itself is too long for screen sizes around 1080p.
                self.mouse_tools.scroll_screen_from_home_button(-400)

            # Check for certain popups for certain Farming Modes.
            if (self.farming_mode == "Rise of the Beasts" and self._rise_of_the_beasts.check_for_rotb_extreme_plus()) or (
                    self.farming_mode == "Special" and self.mission_name == "VH Angel Halo" and self.item_name == "Angel Halo Weapons" and self._special.check_for_dimensional_halo()) or (
                    (self.farming_mode == "Event" or self.farming_mode == "Event (Token Drawboxes)") and self._event.check_for_event_nightmare()) or (
                    self.farming_mode == "Xeno Clash" and self._xeno_clash.check_for_xeno_clash_nightmare()):
                return True

            # If the bot tried to repeat a Extreme/Impossible difficulty Event Raid and it lacked the treasures to host it, go back to select the Mission again.
            if (self.farming_mode == "Event (Token Drawboxes)" or self.farming_mode == "Guild Wars") and self.image_tools.confirm_location("not_enough_treasure", tries = 1):
                self.find_and_click_button("ok")
                return True

            # Attempt to close the popup by clicking on any detected "Close" and "Cancel" buttons.
            if self.find_and_click_button("close", tries = 1) is False:
                self.find_and_click_button("cancel", tries = 1)

            self.wait(1)

        return False

    def _clear_pending_battle(self):
        """Process a Pending Battle.

        Returns:
            (bool): Return True if a Pending Battle was successfully processed. Otherwise, return False.
        """
        if self.find_and_click_button("tap_here_to_see_rewards", tries = 1):
            self.print_and_save(f"[INFO] Clearing this Pending Battle...")

            self.wait(1)

            # If there is loot available, start loot detection.
            if self.image_tools.confirm_location("no_loot", tries = 1):
                self.print_and_save(f"[INFO] No loot can be collected.")

                # Navigate back to the Quests screen.
                self.find_and_click_button("quests")

                return True
            else:
                if self.farming_mode == "Raid":
                    self.collect_loot(is_completed = True)
                else:
                    self.collect_loot(is_completed = False, is_pending_battle = True)

                self.find_and_click_button("close", tries = 1)
                self.find_and_click_button("ok", tries = 1)

                return True

        return False

    def check_for_pending(self):
        """Check and collect any pending rewards and free up slots for the bot to join more raids.

        Returns:
            (bool): Return True if Pending Battles were detected. Otherwise, return False.
        """
        self.print_and_save(f"\n[INFO] Starting process of checking for Pending Battles...")

        self.wait(1)

        if (self.image_tools.confirm_location("check_your_pending_battles", tries = 1)) or \
                (self.image_tools.confirm_location("pending_battles", tries = 1)) or \
                (self.find_and_click_button("quest_results_pending_battles", tries = 1)):
            self.print_and_save(f"[INFO] Found Pending Battles that need collecting from.")

            self.find_and_click_button("ok", tries = 1)

            self.wait(1)

            if self.image_tools.confirm_location("pending_battles", tries = 1):
                # Process the current Pending Battle.
                while self._clear_pending_battle():
                    # While on the Loot Collected screen, if there are more Pending Battles then head back to the Pending Battles screen.
                    if self.image_tools.find_button("quest_results_pending_battles", tries = 1):
                        self.find_and_click_button("quest_results_pending_battles")

                        self.wait(1)

                        # Close the Skyscope mission popup.
                        if self.image_tools.confirm_location("skyscope"):
                            self.find_and_click_button("close")
                            self.wait(1)

                        if self.image_tools.confirm_location("friend_request", tries = 1):
                            self.find_and_click_button("cancel")

                        self.wait(1)
                    else:
                        # When there are no more Pending Battles, go back to the Home screen.
                        self.find_and_click_button("home")

                        # Close the Skyscope mission popup.
                        if self.image_tools.confirm_location("skyscope"):
                            self.find_and_click_button("close")
                            self.wait(1)

                        break

            self.print_and_save(f"[INFO] Pending battles have been cleared.")
            return True

        self.print_and_save(f"[INFO] No Pending Battles needed to be cleared.")
        return False

    def start_farming_mode(self):
        """Start the Farming Mode using the given parameters.

        Returns:
            (bool): True if Farming Mode ended successfully.
        """
        try:
            if self.item_name != "EXP":
                self.print_and_save("\n######################################################################")
                self.print_and_save("######################################################################")
                self.print_and_save(f"[FARM] Starting Farming Mode for {self.farming_mode}.")
                self.print_and_save(f"[FARM] Farming {self.item_amount_to_farm}x {self.item_name} at {self.mission_name}.")
                self.print_and_save("######################################################################")
                self.print_and_save("######################################################################\n")
            else:
                self.print_and_save("\n######################################################################")
                self.print_and_save("######################################################################")
                self.print_and_save(f"[FARM] Starting Farming Mode for {self.farming_mode}.")
                self.print_and_save(f"[FARM] Doing {self.item_amount_to_farm}x runs for {self.item_name} at {self.mission_name}.")
                self.print_and_save("######################################################################")
                self.print_and_save("######################################################################\n")

            first_run = True
            while self.item_amount_farmed < self.item_amount_to_farm:
                if self.farming_mode == "Quest":
                    self.item_amount_farmed += self._quest.start(first_run)
                elif self.farming_mode == "Special":
                    self.item_amount_farmed += self._special.start(first_run)
                elif self.farming_mode == "Coop":
                    self.item_amount_farmed += self._coop.start(first_run)
                elif self.farming_mode == "Raid":
                    self.item_amount_farmed += self._raid.start(first_run)
                elif self.farming_mode == "Event" or self.farming_mode == "Event (Token Drawboxes)":
                    self.item_amount_farmed += self._event.start(first_run)
                elif self.farming_mode == "Rise of the Beasts":
                    self.item_amount_farmed += self._rise_of_the_beasts.start(first_run)
                elif self.farming_mode == "Guild Wars":
                    self.item_amount_farmed += self._guild_wars.start(first_run)
                elif self.farming_mode == "Dread Barrage":
                    self.item_amount_farmed += self._dread_barrage.start(first_run)
                elif self.farming_mode == "Proving Grounds":
                    self.item_amount_farmed += self._proving_grounds.start(first_run)
                elif self.farming_mode == "Xeno Clash":
                    self.item_amount_farmed += self._xeno_clash.start(first_run)
                elif self.farming_mode == "Arcarum":
                    self.item_amount_farmed += self._arcarum.start()

                if self.item_amount_farmed < self.item_amount_to_farm:
                    # Generate a resting period if the user enabled it.
                    self._delay_between_runs()
                    first_run = False

        except Exception as e:
            self.print_and_save(f"\n[ERROR] Bot encountered exception in Farming Mode: \n{traceback.format_exc()}")
            self.discord_queue.put(f"> Bot encountered exception in Farming Mode: \n{e}")

            self.print_and_save("\n######################################################################")
            self.print_and_save("######################################################################")
            self.print_and_save("[FARM] Ending Farming Mode.")
            self.print_and_save("######################################################################")
            self.print_and_save("######################################################################\n")

            if self.farming_mode == "Raid":
                self.room_finder.disconnect()

            self.image_tools.generate_alert(f"Bot encountered exception in Farming Mode: \n{e}")
            self.is_bot_running.value = 1
            return False

        self.print_and_save("\n######################################################################")
        self.print_and_save("######################################################################")
        self.print_and_save("[FARM] Ending Farming Mode.")
        self.print_and_save("######################################################################")
        self.print_and_save("######################################################################\n")

        if self.farming_mode == "Raid":
            self.room_finder.disconnect()

        self.is_bot_running.value = 1
        return True
