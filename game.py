import datetime
import multiprocessing
import os
import sys
import time
import traceback
from configparser import ConfigParser
from timeit import default_timer as timer
from typing import Iterable

import pyautogui

from image_utils import ImageUtils
from map_selection import MapSelection
from mouse_utils import MouseUtils
from twitter_room_finder import TwitterRoomFinder


class Game:
    """
    Main driver for bot activity and navigation for the web browser game, Granblue Fantasy.

    Attributes
    ----------
    queue (multiprocessing.Queue): Queue to keep track of logging messages to share between backend and frontend.

    isBotRunning (int): Flag in shared memory that signals the frontend that the bot has finished/exited.
    
    combat_script (str, optional): The file path to the combat script to use for Combat Mode. Defaults to empty string.

    debug_mode (bool, optional): Optional flag to print debug messages related to this class. Defaults to False.

    """
    def __init__(self, queue: multiprocessing.Queue, isBotRunning: int, combat_script: str = "", debug_mode: bool = False):
        super().__init__()
        
        # Save a reference to the original current working directory.
        self._owd = os.getcwd()
        
        ########## config.ini ##########
        # Grab the Twitter API keys and tokens from config.ini. The list order is: [consumer key, consumer secret key, access token, access secret token].
        config = ConfigParser()
        config.read("config.ini")
        keys_tokens = [config.get("twitter", "api_key"), config.get("twitter", "api_key_secret"), config.get("twitter", "access_token"), config.get("twitter", "access_token_secret")]
        custom_mouse_speed = float(config.get("configuration", "mouse_speed"))
        
        # Grab the timings between various actions during Combat Mode from config.ini as well.
        self._idle_seconds_after_skill = float(config.get("configuration", "idle_seconds_after_skill"))
        self._idle_seconds_after_summon = float(config.get("configuration", "idle_seconds_after_summon"))
        
        # Determine whether or not the user wants to refill using Full Elixir/Soul Balm.
        self.use_full_elixir = config.getboolean("refill", "refill_using_full_elixir")
        self.use_soul_balm = config.getboolean("refill", "refill_using_soul_balms")
        
        # Keep track of the following for Events.
        self._enable_event_nightmare = config.getboolean("event", "enable_event_nightmare")
        self._event_nightmare_combat_script = config.get("event", "event_nightmare_combat_script")
        
        self._event_nightmare_summon_list = config.get("event", "event_nightmare_summon_list")
        self._event_nightmare_summon_list = self._event_nightmare_summon_list.replace(" ","_").split(",")
        if(len(self._event_nightmare_summon_list) == 1 and self._event_nightmare_summon_list[0] == ""):
            self._event_nightmare_summon_list.clear()
            
        self._event_nightmare_summon_element_list = config.get("event", "event_nightmare_summon_element_list")
        self._event_nightmare_summon_element_list = self._event_nightmare_summon_element_list.replace(" ","_").split(",")
        if(len(self._event_nightmare_summon_element_list) == 1 and self._event_nightmare_summon_element_list[0] == ""):
            self._event_nightmare_summon_element_list.clear()
            
        self._event_nightmare_group_number = config.get("event", "event_nightmare_group_number")
        self._event_nightmare_party_number = config.get("event", "event_nightmare_party_number")
        
        # Keep track of the following for Dimensional Halo.
        self._enable_dimensional_halo = config.getboolean("dimensional_halo", "enable_dimensional_halo")
        self._dimensional_halo_combat_script = config.get("dimensional_halo", "dimensional_halo_combat_script")
        
        self._dimensional_halo_summon_list = config.get("dimensional_halo", "dimensional_halo_summon_list")
        self._dimensional_halo_summon_list = self._dimensional_halo_summon_list.replace(" ","_").split(",")
        if(len(self._dimensional_halo_summon_list) == 1 and self._dimensional_halo_summon_list[0] == ""):
            self._dimensional_halo_summon_list.clear()
            
        self._dimensional_halo_summon_element_list = config.get("dimensional_halo", "dimensional_halo_summon_element_list")
        self._dimensional_halo_summon_element_list = self._dimensional_halo_summon_element_list.replace(" ","_").split(",")
        if(len(self._dimensional_halo_summon_element_list) == 1 and self._dimensional_halo_summon_element_list[0] == ""):
            self._dimensional_halo_summon_element_list.clear()
            
        self._dimensional_halo_group_number = config.get("dimensional_halo", "dimensional_halo_group_number")
        self._dimensional_halo_party_number = config.get("dimensional_halo", "dimensional_halo_party_number")
        self._dimensional_halo_amount = 0
        
        # Keep track of the following for Rise of the Beasts.
        self._enable_rotb_extreme_plus = config.getboolean("rise_of_the_beasts", "enable_rotb_extreme_plus")
        self._rotb_extreme_plus_combat_script = config.get("rise_of_the_beasts", "rotb_extreme_plus_combat_script")
        self._rotb_extreme_plus_summon_list = config.get("rise_of_the_beasts", "rotb_extreme_plus_summon_list")
        self._rotb_extreme_plus_summon_element_list = config.get("rise_of_the_beasts", "rotb_extreme_plus_summon_element_list")
        self._rotb_extreme_plus_group_number = config.get("rise_of_the_beasts", "rotb_extreme_plus_group_number")
        self._rotb_extreme_plus_party_number = config.get("rise_of_the_beasts", "rotb_extreme_plus_party_number")
        self._rotb_extreme_plus_amount = 0
        
        # Keep track of the following for Dread Barrage Unparalleled Foes.
        self._enable_unparalleled_foe = config.getboolean("dread_barrage", "enable_unparalleled_foe")
        self._enable_unparalleled_foe_level_95 = config.getboolean("dread_barrage", "enable_unparalleled_foe_level_95")
        self._enable_unparalleled_foe_level_175 = config.getboolean("dread_barrage", "enable_unparalleled_foe_level_175")
        self.unparalleled_foe_combat_script = config.get("dread_barrage", "unparalleled_foe_combat_script")
        
        self._unparalleled_foe_summon_list = config.get("dread_barrage", "unparalleled_foe_summon_list")
        self._unparalleled_foe_summon_list = self._unparalleled_foe_summon_list.replace(" ","_").split(",")
        if(len(self._unparalleled_foe_summon_list) == 1 and self._unparalleled_foe_summon_list[0] == ""):
            self._unparalleled_foe_summon_list.clear()
            
        self._unparalleled_foe_summon_element_list = config.get("dread_barrage", "unparalleled_foe_summon_element_list")
        self._unparalleled_foe_summon_element_list = self._unparalleled_foe_summon_element_list.replace(" ","_").split(",")
        if(len(self._unparalleled_foe_summon_element_list) == 1 and self._unparalleled_foe_summon_element_list[0] == ""):
            self._unparalleled_foe_summon_element_list.clear()
            
        self._unparalleled_foe_group_number = config.get("dread_barrage", "unparalleled_foe_group_number")
        self._unparalleled_foe_party_number = config.get("dread_barrage", "unparalleled_foe_party_number")
        ########## config.ini ##########
        
        # Start a timer signaling bot start in order to keep track of elapsed time and create a Queue to share logging messages between backend and frontend.
        self._starting_time = timer()
        self._queue = queue
        
        # Keep track of a bot running status flag shared in memory. Value of 0 means the bot is currently running and a value of 1 means that the bot has stopped.
        self._isBotRunning = isBotRunning
        
        # Set a debug flag to determine whether or not to print debugging messages.
        self._debug_mode = debug_mode
        
        # Initialize the objects of helper classes.
        self._map_selection = MapSelection(self, isBotRunning)
        self.room_finder = TwitterRoomFinder(self, keys_tokens[0], keys_tokens[1], keys_tokens[2], keys_tokens[3], debug_mode=self._debug_mode)
        self.image_tools = ImageUtils(game=self, debug_mode=self._debug_mode)
        self.mouse_tools = MouseUtils(game=self, mouse_speed=custom_mouse_speed, debug_mode=self._debug_mode)
        
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
        
        # The amount of time to pause after each call to PyAutoGUI. This applies to calls inside mouse_utils and image_utils.
        pyautogui.PAUSE = 0.25
        
        # Calibrate the dimensions of the game window on bot launch.
        self.go_back_home(confirm_location_check=True, display_info_check=True)

    def printtime(self):
        """Formats the time since the bot started into a readable, printable HH:MM:SS format using timedelta.

        Returns:
            str: A formatted string that displays the elapsed time since the bot started.
        """
        return str(datetime.timedelta(seconds=(timer() - self._starting_time))).split('.')[0]
    
    def print_and_save(self, message: str):
        """Saves the logging message into the Queue to be shared with the frontend and then prints it to console.

        Args:
            message (str): A logging message containing various information.
        
        Returns:
            None
        """
        self._queue.put(message)
        print(message)
        return None

    def _calibrate_game_window(self, display_info_check: bool = False):
        """Recalibrate the dimensions of the game window for fast and accurate image matching.

        Args:
            display_info_check (bool, optional): Displays the screen size and the dimensions of the game window. Defaults to False.

        Returns:
            None
        """
        if(self._debug_mode):
            self.print_and_save(f"\n{self.printtime()} [DEBUG] Recalibrating the dimensions of the game window...")
            
        try:
            # Save the location of the "Home" button at the bottom of the game window.
            self.home_button_location = self.image_tools.find_button("home")
            
            # Set the dimensions of the game window and save it in ImageUtils so that future operations do not go out of bounds.
            home_news_button = self.image_tools.find_button("home_news")
            home_menu_button = self.image_tools.find_button("home_menu")
            
            # Use the locations of the "News" and "Menu" buttons on the Home screen to calculate the dimensions of the game window in the following format:
            # window_left: The x-coordinate of the left edge.
            # window_top: The y-coordinate of the top edge.
            # window_width: The width of the region.
            # window_height: The height of the region.
            window_left = home_news_button[0] - 35
            window_top = home_menu_button[1] - 24
            window_width = window_left + 410
            window_height = (self.home_button_location[1] + 24) - window_top
            
            self.image_tools.update_window_dimensions(window_left, window_top, window_width, window_height)
        except Exception:
            self.print_and_save(f"\n{self.printtime()} [ERROR] Bot encountered exception while calibrating game window dimensions: \n{traceback.format_exc()}")
            self._isBotRunning.value = 1
            
        if(self._debug_mode):
            self.print_and_save(f"{self.printtime()} [SUCCESS] Dimensions of the game window has been successfully recalibrated.")
            
        if(display_info_check):
            window_dimensions = self.image_tools.get_window_dimensions()
            self.print_and_save("\n********************************************************************************")
            self.print_and_save("********************************************************************************")
            self.print_and_save(f"{self.printtime()} [INFO] Screen Size: {pyautogui.size()}")
            self.print_and_save(f"{self.printtime()} [INFO] Game Window Dimensions: Region({window_dimensions[0]}, {window_dimensions[1]}, {window_dimensions[2]}, {window_dimensions[3]})")
            self.print_and_save("********************************************************************************")
            self.print_and_save("********************************************************************************")
            
        return None

    def go_back_home(self, confirm_location_check: bool = False, display_info_check: bool = False):
        """Go back to the Home screen to reset the bot's position. Also able to recalibrate the region dimensions of the game window if display_info_check is True.

        Args:
            confirm_location_check (bool, optional): Check to see if the current location is confirmed to be at the Home screen. Defaults to False.
            display_info_check (bool, optional): Recalibrate the game window dimensions and displays the info. Defaults to False.

        Returns:
            None
        """   
        if(not self.image_tools.confirm_location("home")):
            self.print_and_save(f"\n{self.printtime()} [INFO] Moving back to the Home screen...")
            if(self.home_button_location != None):
                self.mouse_tools.move_and_click_point(self.home_button_location[0], self.home_button_location[1])
            else:
                self.find_and_click_button("home")
        else:
            self.print_and_save(f"{self.printtime()} [INFO] Bot is at the Home screen.")
        
        # Recalibrate the dimensions of the game window.
        if(display_info_check):
            self._calibrate_game_window(display_info_check=True)
            
        if(confirm_location_check):
            self.image_tools.confirm_location("home")
            
        return None

    def wait(self, seconds: int = 3):
        """Wait the specified seconds to account for ping or loading.

        Args:
            seconds (int, optional): Number of seconds for the execution to wait for. Defaults to 3.

        Returns:
            None
        """
        time.sleep(seconds)
        return None
    
    def find_and_click_button(self, button_name: str, tries: int = 2, suppress_error: bool = False):
        """Find the center point of a button image and click it.

        Args:
            button_name (str): Name of the button image file in the /images/buttons/ folder.
            tries (int): Number of tries to attempt to find the specified button image. Defaults to 2.
            suppress_error (bool): Suppresses template matching error depending on boolean. Defaults to False.

        Returns:
            (bool): Return True if the button was found and clicked. Otherwise, return False.
        """
        if(self._debug_mode):
            self.print_and_save(f"{self.printtime()} [DEBUG] Attempting to find and click the button: \"{button_name}\".")
        
        if(button_name.lower() == "quest"):
            temp_location = self.image_tools.find_button("quest_blue", tries=tries, suppress_error=suppress_error)
            if(temp_location == None):
                temp_location = self.image_tools.find_button("quest_red", tries=tries, suppress_error=suppress_error)
            if(temp_location == None):
                temp_location = self.image_tools.find_button("quest_blue_strike_time", tries=tries, suppress_error=suppress_error)
            if(temp_location == None):
                temp_location = self.image_tools.find_button("quest_red_strike_time", tries=tries, suppress_error=suppress_error) 
        elif(button_name.lower() == "raid"):
            temp_location = self.image_tools.find_button("raid_flat", tries=tries, suppress_error=suppress_error)
            if(temp_location == None):
                temp_location = self.image_tools.find_button("raid_bouncing", tries=tries, suppress_error=suppress_error)
        elif(button_name.lower() == "coop_start"):
            temp_location = self.image_tools.find_button("coop_start_flat", tries=tries, suppress_error=suppress_error)
            if(temp_location == None):
                temp_location = self.image_tools.find_button("coop_start_faded", tries=tries, suppress_error=suppress_error)
        elif(button_name.lower() == "event_special_quest"):
            temp_location = self.image_tools.find_button("event_special_quest", tries=tries, suppress_error=suppress_error)
            if(temp_location == None):
                temp_location = self.image_tools.find_button("event_special_quest_flat", tries=tries, suppress_error=suppress_error)
            if(temp_location == None):
                temp_location = self.image_tools.find_button("event_special_quest_bouncing", tries=tries, suppress_error=suppress_error)   
        else:
            temp_location = self.image_tools.find_button(button_name.lower(), tries=tries, suppress_error=suppress_error)
        
        if(temp_location != None):
            self.mouse_tools.move_and_click_point(temp_location[0], temp_location[1])
            return True
        else:
            return False
        
    def _party_wipe_check(self):
        """Check to see if the Party has wiped during Combat Mode. Update the retreat check flag if so.

        Returns:
            None
        """
        try:
            # Check to see if Party has wiped.
            if(self._debug_mode):
                self.print_and_save(f"\n{self.printtime()} [DEBUG] Checking to see if the Party wiped...")
                
            party_wipe_indicator = self.image_tools.find_button("party_wipe_indicator", tries=1, suppress_error=True)
            if(party_wipe_indicator != None):
                # Click on the blue indicator to get rid of the overlay.
                self.wait(2)
                self.mouse_tools.move_and_click_point(party_wipe_indicator[0], party_wipe_indicator[1])
                
                if((self.farming_mode.lower() != "raid" and self.farming_mode.lower() != "dread barrage") and self.image_tools.confirm_location("continue")):
                    # Cancel the popup that asks you if you want to use a Full Elixir to come back. Then click the red "Retreat" button.
                    self.print_and_save(f"{self.printtime()} [COMBAT] Party has unfortunately wiped during Combat Mode. Retreating now...")
                    self.find_and_click_button("cancel")
                    self.find_and_click_button("retreat_confirmation")
                    self._retreat_check = True
                elif((self.farming_mode.lower() == "raid" or self.farming_mode.lower() == "dread barrage") and self.image_tools.confirm_location("salute_participants")):
                    # Salute the participants.
                    self.print_and_save(f"{self.printtime()} [COMBAT] Party has unfortunately wiped during Combat Mode. Backing out now without retreating...")
                    self.find_and_click_button("salute")
                    self.find_and_click_button("ok")
                    
                    # Then cancel the popup that asks you if you want to use a Full Elixir to come back.
                    self.find_and_click_button("cancel")
                    
                    # Then click the "Home" button.
                    self.find_and_click_button("raid_retreat_home")
                    
                    self._retreat_check = True
                elif(self.farming_mode.lower() == "coop" and self.image_tools.confirm_location("salute_participants")):
                    # Salute the participants.
                    self.print_and_save(f"{self.printtime()} [COMBAT] Party has unfortunately wiped during Combat Mode. Leaving the Coop room...")
                    self.find_and_click_button("salute")
                    self.find_and_click_button("ok")
                    
                    # Then cancel the popup that asks you if you want to use a Full Elixir to come back.
                    self.find_and_click_button("cancel")
                    
                    # Then click the "Leave" button.
                    self.find_and_click_button("leave")
                    
                    self._retreat_check = True
            else:
                if(self._debug_mode):
                    self.print_and_save(f"{self.printtime()} [DEBUG] Party has not wiped.")
                    
            return None
        except Exception:
            self.print_and_save(f"\n{self.printtime()} [ERROR] Bot encountered exception while checking if Party wiped during Combat Mode: \n{traceback.format_exc()}")
            self._isBotRunning.value = 1
            
    def check_for_captcha(self):
        """Checks for CAPTCHA right after selecting a Summon and if detected, alert the user and then stop the bot.

        Returns:
            None
        """
        try:
            self.wait(2)
            if(self.image_tools.confirm_location("captcha", tries=1)):
                raise Exception(f"CAPTCHA DETECTED!")
            else:
                self.print_and_save(f"\n{self.printtime()} [CAPTCHA] CAPTCHA not detected. Moving on to Party Selection...")
            
            return None
        except Exception:
            self.print_and_save(f"\n{self.printtime()} [ERROR] Bot encountered exception while checking for CAPTCHA: \n{traceback.format_exc()}")
            self.image_tools.generate_alert_for_captcha()
            self._isBotRunning.value = 1
            self.wait(1)

    def _select_summon(self, summon_list: Iterable[str], summon_element_list: Iterable[str]):
        """Finds and selects the specified Summon based on the current index on the Summon Selection screen and then checks for CAPTCHA right afterwards. 

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
        if (summon_location != None):
            self.mouse_tools.move_and_click_point(summon_location[0], summon_location[1])
            
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
        self.print_and_save(f"\n{self.printtime()} [INFO] Now refreshing Summons...")
        self.go_back_home(confirm_location_check=True)
        self.mouse_tools.scroll_screen_from_home_button(-600)

        try:
            list_of_steps_in_order = ["gameplay_extras", "trial_battles", "trial_battles_old_lignoid", "play_round_button", "choose_a_summon",
                                      "party_selection_ok", "close", "menu", "retreat", "retreat_confirmation", "next"]
            
            # Go through each step in order from left to right from the list of steps.
            while (len(list_of_steps_in_order) > 0):
                step = list_of_steps_in_order.pop(0)
                if(step == "trial_battles_old_lignoid"):
                    self.image_tools.confirm_location("trial_battles")
                elif(step == "close"):
                    self.wait(2)
                    self.image_tools.confirm_location("trial_battles_description")
                
                # Find the location of the specified button.
                image_location = self.image_tools.find_button(step)
                
                # If the bot cannot find the "Trial Battles" button under the "Gameplay Extras" section, keep scrolling down until it does.
                while(step == "trial_battles" and image_location == None):
                    self.mouse_tools.scroll_screen_from_home_button(-300)
                    image_location = self.image_tools.find_button(step)
                    
                if(step == "choose_a_summon"):
                    self.mouse_tools.move_and_click_point(image_location[0], image_location[1] + 187)
                else:
                    self.mouse_tools.move_and_click_point(image_location[0], image_location[1])
            
            if(self.image_tools.confirm_location("trial_battles")):
                self.print_and_save(f"{self.printtime()} [SUCCESS] Summons have now been refreshed.")
            
            return None
        except Exception:
            self.print_and_save(f"\n{self.printtime()} [ERROR] Bot encountered exception while resetting Summons: \n{traceback.format_exc()}")
            self._isBotRunning.value = 1

    def _find_party_and_start_mission(self, group_number: int, party_number: int, tries: int = 3):
        """Select the specified Group and Party. It will then start the mission.

        Args:
            group_number (int): The Group that the specified Party in in.
            party_number (int): The specified Party to start the mission with.
            tries (int, optional): Number of tries to select a Set before failing. Defaults to 3.

        Returns:
            (bool): Returns False if it detects the "Raid is full/Raid is already done" dialog. Otherwise, return True.
        """
        # Find the Group that the Party is in first. If the specified Group number is less than 8, it is in Set A. Otherwise, it is in Set B. If failed,
        # alternate searching for Set A / Set B until found or tries are depleted.
        set_location = None
        try:
            if(group_number < 8):
                while (set_location == None):
                    set_location = self.image_tools.find_button("party_set_a", tries=1)           
                    if (set_location == None):
                        tries -= 1
                        if (tries <= 0):
                            raise NotFoundException("Could not find Set A.")
                        
                        # See if the user had Set B active instead of Set A if matching failed.
                        set_location = self.image_tools.find_button("party_set_b", tries=1)
            else:
                while (set_location == None):
                    set_location = self.image_tools.find_button("party_set_b", tries=1)
                    if (set_location == None):
                        tries -= 1
                        if (tries <= 0):
                            raise NotFoundException("Could not find Set B.")
                        
                        # See if the user had Set A active instead of Set B if matching failed.
                        set_location = self.image_tools.find_button("party_set_a", tries=1)
        except Exception:
            self.print_and_save(f"\n{self.printtime()} [ERROR] Bot encountered exception while selecting A or B Set: \n{traceback.format_exc()}")
            self._isBotRunning.value = 1
            
        # Center the mouse on the "Set A" / "Set B" button and then click the correct Group tab.
        if(self._debug_mode):
            self.print_and_save(f"\n{self.printtime()} [DEBUG] Successfully selected the correct Set. Now selecting Group {group_number}...")
        
        x = None
        if (group_number == 1):
            x = set_location[0] - 350
        elif(group_number == 2):
            x = set_location[0] - 290
        elif(group_number == 3):
            x = set_location[0] - 230
        elif(group_number == 4):
            x = set_location[0] - 170
        elif(group_number == 5):
            x = set_location[0] - 110
        elif(group_number == 6):
            x = set_location[0] - 50
        else:
            x = set_location[0] + 10
        
        y = set_location[1] + 50
        self.mouse_tools.move_and_click_point(x, y)
        
        # Now select the correct Party.
        if(self._debug_mode):
            self.print_and_save(f"{self.printtime()} [DEBUG] Successfully selected Group {group_number}. Now selecting Party {party_number}...")
        
        x = None    
        if(party_number == 1):
            x = set_location[0] - 309
        elif(party_number == 2):
            x = set_location[0] - 252
        elif(party_number == 3):
            x = set_location[0] - 195
        elif(party_number == 4):
            x = set_location[0] - 138
        elif(party_number == 5):
            x = set_location[0] - 81
        elif(party_number == 6):
            x = set_location[0] - 24
            
        y = set_location[1] + 325
        self.mouse_tools.move_and_click_point(x, y)
        
        if(self._debug_mode):
            self.print_and_save(f"{self.printtime()} [DEBUG] Successfully selected Party {party_number}. Now starting the mission.")
            
        # Find and click the "OK" button to start the mission.
        self.find_and_click_button("ok")
        
        # If a popup appears and says "This raid battle has already ended. The Home screen will now appear.", return False.
        if(self.farming_mode.lower() == "raid" and self.image_tools.confirm_location("raid_just_ended_home_redirect")):
            self.print_and_save(f"\n{self.printtime()} [WARNING] Raid unfortunately just ended. Backing out now...")
            self.find_and_click_button("ok")
            return False
        
        return True

    def _find_charge_attacks(self):
        """Find total number of characters ready to Charge Attack.

        Returns:
            number_of_charge_attacks (int): Total number of image matches found for charge attacks.
        """
        number_of_charge_attacks = 0
        list_of_charge_attacks = self.image_tools.find_all("full_charge", custom_region=(self._attack_button_location[0] - 356, self._attack_button_location[1] + 67, 
                                                                                         self._attack_button_location[0] - 40, self._attack_button_location[1] + 214), hide_info=True)
        
        number_of_charge_attacks = len(list_of_charge_attacks)
        return number_of_charge_attacks

    def _find_dialog_in_combat(self):
        """Check if there are dialog popups from either Lyria or Vyrn and click them away.

        Returns:
            None
        """
        dialog_location = self.image_tools.find_dialog(self._attack_button_location[0], self._attack_button_location[1], tries=1)
        if (dialog_location != None):
            self.mouse_tools.move_and_click_point(dialog_location[0] + 180, dialog_location[1] - 51)
            
        return None
        
    def check_for_ap(self, use_full_elixir: bool = False):
        """Check if the user encountered the "Not Enough AP" popup and it will refill using either Half or Full Elixir.

        Args:
            use_full_elixir (bool, optional): Will use Full Elixir instead of Half Elixir based on whether this is True or not. Defaults to False.

        Returns:
            None
        """
        # Loop until the user gets to the Summon Selection screen.
        while((self.farming_mode.lower() != "coop" and not self.image_tools.confirm_location("select_summon", tries=2)) or 
              (self.farming_mode.lower() == "coop" and not self.image_tools.confirm_location("coop_without_support_summon", tries=2))):
            if(self.image_tools.confirm_location("not_enough_ap", tries=2)):
                # If the bot detects that the user has run out of AP, it will refill using either Half Elixir or Full Elixir.
                if(use_full_elixir == False):
                    self.print_and_save(f"\n{self.printtime()} [INFO] AP ran out! Using Half Elixir...")
                    half_ap_location = self.image_tools.find_button("refill_half_ap")
                    self.mouse_tools.move_and_click_point(half_ap_location[0], half_ap_location[1] + 175)
                else:
                    self.print_and_save(f"\n{self.printtime()} [INFO] AP ran out! Using Full Elixir...")
                    full_ap_location = self.image_tools.find_button("refill_full_ap")
                    self.mouse_tools.move_and_click_point(full_ap_location[0], full_ap_location[1] + 175)
                
                # Press the "OK" button to move to the Summon Selection screen.
                self.wait(1)
                self.find_and_click_button("ok")
                return None
            elif(self.farming_mode.lower() == "coop" and not self._coop_first_run and self.image_tools.find_button("attack")):
                break
            else:
                self.wait(1)
            
        self.print_and_save(f"{self.printtime()} [INFO] AP is available. Continuing...")
        return None

    def check_for_ep(self, use_soul_balm: bool = False):
        """Check if the user encountered the "Not Enough EP" popup and it will refill using either Soul Berry or Soul Balm.

        Args:
            use_soul_balm (bool, optional): Will use Soul Balm instead of Soul Berry based on whether this is True or not. Defaults to False.

        Returns:
            None
        """
        if(self.farming_mode.lower() == "raid" and self.image_tools.confirm_location("not_enough_ep", tries=2)):
            # If the bot detects that the user has run out of EP, it will refill using either Soul Berry or Soul Balm.
            if(use_soul_balm == False):
                self.print_and_save(f"\n{self.printtime()} [INFO] EP ran out! Using Soul Berries...")
                half_ep_location = self.image_tools.find_button("refill_soul_berry")
                self.mouse_tools.move_and_click_point(half_ep_location[0], half_ep_location[1] + 175)
            else:
                self.print_and_save(f"\n{self.printtime()} [INFO] EP ran out! Using Soul Balm...")
                full_ep_location = self.image_tools.find_button("refill_soul_balm")
                self.mouse_tools.move_and_click_point(full_ep_location[0], full_ep_location[1] + 175)
            
            # Press the "OK" button to move to the Summon Selection screen.
            self.wait(1)
            self.find_and_click_button("ok")
        else:
            self.print_and_save(f"{self.printtime()} [INFO] EP is available. Continuing...")
        
        return None

    def _select_character(self, character_number: int):
        """Selects the portrait of the character specified on the Combat screen.

        Args:
            character_number (int): The character that needs to be selected on the Combat screen.

        Returns:
            None
        """
        x = None
        if(character_number == 1):
            x = self._attack_button_location[0] - 317
        elif(character_number == 2):
            x = self._attack_button_location[0] - 240
        elif(character_number == 3):
            x = self._attack_button_location[0] - 158
        elif(character_number == 4):
            x = self._attack_button_location[0] - 76
        
        y = self._attack_button_location[1] + 123
        
        # Double-clicking the character portrait to avoid any non-invasive popups from other Raid participants.
        self.mouse_tools.move_and_click_point(x, y, mouse_clicks=2)
        return None

    def _use_character_skill(self, character_selected: int, skill: int):
        """Activate the specified skill for the already selected character.

        Args:
            character_selected (int): The selected character whose skill needs to be used.
            skill (int): The skill that needs to be used.

        Returns:
            None
        """
        # Determine which skill to use.
        x = None
        if("useskill(1)" in skill.lower()):
            self.print_and_save(f"{self.printtime()} [COMBAT] Character {character_selected} uses Skill 1.")
            x = self._attack_button_location[0] - 213
        elif("useskill(2)" in skill.lower()):
            self.print_and_save(f"{self.printtime()} [COMBAT] Character {character_selected} uses Skill 2.")
            x = self._attack_button_location[0] - 132
        elif("useskill(3)" in skill.lower()):
            self.print_and_save(f"{self.printtime()} [COMBAT] Character {character_selected} uses Skill 3.")
            x = self._attack_button_location[0] - 51
        elif("useskill(4)" in skill.lower()):
            self.print_and_save(f"{self.printtime()} [COMBAT] Character {character_selected} uses Skill 4.")
            x = self._attack_button_location[0] + 39
            
        y = self._attack_button_location[1] + 171
        
        # Double-clicking the skill to avoid any non-invasive popups from other Raid participants.
        self.mouse_tools.move_and_click_point(x, y, mouse_clicks=2)
        return None
    
    def collect_loot(self, isPendingBattle: bool = False, isEventNightmare: bool = False):
        """Collect the loot from the Results screen while clicking away any dialog popups. Primarily for raids.
        
        Args:
            isPendingBattle (bool): Skip the incrementation of runs attempted if this was a Pending Battle. Defaults to False.
            isSkippableEventNightmare (bool): Skip the incrementation of runs attempted if this was a Event Nightmare. Defaults to False.

        Returns:
            None
        """
        # Click away the "EXP Gained" popup and any other popups until the bot reaches the Loot Collected screen.
        if(not self._retreat_check and self.image_tools.confirm_location("exp_gained")):
            while(not self.image_tools.confirm_location("loot_collected", tries=1)):
                close_button_location = self.image_tools.find_button("close", tries=1, suppress_error=True)
                if(close_button_location != None):
                    self.mouse_tools.move_and_click_point(close_button_location[0], close_button_location[1])
                    
                cancel_button_location = self.image_tools.find_button("cancel", tries=1, suppress_error=True)    
                if(cancel_button_location != None):
                    self.mouse_tools.move_and_click_point(cancel_button_location[0], cancel_button_location[1])
                   
                ok_button_location = self.image_tools.find_button("ok", tries=1, suppress_error=True) 
                if(ok_button_location != None):
                    self.mouse_tools.move_and_click_point(ok_button_location[0], ok_button_location[1])
                    
                # Search for and click on the "Extended Mastery" popup.
                self.find_and_click_button("new_extended_mastery_level", tries=1, suppress_error=True)
                
            # Now that the bot is at the Loot Collected screen, detect any user-specified items.
            if(not isPendingBattle and not isEventNightmare):
                self.print_and_save(f"\n{self.printtime()} [INFO] Detecting if any user-specified loot dropped this run...")
                if(self._item_name != "EXP" and self._item_name != "Angel Halo Weapons" and self._item_name != "Repeated Runs"):
                    temp_amount = self.image_tools.find_farmed_items([self._item_name])[0]
                else:
                    temp_amount = 1
                
                self._item_amount_farmed += temp_amount
                self._amount_of_runs_finished += 1
        else:
            # If the bot reached here, that means the raid ended without the bot being able to take action so no loot dropped.
            temp_amount = 0
        
        if(not isPendingBattle and not isEventNightmare):    
            if(self._item_name != "EXP" and self._item_name != "Angel Halo Weapons" and self._item_name != "Repeated Runs"):
                self.print_and_save("\n\n********************************************************************************")
                self.print_and_save("********************************************************************************")
                self.print_and_save(f"{self.printtime()} [FARM] Farming Mode: {self.farming_mode}")
                self.print_and_save(f"{self.printtime()} [FARM] Mission: {self._mission_name}")
                self.print_and_save(f"{self.printtime()} [FARM] Summons: {self._summon_list}")
                self.print_and_save(f"{self.printtime()} [FARM] Amount of {self._item_name} gained this run: {temp_amount}")
                self.print_and_save(f"{self.printtime()} [FARM] Amount of {self._item_name} gained in total: {self._item_amount_farmed} / {self._item_amount_to_farm}")
                self.print_and_save(f"{self.printtime()} [FARM] Amount of runs completed: {self._amount_of_runs_finished}")
                self.print_and_save("********************************************************************************")
                self.print_and_save("********************************************************************************\n")
            else:
                self.print_and_save("\n\n********************************************************************************")
                self.print_and_save("********************************************************************************")
                self.print_and_save(f"{self.printtime()} [FARM] Farming Mode: {self.farming_mode}")
                self.print_and_save(f"{self.printtime()} [FARM] Mission: {self._mission_name}")
                self.print_and_save(f"{self.printtime()} [FARM] Summons: {self._summon_list}")
                self.print_and_save(f"{self.printtime()} [FARM] Amount of runs completed: {self._amount_of_runs_finished} / {self._item_amount_to_farm}")
                self.print_and_save("********************************************************************************")
                self.print_and_save("********************************************************************************\n")
                
        return None
    
    def check_for_friend_request(self):
        """Detect any "Friend Request" popups and click them away.

        Returns:
            None
        """
        if(self.image_tools.confirm_location("friend_request", tries=1)):
            self.print_and_save(f"\n{self.printtime()} [INFO] Detected \"Friend Request\" popup. Closing it now...")
            self.find_and_click_button("cancel")
        
        return None
    
    def _check_for_event_nightmare(self):
        """Checks for Event Nightmare and if it appears and the user enabled it in config.ini, start it.

        Returns:
            (bool): Return True if Event Nightmare was detected and successfully completed. Otherwise, return False.
        """
        if(self._enable_event_nightmare and self.image_tools.confirm_location("limited_time_quests")):
            # First check if the Event Nightmare is skippable.
            event_claim_loot_location = self.image_tools.find_button("event_claim_loot", tries=1, suppress_error=True)
            if(event_claim_loot_location != None):
                self.print_and_save(f"\n{self.printtime()} [EVENT] Skippable Event Nightmare detected. Claiming it now...")
                self.mouse_tools.move_and_click_point(event_claim_loot_location[0], event_claim_loot_location[1])
                self.collect_loot(isEventNightmare=True)
                return True
            else:
                self.print_and_save(f"\n{self.printtime()} [EVENT] Detected Event Nightmare. Starting it now...")
                
                self.print_and_save("\n\n********************************************************************************")
                self.print_and_save("********************************************************************************")
                self.print_and_save(f"{self.printtime()} [EVENT] Event Nightmare")
                self.print_and_save(f"{self.printtime()} [EVENT] Event Nightmare Summon Elements: {self._event_nightmare_summon_element_list}")
                self.print_and_save(f"{self.printtime()} [EVENT] Event Nightmare Summons: {self._event_nightmare_summon_list}")
                self.print_and_save(f"{self.printtime()} [EVENT] Event Nightmare Group Number: {self._event_nightmare_group_number}")
                self.print_and_save(f"{self.printtime()} [EVENT] Event Nightmare Party Number: {self._event_nightmare_party_number}")
                self.print_and_save(f"{self.printtime()} [EVENT] Event Nightmare Combat Script: {self._event_nightmare_combat_script}")
                self.print_and_save("********************************************************************************")
                self.print_and_save("********************************************************************************\n")
                
                self.find_and_click_button("play_next")
                
                # Once the bot is at the Summon Selection screen, select your Summon and Party and start the mission.
                self.wait(1)
                if(self.image_tools.confirm_location("select_summon")):
                    self._select_summon(self._event_nightmare_summon_list, self._event_nightmare_summon_element_list)
                    start_check = self._find_party_and_start_mission(self._event_nightmare_group_number, self._event_nightmare_party_number)
                    
                    # Once preparations are completed, start Combat Mode.
                    if(start_check and self.start_combat_mode(self._event_nightmare_combat_script, isNightmare=True)):
                        self.collect_loot(isEventNightmare=True)
                        return True
                
        elif(not self._enable_event_nightmare and self.image_tools.confirm_location("limited_time_quests")):
            # First check if the Event Nightmare is skippable.
            event_claim_loot_location = self.image_tools.find_button("event_claim_loot", tries=1, suppress_error=True)
            if(event_claim_loot_location != None):
                self.print_and_save(f"\n{self.printtime()} [EVENT] Skippable Event Nightmare detected but user opted to not run it. Claiming it regardless...")
                self.mouse_tools.move_and_click_point(event_claim_loot_location[0], event_claim_loot_location[1])
                self.collect_loot(isEventNightmare=True)
                return True
            else:
                self.print_and_save(f"\n{self.printtime()} [EVENT] Event Nightmare detected but user opted to not run it. Moving on...")
                self.find_and_click_button("close")
        else:
            self.print_and_save(f"\n{self.printtime()} [EVENT] No Event Nightmare detected. Moving on...")
        
        return False
    
    def _check_for_dimensional_halo(self):
        """Checks for Dimensional Halo and if it appears and the user enabled it in config.ini, start it.

        Returns:
            (bool): Return True if Dimensional Halo was detected and successfully completed. Otherwise, return False.
        """
        if(self._enable_dimensional_halo and self.image_tools.confirm_location("limited_time_quests", tries=1)):
            self.print_and_save(f"\n{self.printtime()} [D.HALO] Detected Dimensional Halo. Starting it now...")
            self._dimensional_halo_amount += 1
            
            self.print_and_save("\n\n********************************************************************************")
            self.print_and_save("********************************************************************************")
            self.print_and_save(f"{self.printtime()} [D.HALO] Dimensional Halo")
            self.print_and_save(f"{self.printtime()} [D.HALO] Dimensional Halo Summon Elements: {self._dimensional_halo_summon_element_list}")
            self.print_and_save(f"{self.printtime()} [D.HALO] Dimensional Halo Summons: {self._dimensional_halo_summon_list}")
            self.print_and_save(f"{self.printtime()} [D.HALO] Dimensional Halo Group Number: {self._dimensional_halo_group_number}")
            self.print_and_save(f"{self.printtime()} [D.HALO] Dimensional Halo Party Number: {self._dimensional_halo_party_number}")
            self.print_and_save(f"{self.printtime()} [D.HALO] Dimensional Halo Combat Script: {self._dimensional_halo_combat_script}")
            self.print_and_save(f"{self.printtime()} [D.HALO] Amount of Dimensional Halos encountered: {self._dimensional_halo_amount}")
            self.print_and_save("********************************************************************************")
            self.print_and_save("********************************************************************************\n")
            
            self.find_and_click_button("play_next")
            
            # Once the bot is at the Summon Selection screen, select your Summon and Party and start the mission.
            self.wait(1)
            if(self.image_tools.confirm_location("select_summon")):
                self._select_summon(self._dimensional_halo_summon_list, self._dimensional_halo_summon_element_list)
                start_check = self._find_party_and_start_mission(group_number=self._dimensional_halo_group_number, party_number=self._dimensional_halo_party_number)
                
                # Once preparations are completed, start Combat Mode.
                if(start_check and self.start_combat_mode(self._dimensional_halo_combat_script, isNightmare=True)):
                    self.collect_loot()
                    return True
                
        elif(not self._enable_dimensional_halo and self.image_tools.confirm_location("limited_time_quests", tries=1)):
            self.print_and_save(f"\n{self.printtime()} [D.HALO] Dimensional Halo detected but user opted to not run it. Moving on...")
            self.find_and_click_button("close")
        else:
            self.print_and_save(f"\n{self.printtime()} [D.HALO] No Dimensional Halo detected. Moving on...")
        
        return False
    
    def _wait_for_attack(self):
        """Wait for a maximum of 20 seconds until the bot sees either the Attack or the Next button before starting a new turn.

        Returns:
            None
        """
        tries = 10
        while((not self._retreat_check and self.image_tools.find_button("attack", tries=1, suppress_error=True) == None) or (not self._retreat_check and self.image_tools.find_button("next", tries=1, suppress_error=True) == None)):
            # Stagger the checks for dialog popups.
            if(tries % 2 == 0):
                self._find_dialog_in_combat()
            
            self.wait(1)
            
            tries -= 1
            if(tries < 0 or self.image_tools.find_button("attack", tries=1, suppress_error=True) != None or self.image_tools.find_button("next", tries=1, suppress_error=True) != None):
                break
            
            # Check if the Party wiped after attacking.
            self._party_wipe_check()
            self.wait(1)
        
        return None
    
    def _use_combat_healing_item(self, command: str, target: int = 0):
        """Uses the specified healing item during Combat mode with an optional target if the item needs it.

        Args:
            command (str): The command for the healing item to use.
            target (int, optional): The character target for the item. This depends on what item it is. Defaults to 0.

        Returns:
            None
        """
        if(self._debug_mode):
            self.print_and_save(f"\n{self.printtime()} [DEBUG] Using item: {command}, target: Character {target}.")
        
        # Click on the green "Heal" button.
        self.find_and_click_button("heal")
        
        # Format the item name.
        command = command.lower().replace(" ", "_")
        
        # Click on the specified healing item.
        if(command == "usebluepotion" or command == "usesupportpotion"):
            # Blue and Support Potions share the same image but they are at different positions on the screen.
            potion_location = self.image_tools.find_all(command)
            if(command == "usebluepotion"):
                self.mouse_tools.move_and_click_point(potion_location[0][0], potion_location[0][1])
            elif(command == "usesupportpotion"):
                self.mouse_tools.move_and_click_point(potion_location[1][0], potion_location[1][1])
        else:
            self.find_and_click_button(command)
        
        # After the initial popup vanishes to reveal a new popup, either select a character target or click a button depending on the healing item.
        if(self.image_tools.wait_vanish("tap_the_item_to_use", timeout=5)):
            if(command == "usegreenpotion"):
                self.print_and_save(f"\n{self.printtime()} [COMBAT] Using Green Potion on Character {target}...")
                self._select_character(target)
            elif(command == "usebluepotion"):
                self.print_and_save(f"\n{self.printtime()} [COMBAT] Using Blue Potion on the whole Party...")
                self.find_and_click_button("use") 
            elif(command == "usefullelixir"):
                self.print_and_save(f"\n{self.printtime()} [COMBAT] Using Full Elixir to revive and gain Full Charge...")
                self.find_and_click_button("ok")
            elif(command == "usesupportpotion"):
                self.print_and_save(f"\n{self.printtime()} [COMBAT] Using Support Potion on the whole Party...")
                self.find_and_click_button("ok")
            elif(command == "useclaritypotion"):
                self.print_and_save(f"\n{self.printtime()} [COMBAT] Using Clarity Herb on Character {target}...")
                self._select_character(target)
            elif(command == "userevivalpotion"):
                self.print_and_save(f"\n{self.printtime()} [COMBAT] Using Revival Potion to revive the whole Party...")
                self.find_and_click_button("ok")
        
            # Wait for the healing animation to finish.
            self.wait(1)
            
            if(not self.image_tools.confirm_location("use_item", tries=1)):
                self.print_and_save(f"{self.printtime()} [SUCCESS] Using item was successful.")
            else:
                self.print_and_save(f"{self.printtime()} [WARNING] Using item was not successful. Canceling it now...")
                self.find_and_click_button("cancel")
        else:
            self.print_and_save(f"{self.printtime()} [WARNING] Failed to click on the item. Either it does not exist for this particular mission or you ran out. Canceling it now...")
            self.find_and_click_button("cancel")
        
        return None
    
    def _request_backup(self):
        """Request backup during a Raid.

        Returns:
            None
        """
        self.print_and_save(f"\n{self.printtime()} [COMBAT] Now requesting Backup for this Raid.")
        
        # Scroll down the screen a little bit to have the "Request Backup" button visible on all screen sizes and then click it.
        self.mouse_tools.scroll_screen_from_home_button(-400)
        self.find_and_click_button("request_backup")
        
        # Find the location of the "Cancel" button and then click the button right next to it.
        # This is to ensure that no matter what the blue "Request Backup" button's appearance, it is ensured to be pressed.
        self.wait(1)
        cancel_button_location = self.image_tools.find_button("cancel")
        self.mouse_tools.move_and_click_point(cancel_button_location[0] + 200, cancel_button_location[1])
        
        # If requesting backup was successful, click "OK" to close the popup.
        self.wait(1)
        if(self.image_tools.confirm_location("request_backup_success", tries=1)):
            self.print_and_save(f"{self.printtime()} [COMBAT] Finished requesting Backup.")
            self.find_and_click_button("ok")
        
        # Move the view back up to the top of the page to ensure all elements are visible.
        self.mouse_tools.scroll_screen_from_home_button(400)
        
        return None
    
    def _tweet_backup(self):
        """Request backup during a Raid using Twitter.

        Returns:
            None
        """
        self.print_and_save(f"\n{self.printtime()} [COMBAT] Now requesting Backup for this Raid via Twitter.")
        
        # Scroll down the screen a little bit to have the "Request Backup" button visible on all screen sizes and then click it.
        self.mouse_tools.scroll_screen_from_home_button(-400)
        self.find_and_click_button("request_backup")
        
        # Then click the "Tweet" button.
        self.find_and_click_button("request_backup_tweet")
        self.find_and_click_button("ok")
        
        # If requesting backup via Twitter was successful, click "OK" to close the popup. Otherwise, click "Cancel".
        self.wait(1)
        if(self.image_tools.confirm_location("request_backup_tweet_success", tries=1)):
            self.print_and_save(f"{self.printtime()} [COMBAT] Finished requesting Backup via Twitter.")
            self.find_and_click_button("ok")
        else:
            self.print_and_save(f"{self.printtime()} [COMBAT] Failed requesting Backup via Twitter as there is still a cooldown from the last tweet.")
            self.find_and_click_button("cancel")
            
        # Move the view back up to the top of the page to ensure all elements are visible.
        self.mouse_tools.scroll_screen_from_home_button(400)
        
        return None

    def start_combat_mode(self, script_file_path: str = "", isNightmare: bool = False):
        """Start Combat Mode with the given script file path. Start reading through the text file line by line and have the bot proceed with the commands accordingly.

        Args:
            script_file_path (str, optional): Path to the combat script text file. Defaults to "".
            isNightmare (bool, optional): If Combat Mode is being used for a Nightmare, determines the method of reading the script file.

        Returns:
            (bool): Return True if Combat Mode was successful. Else, return False if the Party wiped or backed out without retreating.
        """
        try:
            self.print_and_save("\n\n################################################################################")
            self.print_and_save("################################################################################")
            self.print_and_save(f"{self.printtime()} [COMBAT] Starting Combat Mode.")
            self.print_and_save("################################################################################")
            self.print_and_save("################################################################################\n")
            
            # Open the combat script text file.
            if(script_file_path == "" or script_file_path == None):
                self.print_and_save(f"\n{self.printtime()} [COMBAT] No script file was provided. Using default full_auto.txt script.")
                os.chdir(os.getcwd() + "/scripts/")
                script = open(os.path.abspath("full_auto.txt"), "r")
                os.chdir(self._owd)
            elif(isNightmare):
                self.print_and_save(f"\n{self.printtime()} [COMBAT] Now loading up combat script for this at {os.getcwd()}\scripts\{script_file_path}")
                os.chdir(os.getcwd() + "/scripts/")
                root, extension = os.path.splitext(script_file_path)
                if(not extension):
                    script = open(os.path.abspath(script_file_path + ".txt"), "r")
                else:
                    script = open(os.path.abspath(script_file_path), "r")
                os.chdir(self._owd)
            else:
                self.print_and_save(f"\n{self.printtime()} [COMBAT] Now loading up combat script at {script_file_path}")
                os.chdir(self._owd)
                script = open(script_file_path, "r")
            
            # Grab all lines in the file and store it in a list.
            lines = script.readlines()
            script.close()
            
            i = 0  # Current index for the list of lines from the script.
            line_number = 1  # Current line number the bot is reading.
            turn_number = 1  # Current turn for the script execution.
            
            # Reset the retreat, semi auto, and full auto flags.
            self._retreat_check = False
            semi_auto = False
            full_auto = False
            
            # Reset the saved locations of the "Attack" and "Back" buttons.
            self._attack_button_location = None
            self._back_button_location = None
            
            # Save the positions of the "Attack" and "Back" button.
            self._attack_button_location = self.image_tools.find_button("attack", tries=10)
            if(self._attack_button_location != None):
                self._back_button_location = (self._attack_button_location[0] - 322, self._attack_button_location[1])
            else:
                self.print_and_save(f"\n{self.printtime()} [ERROR] Cannot find Attack button. Raid must have just ended.")
                return False
                
            # This is where the main workflow of Combat Mode is located and it will loop until the last of the commands have been executed.
            while(i < len(lines) and not self._retreat_check and not semi_auto and not full_auto):
                line = lines[i].strip()
                
                # Skip this line if it is empty or a comment.
                while(line == "" or line[0] == "#" or line[0] == "/"):
                    line_number += 1
                    i += 1
                    line = lines[i].strip()
                    
                # Print each line read if Debug Mode is active.
                if(self._debug_mode):
                    self.print_and_save(f"\n{self.printtime()} [DEBUG] Reading Line {line_number}: \"{line.strip()}\"")
                    
                # If the execution reached the next turn block and it is currently not the correct turn, keep pressing the "Attack" button until the turn number matches.
                if("turn" in line.lower() and int(line.split(":")[0].split(" ")[1]) != turn_number):
                    self.print_and_save(f"\n{self.printtime()} [COMBAT] Attacking until the bot reaches Turn {int(line.split(':')[0].split(' ')[1])}...")
                    
                    while(int(line.split(":")[0].split(" ")[1]) != turn_number):
                        self.print_and_save(f"{self.printtime()} [COMBAT] Starting Turn {turn_number}.")
                        self._find_dialog_in_combat()
                        
                        attack_button_location = self.image_tools.find_button("attack", tries=1, suppress_error=True)
                        if (attack_button_location != None):
                            self.print_and_save(f"{self.printtime()} [COMBAT] Ending Turn {turn_number} by attacking now...")
                            number_of_charge_attacks = self._find_charge_attacks()
                            self.mouse_tools.move_and_click_point(self._attack_button_location[0], self._attack_button_location[1])
                            self.wait(3 + number_of_charge_attacks)
                            self._wait_for_attack()
                            self.print_and_save(f"{self.printtime()} [COMBAT] Turn {turn_number} has ended.")
                            self._party_wipe_check()
                            turn_number += 1
                            
                        next_button_location = self.image_tools.find_button("next", tries=1, suppress_error=True)
                        if(next_button_location != None):
                            self.mouse_tools.move_and_click_point(next_button_location[0], next_button_location[1])
                            self.wait(3)
                            
                        if(self._retreat_check or self.image_tools.confirm_location("exp_gained", tries=1) or self.image_tools.confirm_location("no_loot", tries=1)):
                            self.print_and_save("\n################################################################################")
                            self.print_and_save("################################################################################")
                            self.print_and_save(f"{self.printtime()} [COMBAT] Ending Combat Mode.")
                            self.print_and_save("################################################################################")
                            self.print_and_save("################################################################################")
                            return False
                        elif(self.image_tools.confirm_location("battle_concluded", tries=1)):
                            self.print_and_save(f"\n{self.printtime()} [COMBAT] Battle concluded suddenly.")
                            self.find_and_click_button("ok")
                            
                            self.print_and_save("\n################################################################################")
                            self.print_and_save("################################################################################")
                            self.print_and_save(f"{self.printtime()} [COMBAT] Ending Combat Mode.")
                            self.print_and_save("################################################################################")
                            self.print_and_save("################################################################################")
                            return False
                            
                if(self._retreat_check or self.image_tools.confirm_location("exp_gained", tries=1) or self.image_tools.confirm_location("no_loot", tries=1)):
                    break
                elif(self.image_tools.confirm_location("battle_concluded", tries=1)):
                    self.print_and_save(f"\n{self.printtime()} [COMBAT] Battle concluded suddenly.")
                    self.find_and_click_button("ok")
                    break
                
                # If it is the start of the Turn and it is currently the correct turn, grab the next line for execution.
                if("turn" in line.lower() and int(line.split(":")[0].split(" ")[1]) == turn_number and not self._retreat_check):
                    self.print_and_save(f"\n{self.printtime()} [COMBAT] Starting Turn {turn_number}. Reading script now...")
                    
                    self._find_dialog_in_combat()
                    
                    # Continue reading each line inside the turn block until you reach the "end" command.
                    while(("end" not in line.lower() and "exit" not in line.lower()) and i < len(lines)):
                        # Strip any leading and trailing whitespaces.
                        line = lines[i].strip()
                        
                        # Skip this line if it is empty or a comment.
                        while(line == "" or line[0] == "#" or line[0] == "/"):
                            line_number += 1
                            i += 1
                            line = lines[i].strip()
                        
                        if("end" in line.lower() and not semi_auto and not full_auto):
                            break
                        
                        if("exit" in line.lower() and not semi_auto and not full_auto):
                            # End Combat Mode by heading back to the Home screen without retreating. Usually for raid farming as to maximize the number of raids joined after completing the provided combat script.
                            self.print_and_save(f"\n{self.printtime()} [COMBAT] Reading Line {line_number}: \"{line.strip()}\"")
                            self.print_and_save(f"{self.printtime()} [COMBAT] Leaving this raid without retreating...")
                            self.wait(1)
                            self.go_back_home(confirm_location_check=True)
                            return False
                        
                        self.print_and_save(f"\n{self.printtime()} [COMBAT] Reading Line {line_number}: \"{line}\"")
                        
                        # Determine which character to take action.
                        character_selected = 0
                        if("character1" in line.lower()):
                            character_selected = 1
                        elif("character2" in line.lower()):
                            character_selected = 2
                        elif("character3" in line.lower()):
                            character_selected = 3
                        elif("character4" in line.lower()):
                            character_selected = 4
                            
                        if(character_selected != 0):
                            # Select the character specified.
                            self._select_character(character_selected)
                            
                            # Execute each skill from left to right for this character.
                            commands = line.split(".")[1:]
                            while(len(commands) > 0):
                                command = commands.pop(0).lower()
                                
                                if("useskill" in command):
                                    # Use the skill.
                                    self._use_character_skill(character_selected, command)
                                    
                                    if(self.image_tools.confirm_location("use_skill", tries=1)):
                                        # Check if the skill requires a target.
                                        select_a_character_location = self.image_tools.find_button("select_a_character", tries=1)
                                        if(select_a_character_location != None):
                                            self.print_and_save(f"{self.printtime()} [COMBAT] Skill is now awaiting a target...")
                                            
                                            # Parse and then click on the targeted character.
                                            target = commands.pop(0).lower()
                                            if("target(1)" in target):
                                                self.print_and_save(f"{self.printtime()} [COMBAT] Targeting Character 1.")
                                                self.mouse_tools.move_and_click_point(select_a_character_location[0] - 90, select_a_character_location[1] + 85)
                                            elif("target(2)" in target):
                                                self.print_and_save(f"{self.printtime()} [COMBAT] Targeting Character 2.")
                                                self.mouse_tools.move_and_click_point(select_a_character_location[0], select_a_character_location[1] + 85)
                                            elif("target(3)" in target):
                                                self.print_and_save(f"{self.printtime()} [COMBAT] Targeting Character 3.")
                                                self.mouse_tools.move_and_click_point(select_a_character_location[0] + 90, select_a_character_location[1] + 85)
                                            elif("target(4)" in target):
                                                self.print_and_save(f"{self.printtime()} [COMBAT] Targeting Character 4.")
                                                self.mouse_tools.move_and_click_point(select_a_character_location[0] - 90, select_a_character_location[1] + 250)
                                            elif("target(5)" in target):
                                                self.print_and_save(f"{self.printtime()} [COMBAT] Targeting Character 5.")
                                                self.mouse_tools.move_and_click_point(select_a_character_location[0], select_a_character_location[1] + 250)
                                            elif("target(6)" in target):
                                                self.print_and_save(f"{self.printtime()} [COMBAT] Targeting Character 6.")
                                                self.mouse_tools.move_and_click_point(select_a_character_location[0] + 90, select_a_character_location[1] + 250)
                                            else:
                                                # If the command is not one of the supported targets, close the popup.
                                                self.print_and_save(f"{self.printtime()} [COMBAT] Invalid Character target. Canceling now...")
                                                self.find_and_click_button("cancel")
                                        
                                        # Else, check if the character is skill-sealed.
                                        elif(self.image_tools.confirm_location("skill_unusable", tries=1)):
                                            self.print_and_save(f"{self.printtime()} [COMBAT] Character is currently skill-sealed. Unable to execute command.")
                                            self.find_and_click_button("cancel")
                                        
                            # Now click the "Back" button.
                            self.mouse_tools.move_and_click_point(self._back_button_location[0], self._back_button_location[1])
                            
                            # Attempt to wait to see if the character one-shot the enemy or not. This is user-defined in the config.ini.
                            self.wait(self._idle_seconds_after_skill)
                            
                            if(self._retreat_check or self.image_tools.confirm_location("exp_gained", tries=1) or self.image_tools.confirm_location("no_loot", tries=1)):
                                self.print_and_save("\n################################################################################")
                                self.print_and_save("################################################################################")
                                self.print_and_save(f"{self.printtime()} [COMBAT] Ending Combat Mode.")
                                self.print_and_save("################################################################################")
                                self.print_and_save("################################################################################")
                                return False
                            elif(self.image_tools.confirm_location("battle_concluded", tries=1)):
                                self.print_and_save(f"\n{self.printtime()} [COMBAT] Battle concluded suddenly.")
                                self.find_and_click_button("ok")
                                
                                self.print_and_save("\n################################################################################")
                                self.print_and_save("################################################################################")
                                self.print_and_save(f"{self.printtime()} [COMBAT] Ending Combat Mode.")
                                self.print_and_save("################################################################################")
                                self.print_and_save("################################################################################")
                                return False
                        
                        for j in range(1,7):
                            if(f"summon({j})" in line.lower()):
                                # Click the "Summon" button to bring up the available Summons.
                                self.print_and_save(f"{self.printtime()} [COMBAT] Invoking Summon #{j}.")
                                self.find_and_click_button("summon")
                                
                                # Click on the specified Summon.
                                if(j == 1):
                                    self.mouse_tools.move_and_click_point(self._attack_button_location[0] - 317, self._attack_button_location[1] + 138, mouse_clicks=2)
                                elif(j == 2):
                                    self.mouse_tools.move_and_click_point(self._attack_button_location[0] - 243, self._attack_button_location[1] + 138, mouse_clicks=2)
                                elif(j == 3):
                                    self.mouse_tools.move_and_click_point(self._attack_button_location[0] - 165, self._attack_button_location[1] + 138, mouse_clicks=2)
                                elif(j == 4):
                                    self.mouse_tools.move_and_click_point(self._attack_button_location[0] - 89, self._attack_button_location[1] + 138, mouse_clicks=2)
                                elif(j == 5):
                                    self.mouse_tools.move_and_click_point(self._attack_button_location[0] - 12, self._attack_button_location[1] + 138, mouse_clicks=2)
                                else:
                                    self.mouse_tools.move_and_click_point(self._attack_button_location[0] + 63, self._attack_button_location[1] + 138, mouse_clicks=2)
                                    
                                # Check if it is able to be summoned.
                                if(self.image_tools.confirm_location("summon_details", tries=2)):
                                    ok_button_location = self.image_tools.find_button("ok", tries=1)
                                    if(ok_button_location != None):
                                        self.mouse_tools.move_and_click_point(ok_button_location[0], ok_button_location[1])
                                        
                                        # Wait for the Summon animation to complete. This is user-defined in the config.ini.
                                        self.wait(self._idle_seconds_after_summon)
                                    else:
                                        self.print_and_save(f"{self.printtime()} [COMBAT] Summon #{j} cannot be invoked due to current restrictions.")
                                        self.find_and_click_button("cancel")
                                        
                                        # Click the "Back" button.
                                        self.mouse_tools.move_and_click_point(self._back_button_location[0], self._back_button_location[1])
                                        
                                if(self._retreat_check or self.image_tools.confirm_location("exp_gained", tries=1) or self.image_tools.confirm_location("no_loot", tries=1)):
                                    self.print_and_save("\n################################################################################")
                                    self.print_and_save("################################################################################")
                                    self.print_and_save(f"{self.printtime()} [COMBAT] Ending Combat Mode.")
                                    self.print_and_save("################################################################################")
                                    self.print_and_save("################################################################################")
                                    return False
                                elif(self.image_tools.confirm_location("battle_concluded", tries=1)):
                                    self.print_and_save(f"\n{self.printtime()} [COMBAT] Battle concluded suddenly.")
                                    self.find_and_click_button("ok")
                                    
                                    self.print_and_save("\n################################################################################")
                                    self.print_and_save("################################################################################")
                                    self.print_and_save(f"{self.printtime()} [COMBAT] Ending Combat Mode.")
                                    self.print_and_save("################################################################################")
                                    self.print_and_save("################################################################################")
                                    return False
                                
                        if(self.image_tools.find_button("next", tries=1, suppress_error=True) != None):
                            break
                        
                        if(not semi_auto and not full_auto and "enablesemiauto" in line.lower()):
                            self.print_and_save(f"{self.printtime()} [COMBAT] Bot will now attempt to enable Semi Auto...")
                            semi_auto = True
                            break
                        
                        if(not semi_auto and not full_auto and "enablefullauto" in line.lower()):
                            self.print_and_save(f"{self.printtime()} [COMBAT] Enabling Full Auto. Bot will continue until raid ends or Party wipes.")
                            enabled_full_auto = self.find_and_click_button("full_auto", tries=5)
                            
                            # If the bot failed to find and click the "Full Auto" button, fallback to the "Semi Auto" button.
                            if(not enabled_full_auto):
                                self.print_and_save(f"{self.printtime()} [COMBAT] Bot failed to find the \"Full Auto\" button. Falling back to Semi Auto.")
                                semi_auto = True
                            else:
                                full_auto = True
                            
                            break
                        
                        if("requestbackup" in line.lower() and not semi_auto and not full_auto):
                            # Request Backup for this Raid.
                            self._request_backup()
                        
                        if("tweetbackup" in line.lower() and not semi_auto and not full_auto):
                            # Request Backup via Twitter for this Raid.
                            self._tweet_backup()
                        
                        item_commands = ["usegreenpotion.target(1)", "usegreenpotion.target(2)", "usegreenpotion.target(3)", "usegreenpotion.target(4)", "usebluepotion", "usefullelixir", 
                                         "usesupportpotion", "useclarityherb.target(1)", "useclarityherb.target(2)", "useclarityherb.target(3)", "useclarityherb.target(4)", "userevivalpotion"]
                        if(line.lower() in item_commands and not semi_auto and not full_auto):
                            # Parse the command from the line.
                            command = line.split(".").pop(0).lower()
                            
                            # Parse the target if the user is using a Green Potion or a Clarity Herb.
                            if((command == "usegreenpotion" or command == "useclarityherb") and "target" in line.lower()):
                                target = line.split(".").pop(1).lower()
                                if("target(1)" in target):
                                    target = 1
                                elif("target(2)" in target):
                                    target = 2
                                elif("target(3)" in target):
                                    target = 3
                                elif("target(4)" in target):
                                    target = 4
                            else:
                                target = 0
                            
                            # Use the item and continue to the next line for execution.
                            self._use_combat_healing_item(command, target)
                        
                        # Move onto the next command for execution.
                        line_number += 1
                        i += 1
                            
                if(not semi_auto and not full_auto and "enablesemiauto" in line.lower()):
                    self.print_and_save(f"{self.printtime()} [COMBAT] Bot will now attempt to enable Semi Auto...")
                    semi_auto = True
                    break
                elif(semi_auto):
                    break
                
                if(not semi_auto and not full_auto and "enablefullauto" in line.lower()):
                    self.print_and_save(f"{self.printtime()} [COMBAT] Enabling Full Auto. Bot will continue until raid ends or Party wipes.")
                    enabled_full_auto = self.find_and_click_button("full_auto")
                            
                    # If the bot failed to find and click the "Full Auto" button, fallback to the "Semi Auto" button.
                    if(not enabled_full_auto):
                        self.print_and_save(f"{self.printtime()} [COMBAT] Bot failed to find the \"Full Auto\" button. Falling back to Semi Auto.")
                        semi_auto = True
                    else:
                        full_auto = True
                        
                    break
                
                if("end" in line.lower() and not semi_auto and not full_auto):
                    next_button_location = self.image_tools.find_button("next", tries=1, suppress_error=True)
                    if(next_button_location != None):
                        self.print_and_save(f"{self.printtime()} [COMBAT] All enemies on screen have been eliminated before attacking. Preserving Turn {turn_number} by moving to the next Wave...")
                        self.mouse_tools.move_and_click_point(next_button_location[0], next_button_location[1])
                        self.wait(3)
                    else:
                        self.print_and_save(f"{self.printtime()} [COMBAT] Ending Turn {turn_number} by attacking now...")
                        number_of_charge_attacks = self._find_charge_attacks()
                        self.mouse_tools.move_and_click_point(self._attack_button_location[0], self._attack_button_location[1])
                        
                        # Peek ahead of the script while the Party is currently attacking and see if it detects the command "enableSemiAuto" outside of a Turn block.
                        temp_index = i
                        while(temp_index < len(lines)):
                            temp_line = lines[temp_index].strip()
                            
                            # Skip this line if it is empty or a comment.
                            if(temp_line == "" or temp_line[0] == "#" or temp_line[0] == "/"):
                                temp_index += 1
                                continue
                            
                            # Enable Semi Auto if the command is read. Otherwise it can break out of the loop if it reaches a new Turn block.
                            if("enablesemiauto" in temp_line.lower()):
                                self.print_and_save(f"{self.printtime()} [COMBAT] Enabling Semi Auto. Bot will continue until raid ends or Party wipes.")
                                self.find_and_click_button("semi_auto")
                                semi_auto = True
                                break
                            elif("turn" in temp_line.lower()):
                                break
                            
                            temp_index += 1
                        
                        self.wait(3 + number_of_charge_attacks)
                        self._wait_for_attack()
                        self.print_and_save(f"{self.printtime()} [COMBAT] Turn {turn_number} has ended.")
                        self._party_wipe_check()
                        turn_number += 1
                        
                        next_button_location = self.image_tools.find_button("next", tries=1, suppress_error=True)
                        if(next_button_location != None):
                            self.mouse_tools.move_and_click_point(next_button_location[0], next_button_location[1])
                            self.wait(3)
                        
                if("exit" in line.lower() and not semi_auto and not full_auto):
                    # End Combat Mode by heading back to the Home screen without retreating. Usually for raid farming as to maximize the number of raids joined after completing the provided combat script.
                    self.print_and_save(f"\n{self.printtime()} [COMBAT] Reading Line {line_number}: \"{line.strip()}\"")
                    self.print_and_save(f"{self.printtime()} [COMBAT] Leaving this raid without retreating...")
                    self.wait(1)
                    self.go_back_home(confirm_location_check=True)
                    return False
                    
                # Continue to the next line for execution.
                line_number += 1
                i += 1
            
            # When execution gets to here outside of the main workflow loop for Combat Mode, the bot has reached the end of the combat script and will now attack until the battle ends or the Party wipes.
            self.print_and_save(f"\n{self.printtime()} [COMBAT] Bot has reached end of script. Automatically attacking until battle ends or Party wipes...")
            
            # Keep pressing the location of the "Attack" / "Next" button until the bot reaches the Quest Results screen.
            while(not self._retreat_check and not semi_auto and not full_auto and not self.image_tools.confirm_location("exp_gained", tries=1) and not self.image_tools.confirm_location("no_loot", tries=1)):
                self._find_dialog_in_combat()
                attack_button_location = self.image_tools.find_button("attack", tries=1, suppress_error=True)
                if (attack_button_location != None):
                    self.print_and_save(f"\n{self.printtime()} [COMBAT] Starting Turn {turn_number}.")
                    self.print_and_save(f"{self.printtime()} [COMBAT] Ending Turn {turn_number} by attacking now...")
                    number_of_charge_attacks = self._find_charge_attacks()
                    self.mouse_tools.move_and_click_point(self._attack_button_location[0], self._attack_button_location[1])
                    self.wait(3 + number_of_charge_attacks)
                    self._wait_for_attack()
                    self.print_and_save(f"{self.printtime()} [COMBAT] Turn {turn_number} has ended.")
                    self._party_wipe_check()
                    turn_number += 1
                    
                next_button_location = self.image_tools.find_button("next", tries=1, suppress_error=True)
                if(next_button_location != None):
                    self.mouse_tools.move_and_click_point(next_button_location[0], next_button_location[1])
                    self.wait(3)
                    
            
            # Double check to see if Semi Auto is turned on. Note that the "Semi Auto" button only appears while the Party is attacking.
            if(not self._retreat_check and semi_auto and not full_auto):
                self.print_and_save(f"{self.printtime()} [COMBAT] Double checking to see if Semi Auto is enabled...")
                enabled_semi_auto = self.image_tools.find_button("semi_auto_enabled")
                if(not enabled_semi_auto):
                    # Have the Party attack and then attempt to see if the "Semi Auto" button becomes visible.
                    self.find_and_click_button("attack")
                    enabled_semi_auto = self.find_and_click_button("semi_auto", tries=5)
                    
                    # If the bot still cannot find the "Semi Auto" button, that probably means the user has the "Full Auto" button on the screen instead of the "Semi Auto" button.
                    if(not enabled_semi_auto):
                        self.print_and_save(f"{self.printtime()} [COMBAT] Failed to enable Semi Auto. Falling back to Full Auto...")
                        semi_auto = False
                        full_auto = True
                        
                        # Enable Full Auto.
                        self.find_and_click_button("full_auto")
                    else:
                        self.print_and_save(f"{self.printtime()} [COMBAT] Semi Auto is now enabled.")
            
            # Main workflow loop for Semi Auto. The game will progress the Quest/Raid until it ends or the Party wipes.
            while(not self._retreat_check and semi_auto and not full_auto and not self.image_tools.confirm_location("exp_gained", tries=1) and not self.image_tools.confirm_location("no_loot", tries=1)):
                if(self.image_tools.confirm_location("battle_concluded", tries=1)):
                    self.print_and_save(f"\n{self.printtime()} [COMBAT] Battle concluded suddenly.")
                    self.find_and_click_button("ok")
                    break
                self._party_wipe_check()
                self.wait(3)
            
            # Main workflow loop for Full Auto. The game will progress the Quest/Raid until it ends or the Party wipes.
            while(not self._retreat_check and not semi_auto and full_auto and not self.image_tools.confirm_location("exp_gained", tries=1) and not self.image_tools.confirm_location("no_loot", tries=1)):
                if(self.image_tools.confirm_location("battle_concluded", tries=1)):
                    self.print_and_save(f"\n{self.printtime()} [COMBAT] Battle concluded suddenly.")
                    self.find_and_click_button("ok")
                    break
                self._party_wipe_check()
                self.wait(3)
                
            self.print_and_save("\n################################################################################")
            self.print_and_save("################################################################################")
            self.print_and_save(f"{self.printtime()} [COMBAT] Ending Combat Mode.")
            self.print_and_save("################################################################################")
            self.print_and_save("################################################################################")
            
            if(not self._retreat_check):
                self.print_and_save(f"\n{self.printtime()} [INFO] Bot has reached the Quest Results screen.")
                return True
            else:
                return False
        except FileNotFoundError as e:
            self.print_and_save(f"\n{self.printtime()} [ERROR] Cannot find \"{script_file_path}.txt\": \n{traceback.format_exc()}")
            self._isBotRunning.value = 1
    
    def start_farming_mode(self, item_name: str, item_amount_to_farm: int, farming_mode: str, location_name: str, mission_name: str, summon_element_list: Iterable[str], summon_list: Iterable[str], group_number: int, party_number: int):
        """Start the Farming Mode using the given parameters.

        Args:
            item_name (str): Name of the item to farm.
            item_amount_to_farm (str): Amount of the item to farm.
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
            if(item_name != "EXP"):
                self.print_and_save("\n\n################################################################################")
                self.print_and_save("################################################################################")
                self.print_and_save(f"{self.printtime()} [FARM] Starting Farming Mode for {farming_mode}.")
                self.print_and_save(f"{self.printtime()} [FARM] Farming {item_amount_to_farm}x {item_name} at {mission_name}.")
                self.print_and_save("################################################################################")
                self.print_and_save("################################################################################\n")
            else:
                self.print_and_save("\n\n################################################################################")
                
                self.print_and_save("################################################################################")
                self.print_and_save(f"{self.printtime()} [FARM] Starting Farming Mode for {farming_mode}.")
                self.print_and_save(f"{self.printtime()} [FARM] Doing {item_amount_to_farm}x runs for {item_name} at {mission_name}.")
                self.print_and_save("################################################################################")
                self.print_and_save("################################################################################\n")
            
            # Parse the difficulty for the chosen mission.
            difficulty = ""
            if(farming_mode.lower() == "special" or farming_mode.lower() == "event" or farming_mode.lower() == "event (token drawboxes)" or farming_mode.lower() == "rise of the beasts"):
                if(mission_name.find("N ") == 0):
                    difficulty = "Normal"
                elif(mission_name.find("H ") == 0):
                    difficulty = "Hard"
                elif(mission_name.find("VH ") == 0):
                    difficulty = "Very Hard"
                elif(mission_name.find("EX ") == 0):
                    difficulty = "Extreme"
                elif(mission_name.find("IM ") == 0):
                    difficulty = "Impossible"
            elif(farming_mode.lower() == "dread barrage"):
                if(mission_name.find("1 Star") == 0):
                    difficulty = "1 Star"
                elif(mission_name.find("2 Star") == 0):
                    difficulty = "2 Star"
                elif(mission_name.find("3 Star") == 0):
                    difficulty = "3 Star"
                elif(mission_name.find("4 Star") == 0):
                    difficulty = "4 Star"
                elif(mission_name.find("5 Star") == 0):
                    difficulty = "5 Star"
            
            self._item_amount_farmed = 0
            self._amount_of_runs_finished = 0
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
            if(self.farming_mode.lower() == "special" and self._mission_name == "VH Angel Halo" and self._enable_dimensional_halo and (self._item_name == "EXP" or self._item_name == "Angel Halo Weapons")):
                self.print_and_save(f"\n{self.printtime()} [INFO] Initializing settings for Dimensional Halo...")
                
                if(self._dimensional_halo_combat_script == ""):
                    self.print_and_save(f"{self.printtime()} [INFO] Combat Script for Dimensional Halo will reuse the one for Farming Mode.")
                    self._dimensional_halo_combat_script = self._combat_script
                    
                if(len(self._dimensional_halo_summon_element_list) == 0):
                    self.print_and_save(f"{self.printtime()} [INFO] Summon Elements for Dimensional Halo will reuse the ones for Farming Mode.")
                    self._dimensional_halo_summon_element_list = self._summon_element_list
                    
                if(len(self._dimensional_halo_summon_list) == 0):
                    self.print_and_save(f"{self.printtime()} [INFO] Summons for Dimensional Halo will reuse the ones for Farming Mode.")
                    self._dimensional_halo_summon_list = self._summon_list
                    
                if(self._dimensional_halo_group_number == ""):
                    self.print_and_save(f"{self.printtime()} [INFO] Group Number for Dimensional Halo will reuse the one for Farming Mode.")
                    self._dimensional_halo_group_number = self._group_number
                else:
                    self._dimensional_halo_group_number = int(self._dimensional_halo_group_number)

                if(self._dimensional_halo_party_number == ""):
                    self.print_and_save(f"{self.printtime()} [INFO] Party Number for Dimensional Halo will reuse the one for Farming Mode.")
                    self._dimensional_halo_party_number = self._party_number
                else:
                    self._dimensional_halo_party_number = int(self._dimensional_halo_party_number)
                    
                self.print_and_save(f"{self.printtime()} [INFO] Settings initialized for Dimensional Halo...")
            elif(self._item_name == "Repeated Runs" and self._enable_event_nightmare):
                # Do the same for Event Nightmare if enabled.
                self.print_and_save(f"\n{self.printtime()} [INFO] Initializing settings for Event...")
                
                if(self._event_nightmare_combat_script == ""):
                    self.print_and_save(f"{self.printtime()} [INFO] Combat Script for Event will reuse the one for Farming Mode.")
                    self._event_nightmare_combat_script = self._combat_script
                    
                if(len(self._event_nightmare_summon_element_list) == 0):
                    self.print_and_save(f"{self.printtime()} [INFO] Summon Elements for Event will reuse the ones for Farming Mode.")
                    self._event_nightmare_summon_element_list = self._summon_element_list
                    
                if(len(self._event_nightmare_summon_list) == 0):
                    self.print_and_save(f"{self.printtime()} [INFO] Summons for Event will reuse the ones for Farming Mode.")
                    self._event_nightmare_summon_list = self._summon_list
                    
                if(self._event_nightmare_group_number == ""):
                    self.print_and_save(f"{self.printtime()} [INFO] Group Number for Event will reuse the one for Farming Mode.")
                    self._event_nightmare_group_number = self._group_number
                else:
                    self._event_nightmare_group_number = int(self._event_nightmare_group_number)
                    
                if(self._event_nightmare_party_number == ""):
                    self.print_and_save(f"{self.printtime()} [INFO] Party Number for Event will reuse the one for Farming Mode.")
                    self._event_nightmare_party_number = self._party_number
                else:
                    self._event_nightmare_party_number = int(self._event_nightmare_party_number)
                    
                self.print_and_save(f"{self.printtime()} [INFO] Settings initialized for Event...")
            elif(self._item_name == "Repeated Runs" and self._enable_rotb_extreme_plus):
                # Do the same for Rise of the Beasts Extreme+ if enabled.
                self.print_and_save(f"\n{self.printtime()} [INFO] Initializing settings for Rise of the Beasts Extreme+...")
                
                if(self._rotb_extreme_plus_combat_script == ""):
                    self.print_and_save(f"{self.printtime()} [INFO] Combat Script for Rise of the Beasts Extreme+ will reuse the one for Farming Mode.")
                    self._event_nightmare_combat_script = self._combat_script
                    
                if(len(self._rotb_extreme_plus_summon_element_list) == 0):
                    self.print_and_save(f"{self.printtime()} [INFO] Summon Elements for Rise of the Beasts Extreme+ will reuse the ones for Farming Mode.")
                    self._rotb_extreme_plus_summon_element_list = self._summon_element_list
                    
                if(len(self._rotb_extreme_plus_summon_list) == 0):
                    self.print_and_save(f"{self.printtime()} [INFO] Summons for Rise of the Beasts Extreme+ will reuse the ones for Farming Mode.")
                    self._rotb_extreme_plus_summon_list = self._summon_list
                    
                if(self._rotb_extreme_plus_group_number == ""):
                    self.print_and_save(f"{self.printtime()} [INFO] Group Number for Rise of the Beasts Extreme+ will reuse the one for Farming Mode.")
                    self._rotb_extreme_plus_group_number = self._group_number
                else:
                    self._rotb_extreme_plus_group_number = int(self._rotb_extreme_plus_group_number)
                    
                if(self._rotb_extreme_plus_party_number == ""):
                    self.print_and_save(f"{self.printtime()} [INFO] Party Number for Rise of the Beasts Extreme+ will reuse the one for Farming Mode.")
                    self._rotb_extreme_plus_party_number = self._party_number
                else:
                    self._rotb_extreme_plus_party_number = int(self._rotb_extreme_plus_party_number)
                    
                self.print_and_save(f"{self.printtime()} [INFO] Settings initialized for Rise of the Beasts Extreme+...")
            elif(self._item_name == "Repeated Runs" and self._enable_unparalleled_foe):
                # Do the same for Dread Barrage Unparalleled Foes if enabled.
                self.print_and_save(f"\n{self.printtime()} [INFO] Initializing settings for Dread Barrage Unparalleled Foes...")
                
                if(self.unparalleled_foe_combat_script == ""):
                    self.print_and_save(f"{self.printtime()} [INFO] Combat Script for Dread Barrage Unparalleled Foes will reuse the one for Farming Mode.")
                    self.unparalleled_foe_combat_script = self._combat_script
                    
                if(len(self._unparalleled_foe_summon_element_list) == 0):
                    self.print_and_save(f"{self.printtime()} [INFO] Summon Elements for Dread Barrage Unparalleled Foes will reuse the ones for Farming Mode.")
                    self._unparalleled_foe_summon_element_list = self._summon_element_list
                    
                if(len(self._unparalleled_foe_summon_list) == 0):
                    self.print_and_save(f"{self.printtime()} [INFO] Summons for Dread Barrage Unparalleled Foes will reuse the ones for Farming Mode.")
                    self._unparalleled_foe_summon_list = self._summon_list
                    
                if(self._unparalleled_foe_group_number == ""):
                    self.print_and_save(f"{self.printtime()} [INFO] Group Number for Dread Barrage Unparalleled Foes will reuse the one for Farming Mode.")
                    self._unparalleled_foe_group_number = self._group_number
                else:
                    unparalleled_foe_group_number = int(unparalleled_foe_group_number)
                    
                if(self._unparalleled_foe_party_number == ""):
                    self.print_and_save(f"{self.printtime()} [INFO] Party Number for Dread Barrage Unparalleled Foes will reuse the one for Farming Mode.")
                    self._unparalleled_foe_party_number = self._party_number
                else:
                    self._unparalleled_foe_party_number = int(self._unparalleled_foe_party_number)
                    
                self.print_and_save(f"{self.printtime()} [INFO] Settings initialized for Dread Barrage Unparalleled Foes...")
                
            # Main workflow for Farming Mode.
            if((farming_mode.lower() != "raid" and self._map_selection.select_map(farming_mode, location_name, item_name, mission_name, difficulty)) or 
               (farming_mode.lower() == "raid" and self._map_selection.join_raid(item_name, mission_name))):
                while(self._item_amount_farmed < self._item_amount_to_farm):
                    # Loop until the specified Summon has been selected successfully.
                    self.print_and_save(f"\n{self.printtime()} [INFO] Selecting Summon before starting mission for Farming Mode...")
                    while(summon_check == False and farming_mode.lower() != "coop"): 
                        # Select the Summon element and the Summon itself.
                        summon_check = self._select_summon(summon_list, summon_element_list)
                        
                        # If the Summons were reset, select the mission again.
                        if(summon_check == False):
                            if(farming_mode.lower() != "raid"):
                                self.print_and_save(f"\n{self.printtime()} [INFO] Selecting mission again after resetting Summons...")
                                self._map_selection.select_map(farming_mode, location_name, item_name, mission_name, difficulty)
                            else:
                                self.print_and_save(f"\n{self.printtime()} [INFO] Joining raids again after resetting Summons...")
                                self._map_selection.join_raid(item_name, mission_name)
                    
                    # Select the specified Party and then start the mission.
                    if(farming_mode.lower() != "coop"):
                        start_check = self._find_party_and_start_mission(group_number, party_number)
                    else:
                        # Only select the Party for this Coop mission once. After that, subsequent runs always has that Party selected.
                        if(self._coop_first_run):
                            start_check = self._find_party_and_start_mission(group_number, party_number)
                            self._coop_first_run = False
                            self.find_and_click_button("coop_start")
                            
                        self.print_and_save(f"{self.printtime()} [INFO] Starting Coop mission.")
                        
                    # After Party has been successfully selected, start Combat Mode.
                    if(start_check and farming_mode.lower() != "raid"):
                        # Check for the "Items Picked Up" popup that appears after starting a Quest mission.
                        self.wait(2)
                        if(farming_mode.lower() == "quest" and self.image_tools.confirm_location("items_picked_up", tries=5)):
                            self.find_and_click_button("ok")
                        
                        # Start Combat Mode for this mission.
                        if(self.start_combat_mode(self._combat_script)):
                            # If Combat Mode finished successfully without retreating or exiting prematurely, start loot detection.
                            self.collect_loot()
                            
                            if(self._item_amount_farmed < self._item_amount_to_farm):
                                # Click the Play Again button or the Room button if its Coop.
                                if(farming_mode.lower() != "coop"):
                                    if(not self.find_and_click_button("play_again")):
                                        # Clear away any Pending Battles.
                                        self._map_selection.check_for_pending(farming_mode)
                                        
                                        # Start the mission again.
                                        self._map_selection.select_map(farming_mode, location_name, item_name, mission_name, difficulty)
                                else:
                                    self.find_and_click_button("coop_room")
                                    self.wait(1)
                                    
                                    # Check for the "Daily Missions" popup for Coop.
                                    if(self.image_tools.confirm_location("coop_daily_missions", tries=1)):
                                        self.find_and_click_button("close")
                                    
                                    # Now click the "Start" button.
                                    self.find_and_click_button("coop_start")
                                    
                                # Check for "Missions" popup for Dread Barrage.
                                if(farming_mode.lower() == "dread barrage" and self.image_tools.confirm_location("dread_barrage_missions", tries=1)):
                                    self.print_and_save(f"{self.printtime()} [INFO] Found \"Missions\" popup for Dread Barrage. Closing it now...")
                                    self.find_and_click_button("close")
                                
                                # If the user wants to fight Unparalleled Foes during Dread Barrage, then start it.
                                if(farming_mode.lower() == "dread barrage" and self.image_tools.confirm_location("dread_barrage_unparalleled_foe", tries=1)):
                                    # Find the locations of the "AP 0" text underneath each Unparalleled Foe.
                                    ap_0_locations = self.image_tools.find_all("ap_0")
                                    
                                    if(self._enable_unparalleled_foe_level_95 and not self._enable_unparalleled_foe_level_175):
                                        # Start the Level 95 Unparalleled Foe.
                                        self.print_and_save(f"\n{self.printtime()} [INFO] Starting Level 95 Unparalleled Foe...")
                                        self.mouse_tools.move_and_click_point(ap_0_locations[0][0], ap_0_locations[0][1])
                                    elif(self._enable_unparalleled_foe_level_175 and not self._enable_unparalleled_foe_level_95):
                                        # Start the Level 175 Unparalleled Foe.
                                        self.print_and_save(f"\n{self.printtime()} [INFO] Starting Level 175 Unparalleled Foe...")
                                        self.mouse_tools.move_and_click_point(ap_0_locations[1][0], ap_0_locations[1][1])
                                    elif(not self._enable_unparalleled_foe_level_95 and not self._enable_unparalleled_foe_level_175):
                                        # Close the popup.
                                        self.print_and_save(f"\n{self.printtime()} [INFO] Closing Dread Barrage Unparalleled Foes popup...")
                                        self.find_and_click_button("close")
                                    else:
                                        # Every other case will default to the Level 95 Unparalleled Foe.
                                        self.print_and_save(f"\n{self.printtime()} [INFO] Defaulting to Level 95 Unparalleled Foe. Starting it now...")
                                        self.mouse_tools.move_and_click_point(ap_0_locations[0][0], ap_0_locations[0][1])
                                
                                # Check for "Trophy Achieved" popup.
                                if(self.image_tools.confirm_location("trophy_achieved", tries=1)):
                                    self.print_and_save(f"{self.printtime()} [INFO] Detected \"Trophy Achieved\" popup. Closing it now...")
                                    self.find_and_click_button("close")
                                
                                # Check for any Skyscope popups.
                                if(self.enable_skyscope and self.image_tools.confirm_location("skyscope", tries=1)):
                                    self.find_and_click_button("close")
                                
                                # Check for "Daily Missions" popup for Rise of the Beasts.
                                if(farming_mode.lower() == "rise of the beasts" and self.image_tools.confirm_location("event_daily_missions", tries=1)):
                                    self.find_and_click_button("close")
                                
                                # Check for "Friend Request" popup.
                                self.check_for_friend_request()
                                
                                # Check for "Proud Solo Quest" popup for Rise of the Beasts.
                                if(farming_mode.lower() == "rise of the beasts" and self.image_tools.confirm_location("proud_solo_quest", tries=1)):
                                    self.find_and_click_button("close")
                                
                                # Check for Dimensional Halo and Event Nightmare.
                                if(self.farming_mode.lower() == "special" and self._mission_name == "VH Angel Halo" and (self._item_name == "EXP" or self._item_name == "Angel Halo Weapons")):
                                    if(self._check_for_dimensional_halo()):
                                        # Make sure the bot goes back to the Home screen when completing a Dimensional Halo so that the "Play Again" functionality comes back.
                                        self._map_selection.select_map(farming_mode, location_name, item_name, mission_name, difficulty)
                                elif((self.farming_mode.lower() == "event" or self.farming_mode.lower() == "event (token drawboxes)")):
                                    if(self._check_for_event_nightmare()):
                                        # Make sure the bot goes back to the Home screen when completing a Event Nightmare so that the "Play Again" functionality comes back.
                                        self._map_selection.select_map(farming_mode, location_name, item_name, mission_name, difficulty)
                                
                                # Check for available AP and then reset the Summon check flag.
                                self.check_for_ap(use_full_elixir=self.use_full_elixir)
                                summon_check = False
                                
                                # If the bot tried to repeat a Extreme/Impossible difficulty Event Raid and it lacked the treasures to host it, go back to select_map().
                                if(self.farming_mode.lower() == "event (token drawboxes)" and self.image_tools.confirm_location("not_enough_treasure")):
                                    self.find_and_click_button("ok")
                                    self._map_selection.select_map(farming_mode, location_name, item_name, mission_name, difficulty)
                        else:
                            # Start the mission again if the Party wiped or exited prematurely during Combat Mode.
                            self.print_and_save(f"\n{self.printtime()} [INFO] Selecting mission again due to retreating...")
                            self._map_selection.select_map(farming_mode, location_name, item_name, mission_name, difficulty)
                    
                    elif(start_check and farming_mode.lower() == "raid"): 
                        # Cover the occasional case where joining the raid after selecting the Summon and Party led to the Quest Results screen with no loot to collect.
                        if(self.image_tools.confirm_location("no_loot")):
                            self.print_and_save(f"\n{self.printtime()} [INFO] Seems that the raid just ended. Moving back to the Home screen and joining another raid...")
                            self.go_back_home(confirm_location_check=True)
                            summon_check = False
                        else:
                            # Start Combat Mode for this Raid.
                            if(self.start_combat_mode(self._combat_script)):
                                # If Combat Mode finished successfully without retreating or exiting prematurely, start loot detection.
                                self.collect_loot()
                                
                                if(self._item_amount_farmed < self._item_amount_to_farm):
                                    # Clear away any Pending Battles.
                                    self._map_selection.check_for_pending(farming_mode)
                                    
                                    # Join a new raid.
                                    self._map_selection.join_raid(item_name, mission_name)
                                    summon_check = False
                            else:
                                # Join a new raid.
                                self._map_selection.join_raid(item_name, mission_name)
                                summon_check = False
                    elif(not start_check and farming_mode.lower() == "raid"):
                        # If the bot reached here, it means that the Raid ended before the bot could start the mission after selecting the Summon and Party.
                        self.print_and_save(f"{self.printtime()} [INFO] Seems that the raid ended before the bot was able to join. Now looking for another raid to join...")
                        self._map_selection.join_raid(item_name, mission_name)
                        summon_check = False
            else:
                raise Exception("Confirming the location of the Summon Selection screen after selecting the mission returned False.")
        except Exception:
            self.print_and_save(f"\n{self.printtime()} [ERROR] Bot encountered exception in Farming Mode: \n{traceback.format_exc()}")
            
        self.print_and_save("\n################################################################################")
        self.print_and_save("################################################################################")
        self.print_and_save(f"{self.printtime()} [FARM] Ending Farming Mode.")
        self.print_and_save("################################################################################")
        self.print_and_save("################################################################################\n")
        
        self._isBotRunning.value = 1
        return None
