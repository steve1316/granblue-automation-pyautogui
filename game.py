import pyautogui
import time
import sys

import image_utils
import mouse_utils


class Game:
    def __init__(self, custom_mouse_speed: float = 0.5, debug_mode: bool = False):
        super().__init__()

        self.debug_mode = debug_mode
        self.image_tools = image_utils.ImageUtils(debug_mode=self.debug_mode)
        self.mouse_tools = mouse_utils.MouseUtils(
            mouse_speed=custom_mouse_speed, debug_mode=self.debug_mode)
        self.home_button_x = None
        self.home_button_y = None
        self.attack_button_x = None
        self.attack_button_y = None
        self.calibrate_game_window()

    def wait_for_ping(self, seconds: int = 3):
        """Wait the specified seconds to account for ping or loading.

        Args:
            seconds (int, optional): Number of seconds for the execution to wait for. Defaults to 3.

        Returns:
            None
        """
        time.sleep(seconds)
        return None

    def calibrate_game_window(self):
        """Recalibrate the dimensions of the game window for fast and accurate image matching.

        Returns:
            None
        """
        if(self.debug_mode):
            print(
                "\n[DEBUG] Recalibrating the dimensions of the game window...")

        self.home_button_x, self.home_button_y = self.image_tools.find_button(
            "home", sleep_time=1)

        # TODO: Recalibrate based on "News" Button together with "Home" Button potentially for smaller sized screens. Need to get to Home Screen first.
        self.image_tools.window_left = self.home_button_x - 439
        self.image_tools.window_top = self.home_button_y - 890
        self.image_tools.window_width = self.image_tools.window_left + 480
        self.image_tools.window_height = self.image_tools.window_top + 917

        if(self.debug_mode):
            print(
                f"\n[DEBUG] Screen size: {pyautogui.size()}.")
            print(
                f"[DEBUG] Game window size: Region({self.image_tools.window_left}, {self.image_tools.window_top}, {self.image_tools.window_width}, {self.image_tools.window_height}).")

        return None

    def go_back_home(self, confirm_location_check: bool = False):
        """Go back to the Home Screen to reset the bot's position. Also recalibrates the region dimensions of the game window.

        Args:
            confirm_location_check (bool, optional): Check to see if the location is correct. Defaults to False.

        Returns:
            None
        """
        if(self.debug_mode):
            print("\n[DEBUG] Moving back to the Home Screen...")

        self.calibrate_game_window()
        self.mouse_tools.move_and_click_point(
            self.home_button_x, self.home_button_y)
        if(confirm_location_check):
            self.image_tools.confirm_location("home")
        return None

    def find_summon_element(self, summon_element_name: str, tries: int = 3):
        """Select the specified element tab for summons. Search selected tabs first, then unselected tabs.

        # Todo: ALL images need to be segmented into Lite, Regular, and High to account for different Graphics Settings. Have not tested if confidence helps or not.

        Args:
            summon_element_name (str): Name of the summon element image file in the images/buttons/ folder.
            tries (int, optional): Number of tries before failing. Defaults to 3.

        Returns:
            (bool): True if successfully found and clicked the summon element tab. Otherwise, return False.
        """
        if(self.debug_mode):
            print(
                f"\n[DEBUG] Now attempting to find selected {summon_element_name.upper()} Summon Element tab...")

        summon_element_location = None

        while (summon_element_location == None):
            # See if the specified Element Summon tab is already selected.
            summon_element_location = self.image_tools.find_button(
                f"summon{summon_element_name}Selected", tries=1)

            # If searching for selected tabs did not work, search for unselected tabs.
            if (summon_element_location == None):
                if(self.debug_mode):
                    print(
                        f"[DEBUG] Could not locate the selected {summon_element_name.upper()} Summon Element tab. Trying again for unselected tab...")

                summon_element_location = self.image_tools.find_button(
                    f"summon{summon_element_name}", tries=1)

                if (summon_element_location == None):
                    tries -= 1
                    if (tries == 0):
                        print(
                            f"[ERROR] Failed to find {summon_element_name.upper()} Summon Element tab after several tries...")
                        return False

        if(self.debug_mode):
            print(
                f"[DEBUG] Locating {summon_element_name.upper()} Summon Element tab was successful. Clicking it now...")

        x, y = summon_element_location
        self.mouse_tools.move_and_click_point(x, y)
        return True

    def find_summon(self, summon_name: str):
        """Find the specified Summon on the Summon Selection Screen. Make sure to call this after the find_summon_element() method in order to have the correct Summon Element tab already selected.

        # TODO: Handle user-defined list of preferred summons going from most preferred to least.
        # TODO: If not found after a certain number of times, select very first Summon. Maybe have it as an option?

        Args:
            summon_name (str): Name of the Summon image's file name in images/summons folder.

        Returns:
            (bool): True if the Summon was found and clicked. Otherwise, return False.
        """
        tries = 3
        while(True):
            summon_location = self.image_tools.find_summon(
                summon_name, self.home_button_x, self.home_button_y)
            if (summon_location != None):
                x, y = summon_location
                self.mouse_tools.move_and_click_point(x, y)
                return True
            else:
                # If a Summon is not found, start a Trial Battle to refresh Summons.
                self.reset_summons()
                tries -= 1
                if (tries == 0):
                    break
        return False

    def reset_summons(self):
        """Reset the Summons available by starting and then retreating from a Trial Battle.

        Returns:
            None
        """
        self.go_back_home()
        self.mouse_tools.scroll_screen(
            self.home_button_x, self.home_button_y - 50, -600)

        list_of_steps_in_order = ["gameplayExtras", "trialBattles",
                                  "trialBattles_oldLignoid", "trialBattles_play",
                                  "wind", "partySelectionOK", "trialBattles_close",
                                  "menu", "retreat", "retreat_confirmation", "next"]

        # Go through each step in order from left to right.
        while (len(list_of_steps_in_order) > 0):
            image_name = list_of_steps_in_order.pop(0)
            x, y = self.image_tools.find_button(image_name)
            self.mouse_tools.move_and_click_point(x, y)
            if(image_name == "wind"):
                self.find_summon_element(image_name)
                self.mouse_tools.move_and_click_point(x, y + 140)
                self.wait_for_ping(5)
            elif (image_name == "retreat_confirmation"):
                self.wait_for_ping(3)
        return None

    def find_party_and_start_mission(self, group_number: int, party_number: int, tries: int = 3, sleep_time: int = 3):
        """Select the specified group and party. It will then start the mission.

        Args:
            group_number (int): The group that the specified party in in.
            party_number (int): The specified party to start the mission with.
            tries (int, optional): Number of tries before failing. Defaults to 3.
            sleep_time (int, optional): Number of seconds for execution to pause for in cases of image match fail. Defaults to 3.

        Returns:
            None
        """
        # Find the Group first. If the selected group number is less than 8, it is in Set A. Otherwise, it is in Set B. If failed,
        # alternate searching for Set A / Set B until found or tries are depleted.
        set_location = None
        if(group_number < 8):
            if(self.debug_mode):
                print(
                    f"\n[DEBUG] Now attempting to find Set A, Group {group_number}...")

            while (set_location == None):
                set_location = pyautogui.locateOnScreen(f"images/buttons/partySetA.png", confidence=self.image_tools.confidence, region=(
                    self.image_tools.window_left, self.image_tools.window_top, self.image_tools.window_width, self.image_tools.window_height))
                if (set_location == None):
                    if(self.debug_mode):
                        print(
                            f"[DEBUG] Locating Set A failed. Trying again...")

                    tries -= 1
                    if (tries == 0):
                        sys.exit(
                            f"[ERROR] Could not find Set A after several tries. Exiting Program...")

                    # See if the user had Set B active instead of Set A if matching failed.
                    set_location = pyautogui.locateOnScreen(f"images/buttons/partySetB.png", confidence=self.image_tools.confidence, region=(
                        self.image_tools.window_left, self.image_tools.window_top, self.image_tools.window_width, self.image_tools.window_height))

                    self.wait_for_ping(sleep_time)
        else:
            if(self.debug_mode):
                print(
                    f"\n[DEBUG] Now attempting to find Set B, Group {group_number}...")

            while (set_location == None):
                set_location = pyautogui.locateOnScreen(f"images/buttons/partySetB.png", confidence=self.image_tools.confidence, region=(
                    self.image_tools.window_left, self.image_tools.window_top, self.image_tools.window_width, self.image_tools.window_height))
                if (set_location == None):
                    if(self.debug_mode):
                        print(
                            f"[DEBUG] Locating Set B failed. Trying again...")

                    tries -= 1
                    if (tries == 0):
                        sys.exit(
                            f"[ERROR] Could not find Set B after several tries. Exiting Program...")

                    # See if the user had Set A active instead of Set B if matching failed.
                    set_location = pyautogui.locateOnScreen(f"images/buttons/partySetA.png", confidence=self.image_tools.confidence, region=(
                        self.image_tools.window_left, self.image_tools.window_top, self.image_tools.window_width, self.image_tools.window_height))

                    self.wait_for_ping(sleep_time)

        if(self.debug_mode):
            print(
                f"[DEBUG] Successfully found the correct Set. Now selecting Group {group_number}...")

        # Center the mouse on the Set A / Set B Button and then click the correct Group Number Tab.
        x, y = pyautogui.center(set_location)
        if(group_number == 1):
            self.mouse_tools.click_point_instantly(
                x - 350, y + 50)
        elif(group_number == 2):
            self.mouse_tools.click_point_instantly(
                x - 290, y + 50)
        elif(group_number == 3):
            self.mouse_tools.click_point_instantly(
                x - 230, y + 50)
        elif(group_number == 4):
            self.mouse_tools.click_point_instantly(
                x - 170, y + 50)
        elif(group_number == 5):
            self.mouse_tools.click_point_instantly(
                x - 110, y + 50)
        elif(group_number == 6):
            self.mouse_tools.click_point_instantly(
                x - 50, y + 50)
        else:
            self.mouse_tools.click_point_instantly(
                x + 10, y + 50)

        # Now select the correct Party.
        if(self.debug_mode):
            print(
                f"[DEBUG] Successfully found Group {group_number}. Now selecting Party {party_number}...")
        if(party_number == 1):
            self.mouse_tools.click_point_instantly(x - 309, y + 325)
        elif(party_number == 2):
            self.mouse_tools.click_point_instantly(x - 252, y + 325)
        elif(party_number == 3):
            self.mouse_tools.click_point_instantly(x - 195, y + 325)
        elif(party_number == 4):
            self.mouse_tools.click_point_instantly(x - 138, y + 325)
        elif(party_number == 5):
            self.mouse_tools.click_point_instantly(x - 81, y + 325)
        elif(party_number == 6):
            self.mouse_tools.click_point_instantly(x - 24, y + 325)

        if(self.debug_mode):
            print(
                f"[DEBUG] Successfully selected Party {party_number}. Now starting the mission.")

        # Find the "OK" Button to start the mission.
        self.wait_for_ping(1)
        ok_button_location = self.image_tools.find_button("partySelectionOK")
        self.mouse_tools.move_and_click_point(
            ok_button_location[0], ok_button_location[1])
        self.wait_for_ping(5)

        return None

    # TODO: Find a suitable OCR framework that can detect the HP % of the enemies. Until then, this bot will not handle if statements.
    # TODO: Maybe have it be in-line? Example: if(enemy1.hp < 70): character1.useSkill(3),character2.useSkill(1).useSkill(4),character4.useSkill(1),end
    # def executeConditionalStatement(self, i, target, line, lines):
    #     whiteSpaceIndex = line.index(" ")
    #     operator = ""
    #     # Perform conditional matching to find what operator is being used. Account for the whitespaces before and after the operator.
    #     if(line[whiteSpaceIndex:(whiteSpaceIndex + 3)] == " < "):
    #         operator = "<"
    #         print("[DEBUG] Operator is <")
    #     elif(line[whiteSpaceIndex:(whiteSpaceIndex + 3)] == " > "):
    #         operator = ">"
    #         print("[DEBUG] Operator is >")
    #     elif(line[whiteSpaceIndex:(whiteSpaceIndex + 4)] == " <= "):
    #         operator = "<="
    #         print("[DEBUG] Operator is <=")
    #     elif(line[whiteSpaceIndex:(whiteSpaceIndex + 4)] == " >= "):
    #         operator = ">="
    #         print("[DEBUG] Operator is >=")
    #     elif(line[whiteSpaceIndex:(whiteSpaceIndex + 4)] == " == "):
    #         operator = "=="
    #         print("[DEBUG] Operator is ==")

    #     # Determine whether or not the conditional is met. If not, return the index right after the end for the if statement.

    #     # If conditional is met, execute each line until you hit end for the if statement.

    #     return i

    def select_character(self, character_number: int):
        """Selects the portrait of the character specified on the screen.

        Args:
            character_number (int): The character that needs to be selected from the Combat Screen.

        Returns:
            None
        """

        if(self.debug_mode):
            print(
                f"[DEBUG] Attack Button location: ({self.attack_button_x}, {self.attack_button_y})")

        # Click the portrait of the specified character.
        if(character_number == 1):
            self.mouse_tools.click_point_instantly(
                self.attack_button_x - 317, self.attack_button_y + 123)
        elif(character_number == 2):
            self.mouse_tools.click_point_instantly(
                self.attack_button_x - 240, self.attack_button_y + 123)
        elif(character_number == 3):
            self.mouse_tools.click_point_instantly(
                self.attack_button_x - 158, self.attack_button_y + 123)
        elif(character_number == 4):
            self.mouse_tools.click_point_instantly(
                self.attack_button_x - 76, self.attack_button_y + 123)

        self.wait_for_ping(2)

        return None

    def use_character_skill(self, character_selected: int, skill: int):
        """Activate the skill specified for the already selected character.

        Args:
            character_selected (int): The character whose skill needs to be used.
            skill (int): The skill that needs to be used.

        Returns:
            None
        """
        # Matches the str occurence to which skill the bot needs to select.
        if("useSkill(1)" in skill):
            print(f"[COMBAT] Character {character_selected} uses Skill 1")
            self.mouse_tools.click_point_instantly(
                self.attack_button_x - 213, self.attack_button_y + 171)
        elif("useSkill(2)" in skill):
            print(f"[COMBAT] Character {character_selected} uses Skill 2")
            self.mouse_tools.click_point_instantly(
                self.attack_button_x - 132, self.attack_button_y + 171)
        elif("useSkill(3)" in skill):
            print(f"[COMBAT] Character {character_selected} uses Skill 3")
            self.mouse_tools.click_point_instantly(
                self.attack_button_x - 51, self.attack_button_y + 171)
        elif("useSkill(4)" in skill):
            print(f"[COMBAT] Character {character_selected} uses Skill 4")
            self.mouse_tools.click_point_instantly(
                self.attack_button_x + 39, self.attack_button_y + 171)

        self.wait_for_ping(2)
        return None

    def find_charge_attacks(self):
        """Find total number of characters ready to Charge Attack.

        Returns:
            number_of_charge_attacks (int): Total number of image matches found for charge attacks.
        """
        # Check if any character has 100% Charge Bar. If so, add 1 second per match.
        number_of_charge_attacks = 0
        list_of_charge_attacks = list(pyautogui.locateAllOnScreen("images/fullCharge.png", region=(
            self.attack_button_x - 356, self.attack_button_y + 67, self.attack_button_x - 40, self.attack_button_y + 214)))

        number_of_charge_attacks = len(list_of_charge_attacks)
        return number_of_charge_attacks

    def find_dialog_in_combat(self, dialog_file_name: str):
        """Check if there are dialog boxes from either Lyria or Vyrn and click them away.

        Args:
            dialog_file_name (str): Image file name of the dialog window. Usually its "lyriaDialog" or "vyrnDialog" for the Combat Screen.

        Returns:
            None
        """
        dialog_location = self.image_tools.find_dialog(
            dialog_file_name, self.attack_button_x, self.attack_button_y, tries=1)

        if (dialog_location != None):
            if(self.debug_mode):
                print(
                    "[DEBUG] Detected dialog window from Lyria/Vyrn on Combat Screen. Closing it now...")

            dialog_x, dialog_y = dialog_location
            self.mouse_tools.click_point_instantly(
                dialog_x + 180, dialog_y - 51)

        return None

    # Start the Combat Mode with the given script name. Start reading through the text file line by line and have the bot proceed accordingly.
    def start_combat_mode(self, script_name: str):

        # Recalibrate the game window.
        self.calibrate_game_window()

        # Open the script text file and process all read lines.
        try:
            script = open(f"scripts/{script_name}.txt", "r")
            if(self.debug_mode):
                print(f"\n[DEBUG] Now loading up {script_name} Combat Plan.")
            lines = script.readlines()

            print("\n[COMBAT] Starting combat script.")

            i = 0  # Index for the list of read lines from the script.
            line_number = 1  # Tells what line number the bot is reading.
            turn_number = 1  # Tells current turn for the script execution.

            # Loop through and execute each line in the combat script until EOF.
            while(i <= len(lines)):
                line = lines[i]

                # Print each line read if debug mode is active.
                if(line[0] != "#" and line[0] != "/" and line.strip() != ""):
                    if(self.debug_mode):
                        print(f"[DEBUG] Line {line_number}: {line.strip()}")
                # else:
                #     line_number += 1

                # Save the position of the center of the "Attack" Button. If already found, don't call this again.
                if(self.attack_button_x == None or self.attack_button_y == None):
                    attack_button_location = self.image_tools.find_button(
                        "attack")
                    self.attack_button_x, self.attack_button_y = attack_button_location

                # Check if there are any dialog windows are open.
                self.find_dialog_in_combat("lyriaDialog")
                self.find_dialog_in_combat("vyrnDialog")

                # If the execution reached the next turn block and it is currently not the correct turn, keep pressing the "Attack" Button until the turn number matches.
                if ("turn" in line.lower() and int(line[5]) != turn_number):
                    if(self.debug_mode):
                        print(
                            f"\n[DEBUG] Current Turn Number {turn_number} does not match expected Turn Number {line[5]}. Pressing Attack Button until they do.")

                    while (int(line[5]) != turn_number):
                        attack_button_location = self.image_tools.find_button(
                            "attack", tries=1)
                        if (attack_button_location != None):
                            number_of_charge_attacks = self.find_charge_attacks()
                            print(
                                f"[COMBAT] Number of Characters ready to ougi: {number_of_charge_attacks}")

                            if (self.debug_mode):
                                print(
                                    f"[DEBUG] Clicking Attack Button to end the current turn and waiting several seconds.")

                            self.mouse_tools.click_point_instantly(
                                self.attack_button_x, self.attack_button_y)

                            self.wait_for_ping(5 + number_of_charge_attacks)
                            turn_number += 1
                        elif(attack_button_location == None):
                            # Try to find the "Next" Button only once per turn.
                            next_button_location = self.image_tools.find_button(
                                "next", tries=1)
                            if(next_button_location != None):
                                if(self.debug_mode):
                                    print(
                                        f"[DEBUG] Detected the Next Button. Clicking it now...")

                                next_button_x, next_button_y = next_button_location
                                self.mouse_tools.click_point_instantly(
                                    next_button_x, next_button_y)

                                self.wait_for_ping(5)
                        else:
                            self.wait_for_ping(1)

                # If it is the start of the Turn and it is currently the correct turn, grab the next line for execution.
                if("turn" in line.lower() and int(line[5]) == turn_number):
                    print(f"\n[COMBAT] Beginning Turn {line[5]}.\n")
                    i += 1
                    line_number += 1

                    # Loop while searching for the "Attack" Button signaling to the bot that the game is ready for input. Meanwhile, look out for dialog windows from Lyria and Vyrn.
                    # while (self.image_tools.find_button("attack", tries=1) == None):
                    #     # Check if there are any dialog windows are open.
                    #     self.find_dialog_in_combat("lyriaDialog")
                    #     self.find_dialog_in_combat("vyrnDialog")

                    self.find_dialog_in_combat("lyriaDialog")
                    self.find_dialog_in_combat("vyrnDialog")

                    # Continue reading each line inside the Turn block until you reach the "end" occurrence.
                    while("end" not in line):
                        # Strip any leading and trailing whitespaces.
                        line = lines[i].strip()

                        # Print each line read if debug mode is active.
                        if(line[0] != "#" and line[0] != "/" and line.strip() != ""):
                            if(self.debug_mode):
                                print(
                                    f"[DEBUG] Line {line_number}: {line.strip()}")

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

                        # Now perform the skill specified in the read str.
                        # TODO: Handle enemy targeting here as well.
                        if(character_selected != 0):
                            # Select the character specified.
                            print(
                                f"[COMBAT] Character {character_selected} acts.")
                            self.select_character(character_selected)

                            # Get all occurrences of "useSkill" and then remove the first element as that is usually the "character#" substr. Then execute each skill from left to right.
                            skills = line.split(".")
                            skills.pop(0)
                            for skill in skills:
                                self.use_character_skill(
                                    character_selected, skill)

                            # Now click the Back button.
                            self.mouse_tools.click_point_instantly(
                                self.attack_button_x - 322, self.attack_button_y)

                            # Increment the following by 1 and continue to the next line for execution.
                            line_number += 1
                            i += 1

                            self.wait_for_ping(1)

                if("end" in line):
                    # Increment by 1 to move to the next line for execution. After that, hit the "Attack" Button to end the turn.
                    # Note: The execution at this point will increment by 2 because of the incrementation after this elif statement so it is imperative that scripts have a space in between "end" and "Turn #:".
                    turn_number += 1
                    i += 1

                    # Check if any character has 100% Charge Bar. If so, add 1 second per match.
                    number_of_charge_attacks = self.find_charge_attacks()
                    print(
                        f"[COMBAT] Number of Characters ready to ougi: {number_of_charge_attacks}")

                    if (self.debug_mode):
                        print(
                            f"[DEBUG] Clicking Attack Button to end the current turn and waiting several seconds.")

                    self.mouse_tools.click_point_instantly(
                        self.attack_button_x, self.attack_button_y)
                    self.wait_for_ping(5 + number_of_charge_attacks)

                    # Try to find the "Next" Button only once per turn.
                    next_button_location = self.image_tools.find_button(
                        "next", tries=1)
                    if(next_button_location != None):
                        if(self.debug_mode):
                            print(
                                f"[DEBUG] Detected Next Button. Clicking it now...")

                        next_button_x, next_button_y = next_button_location
                        self.mouse_tools.click_point_instantly(
                            next_button_x, next_button_y)

                        self.wait_for_ping(5)

                # Increment by 1 to move to the next line for execution.
                line_number += 1
                i += 1

            print(
                "\n[COMBAT] Bot has reached end of script. Pressing the Attack Button until battle ends.")

            # Keep pressing the location of the "Attack" / "Next" Button until the bot reaches the Quest Results Screen.
            while (self.image_tools.confirm_location("expGained", tries=1) == False):
                # Check if there are any dialog windows are open.
                self.find_dialog_in_combat("lyriaDialog")
                self.find_dialog_in_combat("vyrnDialog")

                attack_button_location = self.image_tools.find_button(
                    "attack", tries=1)
                if (attack_button_location != None):
                    # Check if any character has 100% Charge Bar. If so, add 1 second per match.
                    number_of_charge_attacks = self.find_charge_attacks()

                    print(
                        f"[COMBAT] Number of Characters ready to ougi: {number_of_charge_attacks}")

                    self.mouse_tools.click_point_instantly(
                        self.attack_button_x, self.attack_button_y)
                    self.wait_for_ping(7 + number_of_charge_attacks)
                else:
                    next_button_location = self.image_tools.find_button(
                        "next", tries=1)
                    if(next_button_location != None):
                        self.mouse_tools.click_point_instantly(
                            self.attack_button_x + 50, self.attack_button_y)
                        self.wait_for_ping(5)

            # Try to click any detected "OK" Buttons several times.
            print("[INFO] Bot has reached the Quest Results Screen.")
            while (self.image_tools.confirm_location("lootCollected", tries=1) == False):
                # Check if there are any dialog windows are open.
                self.find_dialog_in_combat("lyriaDialog")
                self.find_dialog_in_combat("vyrnDialog")

                ok_button_location = self.image_tools.find_button(
                    "questResultsOK", tries=3)
                if(ok_button_location != None):
                    self.mouse_tools.move_and_click_point(
                        ok_button_location[0], ok_button_location[1])

                self.wait_for_ping(2)

            print(
                f"\n[COMBAT] Combat is over.")

        except FileNotFoundError as e:
            print(
                f"[ERROR] Cannot find \"{script_name}.txt\" inside the /scripts folder.")

    def test_combat_mode(self):
        """Tests almost all of the bot's functionality by starting the Combat Mode by starting the Normal difficulty Angel Halo Special Battle and completing it. This assumes that Angel Halo is at the very bottom of the Special missions list. 

        Returns:
            None
        """
        print(
            "\n[TEST] Testing Combat Mode on Normal Difficulty Angel Halo mission now...")

        summon_check = False
        while(summon_check == False):
            # First go to the Home Screen and calibrate the dimensions of the game window. Then navigation will be as follows: Home Screen -> Quest Screen -> Special Screen.
            self.go_back_home()
            list_of_button_names = ["quest", "special"]
            for button_name in list_of_button_names:
                x, y = self.image_tools.find_button(button_name)
                self.mouse_tools.move_and_click_point(x, y)

            # Attempt to fit all the "Select" buttons into the current view and then find all "Select" Buttons.
            print("\n[TEST] Finding all Special Select Buttons...")
            self.image_tools.confirm_location("special")
            self.mouse_tools.scroll_screen(
                self.home_button_x, self.home_button_y - 50, -300)
            self.wait_for_ping(1)
            list_of_select_button_locations = list(pyautogui.locateAllOnScreen("images/buttons/select.png",
                                                                               region=(self.image_tools.window_left, self.image_tools.window_top, self.image_tools.window_width, self.image_tools.window_height)))

            # Select the Angel Halo mission.
            print("\n[TEST] Now selecting Angel Halo mission...")
            angel_halo_mission = pyautogui.center(
                list_of_select_button_locations.pop())
            print("Here:", angel_halo_mission)
            self.mouse_tools.move_and_click_point(
                angel_halo_mission[0], angel_halo_mission[1])
            self.wait_for_ping(2)

            # Click on Play and head to the Summon Selection Screen.
            print("\n[TEST] Moving to Normal Difficulty Angel Halo...")
            self.image_tools.confirm_location("angelHalo")
            list_of_special_play_button_locations = list(pyautogui.locateAllOnScreen("images/buttons/specialPlay.png",
                                                                                     region=(self.image_tools.window_left, self.image_tools.window_top, self.image_tools.window_width, self.image_tools.window_height)))
            normal_difficulty_mission = pyautogui.center(list_of_special_play_button_locations.pop(
                0))
            self.mouse_tools.move_and_click_point(
                normal_difficulty_mission[0], normal_difficulty_mission[1])
            self.image_tools.confirm_location("selectSummon")

            # Locate Dark summons and click on the first ULB Bahamut.
            print("\n[TEST] Selecting the first found ULB Bahamut Summon...")
            self.find_summon_element("dark")
            summon_check = self.find_summon("bahamutULB")

        # Select first Group, second Party.
        print("\n[TEST] Selecting First Group, Second Party...")
        self.find_party_and_start_mission(1, 2)

        # Start the Combat Mode.
        self.start_combat_mode("test_combat_mode")

        return None
