import datetime
import multiprocessing
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
    Main driver for bot activity and navigation for the web game, Granblue Fantasy.

    Attributes
    ----------
    queue (multiprocessing.Queue): Queue to keep track of logging messages to share between backend and frontend.

    isBotRunning (int): Flag in shared memory that signals the frontend that the bot has finished/exited.
    
    combat_script (str, optional): The combat script to use for Combat Mode. Defaults to empty string.

    debug_mode (bool, optional): Optional flag to print debug messages related to this class. Defaults to False.

    """

    def __init__(self, queue: multiprocessing.Queue, isBotRunning: int, combat_script: str = "", debug_mode: bool = False):
        super().__init__()
        
        self.config = ConfigParser()
        self.config.read("config.ini")

        # Grab the Twitter API keys and tokens from config.ini. The list order is: [consumer key, consumer secret key, access token, access secret token].
        keys_tokens = [self.config.get("twitter", "api_key"), self.config.get("twitter", "api_key_secret"), self.config.get("twitter", "access_token"), self.config.get("twitter", "access_token_secret")]
        custom_mouse_speed = float(self.config.get("configuration", "mouse_speed"))
        
        # Grab the timings between various actions during Combat Mode from config.ini as well.
        self.idle_seconds_after_skill = float(self.config.get("configuration", "idle_seconds_after_skill"))
        self.idle_seconds_after_summon = float(self.config.get("configuration", "idle_seconds_after_summon"))
        
        # Determine whether or not the user wants to refill using Full Elixir/Soul Balm.
        self.quest_refill = self.config.getboolean("refill", "refill_using_full_elixir")
        self.raid_refill = self.config.getboolean("refill", "refill_using_soul_balms")

        # Start a timer signaling bot start in order to keep track of elapsed time and create a Queue to share logging messages between backend and frontend.
        self.starting_time = timer()
        self.queue = queue
        
        # Set a debug flag to determine whether or not to print debugging messages.
        self.debug_mode = debug_mode

        # Initialize the objects of helper classes.
        self.map_selection = MapSelection(self)
        self.room_finder = TwitterRoomFinder(self, keys_tokens[0], keys_tokens[1], keys_tokens[2], keys_tokens[3], debug_mode=self.debug_mode)
        self.image_tools = ImageUtils(game=self, starting_time=self.starting_time, debug_mode=self.debug_mode)
        self.mouse_tools = MouseUtils(game=self, starting_time=self.starting_time, mouse_speed=custom_mouse_speed, debug_mode=self.debug_mode)
        
        # Save the locations of the "Home", "Attack", and "Back" buttons for use in other classes.
        self.home_button_location = None
        self.attack_button_location = None
        self.back_button_location = None
        
        # Keep track of the following for Combat Mode.
        self.combat_script = combat_script
        self.isBotRunning = isBotRunning
        self.retreat_check = False
        self.suppress_error = True
        
        # Keep track of the following for Farming Mode.
        self.summon_element_name = ""
        self.summon_name = ""
        self.group_number = 0
        self.party_number = 0
        self.map_mode = ""
        self.item_name = ""
        self.item_amount_to_farm = 0
        self.item_amount_farmed = 0
        self.amount_of_runs_finished = 0
        self.mission_name = ""
        
        # Keep track of the following for Events.
        self.enable_event_nightmare = self.config.getboolean("event", "enable_event_nightmare")
        self.event_nightmare_combat_script = self.config.get("event", "event_nightmare_combat_script")
        self.event_nightmare_summon_name = self.config.get("event", "event_nightmare_summon_name")
        self.event_nightmare_summon_element_name = self.config.get("event", "event_nightmare_summon_element_name")
        self.event_nightmare_group_number = self.config.get("event", "event_nightmare_group_number")
        self.event_nightmare_party_number = self.config.get("event", "event_nightmare_party_number")
        
        # Keep track of the following for Dimensional Halo.
        self.enable_dimensional_halo = self.config.getboolean("dimensional_halo", "enable_dimensional_halo")
        self.dimensional_halo_combat_script = self.config.get("dimensional_halo", "dimensional_halo_combat_script")
        self.dimensional_halo_summon_name = self.config.get("dimensional_halo", "dimensional_halo_summon_name")
        self.dimensional_halo_summon_element_name = self.config.get("dimensional_halo", "dimensional_halo_summon_element_name")
        self.dimensional_halo_group_number = self.config.get("dimensional_halo", "dimensional_halo_group_number")
        self.dimensional_halo_party_number = self.config.get("dimensional_halo", "dimensional_halo_party_number")
        self.dimensional_halo_amount = 0
        
        # Keep track of the following for Dread Barrage Unparalleled Foes.
        self.enable_unparalleled_foe = self.config.getboolean("dread_barrage", "enable_unparalleled_foe")
        self.enable_unparalleled_foe_level_95 = self.config.getboolean("dread_barrage", "enable_unparalleled_foe_level_95")
        self.enable_unparalleled_foe_level_175 = self.config.getboolean("dread_barrage", "enable_unparalleled_foe_level_175")
        self.unparalleled_foe_combat_script = self.config.get("dread_barrage", "unparalleled_foe_combat_script")
        self.unparalleled_foe_summon_name = self.config.get("dread_barrage", "unparalleled_foe_summon_name")
        self.unparalleled_foe_summon_element_name = self.config.get("dread_barrage", "unparalleled_foe_summon_element_name")
        self.unparalleled_foe_group_number = self.config.get("dread_barrage", "unparalleled_foe_group_number")
        self.unparalleled_foe_party_number = self.config.get("dread_barrage", "unparalleled_foe_party_number")

        # The amount of time to pause after each call to pyautogui. This applies to calls inside mouse_utils and image_utils.
        pyautogui.PAUSE = 0.25

        # Calibrate the dimensions of the game window on bot launch.
        self.go_back_home(confirm_location_check=True, display_info_check=True)

    def printtime(self):
        """Formats the time since the bot started into a readable, printable HH:MM:SS format using timedelta.

        Returns:
            str: A formatted string that displays the elapsed time since the bot started.
        """
        return str(datetime.timedelta(seconds=(timer() - self.starting_time))).split('.')[0]
    
    def print_and_save(self, message: str):
        """Saves the logging message into the Queue to be shared with the frontend and then prints it to console.

        Args:
            message (str): A logging message containing various information.
        """
        self.queue.put(message)
        print(message)

    def calibrate_game_window(self, display_info_check: bool = False):
        """Recalibrate the dimensions of the game window for fast and accurate image matching.

        Args:
            display_info_check (bool, optional): Display display size of screen and game window size. Defaults to False.

        Returns:
            None
        """
        if(self.debug_mode):
            self.print_and_save(f"\n{self.printtime()} [DEBUG] Recalibrating the dimensions of the game window...")

        try:
            self.home_button_location = self.image_tools.find_button("home")
            
            # Set the dimensions of the game window and save it in ImageUtils so that future operations do not go out of bounds.
            home_news_button = self.image_tools.find_button("home_news")
            home_menu_button = self.image_tools.find_button("home_menu")
            self.image_tools.window_left = home_news_button[0] - 35  # The x-coordinate of the left edge.
            self.image_tools.window_top = home_menu_button[1] - 24  # The y-coordinate of the top edge.
            self.image_tools.window_width = self.image_tools.window_left + 410  # The width of the region.
            self.image_tools.window_height = (self.home_button_location[1] + 24) - self.image_tools.window_top  # The height of the region.
        except Exception:
            self.print_and_save(f"\n{self.printtime()} [ERROR] Bot encountered exception while calibrating game window dimensions: \n{traceback.format_exc()}")
            self.isBotRunning.value = 1

        if(self.debug_mode):
            self.print_and_save(f"{self.printtime()} [SUCCESS] Dimensions of the game window has been successfully recalibrated.")

        if(display_info_check):
            self.print_and_save("\n********************************************************************************")
            self.print_and_save(f"{self.printtime()} [INFO] Screen size: {pyautogui.size()}")
            self.print_and_save(f"{self.printtime()} [INFO] Game window size: Region({self.image_tools.window_left}, {self.image_tools.window_top}, {self.image_tools.window_width}, {self.image_tools.window_height})")
            self.print_and_save("********************************************************************************")

        return None

    def go_back_home(self, confirm_location_check: bool = False, display_info_check: bool = False):
        """Go back to the Home Screen to reset the bot's position. Also able to recalibrate the region dimensions of the game window if display_info_check is True.

        Args:
            confirm_location_check (bool, optional): Check to see if the location is correct. Defaults to False.
            display_info_check (bool, optional): Recalibrate and display size of screen and game window size. Defaults to False.

        Returns:
            None
        """   
        if(not self.image_tools.confirm_location("home")):
            self.print_and_save(f"\n{self.printtime()} [INFO] Moving back to the Home Screen...")
            # Go to the Home Screen.
            if(self.home_button_location != None):
                self.mouse_tools.move_and_click_point(self.home_button_location[0], self.home_button_location[1])
            else:
                self.find_and_click_button("home")
        else:
            self.print_and_save(f"\n{self.printtime()} [INFO] Bot is at the Home Screen.")
        
        # Recalibrate the dimensions of the window if flag is True.
        if (display_info_check):
            self.calibrate_game_window(display_info_check=True)
            
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
            button_name (str): Name of the button image file in the images/buttons/ folder.
            tries (int): Number of tries to attempt to find the specified button image. Defaults to 2.
            suppress_error (bool): Suppresses template matching error depending on boolean. Defaults to False.

        Returns:
            (bool): Return True if the button was found and clicked. Otherwise, return False.
        """
        if(self.debug_mode):
            self.print_and_save(f"{self.printtime()} [DEBUG] Attempting to find and click the button: \"{button_name}\".")
        
        # If the bot is trying to find the Quest button and failed, chances are that the button is now styled red.
        if(button_name == "quest"):
            temp_location = self.image_tools.find_button("quest", tries=tries, suppress_error=suppress_error)
            if(temp_location == None):
                temp_location = self.image_tools.find_button("quest2", tries=tries, suppress_error=suppress_error)
            if(temp_location == None):
                # If the blue or red Quest buttons was not detected, user must be in Strike Time with the red Quest button.
                temp_location = self.image_tools.find_button("quest3", tries=tries, suppress_error=suppress_error)
        elif(button_name == "raid"):
            temp_location = self.image_tools.find_button("raid", tries=tries, suppress_error=suppress_error)
            if(temp_location == None):
                temp_location = self.image_tools.find_button("raid2", tries=tries, suppress_error=suppress_error)
        else:
            temp_location = self.image_tools.find_button(button_name, tries=tries, suppress_error=suppress_error)
        
        if(temp_location != None):    
            self.mouse_tools.move_and_click_point(temp_location[0], temp_location[1])
            return True
        else:
            return False
        
    def party_wipe_check(self):
        """Check to see if the party has wiped during Combat Mode. Update the retreat check flag if so.

        Returns:
            None
        """
        try:
            # Check to see if party has wiped.
            party_wipe_indicator = self.image_tools.find_button("party_wipe_indicator", tries=1, suppress_error=self.suppress_error)
            if(party_wipe_indicator != None):
                self.print_and_save(f"\n{self.printtime()} [COMBAT] Party has unfortunately wiped during Combat Mode. Retreating now...")
                self.wait(3)
                self.mouse_tools.move_and_click_point(party_wipe_indicator[0], party_wipe_indicator[1])
                
                self.image_tools.confirm_location("continue")
                self.find_and_click_button("cancel")
                    
                if(self.map_mode.lower() != "raid" and self.image_tools.confirm_location("retreat")):
                    # For retreating from Quests.
                    self.find_and_click_button("retreat_confirmation")
                    
                    self.retreat_check = True
                elif(self.image_tools.confirm_location("raid_continue")):
                    # For backing out of Raids without retreating.
                    self.find_and_click_button("cancel")
                    if(self.image_tools.confirm_location("raid_retreat")):
                        self.find_and_click_button("raid_retreat_home")
                    
                    self.retreat_check = True

            return None
        except Exception:
            self.print_and_save(f"\n{self.printtime()} [ERROR] Bot encountered exception while checking if party wiped: \n{traceback.format_exc()}")
            self.isBotRunning.value = 1
            
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
        except Exception:
            self.print_and_save(f"\n{self.printtime()} [ERROR] Bot encountered exception while checking for CAPTCHA: \n{traceback.format_exc()}")
            self.image_tools.generate_alert_for_captcha()
            self.isBotRunning.value = 1
            self.wait(1)
        return None

    def find_summon_element(self, summon_element_name: str, tries: int = 3):
        """Select the specified element tab for summons.

        Args:
            summon_element_name (str): Name of the summon element image file in the images/buttons/ folder.
            tries (int, optional): Number of tries before failing. Defaults to 3.

        Returns:
            (bool): True if successfully found and clicked the summon element tab. Otherwise, return False.
        """
        summon_element_location = None
        
        self.wait(1)
        while(summon_element_location == None):
            summon_element_location = self.image_tools.find_button(f"summon_{summon_element_name.lower()}")

            if(summon_element_location == None):
                tries -= 1
                
                if(tries == 0):
                    self.print_and_save(f"{self.printtime()} [ERROR] Failed to find {summon_element_name.upper()} Element tab.")
                    return False

        self.print_and_save(f"\n{self.printtime()} [SUCCESS] Found {summon_element_name.upper()} Element tab.")
        self.mouse_tools.move_and_click_point(summon_element_location[0], summon_element_location[1])
        return True

    def find_summon(self, summon_name: str):
        """Find the specified Summon on the Summon Selection Screen. Make sure to call this after the find_summon_element() method in order to have the correct Summon Element tab already selected.

        Args:
            summon_name (str): Exact name of the Summon image's file name in images/summons folder.

        Returns:
            (bool): True if the Summon was found and clicked. Otherwise, return False.
        """
        summon_name = summon_name.lower().replace(" ", "_")
        summon_location = self.image_tools.find_summon(summon_name, self.home_button_location[0], self.home_button_location[1])
        if (summon_location != None):
            self.mouse_tools.move_and_click_point(summon_location[0], summon_location[1])
            self.print_and_save(f"{self.printtime()} [INFO] Found {summon_name.upper()} Summon.")
            
            # Check for CAPTCHA here. If detected, stop the bot and alert the user.
            self.check_for_captcha()
            
            return True
        else:
            # If a Summon is not found, start a Trial Battle to refresh Summons.
            self.reset_summons()
            return False

    def reset_summons(self):
        """Reset the Summons available by starting and then retreating from a Old Lignoid Trial Battle.

        Returns:
            None
        """
        self.print_and_save(f"\n{self.printtime()} [INFO] Refreshing summons...")
        self.go_back_home(confirm_location_check=True)
        self.mouse_tools.scroll_screen_from_home_button(-600)

        try:
            list_of_steps_in_order = ["gameplay_extras", "trial_battles",
                                    "trial_battles_old_lignoid", "play_round_button",
                                    "choose_a_summon", "party_selection_ok", "close",
                                    "menu", "retreat", "retreat_confirmation", "next"]

            # Go through each step in order from left to right from the list of steps.
            while (len(list_of_steps_in_order) > 0):
                step = list_of_steps_in_order.pop(0)
                if(step == "trial_battles_old_lignoid"):
                    self.image_tools.confirm_location("trial_battles")
                elif(step == "close"):
                    self.wait(2)
                    self.image_tools.confirm_location("trial_battles_description")
                
                image_location = self.image_tools.find_button(step)
                if(step == "choose_a_summon"):
                    self.mouse_tools.move_and_click_point(image_location[0], image_location[1] + 187)
                else:
                    self.mouse_tools.move_and_click_point(image_location[0], image_location[1])
            
            if(self.image_tools.confirm_location("trial_battles")):
                self.print_and_save(f"{self.printtime()} [INFO] Summons have now been refreshed.")
            return None
        except Exception:
            self.print_and_save(f"\n{self.printtime()} [ERROR] Bot encountered exception while resetting summons: \n{traceback.format_exc()}")
            self.isBotRunning.value = 1

    def find_party_and_start_mission(self, group_number: int, party_number: int, tries: int = 3):
        """Select the specified group and party. It will then start the mission.

        Args:
            group_number (int): The group that the specified party in in.
            party_number (int): The specified party to start the mission with.
            tries (int, optional): Number of tries to select a Set before failing. Defaults to 3.

        Returns:
            (bool): Returns False if it detects the "Raid is full/Raid is already done" dialog. Otherwise, return True.
        """
        set_location = None
        
        # Find the Group first. If the selected group number is less than 8, it is in Set A. Otherwise, it is in Set B. If failed,
        # alternate searching for Set A / Set B until found or tries are depleted.
        try:
            if(group_number < 8):
                while (set_location == None):
                    set_location = self.image_tools.find_button("party_set_a")           
                    if (set_location == None):
                        tries -= 1
                        if (tries <= 0):
                            raise NotFoundException("Could not find Set A.")

                        # See if the user had Set B active instead of Set A if matching failed.
                        set_location = self.image_tools.find_button("party_set_b")
            else:
                while (set_location == None):
                    set_location = self.image_tools.find_button("party_set_b")
                    if (set_location == None):
                        tries -= 1
                        if (tries <= 0):
                            raise NotFoundException("Could not find Set B.")

                        # See if the user had Set A active instead of Set B if matching failed.
                        set_location = self.image_tools.find_button("party_set_a")
        except Exception:
            self.print_and_save(f"\n{self.printtime()} [ERROR] Bot encountered exception while selecting A or B Set: \n{traceback.format_exc()}")
            self.isBotRunning.value = 1

        if(self.debug_mode):
            self.print_and_save(f"\n{self.printtime()} [DEBUG] Successfully selected the correct Set. Now selecting Group {group_number}...")

        # Center the mouse on the Set A / Set B Button and then click the correct Group Number Tab.
        x = None
        y = set_location[1] + 50
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

        self.mouse_tools.move_and_click_point(x, y)

        # Now select the correct Party.
        if(self.debug_mode):
            self.print_and_save(f"{self.printtime()} [DEBUG] Successfully selected Group {group_number}. Now selecting Party {party_number}...")

        y = set_location[1] + 325
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

        self.mouse_tools.move_and_click_point(x, y)

        if(self.debug_mode):
            self.print_and_save(f"{self.printtime()} [SUCCESS] Successfully selected Party {party_number}. Now starting the mission.")

        # Find and click the "OK" Button to start the mission.
        self.find_and_click_button("ok")
        
        # If a dialog window pops up and says "This raid battle has already ended. The Home screen will now appear.", return False.
        if(self.map_mode.lower() == "raid" and self.image_tools.confirm_location("raid_just_ended_home_redirect", tries=3)):
            self.print_and_save(f"{self.printtime()} [WARNING] Raid unfortunately just ended.")
            self.find_and_click_button("ok")
            return False
        
        return True

    def find_charge_attacks(self):
        """Find total number of characters ready to Charge Attack.

        Returns:
            number_of_charge_attacks (int): Total number of image matches found for charge attacks.
        """
        number_of_charge_attacks = 0
        list_of_charge_attacks = self.image_tools.find_all("full_charge", custom_region=(self.attack_button_location[0] - 356, self.attack_button_location[1] + 67, 
                                                                                         self.attack_button_location[0] - 40, self.attack_button_location[1] + 214), hide_info=True)

        number_of_charge_attacks = len(list_of_charge_attacks)
        return number_of_charge_attacks

    def find_dialog_in_combat(self):
        """Check if there are dialog boxes from either Lyria or Vyrn and click them away.

        Returns:
            None
        """
        dialog_location = self.image_tools.find_dialog(self.attack_button_location[0], self.attack_button_location[1], tries=1)
        if (dialog_location != None):
            self.mouse_tools.move_and_click_point(dialog_location[0] + 180, dialog_location[1] - 51)

        return None
        
    def check_for_ap(self, use_full_elixirs: bool = False):
        """Check if the user encountered the 'Not Enough AP' popup and it will refill using either Half or Full Elixir.

        Args:
            use_full_elixirs (bool, optional): Will use Full Elixir instead of Half Elixir based on this. Defaults to False.

        Returns:
            None
        """
        # Loop until the user gets to the Summon Selection Screen.
        while((self.map_mode.lower() != "coop" and not self.image_tools.confirm_location("select_summon", tries=2)) or 
              (self.map_mode.lower() == "coop" and not self.image_tools.confirm_location("coop_without_support_summon", tries=2))):
            if(self.image_tools.confirm_location("not_enough_ap", tries=2)):
                # If the bot detects that the user has run out of AP, it will refill using either Half Elixir or Full.
                if(use_full_elixirs == False):
                    self.print_and_save(f"\n{self.printtime()} [INFO] AP ran out! Using Half Elixir...")
                    half_ap_location = self.image_tools.find_button("refill_half_ap")
                    self.mouse_tools.move_and_click_point(half_ap_location[0], half_ap_location[1] + 175)
                else:
                    self.print_and_save(f"\n{self.printtime()} [INFO] AP ran out! Using Full Elixir...")
                    full_ap_location = self.image_tools.find_button("refill_full_ap")
                    self.mouse_tools.move_and_click_point(full_ap_location[0], full_ap_location[1] + 175)
                
                # Press the OK button to move to the Summon Selection Screen.
                self.wait(1)
                self.find_and_click_button("ok")
                return None
            else:
                self.wait(1)
            
        self.print_and_save(f"{self.printtime()} [INFO] AP is available. Continuing...")
        return None

    def check_for_ep(self, use_soul_balm: bool = False):
        """Check if the user encountered the 'Not Enough EP' popup and it will refill using either Soul Berry or Soul Balm.

        Args:
            use_soul_balm (bool, optional): Will use Soul Balm instead of Soul Berry based on this. Defaults to False.

        Returns:
            None
        """
        self.wait(3)
        if(self.image_tools.confirm_location("not_enough_ep", tries=2)):
            # If the bot detects that the user has run out of EP, it will refill using either Soul Berry or Soul Balm.
            if(use_soul_balm == False):
                self.print_and_save(f"\n{self.printtime()} [INFO] EP ran out! Using Soul Berries...")
                half_ep_location = self.image_tools.find_button("refill_soul_berry")
                self.mouse_tools.move_and_click_point(half_ep_location[0], half_ep_location[1] + 175)
            else:
                self.print_and_save(f"\n{self.printtime()} [INFO] EP ran out! Using Soul Balm...")
                full_ep_location = self.image_tools.find_button("refill_soul_balm")
                self.mouse_tools.move_and_click_point(full_ep_location[0], full_ep_location[1] + 175)
            
            # Press the OK button to move to the Summon Selection Screen.
            self.wait(1)
            self.find_and_click_button("ok")
        else:
            self.print_and_save(f"{self.printtime()} [INFO] EP is available. Continuing...")
        
        return None

    def select_character(self, character_number: int):
        """Selects the portrait of the character specified on the screen.

        Args:
            character_number (int): The character that needs to be selected from the Combat Screen.

        Returns:
            None
        """
        # Click the portrait of the specified character.
        x = None
        y = self.attack_button_location[1] + 123
        if(character_number == 1):
            x = self.attack_button_location[0] - 317
        elif(character_number == 2):
            x = self.attack_button_location[0] - 240
        elif(character_number == 3):
            x = self.attack_button_location[0] - 158
        elif(character_number == 4):
            x = self.attack_button_location[0] - 76

        # Double-clicking the character portrait to avoid any non-invasive popups from other Raid participants.
        self.mouse_tools.move_and_click_point(x, y, mouse_clicks=2)
        return None

    def use_character_skill(self, character_selected: int, skill: int):
        """Activate the skill specified for the already selected character.

        Args:
            character_selected (int): The character whose skill needs to be used.
            skill (int): The skill that needs to be used.

        Returns:
            None
        """
        # Matches the string occurence to which skill the bot needs to select.
        x = None
        y = self.attack_button_location[1] + 171
        if("useskill(1)" in skill.lower()):
            self.print_and_save(f"{self.printtime()} [COMBAT] Character {character_selected} uses Skill 1.")
            x = self.attack_button_location[0] - 213
        elif("useskill(2)" in skill.lower()):
            self.print_and_save(f"{self.printtime()} [COMBAT] Character {character_selected} uses Skill 2.")
            x = self.attack_button_location[0] - 132
        elif("useskill(3)" in skill.lower()):
            self.print_and_save(f"{self.printtime()} [COMBAT] Character {character_selected} uses Skill 3.")
            x = self.attack_button_location[0] - 51
        elif("useskill(4)" in skill.lower()):
            self.print_and_save(f"{self.printtime()} [COMBAT] Character {character_selected} uses Skill 4.")
            x = self.attack_button_location[0] + 39

        self.mouse_tools.move_and_click_point(x, y)

        return None
    
    def collect_loot(self):
        """Collect the loot from the Results screen while clicking away any dialog popups. Primarily for raids.

        Returns:
            None
        """
        self.print_and_save(f"\n{self.printtime()} [INFO] Detecting if any loot dropped...")
        
        # Click away the EXP Gained popup and any other popups until the bot reaches the Loot Collected Screen.
        if(self.image_tools.confirm_location("exp_gained") and not self.retreat_check):
            while(not self.image_tools.confirm_location("loot_collected", tries=1)):
                ok_button_location = self.image_tools.find_button("ok", tries=1, suppress_error=True)
                cancel_button_location = self.image_tools.find_button("cancel", tries=1, suppress_error=True)
                close_button_location = self.image_tools.find_button("close", tries=1, suppress_error=True)
                
                if(close_button_location != None):
                    self.mouse_tools.move_and_click_point(close_button_location[0], close_button_location[1])
                
                if(cancel_button_location != None):
                    self.mouse_tools.move_and_click_point(cancel_button_location[0], cancel_button_location[1])

                if(ok_button_location != None):
                    self.mouse_tools.move_and_click_point(ok_button_location[0], ok_button_location[1])
                    
                # Double click the screen to hopefully clear away any EMP Mastery level up popups.
                self.mouse_tools.move_and_click_point(self.home_button_location[0], self.home_button_location[1] - 200, mouse_clicks=2)

            # Now that the bot is at the Loot Collected Screen, detect items.
            if(self.item_name != "EXP" and self.item_name != "Repeated Runs"):
                temp_amount = self.image_tools.find_farmed_items([self.item_name])[0]
            else:
                temp_amount = 1
            
            self.item_amount_farmed += temp_amount
            
        self.amount_of_runs_finished += 1
        
        if(self.item_name != "EXP" and self.item_name != "Repeated Runs"):
            self.print_and_save("\n\n********************************************************************************")
            self.print_and_save(f"{self.printtime()} [FARM] Mode: {self.map_mode}")
            self.print_and_save(f"{self.printtime()} [FARM] Mission: {self.mission_name}")
            self.print_and_save(f"{self.printtime()} [FARM] Summon: {self.summon_name}")
            self.print_and_save(f"{self.printtime()} [FARM] Amount of {self.item_name} gained this run: {temp_amount}")
            self.print_and_save(f"{self.printtime()} [FARM] Amount of {self.item_name} gained in total: {self.item_amount_farmed} / {self.item_amount_to_farm}")
            self.print_and_save(f"{self.printtime()} [FARM] Amount of runs completed: {self.amount_of_runs_finished}")
            self.print_and_save("********************************************************************************\n")
        else:
            self.print_and_save("\n\n********************************************************************************")
            self.print_and_save(f"{self.printtime()} [FARM] Mode: {self.map_mode}")
            self.print_and_save(f"{self.printtime()} [FARM] Mission: {self.mission_name}")
            self.print_and_save(f"{self.printtime()} [FARM] Summon: {self.summon_name}")
            self.print_and_save(f"{self.printtime()} [FARM] Amount of runs completed: {self.amount_of_runs_finished} / {self.item_amount_to_farm}")
            self.print_and_save("********************************************************************************\n")

        return None
    
    def check_for_friend_request(self):
        """Detect any Friend Request popups and click them away.

        Returns:
            None
        """
        if(self.image_tools.confirm_location("friend_request")):
            self.print_and_save(f"\n{self.printtime()} [INFO] Detected Friend Request. Closing it now...")
            self.find_and_click_button("cancel")
        
        return None
    
    def check_for_event_nightmare(self):
        """Checks for Event Nightmare and if it appears and the user enabled it in config.ini, start it.

        Returns:
            (bool): Return True if Event Nightmare was detected and successfully completed. Otherwise, return False.
        """
        if(self.enable_event_nightmare and self.image_tools.confirm_location("limited_time_quests", tries=1)):
            self.print_and_save(f"\n{self.printtime()} [INFO] Detected Event Nightmare. Starting it now...")
            
            self.print_and_save("\n\n********************************************************************************")
            self.print_and_save(f"{self.printtime()} [EVENT] Event Nightmare")
            self.print_and_save(f"{self.printtime()} [EVENT] Summon Element: {self.event_nightmare_summon_element_name}")
            self.print_and_save(f"{self.printtime()} [EVENT] Summon: {self.event_nightmare_summon_name}")
            self.print_and_save(f"{self.printtime()} [EVENT] Group Number: {self.event_nightmare_group_number}")
            self.print_and_save(f"{self.printtime()} [EVENT] Party Number: {self.event_nightmare_party_number}")
            self.print_and_save(f"{self.printtime()} [EVENT] Combat Script: {self.event_nightmare_combat_script}")
            self.print_and_save("********************************************************************************\n")
            
            self.find_and_click_button("play_next")
            
            self.wait(1)
            
            # Once the bot is at the Summon Selection screen, select your summon and party and start the mission.
            if(self.image_tools.confirm_location("select_summon")):
                self.find_summon_element(summon_element_name=self.event_nightmare_summon_element_name)
                self.find_summon(summon_name=self.event_nightmare_summon_name)
                start_check = self.find_party_and_start_mission(group_number=self.event_nightmare_group_number, party_number=self.event_nightmare_party_number)
                if(start_check and self.start_combat_mode(f"scripts/{self.event_nightmare_combat_script}.txt")):
                    self.collect_loot()
                    return True
                
        elif(not self.enable_event_nightmare and self.image_tools.confirm_location("limited_time_quests", tries=1)):
            self.print_and_save(f"\n{self.printtime()} [INFO] Event Nightmare detected but user opted to not run it. Moving on...")
            self.find_and_click_button("close")
        else:
            self.print_and_save(f"\n{self.printtime()} [INFO] No Event Nightmare detected. Moving on...")
        
        return False
    
    def check_for_dimensional_halo(self):
        """Checks for Dimensional Halo and if it appears and the user enabled it in config.ini, start it.

        Returns:
            (bool): Return True if Dimensional Halo was detected and successfully completed. Otherwise, return False.
        """
        if(self.enable_dimensional_halo and self.image_tools.confirm_location("limited_time_quests", tries=1)):
            self.print_and_save(f"\n{self.printtime()} [INFO] Detected Dimensional Halo. Starting it now...")
            self.dimensional_halo_amount += 1
            
            self.print_and_save("\n\n********************************************************************************")
            self.print_and_save(f"{self.printtime()} [D.HALO] Dimensional Halo")
            self.print_and_save(f"{self.printtime()} [D.HALO] Summon Element: {self.dimensional_halo_summon_element_name}")
            self.print_and_save(f"{self.printtime()} [D.HALO] Summon: {self.dimensional_halo_summon_name}")
            self.print_and_save(f"{self.printtime()} [D.HALO] Group Number: {self.dimensional_halo_group_number}")
            self.print_and_save(f"{self.printtime()} [D.HALO] Party Number: {self.dimensional_halo_party_number}")
            self.print_and_save(f"{self.printtime()} [D.HALO] Combat Script: {self.dimensional_halo_combat_script}")
            self.print_and_save(f"{self.printtime()} [D.HALO] Amount of Dimensional Halos encountered: {self.dimensional_halo_amount}")
            self.print_and_save("********************************************************************************\n")
            
            self.find_and_click_button("play_next")
            
            self.wait(1)
            
            # Once the bot is at the Summon Selection screen, select your summon and party and start the mission.
            if(self.image_tools.confirm_location("select_summon")):
                self.find_summon_element(summon_element_name=self.dimensional_halo_summon_element_name)
                self.find_summon(summon_name=self.dimensional_halo_summon_name)
                start_check = self.find_party_and_start_mission(group_number=self.dimensional_halo_group_number, party_number=self.dimensional_halo_party_number)
                if(start_check and self.start_combat_mode(f"scripts/{self.dimensional_halo_combat_script}.txt")):
                    self.collect_loot()
                    return True
                
        elif(not self.enable_dimensional_halo and self.image_tools.confirm_location("limited_time_quests", tries=1)):
            self.print_and_save(f"\n{self.printtime()} [INFO] Dimensional Halo detected but user opted to not run it. Moving on...")
            self.find_and_click_button("close")
        else:
            self.print_and_save(f"\n{self.printtime()} [INFO] No Dimensional Halo detected. Moving on...")
        
        return False
    
    def wait_for_attack(self):
        """Wait until the bot sees either the Attack or the Next button before starting the next turn or moving the execution forward. It will wait about 20 seconds before moving on to avoid an infinite loop.

        Returns:
            None
        """
        tries = 10
        while(self.image_tools.find_button("attack", tries=1, suppress_error=self.suppress_error) == None or self.image_tools.find_button("next", tries=1, suppress_error=self.suppress_error) == None):
            self.wait(1)
            self.find_dialog_in_combat()
            tries -= 1
            if(tries < 0 or self.image_tools.find_button("attack", tries=1, suppress_error=self.suppress_error) != None or self.image_tools.find_button("next", tries=1, suppress_error=self.suppress_error) != None):
                break
            self.wait(1)
        
        return None
    
    def request_backup(self):
        """Request backup during a Raid.

        Returns:
            None
        """
        self.print_and_save(f"\n{self.printtime()} [COMBAT] Now requesting Backup for this Raid.")
        
        # Scroll down the screen a little bit to have the "Request Backup" button visible on all screen sizes.
        self.mouse_tools.scroll_screen_from_home_button(-400)
        
        # Now click the "Request Backup" button.
        self.find_and_click_button("request_backup")
        
        # Find the location of the "Cancel" button and then click the button right next to it.
        # This is to ensure that no matter what the blue "Request Backup" button's appearance, it is ensured to be pressed.
        cancel_button_location = self.image_tools.find_button("cancel")
        self.mouse_tools.move_and_click_point(cancel_button_location[0] + 200, cancel_button_location[1])
        self.wait(1)
        
        if(self.image_tools.confirm_location("request_backup_success", tries=1)):
            self.print_and_save(f"{self.printtime()} [COMBAT] Finished requesting Backup.")
            self.find_and_click_button("ok")
        
        return None
    
    def tweet_backup(self):
        """Request backup during a Raid using Twitter.

        Returns:
            None
        """
        self.print_and_save(f"\n{self.printtime()} [COMBAT] Now requesting Backup for this Raid via Twitter.")
        
        # Scroll down the screen a little bit to have the "Request Backup" button visible on all screen sizes.
        self.mouse_tools.scroll_screen_from_home_button(-400)
        
        # Now click the "Request Backup" button.
        self.find_and_click_button("request_backup")
        
        # Then click the "Tweet" button.
        self.find_and_click_button("request_backup_tweet")
        self.find_and_click_button("ok")
        self.wait(1)
        
        # On success, click the "OK" button. Otherwise, click the "Cancel" button.
        if(self.image_tools.confirm_location("request_backup_tweet_success", tries=1)):
            self.print_and_save(f"{self.printtime()} [COMBAT] Finished requesting Backup via Twitter.")
            self.find_and_click_button("ok")
        else:
            self.print_and_save(f"{self.printtime()} [COMBAT] Failed requesting Backup via Twitter as there is still a cooldown from the last tweet.")
            self.find_and_click_button("cancel")

        return None

    def start_combat_mode(self, script_file_path: str = ""):
        """Start the Combat Mode with the given script file name. Start reading through the text file line by line and have the bot proceed accordingly.

        Args:
            script_file_path (str, optional): Path to the combat script text file. Defaults to "".

        Returns:
            (bool): Return True if Combat Mode was successful. Else, return False if the party wiped or backed out without retreating.
        """
        # Open the script text file and process all read lines.
        try:
            self.print_and_save("\n\n################################################################################")
            self.print_and_save(f"{self.printtime()} [COMBAT] Starting Combat Mode.")
            self.print_and_save("################################################################################\n")
            
            if(script_file_path == "" or script_file_path == None):
                self.print_and_save(f"\n{self.printtime()} [COMBAT] No script file was given. Using default semi-attack script...")
                script = open(f"scripts/empty.txt", "r")
            else:
                self.print_and_save(f"\n{self.printtime()} [COMBAT] Now loading up combat script at {script_file_path}...")
                script = open(script_file_path, "r")
            
            # Grab all lines in the file and store it into the lines list.
            lines = script.readlines()            

            i = 0  # Index for the list of read lines from the script.
            line_number = 1  # Tells what line number the bot is reading.
            turn_number = 1  # Tells current turn for the script execution.

            # Flag to suppress error messages in attempts to finding the "Attack" / "Next" Buttons and then reset the retreat check flag.
            self.suppress_error = True
            self.retreat_check = False
            
            # Flag for Full Auto. Every command after it will be ignored until the raid is cleared or party wiped.
            full_auto = False

            # This is where the main workflow occurs in. Continue until EOF is reached in the combat script.
            while(i != len(lines) and not self.retreat_check):
                # Grab the specified line from the list of lines.
                line = lines[i]

                # Print each line read if debug mode is active.
                if(line[0] != "#" and line[0] != "/" and line.strip() != ""):
                    if(self.debug_mode):
                        self.print_and_save(f"\n{self.printtime()} [DEBUG] Reading Line {line_number}: \"{line.strip()}\"")

                # Save the position of the center of the "Attack" and "Back" Button. If already found, don't call this again.
                if(self.attack_button_location == None or self.back_button_location == None):
                    self.attack_button_location = self.image_tools.find_button("attack", tries=10 , suppress_error=self.suppress_error)
                    if(self.attack_button_location != None):
                        self.back_button_location = (self.attack_button_location[0] - 322, self.attack_button_location[1])
                    else:
                        self.print_and_save(f"\n{self.printtime()} [ERROR] Cannot find Attack button. Raid must have just ended.")
                        return False

                # If the execution reached the next turn block and it is currently not the correct turn, keep pressing the "Attack" Button until the turn number matches.
                if(line[0] != "#" and line[0] != "/" and line.strip() != "" and "turn" in line.lower() and int(line.split(":")[0].split(" ")[1]) != turn_number):
                    self.print_and_save(f"\n{self.printtime()} [COMBAT] Attacking until the bot reaches Turn {int(line.split(':')[0].split(' ')[1])}...")
                    while(int(line.split(":")[0].split(" ")[1]) != turn_number):
                        self.print_and_save(f"{self.printtime()} [COMBAT] Starting Turn {turn_number}.")
                        self.find_dialog_in_combat()
                        attack_button_location = self.image_tools.find_button("attack", tries=1, suppress_error=self.suppress_error)

                        if (attack_button_location != None):
                            self.print_and_save(f"{self.printtime()} [COMBAT] Ending Turn {turn_number} by attacking now...")   
                            number_of_charge_attacks = self.find_charge_attacks()
                            self.mouse_tools.move_and_click_point(self.attack_button_location[0], self.attack_button_location[1])
                            self.wait(3 + number_of_charge_attacks)
                            
                            # Wait for the Attack / Next button or move on after about 20 seconds.
                            self.wait_for_attack()
                            self.print_and_save(f"{self.printtime()} [COMBAT] Turn {turn_number} has ended.")
                            turn_number += 1
                           
                            # Check to see if the party wiped.
                            self.party_wipe_check()

                        next_button_location = self.image_tools.find_button("next", tries=1, suppress_error=self.suppress_error)
                        if(next_button_location != None):
                            self.mouse_tools.move_and_click_point(next_button_location[0], next_button_location[1])
                            self.wait(3)
                            
                        # Check for battle end.
                        if(self.retreat_check or self.image_tools.confirm_location("exp_gained", tries=1) or self.image_tools.confirm_location("no_loot", tries=1)):
                            break
                            
                # Check for battle end.
                if(self.retreat_check or self.image_tools.confirm_location("exp_gained", tries=1) or self.image_tools.confirm_location("no_loot", tries=1)):
                    break

                # If it is the start of the Turn and it is currently the correct turn, grab the next line for execution.
                if(line[0] != "#" and line[0] != "/" and line.strip() != "" and "turn" in line.lower() and int(line.split(":")[0].split(" ")[1]) == turn_number and not self.retreat_check):
                    self.print_and_save(f"\n{self.printtime()} [COMBAT] Starting Turn {turn_number}. Reading script now...")
                    
                    i += 1
                    line_number += 1

                    self.find_dialog_in_combat()

                    # Continue reading each line inside the Turn block until you reach the "end" occurrence.
                    while("end" not in line.lower() and line.strip() != ""):
                        # Strip any leading and trailing whitespaces.
                        line = lines[i].strip()
                        if(line == ""):
                            line_number += 1
                            i += 1
                            continue
                        
                        if(i >= len(lines[i])):
                            break
                        
                        self.print_and_save(f"\n{self.printtime()} [COMBAT] Reading Line {line_number}: \"{line}\"")

                        # Determine which character will perform the action.
                        character_selected = 0
                        if("character1" in line.lower()):
                            character_selected = 1
                        elif("character2" in line.lower()):
                            character_selected = 2
                        elif("character3" in line.lower()):
                            character_selected = 3
                        elif("character4" in line.lower()):
                            character_selected = 4

                        # Now perform the skill specified in the read string.
                        if(character_selected != 0):
                            # Select the character specified.
                            self.select_character(character_selected)

                            # Execute each skill from left to right for the current character.
                            commands = line.split(".")[1:]
                            
                            while(len(commands) > 0):
                                command = commands.pop(0).lower()
                                if("useskill" in command):
                                    self.use_character_skill(character_selected, command)
                                    
                                    # If the "Use Skill" popup appears, that means either the skill requires a target or the character is skill-sealed.
                                    if(self.image_tools.confirm_location("use_skill", tries=1)):
                                        # Check if the skill requires a target.
                                        select_a_character_location = self.image_tools.find_button("select_a_character", tries=1)
                                        if(select_a_character_location != None):
                                            self.print_and_save(f"{self.printtime()} [COMBAT] Skill is now awaiting a target...")
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
                                                self.find_and_click_button("cancel", tries=1, suppress_error=True)
                                        
                                        # Else, check if the character is skill-sealed.
                                        elif(self.image_tools.confirm_location("skill_unusable", tries=1)):
                                            self.print_and_save(f"{self.printtime()} [COMBAT] Character is currently skill-sealed. Unable to execute command.")
                                            self.find_and_click_button("cancel", tries=1, suppress_error=True)
                                        
                            # Now click the Back button.
                            self.mouse_tools.move_and_click_point(self.back_button_location[0], self.back_button_location[1])

                            # Attempt to wait to see if the character one-shot the enemy or not. This is user-defined in the config.ini.
                            self.wait(self.idle_seconds_after_skill)
                            
                            # Continue to the next line for execution.
                            line_number += 1
                            i += 1
                            
                            # Check for battle end.
                            if(self.image_tools.confirm_location("exp_gained", tries=1) or self.image_tools.confirm_location("no_loot", tries=1)):
                                break
                        
                        for j in range(1,7):
                            if(f"summon({j})" in line.lower()):
                                # Click the Summon Button to bring up the available Summons.
                                self.print_and_save(f"{self.printtime()} [COMBAT] Invoking Summon #{j}.")
                                self.find_and_click_button("summon")
                                
                                # Click on the specified Summon.
                                if(j == 1):
                                    self.mouse_tools.move_and_click_point(self.attack_button_location[0] - 317, self.attack_button_location[1] + 138)
                                elif(j == 2):
                                    self.mouse_tools.move_and_click_point(self.attack_button_location[0] - 243, self.attack_button_location[1] + 138)
                                elif(j == 3):
                                    self.mouse_tools.move_and_click_point(self.attack_button_location[0] - 165, self.attack_button_location[1] + 138)
                                elif(j == 4):
                                    self.mouse_tools.move_and_click_point(self.attack_button_location[0] - 89, self.attack_button_location[1] + 138)
                                elif(j == 5):
                                    self.mouse_tools.move_and_click_point(self.attack_button_location[0] - 12, self.attack_button_location[1] + 138)
                                else:
                                    self.mouse_tools.move_and_click_point(self.attack_button_location[0] + 63, self.attack_button_location[1] + 138)
                                    
                                # Check if it is summonable. Click OK if so. If not, then click Cancel and move on.
                                if(self.image_tools.confirm_location("summon_details", tries=2)):
                                    ok_button_location = self.image_tools.find_button("ok", tries=1)
                                    if(ok_button_location != None):
                                        self.mouse_tools.move_and_click_point(ok_button_location[0], ok_button_location[1])
                                        
                                        # Wait for the Summon animation to complete. This is user-defined in the config.ini.
                                        self.wait(self.idle_seconds_after_summon)
                                    else:
                                        self.print_and_save(f"{self.printtime()} [COMBAT] Summon #{j} cannot be invoked due to current restrictions.")
                                        self.find_and_click_button("cancel")
                                        
                                        # Now click the Back button.
                                        self.mouse_tools.move_and_click_point(self.back_button_location[0], self.back_button_location[1])
                                        
                                # Check for battle end.
                                if(self.image_tools.confirm_location("exp_gained", tries=1) or self.image_tools.confirm_location("no_loot", tries=1)):
                                    break
                                
                                # Continue to the next line for execution.
                                line_number += 1
                                i += 1
                                
                        if(self.image_tools.find_button("next", tries=1, suppress_error=self.suppress_error) != None):
                            break
                        
                        if("enablefullauto" in line.lower()):
                            self.print_and_save(f"{self.printtime()} [COMBAT] Enabling Full Auto. Bot will continue until raid ends or party wipes.")
                            self.find_and_click_button("full_auto")
                            full_auto = True
                            break
                        
                        if(line[0] != "#" and line[0] != "/" and line.strip() != "" and "requestbackup" in line.lower() and not full_auto):
                            # Request Backup for this Raid.
                            self.request_backup()
                            line_number += 1
                            i += 1
                            line = lines[i]
                        
                        if(line[0] != "#" and line[0] != "/" and line.strip() != "" and "tweetbackup" in line.lower() and not full_auto):
                            # Request Backup via Twitter for this Raid.
                            self.tweet_backup()
                            line_number += 1
                            i += 1
                            line = lines[i]

                if(line[0] != "#" and line[0] != "/" and line.strip() != "" and "end" in line.lower() and not full_auto):
                    # Attempt to find the "Next" Button first before attacking to preserve the turn number in the backend. If so, skip clicking the "Attack" Button.
                    # Otherwise, click the "Attack" Button, increment the turn number, and then attempt to find the "Next" Button.
                    next_button_location = self.image_tools.find_button("next", tries=1, suppress_error=self.suppress_error)
                    if(next_button_location != None):
                        self.print_and_save(f"{self.printtime()} [COMBAT] All enemies on screen have been eliminated before attacking. Preserving Turn {turn_number} by moving to the next Wave...")
                        self.mouse_tools.move_and_click_point(next_button_location[0], next_button_location[1])
                        self.wait(3)
                    else:
                        self.print_and_save(f"{self.printtime()} [COMBAT] Ending Turn {turn_number} by attacking now...")
                        number_of_charge_attacks = self.find_charge_attacks()
                        self.mouse_tools.move_and_click_point(self.attack_button_location[0], self.attack_button_location[1])
                        self.wait(3 + number_of_charge_attacks)
                        
                        # Wait for the Attack / Next button or move on after about 20 seconds.
                        self.wait_for_attack()
                        self.print_and_save(f"{self.printtime()} [COMBAT] Turn {turn_number} has ended.")
                        turn_number += 1
                        
                        next_button_location = self.image_tools.find_button("next", tries=1, suppress_error=self.suppress_error)
                        if(next_button_location != None):
                            self.mouse_tools.move_and_click_point(next_button_location[0], next_button_location[1])
                            self.wait(3)
                        
                        # Check to see if the party wiped.
                        self.party_wipe_check()
                        
                if(line[0] != "#" and line[0] != "/" and line.strip() != "" and "exit" in line.lower() and not full_auto):
                    # End Combat Mode by heading back to the Home Screen without retreating. 
                    # Usually for raid farming as to maximize the number of raids joined after completing the provided combat script.
                    self.print_and_save(f"\n{self.printtime()} [COMBAT] Reading Line {line_number}: \"{line.strip()}\"")
                    self.print_and_save(f"{self.printtime()} [COMBAT] Leaving this raid without retreating...")
                    
                    self.wait(1)
                    self.go_back_home(confirm_location_check=True)
                    
                    # Return False to indicate that the Combat Mode ended prematurely.
                    return False

                # Continue to the next line for execution.
                line_number += 1
                i += 1
            
            # When execution gets to here outside the while loop from above, it means that the bot has reached the end of the combat script and will now attack 
            # until the battle ends or the party wipes.
            self.print_and_save(f"\n{self.printtime()} [COMBAT] Bot has reached end of script. Auto-attacking until battle ends...")

            # Keep pressing the location of the "Attack" / "Next" Button until the bot reaches the Quest Results Screen.
            while(not self.retreat_check and not full_auto and not self.image_tools.confirm_location("exp_gained", tries=1) and not self.image_tools.confirm_location("no_loot", tries=1)):
                self.find_dialog_in_combat()
                attack_button_location = self.image_tools.find_button("attack", tries=1, suppress_error=self.suppress_error)
                if (attack_button_location != None):
                    self.print_and_save(f"\n{self.printtime()} [COMBAT] Starting Turn {turn_number}.")
                    self.print_and_save(f"{self.printtime()} [COMBAT] Ending Turn {turn_number} by attacking now...")
                    number_of_charge_attacks = self.find_charge_attacks()
                    self.mouse_tools.move_and_click_point(self.attack_button_location[0], self.attack_button_location[1])
                    self.wait(3 + number_of_charge_attacks)
                    
                    # Wait for the Attack / Next button or move on after about 20 seconds.
                    self.wait_for_attack()
                    self.print_and_save(f"{self.printtime()} [COMBAT] Turn {turn_number} has ended.")
                    turn_number += 1

                next_button_location = self.image_tools.find_button("next", tries=1, suppress_error=self.suppress_error)
                if(next_button_location != None):
                    self.mouse_tools.move_and_click_point(next_button_location[0], next_button_location[1])
                    self.wait(3)

                # Check to see if the party wiped.
                self.party_wipe_check()
            
            # Loop for Full Auto. The game will progress the Quest/Raid without any input required from the bot.     
            while(not self.retreat_check and full_auto and not self.image_tools.confirm_location("exp_gained", tries=1) and not self.image_tools.confirm_location("no_loot", tries=1)):
                self.party_wipe_check()
                self.wait(3)

            self.print_and_save("\n################################################################################")
            self.print_and_save(f"{self.printtime()} [COMBAT] Ending Combat Mode.")
            self.print_and_save("################################################################################")
            
            if(not self.retreat_check):
                self.print_and_save(f"\n{self.printtime()} [INFO] Bot has reached the Quest Results Screen.")
                return True
            else:
                return False
        except FileNotFoundError as e:
            self.print_and_save(f"\n{self.printtime()} [ERROR] Cannot find \"{script_file_path}.txt\" inside the /scripts folder: \n{traceback.format_exc()}")
            self.isBotRunning.value = 1
    
    def start_farming_mode(self, summon_element_name: str, summon_name: str, group_number: int, party_number: int, map_mode: str, map_name: str, item_name: str, 
                           item_amount_to_farm: int, mission_name: str):
        """Start the Farming Mode using the given parameters.

        Args:
            summon_element_name (str): Name of the summon element image file in the images/buttons/ folder.
            summon_name (str): Exact name of the Summon image's file name in images/summons folder.
            group_number (int): The group that the specified party in in.
            party_number (int): The specified party to start the mission with.
            map_mode (str): Mode to look for the specified item and map in.
            map_name (str): Name of the map to look for the specified mission in.
            item_name (str): Name of the item to farm.
            item_amount_to_farm (int): Amount of the item to farm.
            mission_name (str): Name of the mission to farm the item in.
        
        Returns:
            None
        """
        try:
            if(item_name != "EXP"):
                self.print_and_save("\n\n################################################################################")
                self.print_and_save(f"{self.printtime()} [FARM] Starting Farming Mode for {map_mode}.")
                self.print_and_save(f"{self.printtime()} [FARM] Farming {item_amount_to_farm}x {item_name} at {mission_name}.")
                self.print_and_save("################################################################################\n")
            else:
                self.print_and_save("\n\n################################################################################")
                self.print_and_save(f"{self.printtime()} [FARM] Starting Farming Mode for {map_mode}.")
                self.print_and_save(f"{self.printtime()} [FARM] Doing {item_amount_to_farm}x runs for {item_name} at {mission_name}.")
                self.print_and_save("################################################################################\n")
            
            difficulty = ""
            
            if(map_mode.lower() == "special" or map_mode.lower() == "event"):
                # Attempt to see if the difficulty starts at the 0th index to differentiate between cases like "H" and "VH".
                if(mission_name.find("N ") == 0):
                    difficulty = "Normal"
                elif(mission_name.find("H ") == 0):
                    difficulty = "Hard"
                elif(mission_name.find("VH ") == 0):
                    difficulty = "Very Hard"
                elif(mission_name.find("EX ") == 0):
                    difficulty = "Extreme"
            elif(map_mode.lower() == "dread barrage"):
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

            # Save the following information to share between the Game class and the MapSelection class.
            self.summon_element_name = summon_element_name
            self.summon_name = summon_name
            self.group_number = group_number
            self.party_number = party_number
            self.map_mode = map_mode
            self.item_name = item_name
            self.item_amount_to_farm = item_amount_to_farm
            self.mission_name = mission_name
            
            # If Dimensional Halo is enabled, save settings for it based on conditions.
            if(self.item_name == "EXP" and self.enable_dimensional_halo):
                self.print_and_save(f"\n{self.printtime()} [INFO] Initializing settings for Dimensional Halo...")
                
                if(self.dimensional_halo_combat_script == ""):
                    self.print_and_save(f"{self.printtime()} [INFO] Combat Script for Dimensional Halo will reuse the one for Farming Mode.")
                    self.dimensional_halo_combat_script = self.combat_script
                    
                if(self.dimensional_halo_summon_element_name == ""):
                    self.print_and_save(f"{self.printtime()} [INFO] Summon Element for Dimensional Halo will reuse the one for Farming Mode.")
                    self.dimensional_halo_summon_name = self.summon_element_name
                    
                if(self.dimensional_halo_summon_name == ""):
                    self.print_and_save(f"{self.printtime()} [INFO] Summon for Dimensional Halo will reuse the one for Farming Mode.")
                    self.dimensional_halo_summon_name = self.summon_name
                    
                if(self.dimensional_halo_group_number == ""):
                    self.print_and_save(f"{self.printtime()} [INFO] Group Number for Dimensional Halo will reuse the one for Farming Mode.")
                    self.dimensional_halo_group_number = self.group_number
                else:
                    self.dimensional_halo_group_number = int(self.dimensional_halo_group_number)
                    
                if(self.dimensional_halo_party_number == ""):
                    self.print_and_save(f"{self.printtime()} [INFO] Party Number for Dimensional Halo will reuse the one for Farming Mode.")
                    self.dimensional_halo_party_number = self.party_number
                else:
                    self.dimensional_halo_party_number = int(dimensional_halo_party_number)
                    
                self.print_and_save(f"{self.printtime()} [INFO] Settings initialized for Dimensional Halo...")
            elif(self.item_name == "Repeated Runs" and self.enable_event_nightmare):
                # Do the same for Event Nightmare if enabled.
                self.print_and_save(f"\n{self.printtime()} [INFO] Initializing settings for Event...")
                
                if(self.event_nightmare_combat_script == ""):
                    self.print_and_save(f"{self.printtime()} [INFO] Combat Script for Event will reuse the one for Farming Mode.")
                    self.event_nightmare_combat_script = self.combat_script
                    
                if(self.event_nightmare_summon_element_name == ""):
                    self.print_and_save(f"{self.printtime()} [INFO] Summon Element for Event will reuse the one for Farming Mode.")
                    self.event_nightmare_summon_element_name = self.summon_element_name
                    
                if(self.event_nightmare_summon_name == ""):
                    self.print_and_save(f"{self.printtime()} [INFO] Summon for Event will reuse the one for Farming Mode.")
                    self.event_nightmare_summon_name = self.summon_name
                    
                if(self.event_nightmare_group_number == ""):
                    self.print_and_save(f"{self.printtime()} [INFO] Group Number for Event will reuse the one for Farming Mode.")
                    self.event_nightmare_group_number = self.group_number
                else:
                    event_nightmare_group_number = int(event_nightmare_group_number)
                    
                if(self.event_nightmare_party_number == ""):
                    self.print_and_save(f"{self.printtime()} [INFO] Party Number for Event will reuse the one for Farming Mode.")
                    self.event_nightmare_party_number = self.party_number
                else:
                    self.event_nightmare_party_number = int(self.event_nightmare_party_number)
                    
                self.print_and_save(f"{self.printtime()} [INFO] Settings initialized for Event...")
            elif(self.item_name == "Repeated Runs" and self.enable_unparalleled_foe):
                # Do the same for Dread Barrage Unparalleled Foes if enabled.
                self.print_and_save(f"\n{self.printtime()} [INFO] Initializing settings for Dread Barrage Unparalleled Foes...")
                
                if(self.unparalleled_foe_combat_script == ""):
                    self.print_and_save(f"{self.printtime()} [INFO] Combat Script for Dread Barrage Unparalleled Foes will reuse the one for Farming Mode.")
                    self.unparalleled_foe_combat_script = self.combat_script
                    
                if(self.unparalleled_foe_summon_element_name == ""):
                    self.print_and_save(f"{self.printtime()} [INFO] Summon Element for Dread Barrage Unparalleled Foes will reuse the one for Farming Mode.")
                    self.unparalleled_foe_summon_element_name = self.summon_element_name
                    
                if(self.unparalleled_foe_summon_name == ""):
                    self.print_and_save(f"{self.printtime()} [INFO] Summon for Dread Barrage Unparalleled Foes will reuse the one for Farming Mode.")
                    self.unparalleled_foe_summon_name = self.summon_name
                    
                if(self.unparalleled_foe_group_number == ""):
                    self.print_and_save(f"{self.printtime()} [INFO] Group Number for Dread Barrage Unparalleled Foes will reuse the one for Farming Mode.")
                    self.unparalleled_foe_group_number = self.group_number
                else:
                    unparalleled_foe_group_number = int(unparalleled_foe_group_number)
                    
                if(self.unparalleled_foe_party_number == ""):
                    self.print_and_save(f"{self.printtime()} [INFO] Party Number for Dread Barrage Unparalleled Foes will reuse the one for Farming Mode.")
                    self.unparalleled_foe_party_number = self.party_number
                else:
                    self.unparalleled_foe_party_number = int(self.unparalleled_foe_party_number)
                    
                self.print_and_save(f"{self.printtime()} [INFO] Settings initialized for Dread Barrage Unparalleled Foes...")
            
            self.item_amount_farmed = 0
            self.amount_of_runs_finished = 0
            summon_check = False
            coop_first_run = False
            
            if((map_mode.lower() != "raid" and self.map_selection.select_map(map_mode, map_name, item_name, mission_name, difficulty)) or (map_mode.lower() == "raid" and self.map_selection.join_raid(item_name, mission_name))):
                # Keep playing the mission until the bot gains enough of the item specified.
                while(self.item_amount_farmed < self.item_amount_to_farm):
                    # Loop until the Summon has been selected successfully.
                    while(summon_check == False and map_mode.lower() != "coop"): 
                        self.print_and_save(f"\n{self.printtime()} [INFO] AP/EP check done. Now selecting summon...")
                        
                        self.find_summon_element(summon_element_name)
                        summon_check = self.find_summon(summon_name)
                        
                        # If the Summons were reset, head back to the location of the mission.
                        if(summon_check == False):
                            if(map_mode.lower() != "raid"):
                                self.print_and_save(f"\n{self.printtime()} [INFO] Selecting mission again...")
                                self.map_selection.select_map(map_mode, map_name, item_name, mission_name, difficulty)
                            else:
                                self.print_and_save(f"\n{self.printtime()} [INFO] Joining raids again...")
                                self.map_selection.join_raid(item_name, mission_name)
                    
                    # Select the Party specified and then start the mission.
                    if(map_mode.lower() != "coop"):
                        start_check = self.find_party_and_start_mission(group_number, party_number)
                    else:
                        # Only select the Party for this Coop mission once. After that, subsequent runs always has that Party selected.
                        if(not coop_first_run):
                            self.print_and_save(f"\n{self.printtime()} [INFO] Selecting party for this Coop session...")
                            start_check = self.find_party_and_start_mission(group_number, party_number)
                            coop_first_run = True

                        self.print_and_save(f"{self.printtime()} [INFO] Starting Coop mission.")
                        self.find_and_click_button("coop_start")
                    
                    # After Party has been successfully selected, start Combat Mode.
                    if(start_check and map_mode.lower() != "raid"):
                        # Check for the Items Picked Up popup that appears after starting a Quest mission.
                        self.wait(2)
                        if(map_mode.lower() == "quest" and self.image_tools.confirm_location("items_picked_up", tries=5)):
                            self.find_and_click_button("ok")
                        
                        # Start Combat Mode here.
                        if(self.start_combat_mode(self.combat_script)):
                            # After Combat Mode has finished successfully without retreating or exiting prematurely, collect the loot.
                            self.collect_loot()
                            
                            if(self.item_amount_farmed < self.item_amount_to_farm):
                                # Click the Play Again button or the Room button if its Coop.
                                if(map_mode.lower() != "coop"):
                                    if(not self.find_and_click_button("play_again")):
                                        # Clear away any Pending Battles.
                                        self.map_selection.check_for_pending(map_mode)
                                        
                                        # Start the Quest again.
                                        self.map_selection.select_map(map_mode, map_name, item_name, mission_name, difficulty)
                                else:
                                    self.find_and_click_button("coop_room")

                                # Check for Missions popup for Dread Barrage.
                                if(map_mode.lower() == "dread barrage" and self.image_tools.confirm_location("dread_barrage_missions", tries=1)):
                                    self.print_and_save(f"{self.printtime()} [INFO] Found Missions popup for Dread Barrage. Closing it now...")
                                    self.find_and_click_button("close")
                                
                                # If the user wants to fight Unparalleled Foes during Dread Barrage, then start the specified one.
                                if(map_mode.lower() == "dread barrage" and self.image_tools.confirm_location("dread_barrage_unparalleled_foe", tries=1)):
                                    ap_0_locations = self.image_tools.find_all("ap_0")
                                    
                                    if(self.enable_unparalleled_foe_level_95 and not self.enable_unparalleled_foe_level_175):
                                        # Start the Level 95 Unparalleled Foe.
                                        self.print_and_save(f"\n{self.printtime()} [INFO] Starting Level 95 Unparalleled Foe...")
                                        self.mouse_tools.move_and_click_point(ap_0_locations[0][0], ap_0_locations[0][1])
                                    elif(self.enable_unparalleled_foe_level_175 and not self.enable_unparalleled_foe_level_95):
                                        # Start the Level 175 Unparalleled Foe.
                                        self.print_and_save(f"\n{self.printtime()} [INFO] Starting Level 175 Unparalleled Foe...")
                                        self.mouse_tools.move_and_click_point(ap_0_locations[1][0], ap_0_locations[1][1])
                                    elif(not self.enable_unparalleled_foe_level_95 and not self.enable_unparalleled_foe_level_175):
                                        # Close the popup.
                                        self.print_and_save(f"\n{self.printtime()} [INFO] Closing Dread Barrage Unparalleled Foes popup...")
                                        self.find_and_click_button("close")
                                    else:
                                        # Every other case will default to the Level 95 Unparalleled Foe.
                                        self.print_and_save(f"\n{self.printtime()} [INFO] Defaulting to Level 95 Unparalleled Foe. Starting it now...")
                                        self.mouse_tools.move_and_click_point(ap_0_locations[0][0], ap_0_locations[0][1])
                                
                                # Check for Friend Request popup.
                                self.check_for_friend_request()
                                
                                # Check for Dimensional Halo if enabled.
                                if(self.item_name == "EXP" and self.enable_dimensional_halo):
                                    self.check_for_dimensional_halo()
                                elif(self.map_mode.lower() == "event" and self.enable_event_nightmare):
                                    self.check_for_event_nightmare()
                                
                                # Check for available AP.
                                self.check_for_ap(use_full_elixirs=self.quest_refill)
                                summon_check = False
                                
                                if(self.map_mode.lower() == "event" and self.image_tools.confirm_location("not_enough_treasure")):
                                    # If the bot tried to repeat a Extreme difficulty Event Raid and it lacked the treasures to host it, go back to select_map.
                                    self.find_and_click_button("ok")
                                    self.map_selection.select_map(map_mode, map_name, item_name, mission_name, difficulty)
                        else:
                            self.print_and_save(f"\n{self.printtime()} [INFO] Selecting mission again due to retreating...")
                            self.map_selection.select_map(map_mode, map_name, item_name, mission_name, difficulty)
                    elif(start_check and map_mode.lower() == "raid"): 
                        # Cover the occasional case where joining the raid after selecting the Summon and Party leds to the Quest Results Screen with no loot to collect.
                        if(self.image_tools.confirm_location("no_loot")):
                            self.print_and_save(f"\n{self.printtime()} [INFO] Seems that the raid just ended. Moving on...")
                            self.go_back_home()
                            summon_check = False
                        else:
                            # Start Combat Mode for this Raid.
                            if(self.start_combat_mode(self.combat_script)):
                                # After Combat Mode has finished, count the number of the specified item that has dropped. This should put the bot back to the Quest Screen.
                                self.collect_loot()
                                
                                if(self.item_amount_farmed < self.item_amount_to_farm):
                                    # Clear away any Pending Battles.
                                    self.map_selection.check_for_pending(map_mode)
                                    
                                    # Join a new raid.
                                    self.map_selection.join_raid(item_name, mission_name)
                                    summon_check = False
                            else:
                                # If Combat Mode exited via the exit command, check for Pending Battles.
                                self.map_selection.check_for_pending("raid")
                                
                                # Join a new raid.
                                self.map_selection.join_raid(item_name, mission_name)
                                summon_check = False
                    else:
                        if(map_mode.lower() == "raid"):
                            # If the bot reached here, it means that the Raid ended before the bot could start the mission after selecting the Summon and Party.
                            self.print_and_save(f"{self.printtime()} [INFO] Now looking for another raid to join...")
                            self.map_selection.join_raid(item_name, mission_name)
                            summon_check = False
            else:
                raise Exception("Confirming the location of the Summon Selection Screen after completing the process of selecting the mission returned False.")
        except Exception:
            self.print_and_save(f"\n{self.printtime()} [ERROR] Bot encountered exception in Farming Mode: \n{traceback.format_exc()}")
            
        self.print_and_save("\n################################################################################")
        self.print_and_save(f"{self.printtime()} [FARM] Ending Farming Mode.")
        self.print_and_save("################################################################################\n")
        
        self.isBotRunning.value = 1
        return None
