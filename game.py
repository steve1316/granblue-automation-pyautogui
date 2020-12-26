import datetime
import multiprocessing
import sys
import time
from timeit import default_timer as timer

import pyautogui

from image_utils import ImageUtils
from map_selection import MapSelection
from mouse_utils import MouseUtils


class Game:
    """
    Main driver for bot activity and navigation for the web game, Granblue Fantasy.

    Attributes
    ----------
    queue (multiprocessing.Queue): Queue to keep track of logging messages to share between backend and frontend.

    isBotRunning (int): Flag in shared memory that signals the frontend that the bot has finished/exited.
    
    custom_mouse_speed (float, optional): The speed at which the mouse moves at. Defaults to 0.5.

    debug_mode (bool, optional): Optional flag to print debug messages related to this class. Defaults to True.

    """

    def __init__(self, queue: multiprocessing.Queue, isBotRunning: int, custom_mouse_speed: float = 0.5, debug_mode: bool = False):
        super().__init__()

        # Start a timer signaling bot start in order to keep track of elapsed time in logging messages.
        self.starting_time = timer()

        # Queue to keep share logging messages between backend and frontend.
        self.queue = queue
        self.isBotRunning = isBotRunning
        
        # Initialize the Map Selection class.
        self.map_selection = MapSelection(self)

        # Set a debug flag to determine whether or not to print debugging messages.
        self.debug_mode = debug_mode
        
        self.image_tools = ImageUtils(game=self, starting_time=self.starting_time, debug_mode=self.debug_mode)
        self.mouse_tools = MouseUtils(game=self, starting_time=self.starting_time, mouse_speed=custom_mouse_speed, debug_mode=self.debug_mode)
        
        # Save the locations of the "Home" and "Attack" buttons for use in other classes.
        self.home_button_location = None
        self.attack_button_location = None

        # The amount of time to pause after each call to pyautogui. This applies to calls inside mouse_utils and image_utils.
        pyautogui.PAUSE = 1.0

        # Calibrate the dimensions of the game window on bot launch.
        self.calibrate_game_window()

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

        self.image_tools.window_left = self.home_button_location[0] - 439
        self.image_tools.window_top = self.home_button_location[1] - 890
        self.image_tools.window_width = self.image_tools.window_left + 480
        self.image_tools.window_height = self.image_tools.window_top + 917

        if(self.debug_mode):
            self.print_and_save(f"\n{self.printtime()} [SUCCESS] Dimensions of the game window has been successfully recalibrated.")

        if(display_info_check):
            self.print_and_save("\n\n********************************************************************************")
            self.print_and_save(f"{self.printtime()} [INFO] Screen size: {pyautogui.size()}.")
            self.print_and_save(f"{self.printtime()} [INFO] Game window size: Region({self.image_tools.window_left}, {self.image_tools.window_top}, {self.image_tools.window_width}, {self.image_tools.window_height}).")
            self.print_and_save("********************************************************************************\n")

        return None

    def go_back_home(self, confirm_location_check: bool = False, display_info_check: bool = False):
        """Go back to the Home Screen to reset the bot's position. Also recalibrates the region dimensions of the game window.

        Args:
            confirm_location_check (bool, optional): Check to see if the location is correct. Defaults to False.
            display_info_check (bool, optional): Display display size of screen and game window size. Defaults to False.

        Returns:
            None
        """
        if(self.debug_mode):
            self.print_and_save(f"\n{self.printtime()} [DEBUG] Moving back to the Home Screen...")

        if (display_info_check):
            self.calibrate_game_window(display_info_check=True)
        else:
            self.calibrate_game_window()

        # After recalibrating the dimensions of the game window, click the "Home" button.
        self.mouse_tools.move_and_click_point(self.home_button_location[0], self.home_button_location[1])

        if(confirm_location_check):
            self.image_tools.confirm_location("home")

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
            
            # TODO: Inform user that bot has found summon.

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
        self.mouse_tools.scroll_screen(self.home_button_location[0], self.home_button_location[1] - 50, -500)

        list_of_steps_in_order = ["gameplay_extras", "trial_battles",
                                  "trial_battles_old_lignoid", "trial_battles_play",
                                  "wind", "party_selection_ok", "trial_battles_close",
                                  "menu", "retreat", "retreat_confirmation", "next"]

        temp_location = None

        # Go through each step in order from left to right.
        while (len(list_of_steps_in_order) > 0):
            image_name = list_of_steps_in_order.pop(0)
            
            if(image_name != "wind"):
                temp_location = self.image_tools.find_button(image_name)
                self.mouse_tools.move_and_click_point(temp_location[0], temp_location[1])
            else:
                self.find_summon_element(image_name)

                # This will use the temp_location coordinates of the last location which was the Play button for the Trial Battle.
                self.mouse_tools.move_and_click_point(temp_location[0], temp_location[1] + 140)

        self.print_and_save(f"\n{self.printtime()} [INFO] Summons have now been refreshed.")
        return None

    def find_party_and_start_mission(self, group_number: int, party_number: int, tries: int = 3):
        """Select the specified group and party. It will then start the mission.

        Args:
            group_number (int): The group that the specified party in in.
            party_number (int): The specified party to start the mission with.
            tries (int, optional): Number of tries before failing. Defaults to 3.

        Returns:
            None
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

        self.mouse_tools.click_point_instantly(x, y)

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

        self.mouse_tools.click_point_instantly(x, y)

        if(self.debug_mode):
            self.print_and_save(f"\n{self.printtime()} [SUCCESS] Successfully selected Party {party_number}. Now starting the mission.")

        # Find and click the "OK" Button to start the mission.
        self.wait_for_ping(1)
        ok_button_location = self.image_tools.find_button("party_selection_ok")
        
        self.mouse_tools.move_and_click_point(ok_button_location[0], ok_button_location[1])
        self.wait_for_ping(5)

        return None

    def find_charge_attacks(self):
        """Find total number of characters ready to Charge Attack.

        Returns:
            number_of_charge_attacks (int): Total number of image matches found for charge attacks.
        """
        number_of_charge_attacks = 0
        list_of_charge_attacks = self.image_tools.find_all("full_charge", custom_region=(self.attack_button_location[0] - 356, self.attack_button_location[1] + 67, 
                                                                                         self.attack_button_location[0] - 40, self.attack_button_location[1] + 214))

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

            self.mouse_tools.click_point_instantly(dialog_location[0] + 180, dialog_location[1] - 51)

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

        self.mouse_tools.click_point_instantly(x, y)
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

        self.mouse_tools.click_point_instantly(x, y)
        self.wait_for_ping(2)

        return None

    def start_combat_mode(self, script_name: str):
        """Start the Combat Mode with the given script file name. Start reading through the text file line by line and have the bot proceed accordingly.

        Args:
            script_name (str): Name of the combat script text file in the /scripts/ folder.

        Returns:
            (bool): Return True if Combat Mode was successful. #TODO: Return False if the party wiped.
        """
        # Recalibrate the game window.
        self.calibrate_game_window()

        # Open the script text file and process all read lines.
        try:
            script = open(f"scripts/{script_name}.txt", "r")
            if(self.debug_mode):
                self.print_and_save(f"\n{self.printtime()} [DEBUG] Now loading up {script_name} Combat Plan.")
            
            lines = script.readlines()

            self.print_and_save("\n\n################################################################################")
            self.print_and_save(f"{self.printtime()} [COMBAT] Starting Combat Mode.")
            self.print_and_save("################################################################################\n")

            i = 0  # Index for the list of read lines from the script.
            line_number = 1  # Tells what line number the bot is reading.
            turn_number = 1  # Tells current turn for the script execution.

            # Flag to suppress error messages in attempts to finding the "Attack" / "Next" Buttons.
            suppress_error = True

            # Loop through and execute each line in the combat script until EOF.
            while(i != len(lines)):
                line = lines[i]

                # Print each line read if debug mode is active.
                if(line[0] != "#" and line[0] != "/" and line.strip() != ""):
                    if(self.debug_mode):
                        self.print_and_save(f"\n{self.printtime()} [DEBUG] Reading Line {line_number}: \"{line.strip()}\"")

                # Save the position of the center of the "Attack" Button. If already found, don't call this again.
                if(self.attack_button_location == None):
                    self.attack_button_location = self.image_tools.find_button("attack", suppress_error=suppress_error)

                # If the execution reached the next turn block and it is currently not the correct turn, keep pressing the "Attack" Button until the turn number matches.
                if ("turn" in line.lower() and int(line[5]) != turn_number):
                    while (int(line[5]) != turn_number):
                        self.print_and_save(f"\n{self.printtime()} [COMBAT] Starting Turn {turn_number}.")

                        self.find_dialog_in_combat("lyria")
                        self.find_dialog_in_combat("vyrn")

                        attack_button_location = self.image_tools.find_button("attack", tries=1, suppress_error=suppress_error)

                        if (attack_button_location != None):
                            number_of_charge_attacks = self.find_charge_attacks()
                            
                            self.print_and_save(f"{self.printtime()} [COMBAT] Ending Turn {turn_number} by attacking now...")

                            self.mouse_tools.click_point_instantly(self.attack_button_location[0], self.attack_button_location[1])
                            self.wait_for_ping(6 + number_of_charge_attacks)
                            
                            turn_number += 1

                            # Try to find the "Next" Button only once per turn.
                            next_button_location = self.image_tools.find_button("next", tries=1, suppress_error=suppress_error)
                            if(next_button_location != None):
                                if(self.debug_mode):
                                    self.print_and_save(f"{self.printtime()} [DEBUG] Detected the Next Button. Clicking it now...")

                                self.mouse_tools.click_point_instantly(next_button_location[0], next_button_location[1])
                                self.wait_for_ping(6)

                # If it is the start of the Turn and it is currently the correct turn, grab the next line for execution.
                if ("turn" in line.lower() and int(line[5]) == turn_number):
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
                            self.mouse_tools.click_point_instantly(self.attack_button_location[0] - 322, self.attack_button_location[1])

                            # Continue to the next line for execution.
                            line_number += 1
                            i += 1

                if("end" in line):
                    # Check if any character has 100% Charge Bar. If so, add 1 second per match.
                    number_of_charge_attacks = self.find_charge_attacks()
                    
                    self.print_and_save(f"{self.printtime()} [COMBAT] Ending Turn {turn_number} by attacking now...")

                    self.mouse_tools.click_point_instantly(self.attack_button_location[0], self.attack_button_location[1])
                    self.wait_for_ping(6 + number_of_charge_attacks)

                    turn_number += 1

                    # Try to find the "Next" Button only once per turn.
                    next_button_location = self.image_tools.find_button("next", tries=1, suppress_error=suppress_error)
                    if(next_button_location != None):
                        if(self.debug_mode):
                            self.print_and_save(f"{self.printtime()} [DEBUG] Detected Next Button. Clicking it now...")

                        self.mouse_tools.click_point_instantly(next_button_location[0], next_button_location[1])
                        self.wait_for_ping(6)

                # Continue to the next line for execution.
                line_number += 1
                i += 1

                if (self.image_tools.confirm_location("exp_gained", tries=1) == True):
                    break

            self.print_and_save(f"\n{self.printtime()} [COMBAT] Bot has reached end of script. Auto-attacking until battle ends...")

            # Keep pressing the location of the "Attack" / "Next" Button until the bot reaches the Quest Results Screen.
            while (self.image_tools.confirm_location("exp_gained", tries=1) == False):
                self.find_dialog_in_combat("lyria")
                self.find_dialog_in_combat("vyrn")

                attack_button_location = self.image_tools.find_button("attack", tries=1, suppress_error=suppress_error)
                next_button_location = self.image_tools.find_button("next", tries=1, suppress_error=suppress_error)

                if (attack_button_location != None):
                    self.print_and_save(f"\n{self.printtime()} [COMBAT] Starting Turn {turn_number}.")

                    # Check if any character has 100% Charge Bar. If so, add 1 second per match.
                    number_of_charge_attacks = self.find_charge_attacks()

                    self.print_and_save(f"{self.printtime()} [COMBAT] Ending Turn {turn_number} by attacking now...")

                    self.mouse_tools.click_point_instantly(self.attack_button_location[0], self.attack_button_location[1])
                    self.wait_for_ping(6 + number_of_charge_attacks)
                    
                    turn_number += 1

                elif(next_button_location != None):
                    self.mouse_tools.click_point_instantly(self.attack_button_location[0] + 50, self.attack_button_location[1])
                    self.wait_for_ping(6)

            # Try to click any detected "OK" Buttons several times.
            self.print_and_save(f"\n{self.printtime()} [INFO] Bot has reached the Quest Results Screen.")
            while (self.image_tools.confirm_location("loot_collected", tries=1) == False):
                ok_button_location = self.image_tools.find_button("quest_results_ok", tries=1)

                # TODO: Look for "Close" Buttons here as well in case of reaching uncap.

                if(ok_button_location != None):
                    self.mouse_tools.move_and_click_point(ok_button_location[0], ok_button_location[1])
                    self.wait_for_ping(1)

            self.print_and_save("\n################################################################################")
            self.print_and_save(f"{self.printtime()} [COMBAT] Ending Combat Mode.")
            self.print_and_save("################################################################################")
        except FileNotFoundError:
            sys.exit(f"\n{self.printtime()} [ERROR] Cannot find \"{script_name}.txt\" inside the /scripts folder. Exiting application now...")

        return True
    
    def start_farming_mode(self, summon_element_name: str, summon_name: str, group_number: int, party_number: int, script_name: str, map_mode: str, map_name: str, item_name: str, item_amount_to_farm: int, mission_name: str):
        if(self.map_selection.select_map(map_mode, map_name, item_name, mission_name)):
            amount_of_runs_finished = 0
            item_amount_farmed = 0
            while(item_amount_farmed < item_amount_to_farm):
                self.find_summon_element(summon_element_name)
                self.find_summon(summon_name)
                
                self.find_party_and_start_mission(group_number, party_number)
                
                if(self.image_tools.confirm_location("items_picked_up", tries=3)):
                    location = self.image_tools.find_button("items_picked_up_ok")
                    self.mouse_tools.move_and_click_point(location[0], location[1])
                
                if(self.start_combat_mode(script_name)):
                    temp_amount = self.image_tools.find_farmed_items([item_name])[0]
                    item_amount_farmed += temp_amount
                    
                    self.print_and_save(f"\nAmount gained this run: {temp_amount}")
                    self.print_and_save(f"Amount gained in total: {item_amount_farmed}")
                    
                    if(item_amount_farmed < item_amount_to_farm):
                        location = self.image_tools.find_button("play_again")
                        self.mouse_tools.move_and_click_point(location[0], location[1])
                        
                        # TODO: Add check for not enough AP.
                        
                        if(self.image_tools.confirm_location("friend_request")):
                            location = self.image_tools.find_button("friend_request_cancel")
                            self.mouse_tools.move_and_click_point(location[0], location[1])

                amount_of_runs_finished += 1
                self.print_and_save(f"\nAmount of runs completed: {amount_of_runs_finished}")
        else:
            self.print_and_save("\nSomething went wrong with navigating to the map.")
            
        self.isBotRunning.value = 1

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
