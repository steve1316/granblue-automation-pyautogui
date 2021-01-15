import datetime
import multiprocessing
import sys
import time
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
    
    keys_tokens (Iterable[str]): List of keys and tokens for Twitter API. Its order is: [consumer key, consumer secret key, access token, access secret token].
    
    custom_mouse_speed (float, optional): The speed at which the mouse moves at. Defaults to 0.5.
    
    combat_script (str, optional): The combat script to use for Combat Mode. Defaults to empty string.

    debug_mode (bool, optional): Optional flag to print debug messages related to this class. Defaults to False.

    """

    def __init__(self, queue: multiprocessing.Queue, isBotRunning: int, keys_tokens: Iterable[str], combat_script: str = "", custom_mouse_speed: float = 0.5, debug_mode: bool = False):
        super().__init__()

        # Start a timer signaling bot start in order to keep track of elapsed time and create a Queue to share logging messages between backend and frontend.
        self.starting_time = timer()
        self.queue = queue

        # Initialize the MapSelection and TwitterRoomFinder objects.
        self.map_selection = MapSelection(self)
        self.room_finder = TwitterRoomFinder(self, keys_tokens[0], keys_tokens[1], keys_tokens[2], keys_tokens[3])

        # Set a debug flag to determine whether or not to print debugging messages.
        self.debug_mode = debug_mode
        
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

        # The amount of time to pause after each call to pyautogui. This applies to calls inside mouse_utils and image_utils.
        pyautogui.PAUSE = 0.5

        # Calibrate the dimensions of the game window on bot launch.
        self.go_back_home(display_info_check=True)

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

        self.home_button_location = self.image_tools.find_button("home", sleep_time=1)
        
        # Set the dimensions of the game window and save it in ImageUtils so that future operations do not go out of bounds.
        home_news_button = self.image_tools.find_button("home_news")
        home_menu_button = self.image_tools.find_button("home_menu")
        self.image_tools.window_left = home_news_button[0] - 35 # The x-coordinate of the left edge
        self.image_tools.window_top = home_menu_button[1] - 24 # The y-coordinate of the top edge
        self.image_tools.window_width = self.image_tools.window_left + 468 # The width of the region
        self.image_tools.window_height = (self.home_button_location[1] + 24) - self.image_tools.window_top # The height of the region

        if(self.debug_mode):
            self.print_and_save(f"\n{self.printtime()} [SUCCESS] Dimensions of the game window has been successfully recalibrated.")

        if(display_info_check):
            self.print_and_save("\n\n********************************************************************************")
            self.print_and_save(f"{self.printtime()} [INFO] Screen size: {pyautogui.size()}.")
            self.print_and_save(f"{self.printtime()} [INFO] Game window size: Region({self.image_tools.window_left}, {self.image_tools.window_top}, {self.image_tools.window_width}, {self.image_tools.window_height}).")
            self.print_and_save("********************************************************************************\n")

        return None

    def go_back_home(self, confirm_location_check: bool = False, display_info_check: bool = False):
        """Go back to the Home Screen to reset the bot's position. Also able to recalibrate the region dimensions of the game window if display_info_check is True.

        Args:
            confirm_location_check (bool, optional): Check to see if the location is correct. Defaults to False.
            display_info_check (bool, optional): Recalibrate and display size of screen and game window size. Defaults to False.

        Returns:
            None
        """
        if(self.debug_mode):
            self.print_and_save(f"\n{self.printtime()} [DEBUG] Moving back to the Home Screen...")
        
        if(confirm_location_check):
            self.image_tools.confirm_location("home")
        else:    
            # Go to the Home Screen.
            if(self.home_button_location != None):
                self.mouse_tools.move_and_click_point(self.home_button_location[0], self.home_button_location[1])
            else:
                temp_home_button_location = self.image_tools.find_button("home")
                self.mouse_tools.move_and_click_point(temp_home_button_location[0], temp_home_button_location[1])
        
        # Recalibrate the dimensions of the window if flag is True.
        if (display_info_check):
            self.calibrate_game_window(display_info_check=True)
            
        return None

    def wait_for_ping(self, seconds: int = 3):
        """Wait the specified seconds to account for ping or loading.

        Args:
            seconds (int, optional): Number of seconds for the execution to wait for. Defaults to 3.

        Returns:
            None
        """
        time.sleep(seconds)
        return None
    
    def find_and_click_button(self, button_name: str, suppress_error: bool = False):
        """Find the center point of a button image and click it.

        Args:
            button_name (str): Name of the button image file in the images/buttons/ folder.
            suppress_error (bool): Suppresses template matching error depending on boolean. Defaults to False.

        Returns:
            None
        """
        # If the bot is trying to find the Quest button and failed, chances are that the button is now styled red.
        if(button_name == "quest"):
            temp_location = self.image_tools.find_button("quest", tries=2, suppress_error=suppress_error)
            if(temp_location == None):
                temp_location = self.image_tools.find_button("quest2", tries=2, suppress_error=suppress_error)
        else:
            temp_location = self.image_tools.find_button(button_name, suppress_error=suppress_error)
            
        self.mouse_tools.move_and_click_point(temp_location[0], temp_location[1])
        return None
    
    def party_wipe_check(self):
        """Check to see if the party has wiped during Combat Mode. Update the retreat check flag if so.

        Returns:
            None
        """
        # Check to see if party has wiped.
        party_wipe_indicator = self.image_tools.find_button("party_wipe_indicator", tries=1, suppress_error=self.suppress_error)
        if(party_wipe_indicator != None):
            self.print_and_save(f"\n{self.printtime()} [COMBAT] Party has unfortunately wiped during Combat Mode. Retreating now...")
            self.wait_for_ping(3)
            self.mouse_tools.move_and_click_point(party_wipe_indicator[0], party_wipe_indicator[1])
            
            self.image_tools.confirm_location("continue")
            cancel_button = self.image_tools.find_button("summon_cancel")
            self.mouse_tools.move_and_click_point(cancel_button[0], cancel_button[1])
                
            self.image_tools.confirm_location("retreat")
            retreat_button = self.image_tools.find_button("retreat_confirmation")
            self.mouse_tools.move_and_click_point(retreat_button[0], retreat_button[1])
            
            self.retreat_check = True
        
        return None

    def find_summon_element(self, summon_element_name: str, tries: int = 3):
        """Select the specified element tab for summons.

        # Todo: ALL images need to be segmented into Lite, Regular, and High to account for different Graphics Settings. Have not tested if confidence helps or not. Might not be needed anymore with GuiBot fallback.

        Args:
            summon_element_name (str): Name of the summon element image file in the images/buttons/ folder.
            tries (int, optional): Number of tries before failing. Defaults to 3.

        Returns:
            (bool): True if successfully found and clicked the summon element tab. Otherwise, return False.
        """
        if(self.debug_mode):
            self.print_and_save(f"\n{self.printtime()} [DEBUG] Now attempting to find {summon_element_name.upper()} Summon Element tab...")

        summon_element_location = None

        while (summon_element_location == None):
            summon_element_location = self.image_tools.find_button(f"summon_{summon_element_name.lower()}", tries=1)

            if (summon_element_location == None):
                tries -= 1
                
                if (tries == 0):
                    self.print_and_save(f"{self.printtime()} [FAILED] Failed to find {summon_element_name.upper()} Summon Element tab.")
                    return False

        self.print_and_save(f"{self.printtime()} [SUCCESS] Found {summon_element_name.upper()} Summon Element tab.")

        self.mouse_tools.move_and_click_point(summon_element_location[0], summon_element_location[1])

        return True

    def find_summon(self, summon_name: str):
        """Find the specified Summon on the Summon Selection Screen. Make sure to call this after the find_summon_element() method in order to have the correct Summon Element tab already selected.

        # TODO: Handle user-defined list of preferred summons going from most preferred to least.
        # TODO: If not found after a certain number of times, select very first Summon. Maybe have it as an option?

        Args:
            summon_name (str): Exact name of the Summon image's file name in images/summons folder.

        Returns:
            (bool): True if the Summon was found and clicked. Otherwise, return False.
        """
        summon_location = self.image_tools.find_summon(summon_name, self.home_button_location[0], self.home_button_location[1])
        if (summon_location != None):
            self.mouse_tools.move_and_click_point(summon_location[0], summon_location[1])
            
            self.print_and_save(f"\n{self.printtime()} [INFO] Found {summon_name.upper()} Summon. Clicking it now...\n")

            return True
        else:
            # If a Summon is not found, start a Trial Battle to refresh Summons.
            self.reset_summons()

            return False

    def reset_summons(self):
        """Reset the Summons available by starting and then retreating from a Trial Battle.

        Returns:
            None
        """
        self.print_and_save(f"\n{self.printtime()} [INFO] Now refreshing summons...")
        
        self.go_back_home(confirm_location_check=True)
        self.mouse_tools.scroll_screen_from_home_button(-600)

        list_of_steps_in_order = ["gameplay_extras", "trial_battles",
                                  "trial_battles_old_lignoid", "trial_battles_play",
                                  "choose_a_summon", "party_selection_ok", "trial_battles_close",
                                  "menu", "retreat", "retreat_confirmation", "next"]

        # Go through each step in order from left to right from the list of steps.
        while (len(list_of_steps_in_order) > 0):
            step = list_of_steps_in_order.pop(0)
            
            if(step == "trial_battles_old_lignoid"):
                self.image_tools.confirm_location("trial_battles")
            
            image_location = self.image_tools.find_button(step)
            
            if(step == "choose_a_summon"):
                self.mouse_tools.move_and_click_point(image_location[0], image_location[1] + 187)
            else:
                self.mouse_tools.move_and_click_point(image_location[0], image_location[1])
        
        self.image_tools.confirm_location("trial_battles")
        self.print_and_save(f"\n{self.printtime()} [INFO] Summons have now been refreshed.")
        return None

    def find_party_and_start_mission(self, group_number: int, party_number: int, tries: int = 2):
        """Select the specified group and party. It will then start the mission.

        Args:
            group_number (int): The group that the specified party in in.
            party_number (int): The specified party to start the mission with.
            tries (int, optional): Number of tries before failing. Defaults to 2.

        Returns:
            (bool): Returns False if it detects the "Raid is full/Raid is already done" dialog. Otherwise, return True.
        """
        set_location = None
        
        # Find the Group first. If the selected group number is less than 8, it is in Set A. Otherwise, it is in Set B. If failed,
        # alternate searching for Set A / Set B until found or tries are depleted.
        if(group_number < 8):
            if(self.debug_mode):
                self.print_and_save(f"\n{self.printtime()} [DEBUG] Now attempting to find Set A...")

            while (set_location == None):
                set_location = self.image_tools.find_button("party_set_a")
                
                if (set_location == None):
                    tries -= 1
                    
                    if(self.debug_mode):
                        self.print_and_save(f"{self.printtime()} [DEBUG] Locating Set A failed. Trying again for Set B...")

                    if (tries <= 0):
                        sys.exit(f"\n[ERROR] Could not find Set A. Exiting Bot...")

                    # See if the user had Set B active instead of Set A if matching failed.
                    set_location = self.image_tools.find_button("party_set_b")
        else:
            if(self.debug_mode):
                self.print_and_save(f"\n{self.printtime()} [DEBUG] Now attempting to find Set B...")

            while (set_location == None):
                set_location = self.image_tools.find_button("party_set_b")
                
                if (set_location == None):
                    tries -= 1
                    
                    if(self.debug_mode):
                        self.print_and_save(f"{self.printtime()} [DEBUG] Locating Set B failed. Trying again for Set A...")

                    if (tries <= 0):
                        sys.exit(f"\n{self.printtime()} [ERROR] Could not find Set B. Exiting Bot...")

                    # See if the user had Set A active instead of Set B if matching failed.
                    set_location = self.image_tools.find_button("party_set_a")

        if(self.debug_mode):
            self.print_and_save(f"\n{self.printtime()} [SUCCESS] Successfully selected the correct Set. Now selecting Group {group_number}...")

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
            self.print_and_save(f"\n{self.printtime()} [SUCCESS] Successfully selected Group {group_number}. Now selecting Party {party_number}...")

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
            self.print_and_save(f"\n{self.printtime()} [SUCCESS] Successfully selected Party {party_number}. Now starting the mission.")

        # Find and click the "OK" Button to start the mission.
        self.wait_for_ping(1)
        self.find_and_click_button("party_selection_ok")
        
        # If a dialog window pops up and says "This raid battle has already ended. The Home screen will now appear.", return False.
        if(self.image_tools.confirm_location("raid_already_ended_home_redirect")):
            return False
        
        self.wait_for_ping(5)
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

    def find_dialog_in_combat(self, dialog_file_name: str):
        """Check if there are dialog boxes from either Lyria or Vyrn and click them away.

        Args:
            dialog_file_name (str): Image file name of the dialog window. Usually its "dialog_lyria" or "vyrnDialog" for the Combat Screen.

        Returns:
            None
        """
        dialog_location = self.image_tools.find_dialog(dialog_file_name, self.attack_button_location[0], self.attack_button_location[1], tries=1)

        if (dialog_location != None):
            if(self.debug_mode):
                self.print_and_save(f"{self.printtime()} [DEBUG] Detected dialog window from Lyria/Vyrn on Combat Screen. Closing it now...")

            self.mouse_tools.move_and_click_point(dialog_location[0] + 180, dialog_location[1] - 51)

        return None
    
        
    def check_for_ap(self, use_full_elixirs: bool = False):
        """Check if the user encountered the 'Not Enough AP' popup and it will refill using either Half or Full Elixir.

        Args:
            use_full_elixirs (bool, optional): Will use Full Elixir instead of Half Elixir based on this. Defaults to False.

        Returns:
            None
        """
        if(self.image_tools.confirm_location("not_enough_ap", tries=2)):
            # If the bot detects that the user has run out of AP, it will refill using either Half Elixir or Full.
            # TODO: Implement check for when the user ran out of both of them, or one of them.
            if(use_full_elixirs == False):
                self.print_and_save(f"\n{self.printtime()} [INFO] AP ran out! Using Half Elixir...")
                half_ap_location = self.image_tools.find_button("refill_half_ap")
                self.mouse_tools.move_and_click_point(half_ap_location[0], half_ap_location[1] + 175)
            else:
                self.print_and_save(f"\n{self.printtime()} [INFO] AP ran out! Using Full Elixir...")
                full_ap_location = self.image_tools.find_button("refill_full_ap")
                self.mouse_tools.move_and_click_point(full_ap_location[0], full_ap_location[1] + 175)
            
            # Press the OK button to move to the Summon Selection Screen.
            self.wait_for_ping(1)
            self.find_and_click_button("ok")
        else:
            self.print_and_save(f"\n{self.printtime()} [INFO] AP is available. Continuing...")
        
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

        self.mouse_tools.move_and_click_point(x, y)
        self.wait_for_ping(1)

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
        
        if("useSkill(1)" in skill):
            self.print_and_save(f"{self.printtime()} [COMBAT] Character {character_selected} uses Skill 1.")
            x = self.attack_button_location[0] - 213
        elif("useSkill(2)" in skill):
            self.print_and_save(f"{self.printtime()} [COMBAT] Character {character_selected} uses Skill 2.")
            x = self.attack_button_location[0] - 132
        elif("useSkill(3)" in skill):
            self.print_and_save(f"{self.printtime()} [COMBAT] Character {character_selected} uses Skill 3.")
            x = self.attack_button_location[0] - 51
        elif("useSkill(4)" in skill):
            self.print_and_save(f"{self.printtime()} [COMBAT] Character {character_selected} uses Skill 4.")
            x = self.attack_button_location[0] + 39

        self.mouse_tools.move_and_click_point(x, y)
        
        # Check to see if the character is skill-sealed.
        if(self.image_tools.confirm_location("use_skill", tries=1)):
            self.print_and_save(f"{self.printtime()} [COMBAT] Character is currently skill-sealed. Unable to execute command.")
            self.find_and_click_button("friend_request_cancel")
        else:
            self.wait_for_ping(2)

        return None

    def start_combat_mode(self, script_file_path: str = ""):
        """Start the Combat Mode with the given script file name. Start reading through the text file line by line and have the bot proceed accordingly.

        Args:
            script_file_path (str, optional): Path to the combat script text file. Defaults to "".

        Returns:
            (bool): Return True if Combat Mode was successful. #TODO: Return False if the party wiped.
        """
        # Open the script text file and process all read lines.
        try:
            if(script_file_path == "" or script_file_path == None):
                self.print_and_save(f"\n{self.printtime()} [INFO] No script file was given. Using default semi-attack script...")
                script = open(f"scripts/test_empty.txt", "r")
            else:
                self.print_and_save(f"\n{self.printtime()} [INFO] Now loading up combat script at {script_file_path}...")
                script = open(script_file_path, "r")
            
            lines = script.readlines()

            self.print_and_save("\n\n################################################################################")
            self.print_and_save(f"{self.printtime()} [COMBAT] Starting Combat Mode.")
            self.print_and_save("################################################################################\n")

            i = 0  # Index for the list of read lines from the script.
            line_number = 1  # Tells what line number the bot is reading.
            turn_number = 1  # Tells current turn for the script execution.

            # Flag to suppress error messages in attempts to finding the "Attack" / "Next" Buttons.
            self.suppress_error = True
            
            # Reset the retreat check flag.
            self.retreat_check = False

            # Loop through and execute each line in the combat script until EOF.
            while(i != len(lines) and not self.retreat_check):
                line = lines[i]

                # Print each line read if debug mode is active.
                if(line[0] != "#" and line[0] != "/" and line.strip() != ""):
                    if(self.debug_mode):
                        self.print_and_save(f"\n{self.printtime()} [DEBUG] Reading Line {line_number}: \"{line.strip()}\"")

                # Save the position of the center of the "Attack" and "Back" Button. If already found, don't call this again.
                if(self.attack_button_location == None or self.back_button_location == None):
                    self.attack_button_location = self.image_tools.find_button("attack", suppress_error=self.suppress_error)
                    self.back_button_location = (self.attack_button_location[0] - 322, self.attack_button_location[1])

                # If the execution reached the next turn block and it is currently not the correct turn, keep pressing the "Attack" Button until the turn number matches.
                if ("turn" in line.lower() and int(line[5]) != turn_number):
                    while (int(line[5]) != turn_number):
                        self.print_and_save(f"\n{self.printtime()} [COMBAT] Starting Turn {turn_number}.")

                        self.find_dialog_in_combat("lyria")
                        self.find_dialog_in_combat("vyrn")

                        attack_button_location = self.image_tools.find_button("attack", tries=1, suppress_error=self.suppress_error)

                        if (attack_button_location != None):
                            number_of_charge_attacks = self.find_charge_attacks()
                            
                            self.print_and_save(f"{self.printtime()} [COMBAT] Ending Turn {turn_number} by attacking now...")

                            self.mouse_tools.move_and_click_point(self.attack_button_location[0], self.attack_button_location[1])
                            self.wait_for_ping(4 + number_of_charge_attacks)
                            
                            turn_number += 1
                           
                        # Check to see if the party wiped.
                        self.party_wipe_check()

                        # Try to find the "Next" Button only once per turn.
                        next_button_location = self.image_tools.find_button("next", tries=1, suppress_error=self.suppress_error)
                        if(next_button_location != None):
                            if(self.debug_mode):
                                self.print_and_save(f"{self.printtime()} [DEBUG] Detected the Next Button. Clicking it now...")

                            self.mouse_tools.move_and_click_point(next_button_location[0], next_button_location[1])
                            self.wait_for_ping(4)
                            
                        # Check for battle end.
                        if(self.image_tools.confirm_location("exp_gained", tries=1) == True or self.retreat_check):
                            break
                            
                # Check for battle end.
                if(self.image_tools.confirm_location("exp_gained", tries=1) == True or self.retreat_check):
                    break

                # If it is the start of the Turn and it is currently the correct turn, grab the next line for execution.
                if ("turn" in line.lower() and int(line[5]) == turn_number and not self.retreat_check):
                    self.print_and_save(f"\n{self.printtime()} [COMBAT] Starting Turn {turn_number}. Reading script now...")
                    
                    i += 1
                    line_number += 1

                    self.find_dialog_in_combat("lyria")
                    self.find_dialog_in_combat("vyrn")

                    # Continue reading each line inside the Turn block until you reach the "end" occurrence.
                    while("end" not in line):
                        line = lines[i].strip() # Strip any leading and trailing whitespaces.

                        # Print each line read if debug mode is active.
                        if(line[0] != "#" and line[0] != "/" and line.strip() != ""):
                            if(self.debug_mode):
                                self.print_and_save(f"\n{self.printtime()} [DEBUG] Reading Line {line_number}: \"{line.strip()}\"")

                        # Determine which character will perform the action.
                        character_selected = 0
                        if("character1" in line):
                            character_selected = 1
                        elif("character2" in line):
                            character_selected = 2
                        elif("character3" in line):
                            character_selected = 3
                        elif("character4" in line):
                            character_selected = 4

                        # Now perform the skill specified in the read string.
                        # TODO: Handle enemy targeting here as well.
                        if(character_selected != 0):
                            # Select the character specified.
                            self.select_character(character_selected)

                            # Execute each skill from left to right for the current character.
                            skills = line.split(".")
                            skills.pop(0)
                            for skill in skills:
                                self.use_character_skill(character_selected, skill)

                            # Now click the Back button.
                            self.mouse_tools.move_and_click_point(self.back_button_location[0], self.back_button_location[1])

                            # Continue to the next line for execution.
                            line_number += 1
                            i += 1
                            
                            # Attempt to wait to see if the character one-shot the enemy or not.
                            self.wait_for_ping(4)
                            
                            # Check for battle end.
                            if(self.image_tools.confirm_location("exp_gained", tries=1) == True):
                                break
                        
                        # TODO: Allow for Summon chaining. For now, summoning multiple summons requires individual lines.
                        for j in range(1,7):
                            if(f"summon({j})" in line):
                                # Click the Summon Button to bring up the available summons.
                                self.print_and_save(f"{self.printtime()} [COMBAT] Invoking Summon #{j}...")
                                self.find_and_click_button("summon")
                                
                                # Click on the specified summon.
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
                                        self.wait_for_ping(7) # This is 7 seconds to see if the Summon killed all enemies on screen.
                                    else:
                                        self.print_and_save(f"{self.printtime()} [COMBAT] Summon #{j} cannot be invoked due to current restrictions.")
                                        self.find_and_click_button("summon_cancel")
                                        
                                        # Now click the Back button.
                                        self.mouse_tools.move_and_click_point(self.attack_button_location[0] - 322, self.attack_button_location[1])
                                
                                # Continue to the next line for execution.
                                line_number += 1
                                i += 1

                if("end" in line):
                    # Attempt to find the "Next" Button first before attacking to preserve the turn number in the backend. If so, skip clicking the "Attack" Button.
                    # Otherwise, click the "Attack" Button, increment the turn number, and then attempt to find the "Next" Button.
                    next_button_location = self.image_tools.find_button("next", tries=1, suppress_error=self.suppress_error)
                    if(next_button_location != None):
                        self.print_and_save(f"{self.printtime()} [COMBAT] All enemies on screen have been eliminated before attacking. Preserving Turn {turn_number} by moving to the next Wave...")
                        if(self.debug_mode):
                            self.print_and_save(f"{self.printtime()} [DEBUG] Detected Next Button. Clicking it now...")

                        self.mouse_tools.move_and_click_point(next_button_location[0], next_button_location[1])
                        self.wait_for_ping(4)
                    else:
                        # Check if any character has 100% Charge Bar. If so, add 1 second per match.
                        number_of_charge_attacks = self.find_charge_attacks()
                        
                        self.print_and_save(f"{self.printtime()} [COMBAT] Ending Turn {turn_number} by attacking now...")

                        self.mouse_tools.move_and_click_point(self.attack_button_location[0], self.attack_button_location[1])
                        self.wait_for_ping(4 + number_of_charge_attacks)

                        turn_number += 1
                        
                        # Check to see if the party wiped.
                        self.party_wipe_check()
                        
                        next_button_location = self.image_tools.find_button("next", tries=1, suppress_error=self.suppress_error)
                        if(next_button_location != None):
                            if(self.debug_mode):
                                self.print_and_save(f"{self.printtime()} [DEBUG] Detected Next Button. Clicking it now...")

                            self.mouse_tools.move_and_click_point(next_button_location[0], next_button_location[1])
                            self.wait_for_ping(4)

                # Continue to the next line for execution.
                line_number += 1
                i += 1

                if (self.image_tools.confirm_location("exp_gained", tries=1) == True or self.retreat_check):
                    break

            self.print_and_save(f"\n{self.printtime()} [COMBAT] Bot has reached end of script. Auto-attacking until battle ends...")

            # Keep pressing the location of the "Attack" / "Next" Button until the bot reaches the Quest Results Screen.
            while (self.image_tools.confirm_location("exp_gained", tries=1) == False and not self.retreat_check):
                self.find_dialog_in_combat("lyria")
                self.find_dialog_in_combat("vyrn")

                attack_button_location = self.image_tools.find_button("attack", tries=1, suppress_error=self.suppress_error)
                next_button_location = self.image_tools.find_button("next", tries=1, suppress_error=self.suppress_error)

                if (attack_button_location != None):
                    self.print_and_save(f"\n{self.printtime()} [COMBAT] Starting Turn {turn_number}.")

                    # Check if any character has 100% Charge Bar. If so, add 1 second per match.
                    number_of_charge_attacks = self.find_charge_attacks()

                    self.print_and_save(f"{self.printtime()} [COMBAT] Ending Turn {turn_number} by attacking now...")

                    self.mouse_tools.move_and_click_point(self.attack_button_location[0], self.attack_button_location[1])
                    self.wait_for_ping(4 + number_of_charge_attacks)
                    
                    turn_number += 1
                    
                    # Check to see if the party wiped.
                    self.party_wipe_check()

                elif(next_button_location != None):
                    self.mouse_tools.move_and_click_point(next_button_location[0], next_button_location[1])
                    self.wait_for_ping(4)

            # Try to click any detected "OK" Buttons several times.
            if(not self.retreat_check):
                self.print_and_save(f"\n{self.printtime()} [INFO] Bot has reached the Quest Results Screen.")
                while (self.image_tools.confirm_location("loot_collected", tries=2) == False and not self.retreat_check):
                    ok_button_location = self.image_tools.find_button("ok", tries=1)
                    
                    # Check for any uncap messages and attempt to close those messages.
                    close_button_location = self.image_tools.find_button("friend_request_cancel", tries=1, suppress_error=True)

                    if(ok_button_location != None):
                        self.mouse_tools.move_and_click_point(ok_button_location[0], ok_button_location[1])
                        self.wait_for_ping(1)
                        
                    if(close_button_location != None):
                        self.mouse_tools.move_and_click_point(close_button_location[0], close_button_location[1])
                        self.wait_for_ping(1)

            self.print_and_save("\n################################################################################")
            self.print_and_save(f"{self.printtime()} [COMBAT] Ending Combat Mode.")
            self.print_and_save("################################################################################")
        except FileNotFoundError:
            sys.exit(f"\n{self.printtime()} [ERROR] Cannot find \"{script_file_path}.txt\" inside the /scripts folder. Exiting application now...")

        return True
    
    def start_farming_mode(self, summon_element_name: str, summon_name: str, group_number: int, party_number: int, map_mode: str, map_name: str, 
                           item_name: str, item_amount_to_farm: int, mission_name: str, use_full_elixirs: bool = False):
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
            use_full_elixirs (bool, optional): Will use Full Elixir instead of Half Elixir based on this. Defaults to False.
        
        Returns:
            None
        """
        if(item_name != "EXP"):
            self.print_and_save("\n\n################################################################################")
            self.print_and_save(f"{self.printtime()} [FARM] Starting Farming Mode.")
            self.print_and_save(f"{self.printtime()} [FARM] Farming {item_amount_to_farm}x {item_name}")
            self.print_and_save("################################################################################\n")
        else:
            self.print_and_save("\n\n################################################################################")
            self.print_and_save(f"{self.printtime()} [FARM] Starting Farming Mode.")
            self.print_and_save(f"{self.printtime()} [FARM] Doing {item_amount_to_farm}x runs for {item_name}")
            self.print_and_save("################################################################################\n")
        
        difficulty = ""
        
        if(map_mode.lower() == "special"):
            # Attempt to see if the difficulty starts at the 0th index to differentiate between cases like "H" and "VH".
            if(mission_name.find("N ") == 0):
                difficulty = "Normal"
            elif(mission_name.find("H ") == 0):
                difficulty = "Hard"
            elif(mission_name.find("VH ") == 0):
                difficulty = "Very Hard"
            elif(mission_name.find("EX ") == 0):
                difficulty = "Extreme"
        
        amount_of_runs_finished = 0
        item_amount_farmed = 0
        summon_check = False
        
        if((map_mode.lower() != "raid" and self.map_selection.select_map(map_mode, map_name, item_name, mission_name, difficulty)) or (map_mode.lower() == "raid" and self.map_selection.join_raid(item_name, mission_name))):
            # Keep playing the mission until the bot gains enough of the item specified.
            while(item_amount_farmed < item_amount_to_farm):
                while(summon_check == False): 
                    # Check for available AP.
                    self.check_for_ap(use_full_elixirs=use_full_elixirs)
                    
                    self.find_summon_element(summon_element_name)
                    summon_check = self.find_summon(summon_name)
                    
                    # If the Summons were reset, head back to the location of the mission.
                    if(summon_check == False):
                        if(map_mode.lower() != "raid"):
                            self.map_selection.select_map(map_mode, map_name, item_name, mission_name, difficulty)
                        else:
                            self.map_selection.join_raid(item_name, mission_name)
                
                # Select the Party specified and then start the mission.
                start_check = self.find_party_and_start_mission(group_number, party_number)
                
                if(start_check):
                    # Check for the Items Picked Up popup that appears after starting a Quest mission.
                    if(self.image_tools.confirm_location("items_picked_up", tries=3)):
                        self.find_and_click_button("ok")
                    
                    if(self.start_combat_mode(self.combat_script)):
                        # After Combat Mode has finished, count the number of the specified item that has dropped.
                        if(item_name != "EXP"):
                            temp_amount = self.image_tools.find_farmed_items([item_name])[0]
                            item_amount_farmed += temp_amount
                        else:
                            item_amount_farmed += 1
                            
                        amount_of_runs_finished += 1
                        
                        if(item_name != "EXP"):
                            self.print_and_save("\n\n********************************************************************************")
                            self.print_and_save(f"{self.printtime()} [FARM] Amount of {item_name} gained this run: {temp_amount}")
                            self.print_and_save(f"{self.printtime()} [FARM] Amount of {item_name} gained in total: {item_amount_farmed} / {item_amount_to_farm}")
                            self.print_and_save(f"{self.printtime()} [FARM] Amount of runs completed: {amount_of_runs_finished}")
                            self.print_and_save("********************************************************************************\n")
                        else:
                            self.print_and_save("\n\n********************************************************************************")
                            self.print_and_save(f"{self.printtime()} [FARM] Runs done for EXP in total: {item_amount_farmed} / {item_amount_to_farm}")
                            self.print_and_save("********************************************************************************\n")
                        
                        if(item_amount_farmed < item_amount_to_farm):
                            # Click the Play Again button.
                            self.find_and_click_button("play_again")
                            
                            # Loop while clicking any detected Cancel buttons like from Friend Request popups.
                            self.wait_for_ping(1)
                            while(self.image_tools.find_button("friend_request_cancel", tries=1, suppress_error=self.suppress_error) != None and not self.image_tools.confirm_location("not_enough_ap", tries=1)):
                                self.find_and_click_button("friend_request_cancel")
                            
                            # TODO: Check for available BP.
                            
                            
                            summon_check = False
                    else:
                        # If the Raid already ended while the bot was selecting a Summon and Party, go back to finding a new room code.
                        self.map_selection.select_map(map_mode, map_name, item_name, mission_name, difficulty)
        
        else:
            self.print_and_save("\nSomething went wrong with navigating to the map.")
            
        self.print_and_save("\n\n################################################################################")
        self.print_and_save(f"{self.printtime()} [FARM] Ending Farming Mode.")
        self.print_and_save("################################################################################\n")
        
        self.isBotRunning.value = 1
        
        return None

    # TODO: Find a suitable OCR framework that can detect the HP % of the enemies. Until then, this bot will not handle if statements.
    # TODO: Maybe have it be in-line? Example: if(enemy1.hp < 70): character1.useSkill(3),character2.useSkill(1).useSkill(4),character4.useSkill(1),end
    # def executeConditionalStatement(self, i, target, line, lines):
    #     whiteSpaceIndex = line.index(" ")
    #     operator = ""
    #     # Perform conditional matching to find what operator is being used. Account for the whitespaces before and after the operator.
    #     if(line[whiteSpaceIndex:(whiteSpaceIndex + 3)] == " < "):
    #         operator = "<"
    #         self.print_and_save("[DEBUG] Operator is <")
    #     elif(line[whiteSpaceIndex:(whiteSpaceIndex + 3)] == " > "):
    #         operator = ">"
    #         self.print_and_save("[DEBUG] Operator is >")
    #     elif(line[whiteSpaceIndex:(whiteSpaceIndex + 4)] == " <= "):
    #         operator = "<="
    #         self.print_and_save("[DEBUG] Operator is <=")
    #     elif(line[whiteSpaceIndex:(whiteSpaceIndex + 4)] == " >= "):
    #         operator = ">="
    #         self.print_and_save("[DEBUG] Operator is >=")
    #     elif(line[whiteSpaceIndex:(whiteSpaceIndex + 4)] == " == "):
    #         operator = "=="
    #         self.print_and_save("[DEBUG] Operator is ==")

    #     # Determine whether or not the conditional is met. If not, return the index right after the end for the if statement.

    #     # If conditional is met, execute each line until you hit end for the if statement.

    #     return i
