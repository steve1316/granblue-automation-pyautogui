import os
import traceback
from typing import List

from bot.game import Game


class CombatMode:
    def __init__(self, game: Game, idle_seconds_after_skill: int, idle_seconds_after_summon: int, is_bot_running: int, debug_mode: bool = False):
        super().__init__()

        self._game = game

        # Save a reference to the original current working directory.
        self._owd = os.getcwd()

        # Save some variables for use throughout the class.
        self._idle_seconds_after_skill = idle_seconds_after_skill
        self._idle_seconds_after_summon = idle_seconds_after_summon
        self._attack_button_location = None
        self._back_button_location = None
        self._retreat_check = False
        self._is_bot_running = is_bot_running
        self._debug_mode = debug_mode

    def _party_wipe_check(self):
        """Check to see if the Party has wiped during Combat Mode. Update the retreat check flag if so.

        Returns:
            None
        """
        # Check to see if Party has wiped.
        if self._debug_mode:
            self._game.print_and_save(f"\n[DEBUG] Checking to see if the Party wiped...")

        party_wipe_indicator = self._game.image_tools.find_button("party_wipe_indicator", tries = 1, suppress_error = True)
        if party_wipe_indicator is not None:
            # Click on the blue indicator to get rid of the overlay.
            self._game.mouse_tools.move_and_click_point(party_wipe_indicator[0], party_wipe_indicator[1], "party_wipe_indicator")

            if (self._game.farming_mode != "Raid" and self._game.farming_mode != "Dread Barrage") and self._game.image_tools.confirm_location("continue"):
                self._game.print_and_save(f"[WARNING] Party has unfortunately wiped during Combat Mode. Retreating now...")

                # Cancel the popup that asks you if you want to use a Full Elixir to come back. Then click the red "Retreat" button.
                self._game.find_and_click_button("cancel")
                self._game.find_and_click_button("retreat_confirmation")
                self._retreat_check = True
            elif (self._game.farming_mode == "Raid" or self._game.farming_mode == "Dread barrage") and self._game.image_tools.confirm_location("salute_participants"):
                self._game.print_and_save(f"[WARNING] Party has unfortunately wiped during Combat Mode. Backing out now without retreating...")

                # Head back to the Home screen.
                self._game.go_back_home(confirm_location_check = True)
                self._retreat_check = True
            elif self._game.farming_mode == "Coop" and self._game.image_tools.confirm_location("salute_participants"):
                # Salute the participants.
                self._game.print_and_save(f"[WARNING] Party has unfortunately wiped during Combat Mode. Leaving the Coop room...")
                self._game.find_and_click_button("salute")
                self._game.find_and_click_button("ok")

                # Then cancel the popup that asks you if you want to use a Full Elixir to come back.
                self._game.find_and_click_button("cancel")

                # Then click the "Leave" button.
                self._game.find_and_click_button("leave")

                self._retreat_check = True
        elif party_wipe_indicator is None and self._debug_mode:
            self._game.print_and_save(f"[DEBUG] Party has not wiped.")

        return None

    def _find_charge_attacks(self):
        """Find total number of characters ready to Charge Attack.

        Returns:
            number_of_charge_attacks (int): Total number of image matches found for charge attacks.
        """
        list_of_charge_attacks = self._game.image_tools.find_all("full_charge", custom_region = (
            self._attack_button_location[0] - 356, self._attack_button_location[1] + 67, self._attack_button_location[0] - 40, self._attack_button_location[1] + 214), hide_info = True)

        return len(list_of_charge_attacks)

    def _find_dialog_in_combat(self):
        """Check if there are dialog popups from either Lyria or Vyrn and click them away.

        Returns:
            None
        """
        dialog_location = self._game.image_tools.find_dialog(self._attack_button_location[0], self._attack_button_location[1], tries = 1)
        if dialog_location is not None:
            self._game.mouse_tools.move_and_click_point(dialog_location[0] + 180, dialog_location[1] - 51, "template_dialog")

        return None

    def _use_combat_healing_item(self, command: str):
        """Uses the specified healing item during Combat mode with an optional target if the item needs it.

        Args:
            command (str): The command for the healing item to use.

        Returns:
            None
        """
        if self._debug_mode:
            self._game.print_and_save(f"\n[DEBUG] Using item: {command}.")

        target = 0

        # Grab the healing command.
        healing_item_command_list = command.split(".")
        healing_item_command = healing_item_command_list.pop(0)

        # Parse the target if the user is using a Green Potion or a Clarity Herb.
        if (healing_item_command == "usegreenpotion" or healing_item_command == "useclarityherb") and healing_item_command_list[0].__contains__("target"):
            if healing_item_command_list[0] == "target(1)":
                target = 1
            elif healing_item_command_list[0] == "target(2)":
                target = 2
            elif healing_item_command_list[0] == "target(3)":
                target = 3
            elif healing_item_command_list[0] == "target(4)":
                target = 4

        # Click on the green "Heal" button.
        self._game.find_and_click_button("heal")

        # Format the item name from the command.
        formatted_command = command.replace(" ", "_")

        # Click the specified item.
        if formatted_command == "usebluepotion" or formatted_command == "usesupportpotion":
            # Blue and Support Potions share the same image but are at different positions on the screen.
            potion_locations = self._game.image_tools.find_all(formatted_command)

            if command == "usebluepotion":
                self._game.mouse_tools.move_and_click_point(potion_locations[0][0], potion_locations[0][1], "usebluepotion")
            elif command == "usesupportpotion":
                self._game.mouse_tools.move_and_click_point(potion_locations[1][0], potion_locations[1][1], "usesupportpotion")
        else:
            self._game.find_and_click_button(formatted_command)

        # After the initial popup vanishes to reveal a new popup, either select a Character target or confirm the item usage.
        if self._game.image_tools.wait_vanish("tap_the_item_to_use", timeout = 5):
            if command == "usegreenpotion":
                self._game.print_and_save(f"\n[COMBAT] Using Green Potion on Character {target}...")
                self._select_character(target)
            elif command == "usebluepotion":
                self._game.print_and_save(f"\n[COMBAT] Using Blue Potion on the whole Party...")
                self._game.find_and_click_button("use")
            elif command == "usefullelixir":
                self._game.print_and_save(f"\n[COMBAT] Using Full Elixir to revive and gain Full Charge...")
                self._game.find_and_click_button("ok")
            elif command == "usesupportpotion":
                self._game.print_and_save(f"\n[COMBAT] Using Support Potion on the whole Party...")
                self._game.find_and_click_button("ok")
            elif command == "useclaritypotion":
                self._game.print_and_save(f"\n[COMBAT] Using Clarity Herb on Character {target}...")
                self._select_character(target)
            elif command == "userevivalpotion":
                self._game.print_and_save(f"\n[COMBAT] Using Revival Potion to revive the whole Party...")
                self._game.find_and_click_button("ok")

            # Wait for the healing animation to finish.
            self._game.wait(1)

            if not self._game.image_tools.confirm_location("use_item", tries = 1):
                self._game.print_and_save(f"[SUCCESS] Using healing item was successful.")
            else:
                self._game.print_and_save(f"[WARNING] Using healing item was not successful. Canceling it now...")
                self._game.find_and_click_button("cancel")
        else:
            self._game.print_and_save(f"[WARNING] Failed to click on the item. Either it does not exist for this particular mission or you ran out. Canceling it now...")
            self._game.find_and_click_button("cancel")

        return None

    def _request_backup(self):
        """Request backup during a Raid.

        Returns:
            None
        """
        self._game.print_and_save(f"\n[COMBAT] Now requesting Backup for this Raid.")

        # Scroll down the screen a little bit to have the "Request Backup" button visible on all screen sizes and then click it.
        self._game.mouse_tools.scroll_screen_from_home_button(-400)
        self._game.find_and_click_button("request_backup")

        self._game.wait(1)

        # Find the location of the "Cancel" button and then click the button right next to it. This is to ensure that no matter what the blue "Request Backup" button's appearance, it is ensured to be pressed.
        cancel_button_location = self._game.image_tools.find_button("cancel")
        self._game.mouse_tools.move_and_click_point(cancel_button_location[0] + 200, cancel_button_location[1], "cancel")

        self._game.wait(1)

        # If requesting backup was successful, click "OK" to close the popup.
        if self._game.image_tools.confirm_location("request_backup_success", tries = 1):
            self._game.print_and_save(f"[COMBAT] Successfully requested Backup.")
            self._game.find_and_click_button("ok")
        else:
            self._game.print_and_save(f"[COMBAT] Unable to request Backup. Possibly because it is still on cooldown.")
            self._game.find_and_click_button("cancel")

        # Move the view back up to the top of the page to ensure all elements are visible.
        self._game.mouse_tools.scroll_screen_from_home_button(400)

        return None

    def _tweet_backup(self):
        """Request backup during a Raid using Twitter.

        Returns:
            None
        """
        self._game.print_and_save(f"\n[COMBAT] Now requesting Backup for this Raid via Twitter.")

        # Scroll down the screen a little bit to have the "Request Backup" button visible on all screen sizes and then click it.
        self._game.mouse_tools.scroll_screen_from_home_button(-400)
        self._game.find_and_click_button("request_backup")

        self._game.wait(1)

        # Then click the "Tweet" button.
        self._game.find_and_click_button("request_backup_tweet")
        self._game.find_and_click_button("ok")

        self._game.wait(1)

        # If requesting backup via Twitter was successful, click "OK" to close the popup. Otherwise, click "Cancel".
        if self._game.image_tools.confirm_location("request_backup_tweet_success", tries = 1):
            self._game.print_and_save(f"[COMBAT] Successfully requested Backup via Twitter.")
            self._game.find_and_click_button("ok")
        else:
            self._game.print_and_save(f"[COMBAT] Failed requesting Backup via Twitter as there is still a cooldown from the last tweet.")
            self._game.find_and_click_button("cancel")

        # Move the view back up to the top of the page to ensure all elements are visible.
        self._game.mouse_tools.scroll_screen_from_home_button(400)

        return None

    def _select_character(self, character_number: int):
        """Selects the portrait of the character specified on the Combat screen.

        Args:
            character_number (int): The character that needs to be selected on the Combat screen.

        Returns:
            None
        """
        if character_number == 1:
            x = self._attack_button_location[0] - 317
        elif character_number == 2:
            x = self._attack_button_location[0] - 240
        elif character_number == 3:
            x = self._attack_button_location[0] - 158
        elif character_number == 4:
            x = self._attack_button_location[0] - 76
        else:
            self._game.print_and_save(f"[WARNING] Invalid command received for selecting a Character. User wanted to select Character #${character_number}.")
            return

        y = self._attack_button_location[1] + 123

        # Double-clicking the character portrait to avoid any non-invasive popups from other Raid participants.
        self._game.mouse_tools.move_and_click_point(x, y, "template_character", mouse_clicks = 2)
        return None

    def _use_character_skill(self, character_selected: int, skill_command_list: List[str]):
        """Activate the specified skill(s) for the already selected character.

        Args:
            character_selected (int): The selected character whose skill(s) needs to be used.
            skill_command_list (List[str]): The commands to be executed.

        Returns:
            None
        """
        # Execute every skill command in the list.
        while len(skill_command_list) > 0:
            skill = skill_command_list.pop(0)

            if skill == "useskill(1)":
                self._game.print_and_save(f"[COMBAT] Character {character_selected} uses Skill 1.")
                x = self._attack_button_location[0] - 213
            elif skill == "useskill(2)":
                self._game.print_and_save(f"[COMBAT] Character {character_selected} uses Skill 2.")
                x = self._attack_button_location[0] - 132
            elif skill == "useskill(3)":
                self._game.print_and_save(f"[COMBAT] Character {character_selected} uses Skill 3.")
                x = self._attack_button_location[0] - 51
            elif skill == "useskill(4)":
                self._game.print_and_save(f"[COMBAT] Character {character_selected} uses Skill 4.")
                x = self._attack_button_location[0] + 39
            else:
                self._game.print_and_save(f"[WARNING] Invalid command received for using the Character's Skill. User wanted: ${skill}.")
                return

            y = self._attack_button_location[1] + 171

            # Double-clicking the skill to avoid any non-invasive popups from other Raid participants.
            self._game.mouse_tools.move_and_click_point(x, y, "template_skill", mouse_clicks = 2)

            # Check if the skill requires a target.
            if len(skill_command_list) > 0 and self._game.image_tools.confirm_location("use_skill", tries = 1):
                self._game.print_and_save(f"[COMBAT] Skill is awaiting a target...")
                target = skill_command_list.pop(0)

                select_a_character_location = self._game.image_tools.find_button("select_a_character")
                if target == "target(1)":
                    self._game.print_and_save("[COMBAT] Targeting Character 1 for Skill.")
                    self._game.mouse_tools.move_and_click_point(select_a_character_location[0] - 90, select_a_character_location[1] + 85, "template_target")
                elif "target(2)" in target:
                    self._game.print_and_save("[COMBAT] Targeting Character 2 for Skill.")
                    self._game.mouse_tools.move_and_click_point(select_a_character_location[0], select_a_character_location[1] + 85, "template_target")
                elif "target(3)" in target:
                    self._game.print_and_save("[COMBAT] Targeting Character 3 for Skill.")
                    self._game.mouse_tools.move_and_click_point(select_a_character_location[0] + 90, select_a_character_location[1] + 85, "template_target")
                elif "target(4)" in target:
                    self._game.print_and_save("[COMBAT] Targeting Character 4 for Skill.")
                    self._game.mouse_tools.move_and_click_point(select_a_character_location[0] - 90, select_a_character_location[1] + 250, "template_target")
                elif "target(5)" in target:
                    self._game.print_and_save("[COMBAT] Targeting Character 5 for Skill.")
                    self._game.mouse_tools.move_and_click_point(select_a_character_location[0], select_a_character_location[1] + 250, "template_target")
                elif "target(6)" in target:
                    self._game.print_and_save("[COMBAT] Targeting Character 6 for Skill.")
                    self._game.mouse_tools.move_and_click_point(select_a_character_location[0] + 90, select_a_character_location[1] + 250, "template_target")

            # Else, check if the character is skill-sealed.
            elif self._game.image_tools.confirm_location("skill_unusable", tries = 1):
                self._game.print_and_save("[COMBAT] Character is currently skill-sealed. Unable to execute command.")
                self._game.find_and_click_button("cancel")

        # Once all the commands for the selected Character have been processed, click the "Back" button to return.
        self._game.find_and_click_button("back")

        return None
        return None

    def _wait_for_attack(self):
        """Wait for a maximum of 20 seconds until the bot sees either the Attack or the Next button before starting a new turn.

        Returns:
            None
        """
        tries = 10
        while (not self._retreat_check and self._game.image_tools.find_button("attack", tries = 1, suppress_error = True) is None) or (
                not self._retreat_check and self._game.image_tools.find_button("next", tries = 1, suppress_error = True) is None):
            # Stagger the checks for dialog popups.
            if tries % 2 == 0:
                self._find_dialog_in_combat()

            self._game.wait(1)

            tries -= 1
            if tries <= 0 or self._game.image_tools.find_button("attack", tries = 1, suppress_error = True) is not None or \
                    self._game.image_tools.find_button("next", tries = 1, suppress_error = True) is not None:
                break

            # Check if the Party wiped after attacking.
            self._party_wipe_check()

            self._game.wait(1)

        return None

    def start_combat_mode(self, script_file_path: str = "", is_nightmare: bool = False):
        """Start Combat Mode with the given script file path. Start reading through the text file line by line and have the bot proceed with the commands accordingly.

        Args:
            script_file_path (str, optional): Path to the combat script text file. Defaults to "".
            is_nightmare (bool, optional): If Combat Mode is being used for a Nightmare, determines the method of reading the script file.

        Returns:
            (bool): Return True if Combat Mode was successful. Else, return False if the Party wiped or backed out without retreating.
        """
        try:
            self._game.print_and_save("\n\n################################################################################")
            self._game.print_and_save("################################################################################")
            self._game.print_and_save(f"[COMBAT] Starting Combat Mode.")
            self._game.print_and_save("################################################################################")
            self._game.print_and_save("################################################################################\n")

            # Open the combat script text file.
            if script_file_path == "" or script_file_path is None:
                self._game.print_and_save(f"\n[COMBAT] No script file was provided. Using default full_auto.txt script.")
                os.chdir(os.getcwd() + "/scripts/")
                script = open(os.path.abspath("full_auto.txt"), "r")
                os.chdir(self._owd)
            elif is_nightmare:
                self._game.print_and_save(f"\n[COMBAT] Now loading up combat script for this at {os.getcwd()}\scripts\{script_file_path}")
                os.chdir(os.getcwd() + "/scripts/")
                root, extension = os.path.splitext(script_file_path)
                if not extension:
                    script = open(os.path.abspath(script_file_path + ".txt"), "r")
                else:
                    script = open(os.path.abspath(script_file_path), "r")
                os.chdir(self._owd)
            else:
                self._game.print_and_save(f"\n[COMBAT] Now loading up combat script at {script_file_path}")
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
            self._attack_button_location = self._game.image_tools.find_button("attack", tries = 10)
            if self._attack_button_location is not None:
                self._back_button_location = (self._attack_button_location[0] - 322, self._attack_button_location[1])
            else:
                self._game.print_and_save(f"\n[ERROR] Cannot find Attack button. Raid must have just ended.")
                return False

            # This is where the main workflow of Combat Mode is located and it will loop until the last of the commands have been executed.
            while i < len(lines) and not self._retreat_check and not semi_auto and not full_auto:
                line = lines[i].strip()

                # Skip this line if it is empty or a comment.
                while line == "" or line[0] == "#" or line[0] == "/":
                    line_number += 1
                    i += 1
                    line = lines[i].strip()

                # Print each line read if Debug Mode is active.
                if self._debug_mode:
                    self._game.print_and_save(f"\n[DEBUG] Reading Line {line_number}: \"{line.strip()}\"")

                # If the execution reached the next turn block and it is currently not the correct turn, keep pressing the "Attack" button until the turn number matches.
                if "turn" in line.lower() and int(line.split(":")[0].split(" ")[1]) != turn_number:
                    self._game.print_and_save(f"\n[COMBAT] Attacking until the bot reaches Turn {int(line.split(':')[0].split(' ')[1])}...")

                    while int(line.split(":")[0].split(" ")[1]) != turn_number:
                        self._game.print_and_save(f"[COMBAT] Starting Turn {turn_number}.")
                        self._find_dialog_in_combat()

                        attack_button_location = self._game.image_tools.find_button("attack", tries = 1, suppress_error = True)
                        if attack_button_location is not None:
                            self._game.print_and_save(f"[COMBAT] Ending Turn {turn_number} by attacking now...")
                            number_of_charge_attacks = self._find_charge_attacks()
                            self._game.mouse_tools.move_and_click_point(self._attack_button_location[0], self._attack_button_location[1], "attack")
                            self._game.wait(3 + number_of_charge_attacks)
                            self._wait_for_attack()
                            self._game.print_and_save(f"[COMBAT] Turn {turn_number} has ended.")
                            self._party_wipe_check()
                            turn_number += 1

                        next_button_location = self._game.image_tools.find_button("next", tries = 1, suppress_error = True)
                        if next_button_location is not None:
                            self._game.mouse_tools.move_and_click_point(next_button_location[0], next_button_location[1], "next")
                            self._game.wait(3)

                        if self._retreat_check or self._game.image_tools.confirm_location("exp_gained", tries = 1) or self._game.image_tools.confirm_location("no_loot", tries = 1):
                            self._game.print_and_save("\n################################################################################")
                            self._game.print_and_save("################################################################################")
                            self._game.print_and_save("[COMBAT] Ending Combat Mode.")
                            self._game.print_and_save("################################################################################")
                            self._game.print_and_save("################################################################################")
                            return False
                        elif self._game.image_tools.confirm_location("battle_concluded", tries = 1):
                            self._game.print_and_save("\n[COMBAT] Battle concluded suddenly.")
                            self._game.find_and_click_button("ok")

                            self._game.print_and_save("\n################################################################################")
                            self._game.print_and_save("################################################################################")
                            self._game.print_and_save("[COMBAT] Ending Combat Mode.")
                            self._game.print_and_save("################################################################################")
                            self._game.print_and_save("################################################################################")
                            return False

                if self._retreat_check or self._game.image_tools.confirm_location("exp_gained", tries = 1) or self._game.image_tools.confirm_location("no_loot", tries = 1):
                    break
                elif self._game.image_tools.confirm_location("battle_concluded", tries = 1):
                    self._game.print_and_save("\n[COMBAT] Battle concluded suddenly.")
                    self._game.find_and_click_button("ok")
                    break

                # If it is the start of the Turn and it is currently the correct turn, grab the next line for execution.
                if "turn" in line.lower() and int(line.split(":")[0].split(" ")[1]) == turn_number and not self._retreat_check:
                    self._game.print_and_save(f"\n[COMBAT] Starting Turn {turn_number}. Reading script now...")

                    self._find_dialog_in_combat()

                    # Continue reading each line inside the turn block until you reach the "end" command.
                    while ("end" not in line.lower() and "exit" not in line.lower()) and i < len(lines):
                        # Strip any leading and trailing whitespaces.
                        line = lines[i].strip()

                        # Skip this line if it is empty or a comment.
                        while line == "" or line[0] == "#" or line[0] == "/":
                            line_number += 1
                            i += 1
                            line = lines[i].strip()

                        if "end" in line.lower() and not semi_auto and not full_auto:
                            break

                        if "exit" in line.lower() and not semi_auto and not full_auto:
                            # End Combat Mode by heading back to the Home screen without retreating. Usually for raid farming as to maximize the number of raids joined after completing the provided
                            # combat script.
                            self._game.print_and_save(f"\n[COMBAT] Reading Line {line_number}: \"{line.strip()}\"")
                            self._game.print_and_save("[COMBAT] Leaving this raid without retreating...")
                            self._game.wait(1)
                            self._game.go_back_home(confirm_location_check = True)
                            return False

                        self._game.print_and_save(f"\n[COMBAT] Reading Line {line_number}: \"{line}\"")

                        # Determine which character to take action.
                        character_selected = 0
                        if "character1" in line.lower():
                            character_selected = 1
                        elif "character2" in line.lower():
                            character_selected = 2
                        elif "character3" in line.lower():
                            character_selected = 3
                        elif "character4" in line.lower():
                            character_selected = 4

                        if character_selected != 0:
                            # Select the character specified.
                            self._select_character(character_selected)

                            # Execute each skill from left to right for this character.
                            commands = line.split(".")[1:]
                            while len(commands) > 0:
                                command = commands.pop(0).lower()

                                if "useskill" in command:
                                    # Use the skill.
                                    self._use_character_skill(character_selected, command)

                                    if self._game.image_tools.confirm_location("use_skill", tries = 1):
                                        # Check if the skill requires a target.
                                        select_a_character_location = self._game.image_tools.find_button("select_a_character", tries = 1)
                                        if select_a_character_location is not None:
                                            self._game.print_and_save("[COMBAT] Skill is now awaiting a target...")

                                            # Parse and then click on the targeted character.
                                            target = commands.pop(0).lower()
                                            if "target(1)" in target:
                                                self._game.print_and_save("[COMBAT] Targeting Character 1.")
                                                self._game.mouse_tools.move_and_click_point(select_a_character_location[0] - 90,
                                                                                            select_a_character_location[1] + 85, "template_target")
                                            elif "target(2)" in target:
                                                self._game.print_and_save("[COMBAT] Targeting Character 2.")
                                                self._game.mouse_tools.move_and_click_point(select_a_character_location[0],
                                                                                            select_a_character_location[1] + 85, "template_target")
                                            elif "target(3)" in target:
                                                self._game.print_and_save("[COMBAT] Targeting Character 3.")
                                                self._game.mouse_tools.move_and_click_point(select_a_character_location[0] + 90,
                                                                                            select_a_character_location[1] + 85, "template_target")
                                            elif "target(4)" in target:
                                                self._game.print_and_save("[COMBAT] Targeting Character 4.")
                                                self._game.mouse_tools.move_and_click_point(select_a_character_location[0] - 90,
                                                                                            select_a_character_location[1] + 250, "template_target")
                                            elif "target(5)" in target:
                                                self._game.print_and_save("[COMBAT] Targeting Character 5.")
                                                self._game.mouse_tools.move_and_click_point(select_a_character_location[0],
                                                                                            select_a_character_location[1] + 250, "template_target")
                                            elif "target(6)" in target:
                                                self._game.print_and_save("[COMBAT] Targeting Character 6.")
                                                self._game.mouse_tools.move_and_click_point(select_a_character_location[0] + 90,
                                                                                            select_a_character_location[1] + 250, "template_target")
                                            else:
                                                # If the command is not one of the supported targets, close the popup.
                                                self._game.print_and_save("[COMBAT] Invalid Character target. Canceling now...")
                                                self._game.find_and_click_button("cancel")

                                        # Else, check if the character is skill-sealed.
                                        elif self._game.image_tools.confirm_location("skill_unusable", tries = 1):
                                            self._game.print_and_save("[COMBAT] Character is currently skill-sealed. Unable to execute command.")
                                            self._game.find_and_click_button("cancel")

                            # Now click the "Back" button.
                            self._game.mouse_tools.move_and_click_point(self._back_button_location[0], self._back_button_location[1], "back")

                            # Attempt to wait to see if the character one-shot the enemy or not. This is user-defined in the config.ini.
                            self._game.wait(self._idle_seconds_after_skill)

                            if self._retreat_check or self._game.image_tools.confirm_location("exp_gained", tries = 1) or self._game.image_tools.confirm_location("no_loot", tries = 1):
                                self._game.print_and_save("\n################################################################################")
                                self._game.print_and_save("################################################################################")
                                self._game.print_and_save("[COMBAT] Ending Combat Mode.")
                                self._game.print_and_save("################################################################################")
                                self._game.print_and_save("################################################################################")
                                return False
                            elif self._game.image_tools.confirm_location("battle_concluded", tries = 1):
                                self._game.print_and_save("\n[COMBAT] Battle concluded suddenly.")
                                self._game.find_and_click_button("ok")

                                self._game.print_and_save("\n################################################################################")
                                self._game.print_and_save("################################################################################")
                                self._game.print_and_save("[COMBAT] Ending Combat Mode.")
                                self._game.print_and_save("################################################################################")
                                self._game.print_and_save("################################################################################")
                                return False

                        for j in range(1, 7):
                            if f"summon({j})" in line.lower():
                                # Click the "Summon" button to bring up the available Summons.
                                self._game.print_and_save(f"[COMBAT] Invoking Summon #{j}.")
                                self._game.find_and_click_button("summon")

                                # Click on the specified Summon.
                                if j == 1:
                                    self._game.mouse_tools.move_and_click_point(self._attack_button_location[0] - 317, self._attack_button_location[1] + 138, "template_summon", mouse_clicks = 2)
                                elif j == 2:
                                    self._game.mouse_tools.move_and_click_point(self._attack_button_location[0] - 243, self._attack_button_location[1] + 138, "template_summon", mouse_clicks = 2)
                                elif j == 3:
                                    self._game.mouse_tools.move_and_click_point(self._attack_button_location[0] - 165, self._attack_button_location[1] + 138, "template_summon", mouse_clicks = 2)
                                elif j == 4:
                                    self._game.mouse_tools.move_and_click_point(self._attack_button_location[0] - 89, self._attack_button_location[1] + 138, "template_summon", mouse_clicks = 2)
                                elif j == 5:
                                    self._game.mouse_tools.move_and_click_point(self._attack_button_location[0] - 12, self._attack_button_location[1] + 138, "template_summon", mouse_clicks = 2)
                                else:
                                    self._game.mouse_tools.move_and_click_point(self._attack_button_location[0] + 63, self._attack_button_location[1] + 138, "template_summon", mouse_clicks = 2)

                                # Check if it is able to be summoned.
                                if self._game.image_tools.confirm_location("summon_details", tries = 2):
                                    ok_button_location = self._game.image_tools.find_button("ok", tries = 1)
                                    if ok_button_location is not None:
                                        self._game.mouse_tools.move_and_click_point(ok_button_location[0], ok_button_location[1], "ok")

                                        # Wait for the Summon animation to complete. This is user-defined in the config.ini.
                                        self._game.wait(self._idle_seconds_after_summon)
                                    else:
                                        self._game.print_and_save("[COMBAT] Summon #{j} cannot be invoked due to current restrictions.")
                                        self._game.find_and_click_button("cancel")

                                        # Click the "Back" button.
                                        self._game.mouse_tools.move_and_click_point(self._back_button_location[0], self._back_button_location[1], "back")

                                if self._retreat_check or self._game.image_tools.confirm_location("exp_gained", tries = 1) or self._game.image_tools.confirm_location("no_loot", tries = 1):
                                    self._game.print_and_save("\n################################################################################")
                                    self._game.print_and_save("################################################################################")
                                    self._game.print_and_save("[COMBAT] Ending Combat Mode.")
                                    self._game.print_and_save("################################################################################")
                                    self._game.print_and_save("################################################################################")
                                    return False
                                elif self._game.image_tools.confirm_location("battle_concluded", tries = 1):
                                    self._game.print_and_save("\n[COMBAT] Battle concluded suddenly.")
                                    self._game.find_and_click_button("ok")

                                    self._game.print_and_save("\n################################################################################")
                                    self._game.print_and_save("################################################################################")
                                    self._game.print_and_save("[COMBAT] Ending Combat Mode.")
                                    self._game.print_and_save("################################################################################")
                                    self._game.print_and_save("################################################################################")
                                    return False

                        if self._game.image_tools.find_button("next", tries = 1, suppress_error = True) is not None:
                            break

                        if not semi_auto and not full_auto and "enablesemiauto" in line.lower():
                            self._game.print_and_save("[COMBAT] Bot will now attempt to enable Semi Auto...")
                            semi_auto = True
                            break

                        if not semi_auto and not full_auto and "enablefullauto" in line.lower():
                            self._game.print_and_save("[COMBAT] Enabling Full Auto. Bot will continue until raid ends or Party wipes.")
                            enabled_full_auto = self._game.find_and_click_button("full_auto", tries = 5)

                            # If the bot failed to find and click the "Full Auto" button, fallback to the "Semi Auto" button.
                            if not enabled_full_auto:
                                self._game.print_and_save("[COMBAT] Bot failed to find the \"Full Auto\" button. Falling back to Semi Auto.")
                                semi_auto = True
                            else:
                                full_auto = True

                            break

                        if "requestbackup" in line.lower() and not semi_auto and not full_auto:
                            # Request Backup for this Raid.
                            self._request_backup()

                        if "tweetbackup" in line.lower() and not semi_auto and not full_auto:
                            # Request Backup via Twitter for this Raid.
                            self._tweet_backup()

                        item_commands = ["usegreenpotion.target(1)", "usegreenpotion.target(2)", "usegreenpotion.target(3)", "usegreenpotion.target(4)", "usebluepotion", "usefullelixir",
                                         "usesupportpotion", "useclarityherb.target(1)", "useclarityherb.target(2)", "useclarityherb.target(3)", "useclarityherb.target(4)", "userevivalpotion"]
                        if line.lower() in item_commands and not semi_auto and not full_auto:
                            # Parse the command from the line.
                            command = line.split(".").pop(0).lower()

                            # Parse the target if the user is using a Green Potion or a Clarity Herb.
                            if (command == "usegreenpotion" or command == "useclarityherb") and "target" in line.lower():
                                target = line.split(".").pop(1).lower()
                                if "target(1)" in target:
                                    target = 1
                                elif "target(2)" in target:
                                    target = 2
                                elif "target(3)" in target:
                                    target = 3
                                elif "target(4)" in target:
                                    target = 4
                            else:
                                target = 0

                            # Use the item and continue to the next line for execution.
                            self._use_combat_healing_item(command, target)

                        # Move onto the next command for execution.
                        line_number += 1
                        i += 1

                if not semi_auto and not full_auto and "enablesemiauto" in line.lower():
                    self._game.print_and_save("[COMBAT] Bot will now attempt to enable Semi Auto...")
                    semi_auto = True
                    break
                elif semi_auto:
                    break

                if not semi_auto and not full_auto and "enablefullauto" in line.lower():
                    self._game.print_and_save("[COMBAT] Enabling Full Auto. Bot will continue until raid ends or Party wipes.")
                    enabled_full_auto = self._game.find_and_click_button("full_auto")

                    # If the bot failed to find and click the "Full Auto" button, fallback to the "Semi Auto" button.
                    if not enabled_full_auto:
                        self._game.print_and_save("[COMBAT] Bot failed to find the \"Full Auto\" button. Falling back to Semi Auto.")
                        semi_auto = True
                    else:
                        full_auto = True

                    break

                if "end" in line.lower() and not semi_auto and not full_auto:
                    next_button_location = self._game.image_tools.find_button("next", tries = 1, suppress_error = True)
                    if next_button_location is not None:
                        self._game.print_and_save(f"[COMBAT] All enemies on screen have been eliminated before attacking. Preserving Turn {turn_number} by moving to the next Wave...")
                        self._game.mouse_tools.move_and_click_point(next_button_location[0], next_button_location[1], "next")
                        self._game.wait(3)
                    else:
                        self._game.print_and_save(f"[COMBAT] Ending Turn {turn_number} by attacking now...")
                        number_of_charge_attacks = self._find_charge_attacks()
                        self._game.mouse_tools.move_and_click_point(self._attack_button_location[0], self._attack_button_location[1], "attack")

                        # Peek ahead of the script while the Party is currently attacking and see if it detects the command "enableSemiAuto" outside of a Turn block.
                        temp_index = i
                        while temp_index < len(lines):
                            temp_line = lines[temp_index].strip()

                            # Skip this line if it is empty or a comment.
                            if temp_line == "" or temp_line[0] == "#" or temp_line[0] == "/":
                                temp_index += 1
                                continue

                            # Enable Semi Auto if the command is read. Otherwise it can break out of the loop if it reaches a new Turn block.
                            if "enablesemiauto" in temp_line.lower():
                                self._game.print_and_save("[COMBAT] Enabling Semi Auto. Bot will continue until raid ends or Party wipes.")
                                self._game.find_and_click_button("semi_auto")
                                semi_auto = True
                                break
                            elif "turn" in temp_line.lower():
                                break

                            temp_index += 1

                        self._game.wait(3 + number_of_charge_attacks)
                        self._wait_for_attack()
                        self._game.print_and_save(f"[COMBAT] Turn {turn_number} has ended.")
                        self._party_wipe_check()
                        turn_number += 1

                        next_button_location = self._game.image_tools.find_button("next", tries = 1, suppress_error = True)
                        if next_button_location is not None:
                            self._game.mouse_tools.move_and_click_point(next_button_location[0], next_button_location[1], "next")
                            self._game.wait(3)

                if "exit" in line.lower() and not semi_auto and not full_auto:
                    # End Combat Mode by heading back to the Home screen without retreating. Usually for raid farming as to maximize the number of raids joined after completing the provided combat script.
                    self._game.print_and_save(f"\n[COMBAT] Reading Line {line_number}: \"{line.strip()}\"")
                    self._game.print_and_save("[COMBAT] Leaving this raid without retreating...")
                    self._game.wait(1)
                    self._game.go_back_home(confirm_location_check = True)
                    return False

                # Continue to the next line for execution.
                line_number += 1
                i += 1

            # When execution gets to here outside of the main workflow loop for Combat Mode, the bot has reached the end of the combat script and will now attack until the battle ends or the Party wipes.
            self._game.print_and_save("\n[COMBAT] Bot has reached end of script. Automatically attacking until battle ends or Party wipes...")

            # Keep pressing the location of the "Attack" / "Next" button until the bot reaches the Quest Results screen.
            while not self._retreat_check and not semi_auto and not full_auto and not self._game.image_tools.confirm_location("exp_gained", tries = 1) and not self._game.image_tools.confirm_location(
                    "no_loot", tries = 1):
                self._find_dialog_in_combat()
                attack_button_location = self._game.image_tools.find_button("attack", tries = 1, suppress_error = True)
                if attack_button_location is not None:
                    self._game.print_and_save(f"\n[COMBAT] Starting Turn {turn_number}.")
                    self._game.print_and_save(f"[COMBAT] Ending Turn {turn_number} by attacking now...")
                    number_of_charge_attacks = self._find_charge_attacks()
                    self._game.mouse_tools.move_and_click_point(self._attack_button_location[0], self._attack_button_location[1], "attack")
                    self._game.wait(3 + number_of_charge_attacks)
                    self._wait_for_attack()
                    self._game.print_and_save(f"[COMBAT] Turn {turn_number} has ended.")
                    self._party_wipe_check()
                    turn_number += 1

                next_button_location = self._game.image_tools.find_button("next", tries = 1, suppress_error = True)
                if next_button_location is not None:
                    self._game.mouse_tools.move_and_click_point(next_button_location[0], next_button_location[1], "next")
                    self._game.wait(3)

            # Double check to see if Semi Auto is turned on. Note that the "Semi Auto" button only appears while the Party is attacking.
            if not self._retreat_check and semi_auto and not full_auto:
                self._game.print_and_save("[COMBAT] Double checking to see if Semi Auto is enabled...")
                enabled_semi_auto = self._game.image_tools.find_button("semi_auto_enabled")
                if not enabled_semi_auto:
                    # Have the Party attack and then attempt to see if the "Semi Auto" button becomes visible.
                    self._game.find_and_click_button("attack")
                    enabled_semi_auto = self._game.find_and_click_button("semi_auto", tries = 5)

                    # If the bot still cannot find the "Semi Auto" button, that probably means the user has the "Full Auto" button on the screen instead of the "Semi Auto" button.
                    if not enabled_semi_auto:
                        self._game.print_and_save("[COMBAT] Failed to enable Semi Auto. Falling back to Full Auto...")
                        semi_auto = False
                        full_auto = True

                        # Enable Full Auto.
                        self._game.find_and_click_button("full_auto")
                    else:
                        self._game.print_and_save("[COMBAT] Semi Auto is now enabled.")

            # Main workflow loop for Semi Auto. The bot will progress the Quest/Raid until it ends or the Party wipes.
            while not self._retreat_check and semi_auto and not full_auto and not self._game.image_tools.confirm_location("exp_gained", tries = 1) and not self._game.image_tools.confirm_location(
                    "no_loot", tries = 1):
                if self._game.image_tools.confirm_location("battle_concluded", tries = 1):
                    self._game.print_and_save("\n[COMBAT] Battle concluded suddenly.")
                    self._game.find_and_click_button("ok")
                    break
                self._party_wipe_check()
                self._game.wait(3)

            # Main workflow loop for Full Auto. The bot will progress the Quest/Raid until it ends or the Party wipes.
            while not self._retreat_check and not semi_auto and full_auto and not self._game.image_tools.confirm_location("exp_gained", tries = 1) and not self._game.image_tools.confirm_location(
                    "no_loot", tries = 1):
                if self._game.image_tools.confirm_location("battle_concluded", tries = 1):
                    self._game.print_and_save("\n[COMBAT] Battle concluded suddenly.")
                    self._game.find_and_click_button("ok")
                    break
                self._party_wipe_check()
                self._game.wait(3)

            self._game.print_and_save("\n################################################################################")
            self._game.print_and_save("################################################################################")
            self._game.print_and_save("[COMBAT] Ending Combat Mode.")
            self._game.print_and_save("################################################################################")
            self._game.print_and_save("################################################################################")

            if not self._retreat_check:
                self._game.print_and_save("\n[INFO] Bot has reached the Quest Results screen.")
                return True
            else:
                return False
        except FileNotFoundError:
            self._game.print_and_save(f"\n[ERROR] Cannot find \"{script_file_path}.txt\": \n{traceback.format_exc()}")
            self._is_bot_running.value = 1
