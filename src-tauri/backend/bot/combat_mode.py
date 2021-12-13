import copy
import os
from typing import List
import time

from utils.settings import Settings
from utils.message_log import MessageLog
from utils.image_utils import ImageUtils
from utils.mouse_utils import MouseUtils


class CombatMode:
    """
    Provides the utility functions needed for Combat Mode.
    """

    # Save a reference to the original current working directory.
    _owd = os.getcwd()

    _healing_item_commands = ["usegreenpotion.target(1)", "usegreenpotion.target(2)", "usegreenpotion.target(3)", "usegreenpotion.target(4)", "usebluepotion", "usefullelixir",
                              "usesupportpotion", "useclarityherb.target(1)", "useclarityherb.target(2)", "useclarityherb.target(3)", "useclarityherb.target(4)", "userevivalpotion"]

    # Save some variables for use throughout the class.
    _attack_button_location = None
    _retreat_check = False

    @staticmethod
    def _party_wipe_check():
        """Check to see if the Party has wiped during Combat Mode. Update the retreat check flag if so.

        Returns:
            None
        """
        from bot.game import Game

        # Check to see if Party has wiped.
        if Settings.debug_mode:
            MessageLog.print_message(f"\n[DEBUG] Checking to see if the Party wiped...")

        party_wipe_indicator = ImageUtils.find_button("party_wipe_indicator", tries = 1, suppress_error = True)
        if party_wipe_indicator is not None or ImageUtils.confirm_location("salute_participants", tries = 1, suppress_error = True):
            if (Settings.farming_mode != "Raid" and Settings.farming_mode != "Dread Barrage") and ImageUtils.confirm_location("continue"):
                # Click on the blue indicator to get rid of the overlay.
                if party_wipe_indicator is not None:
                    MouseUtils.move_and_click_point(party_wipe_indicator[0], party_wipe_indicator[1], "party_wipe_indicator")

                MessageLog.print_message(f"[WARNING] Party has unfortunately wiped during Combat Mode for this non-Raid battle. Retreating now...")

                # Cancel the popup that asks you if you want to use a Full Elixir to come back. Then click the red "Retreat" button.
                Game.find_and_click_button("cancel")
                Game.find_and_click_button("retreat_confirmation")
                CombatMode._retreat_check = True
            elif Settings.farming_mode == "Raid" or Settings.farming_mode == "Dread Barrage" or Settings.farming_mode == "Guild Wars" or Settings.map_name.__contains__("Raid"):
                MessageLog.print_message(f"[WARNING] Party has unfortunately wiped during Combat Mode for this Raid battle. Backing out now without retreating...")

                # Head back to the Home screen.
                Game.go_back_home(confirm_location_check = True)
                CombatMode._retreat_check = True
            elif Settings.farming_mode == "Coop" and ImageUtils.confirm_location("salute_participants"):
                # Click on the blue indicator to get rid of the overlay.
                if party_wipe_indicator is not None:
                    MouseUtils.move_and_click_point(party_wipe_indicator[0], party_wipe_indicator[1], "party_wipe_indicator")

                # Salute the participants.
                MessageLog.print_message(f"[WARNING] Party has unfortunately wiped during Combat Mode for this Coop battle. Leaving the Coop room...")
                Game.find_and_click_button("salute")
                Game.find_and_click_button("ok")

                # Then cancel the popup that asks you if you want to use a Full Elixir to come back.
                Game.find_and_click_button("cancel")

                # Then click the "Leave" button.
                Game.find_and_click_button("leave")

                CombatMode._retreat_check = True
        elif party_wipe_indicator is None and Settings.debug_mode:
            MessageLog.print_message(f"[DEBUG] Party has not wiped.")

        return None

    @staticmethod
    def _find_dialog_in_combat():
        """Check if there are dialog popups from either Lyria or Vyrn and click them away.

        Returns:
            None
        """
        dialog_location = ImageUtils.find_button("dialog_lyria", tries = 1, suppress_error = True)
        if dialog_location is None:
            dialog_location = ImageUtils.find_button("dialog_vyrn", tries = 1, suppress_error = True)

        if dialog_location is not None:
            MouseUtils.move_and_click_point(dialog_location[0] + 180, dialog_location[1] - 51, "template_dialog")

        return None

    @staticmethod
    def _use_combat_healing_item(command: str):
        """Uses the specified healing item during Combat mode with an optional target if the item needs it.

        Args:
            command (str): The command for the healing item to use.

        Returns:
            None
        """
        from bot.game import Game

        if Settings.debug_mode:
            MessageLog.print_message(f"\n[DEBUG] Using item: {command}.")

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
        Game.find_and_click_button("heal")

        # Format the item name from the command.
        formatted_command = command.replace(" ", "_")

        # Click the specified item.
        if formatted_command == "usebluepotion" or formatted_command == "usesupportpotion":
            # Blue and Support Potions share the same image but are at different positions on the screen.
            potion_locations = ImageUtils.find_all(formatted_command)

            if command == "usebluepotion":
                MouseUtils.move_and_click_point(potion_locations[0][0], potion_locations[0][1], "usebluepotion")
            elif command == "usesupportpotion":
                MouseUtils.move_and_click_point(potion_locations[1][0], potion_locations[1][1], "usesupportpotion")
        else:
            Game.find_and_click_button(formatted_command)

        # After the initial popup vanishes to reveal a new popup, either select a Character target or confirm the item usage.
        if ImageUtils.wait_vanish("tap_the_item_to_use", timeout = 5):
            if command == "usegreenpotion":
                MessageLog.print_message(f"\n[COMBAT] Using Green Potion on Character {target}...")
                CombatMode._select_character(target)
            elif command == "usebluepotion":
                MessageLog.print_message(f"\n[COMBAT] Using Blue Potion on the whole Party...")
                Game.find_and_click_button("use")
            elif command == "usefullelixir":
                MessageLog.print_message(f"\n[COMBAT] Using Full Elixir to revive and gain Full Charge...")
                Game.find_and_click_button("ok")
            elif command == "usesupportpotion":
                MessageLog.print_message(f"\n[COMBAT] Using Support Potion on the whole Party...")
                Game.find_and_click_button("ok")
            elif command == "useclarityherb":
                MessageLog.print_message(f"\n[COMBAT] Using Clarity Herb on Character {target}...")
                CombatMode._select_character(target)
            elif command == "userevivalpotion":
                MessageLog.print_message(f"\n[COMBAT] Using Revival Potion to revive the whole Party...")
                Game.find_and_click_button("ok")

            # Wait for the healing animation to finish.
            Game.wait(1)

            if not ImageUtils.confirm_location("use_item", tries = 5):
                MessageLog.print_message(f"[SUCCESS] Using healing item was successful.")
            else:
                MessageLog.print_message(f"[WARNING] Using healing item was not successful. Canceling it now...")
                Game.find_and_click_button("cancel")
        else:
            MessageLog.print_message(f"[WARNING] Failed to click on the item. Either it does not exist for this particular mission or you ran out. Canceling it now...")
            Game.find_and_click_button("cancel")

        return None

    @staticmethod
    def _request_backup():
        """Request backup during a Raid.

        Returns:
            None
        """
        from bot.game import Game

        MessageLog.print_message(f"\n[COMBAT] Now requesting Backup for this Raid.")

        # Scroll down the screen a little bit to have the "Request Backup" button visible on all screen sizes and then click it.
        tries = 5
        while Game.find_and_click_button("request_backup") is False:
            MouseUtils.scroll_screen_from_home_button(-200)
            tries -= 1
            if tries <= 0:
                MessageLog.print_message(f"\n[COMBAT] Failed to request backup.")
                MouseUtils.scroll_screen_from_home_button(400)
                return None

        Game.wait(1)

        # Find the location of the "Cancel" button and then click the button right next to it. This is to ensure that no matter what the blue "Request Backup" button's appearance, it is ensured to be pressed.
        cancel_button_location = ImageUtils.find_button("cancel")
        if cancel_button_location is not None:
            MouseUtils.move_and_click_point(cancel_button_location[0] + 200, cancel_button_location[1], "cancel")

        Game.wait(1)

        # If requesting backup was successful, click "OK" to close the popup.
        if ImageUtils.confirm_location("request_backup_success", tries = 5):
            MessageLog.print_message(f"[COMBAT] Successfully requested Backup.")
            Game.find_and_click_button("ok")
        else:
            MessageLog.print_message(f"[COMBAT] Unable to request Backup. Possibly because it is still on cooldown.")
            Game.find_and_click_button("cancel")

        # Move the view back up to the top of the page to ensure all elements are visible.
        MouseUtils.scroll_screen_from_home_button(400)

        return None

    @staticmethod
    def _tweet_backup():
        """Request backup during a Raid using Twitter.

        Returns:
            None
        """
        from bot.game import Game

        MessageLog.print_message(f"\n[COMBAT] Now requesting Backup for this Raid via Twitter.")

        # Scroll down the screen a little bit to have the "Request Backup" button visible on all screen sizes and then click it.
        MouseUtils.scroll_screen_from_home_button(-400)
        Game.find_and_click_button("request_backup")

        Game.wait(1)

        # Then click the "Tweet" button.
        Game.find_and_click_button("request_backup_tweet")
        Game.find_and_click_button("ok")

        Game.wait(1)

        # If requesting backup via Twitter was successful, click "OK" to close the popup. Otherwise, click "Cancel".
        if ImageUtils.confirm_location("request_backup_tweet_success", tries = 5):
            MessageLog.print_message(f"[COMBAT] Successfully requested Backup via Twitter.")
            Game.find_and_click_button("ok")
        else:
            MessageLog.print_message(f"[COMBAT] Failed requesting Backup via Twitter as there is still a cooldown from the last tweet.")
            Game.find_and_click_button("cancel")

        # Move the view back up to the top of the page to ensure all elements are visible.
        MouseUtils.scroll_screen_from_home_button(400)

        return None

    @staticmethod
    def _select_character(character_number: int):
        """Selects the portrait of the character specified on the Combat screen.

        Args:
            character_number (int): The character that needs to be selected on the Combat screen.

        Returns:
            None
        """
        if character_number == 1:
            x = CombatMode._attack_button_location[0] - 317
        elif character_number == 2:
            x = CombatMode._attack_button_location[0] - 240
        elif character_number == 3:
            x = CombatMode._attack_button_location[0] - 158
        elif character_number == 4:
            x = CombatMode._attack_button_location[0] - 76
        else:
            MessageLog.print_message(f"[WARNING] Invalid command received for selecting a Character. User wanted to select Character #{character_number}.")
            return

        y = CombatMode._attack_button_location[1] + 123

        # Double-clicking the character portrait to avoid any non-invasive popups from other Raid participants.
        MouseUtils.move_and_click_point(x, y, "template_character", mouse_clicks = 2)

        return None

    @staticmethod
    def _select_enemy_target(command: str):
        """Selects the targeted enemy.

        Args:
            command (str): The command to be executed.

        Returns:
            None
        """
        for target in range(1, 3):
            if command == f"targetenemy({target})":
                from bot.game import Game

                if target == 1:
                    x = CombatMode._attack_button_location[0] - 280
                elif target == 2:
                    x = CombatMode._attack_button_location[0] - 120
                else:
                    x = CombatMode._attack_button_location[0] + 40

                y = CombatMode._attack_button_location[1] - 290

                MouseUtils.move_and_click_point(x, y, "template_enemy_target")
                Game.find_and_click_button("set_target")
                MessageLog.print_message(f"[COMBAT] Targeted Enemy #{target}.")

        return None

    @staticmethod
    def _use_character_skill(character_selected: int, skill_command_list: List[str]):
        """Activate the specified skill(s) for the already selected character.

        Args:
            character_selected (int): The selected character whose skill(s) needs to be used.
            skill_command_list (List[str]): The commands to be executed.

        Returns:
            None
        """
        from bot.game import Game

        # Execute every skill command in the list.
        while len(skill_command_list) > 0:
            skill = skill_command_list.pop(0)

            if skill == "useskill(1)":
                MessageLog.print_message(f"[COMBAT] Character {character_selected} uses Skill 1.")
                x = CombatMode._attack_button_location[0] - 213
            elif skill == "useskill(2)":
                MessageLog.print_message(f"[COMBAT] Character {character_selected} uses Skill 2.")
                x = CombatMode._attack_button_location[0] - 132
            elif skill == "useskill(3)":
                MessageLog.print_message(f"[COMBAT] Character {character_selected} uses Skill 3.")
                x = CombatMode._attack_button_location[0] - 51
            elif skill == "useskill(4)":
                MessageLog.print_message(f"[COMBAT] Character {character_selected} uses Skill 4.")
                x = CombatMode._attack_button_location[0] + 39
            else:
                MessageLog.print_message(f"[WARNING] Invalid command received for using the Character's Skill. User wanted: {skill}.")
                return

            y = CombatMode._attack_button_location[1] + 171

            MouseUtils.move_and_click_point(x, y, "template_skill")

            # Check if the skill requires a target.
            if len(skill_command_list) > 0 and ImageUtils.confirm_location("use_skill", tries = 2):
                MessageLog.print_message(f"[COMBAT] Skill is awaiting a target...")
                target = skill_command_list.pop(0)

                select_a_character_location = ImageUtils.find_button("select_a_character")
                if target == "target(1)":
                    MessageLog.print_message("[COMBAT] Targeting Character 1 for Skill.")
                    MouseUtils.move_and_click_point(select_a_character_location[0] - 90, select_a_character_location[1] + 85, "template_target")
                elif "target(2)" in target:
                    MessageLog.print_message("[COMBAT] Targeting Character 2 for Skill.")
                    MouseUtils.move_and_click_point(select_a_character_location[0], select_a_character_location[1] + 85, "template_target")
                elif "target(3)" in target:
                    MessageLog.print_message("[COMBAT] Targeting Character 3 for Skill.")
                    MouseUtils.move_and_click_point(select_a_character_location[0] + 90, select_a_character_location[1] + 85, "template_target")
                elif "target(4)" in target:
                    MessageLog.print_message("[COMBAT] Targeting Character 4 for Skill.")
                    MouseUtils.move_and_click_point(select_a_character_location[0] - 90, select_a_character_location[1] + 250, "template_target")
                elif "target(5)" in target:
                    MessageLog.print_message("[COMBAT] Targeting Character 5 for Skill.")
                    MouseUtils.move_and_click_point(select_a_character_location[0], select_a_character_location[1] + 250, "template_target")
                elif "target(6)" in target:
                    MessageLog.print_message("[COMBAT] Targeting Character 6 for Skill.")
                    MouseUtils.move_and_click_point(select_a_character_location[0] + 90, select_a_character_location[1] + 250, "template_target")

            # Else, check if the character is skill-sealed.
            elif ImageUtils.confirm_location("skill_unusable", tries = 2):
                MessageLog.print_message("[COMBAT] Character is currently skill-sealed. Unable to execute command.")
                Game.find_and_click_button("cancel")

        # Once all the commands for the selected Character have been processed, click the "Back" button to return.
        Game.find_and_click_button("back")

        return None

    @staticmethod
    def _use_summon(command: str):
        """Activate the specified Summon.

        Args:
            command (str): The command to be executed.

        Returns:
            None
        """
        for summon_index in range(1, 7):
            if command == f"summon({summon_index})":
                from bot.game import Game

                # Click the "Summon" button to bring up the available Summons.
                MessageLog.print_message(f"[COMBAT] Invoking Summon #{summon_index}.")
                Game.find_and_click_button("summon")

                # Click on the specified Summon.
                if summon_index == 1:
                    MouseUtils.move_and_click_point(CombatMode._attack_button_location[0] - 317, CombatMode._attack_button_location[1] + 138, "template_summon", mouse_clicks = 2)
                elif summon_index == 2:
                    MouseUtils.move_and_click_point(CombatMode._attack_button_location[0] - 243, CombatMode._attack_button_location[1] + 138, "template_summon", mouse_clicks = 2)
                elif summon_index == 3:
                    MouseUtils.move_and_click_point(CombatMode._attack_button_location[0] - 165, CombatMode._attack_button_location[1] + 138, "template_summon", mouse_clicks = 2)
                elif summon_index == 4:
                    MouseUtils.move_and_click_point(CombatMode._attack_button_location[0] - 89, CombatMode._attack_button_location[1] + 138, "template_summon", mouse_clicks = 2)
                elif summon_index == 5:
                    MouseUtils.move_and_click_point(CombatMode._attack_button_location[0] - 12, CombatMode._attack_button_location[1] + 138, "template_summon", mouse_clicks = 2)
                else:
                    MouseUtils.move_and_click_point(CombatMode._attack_button_location[0] + 63, CombatMode._attack_button_location[1] + 138, "template_summon", mouse_clicks = 2)

                # Check if it is able to be summoned.
                if ImageUtils.confirm_location("summon_details"):
                    if Game.find_and_click_button("ok") is False:
                        MessageLog.print_message("[COMBAT] Summon #{j} cannot be invoked due to current restrictions.")
                        Game.find_and_click_button("cancel")

                # Click the "Back" button to return.
                Game.find_and_click_button("back", tries = 1)

        return None

    @staticmethod
    def _wait_for_attack():
        """Wait for several tries until the bot sees either the Attack or the Next button before starting a new turn.

        Returns:
            None
        """
        MessageLog.print_message("\n[COMBAT] Now waiting for attack to end...")
        tries = 10
        while tries > 0 and not CombatMode._retreat_check and ImageUtils.find_button("attack", tries = 1, suppress_error = True) is None and \
                ImageUtils.find_button("next", tries = 1, suppress_error = True) is None:
            # Stagger the checks for dialog popups.
            if tries % 2 == 0:
                CombatMode._find_dialog_in_combat()

                # Check if the Party wiped after attacking.
                CombatMode._party_wipe_check()

                if ImageUtils.confirm_location("battle_concluded", tries = 1, suppress_error = True) is True or \
                        ImageUtils.confirm_location("exp_gained", tries = 1, suppress_error = True) is True:
                    break

            tries -= 1

        MessageLog.print_message("[COMBAT] Attack ended.")

        return None

    @staticmethod
    def _reload_for_attack():
        """Determine whether or not to reload after an Attack.

        Returns:
            None
        """
        event_raids = ["VH Event Raid", "EX Event Raid", "IM Event Raid"]
        rotb_raids = ["EX Zhuque", "EX Xuanwu", "EX Baihu", "EX Qinglong", "Lvl 100 Shenxian"]
        dread_barrage_raids = ["1 Star", "2 Star", "3 Star", "4 Star", "5 Star"]
        proving_grounds_raids = ["Extreme", "Extreme+"]
        guild_wars_raids = ["Very Hard", "Extreme", "Extreme+", "NM90", "NM100", "NM150"]
        xeno_clash_raids = ["Xeno Clash Raid"]

        # If the "Cancel" button vanishes, that means the attack is in-progress. Now reload the page and wait for either the attack to finish or Battle ended.
        if Settings.farming_mode == "Raid" or \
                event_raids.__contains__(Settings.mission_name) or \
                rotb_raids.__contains__(Settings.mission_name) or \
                dread_barrage_raids.__contains__(Settings.mission_name) or \
                (Settings.farming_mode == "Proving Grounds" and proving_grounds_raids.__contains__(Settings.mission_name)) or \
                (Settings.farming_mode == "Guild Wars" and guild_wars_raids.__contains__(Settings.mission_name)) or \
                xeno_clash_raids.__contains__(Settings.mission_name):
            from bot.game import Game

            MessageLog.print_message("[COMBAT] Reloading now.")
            Game.find_and_click_button("reload")
            Game.wait(3.0)

        return None

    @staticmethod
    def _process_incorrect_turn(turn_number: int) -> int:
        """Processes the current turn manually in order to get the bot to the expected turn number.

        Args:
            turn_number (int): The current turn number.

        Returns:
            (int): The incremented turn number.
        """
        from bot.game import Game

        MessageLog.print_message(f"[COMBAT] Starting Turn {turn_number}.")

        # Clear any detected dialog popups that might obstruct the "Attack" button.
        CombatMode._find_dialog_in_combat()

        # Click the "Attack" button.
        MessageLog.print_message(f"[COMBAT] Ending Turn {turn_number}.")
        Game.find_and_click_button("attack", tries = 10)

        # Wait until the "Cancel" button vanishes from the screen.
        if ImageUtils.find_button("combat_cancel", tries = 3) is not None:
            while ImageUtils.wait_vanish("combat_cancel", timeout = 5) is False:
                if Settings.debug_mode:
                    MessageLog.print_message("[DEBUG] The \"Cancel\" button has not vanished from the screen yet.")
                Game.wait(1)

        CombatMode._reload_for_attack()
        CombatMode._wait_for_attack()

        MessageLog.print_message(f"[COMBAT] Turn {turn_number} has ended.")

        if Game.find_and_click_button("next", tries = 1, suppress_error = True):
            Game.wait(3)

        turn_number += 1

        return turn_number

    @staticmethod
    def start_combat_mode(script_commands: List[str] = None, is_nightmare: bool = False):
        """Start Combat Mode with the given script file path. Start reading through the text file line by line and have the bot proceed with the commands accordingly.

        Args:
            script_commands (List[str]): List of script commands to use instead of reading from a text file. Defaults to None.
            is_nightmare (bool, optional): If Combat Mode is being used for a Nightmare, determines the method of reading the script file.

        Returns:
            (bool): Return True if Combat Mode was successful. Else, return False if the Party wiped or backed out without retreating.
        """
        from bot.game import Game

        start_time: float = time.time()

        # Reset flags and Attack button location.
        CombatMode._retreat_check = False
        semi_auto = False
        full_auto = False
        manual_attack_and_reload = False
        CombatMode._attack_button_location = None
        command_turn_number = 1
        turn_number = 1  # Current turn for the script execution.

        MessageLog.print_message("\n######################################################################")
        MessageLog.print_message("######################################################################")
        MessageLog.print_message(f"[COMBAT] Starting Combat Mode.")
        MessageLog.print_message("######################################################################")
        MessageLog.print_message("######################################################################\n")

        if script_commands is not None:
            command_list = script_commands
        else:
            if is_nightmare:
                MessageLog.print_message(f"Name of Nightmare combat script loaded: {Settings.nightmare_combat_script_name}")
                command_list = copy.deepcopy(Settings.nightmare_combat_script)
            else:
                MessageLog.print_message(f"Name of combat script loaded: {Settings.combat_script_name}")
                command_list = copy.deepcopy(Settings.combat_script)

        MessageLog.print_message(f"Size of script commands: {len(command_list)}")

        # If current Farming Mode is Arcarum, attempt to dismiss potential stage effect popup like "Can't use Charge Attacks".
        if Settings.farming_mode == "Arcarum":
            Game.find_and_click_button("arcarum_stage_effect_active", tries = 5)

        # Save the positions of the "Attack" and "Back" button.
        CombatMode._attack_button_location = ImageUtils.find_button("attack", tries = 50)
        if CombatMode._attack_button_location is None:
            MessageLog.print_message(f"\n[ERROR] Cannot find Attack button. Raid must have just ended.")
            return False

        ######################################################################
        ######################################################################
        # This is where the main workflow of Combat Mode is located.
        while len(command_list) > 0 and CombatMode._retreat_check is False and semi_auto is False and full_auto is False:
            # All the logic that follows assumes that the command string is lowercase to allow case-insensitive commands.
            command = command_list.pop(0).strip().lower()
            if command == "" or command[0] == "#" or command[0] == "/":
                continue

            # Check if the Battle has ended.
            if CombatMode._retreat_check or ImageUtils.confirm_location("no_loot", tries = 1, suppress_error = True):
                MessageLog.print_message("\n######################################################################")
                MessageLog.print_message("######################################################################")
                MessageLog.print_message("[COMBAT] Combat Mode has ended with no loot.")
                MessageLog.print_message("######################################################################")
                MessageLog.print_message("######################################################################")
                return False
            elif ImageUtils.confirm_location("battle_concluded", tries = 1, suppress_error = True):
                MessageLog.print_message("\n[COMBAT] Battle concluded suddenly.")
                MessageLog.print_message("\n######################################################################")
                MessageLog.print_message("######################################################################")
                MessageLog.print_message("[COMBAT] Ending Combat Mode.")
                MessageLog.print_message("######################################################################")
                MessageLog.print_message("######################################################################")
                Game.find_and_click_button("reload")
                return True
            elif ImageUtils.confirm_location("exp_gained", tries = 1, suppress_error = True):
                MessageLog.print_message("\n######################################################################")
                MessageLog.print_message("######################################################################")
                MessageLog.print_message("[COMBAT] Ending Combat Mode.")
                MessageLog.print_message("######################################################################")
                MessageLog.print_message("######################################################################")
                return True

            MessageLog.print_message(f"\n[COMBAT] Reading command: \"{command}\"")

            if command.__contains__("turn"):
                # Clear any detected dialog popups that might obstruct the "Attack" button.
                CombatMode._find_dialog_in_combat()

                # Parse the Turn's number.
                command_turn_number = int(command.split(":")[0].split(" ")[1])

                # If the command is a "Turn #:" and it is currently not the correct Turn, attack until the Turn numbers match.
                if CombatMode._retreat_check is False and turn_number != command_turn_number:
                    MessageLog.print_message(f"[COMBAT] Attacking until the bot reaches Turn {command_turn_number}.")
                    while turn_number != command_turn_number:
                        turn_number = CombatMode._process_incorrect_turn(turn_number)
                else:
                    MessageLog.print_message(f"\n[COMBAT] Starting Turn {turn_number}.")

            elif turn_number == command_turn_number:
                # Process all commands here that belong inside a Turn block.

                # Determine which Character to take action.
                if "character1." in command:
                    character_selected = 1
                elif "character2." in command:
                    character_selected = 2
                elif "character3." in command:
                    character_selected = 3
                elif "character4." in command:
                    character_selected = 4
                else:
                    character_selected = 0

                if character_selected != 0:
                    # Select the specified Character.
                    CombatMode._select_character(character_selected)

                    # Now execute each Skill command starting from left to right.
                    skill_command_list = command.split(".")
                    skill_command_list.pop(0)  # Remove the "character" portion of the string.
                    CombatMode._use_character_skill(character_selected, skill_command_list)

                # Handle any other supported command.
                elif command == "requestbackup":
                    CombatMode._request_backup()
                elif command == "tweetbackup":
                    CombatMode._tweet_backup()
                elif CombatMode._healing_item_commands.__contains__(command):
                    CombatMode._use_combat_healing_item(command)
                elif command.__contains__("summon") and command != "quicksummon":
                    CombatMode._use_summon(command)
                elif command == "quicksummon":
                    MessageLog.print_message("[COMBAT] Quick Summoning now...")
                    if Game.find_and_click_button("quick_summon1") or Game.find_and_click_button("quick_summon2"):
                        MessageLog.print_message("[COMBAT] Successfully quick summoned!")
                    else:
                        MessageLog.print_message("[COMBAT] Was not able to quick summon this Turn.")
                elif command == "enablesemiauto":
                    MessageLog.print_message("[COMBAT] Bot will now attempt to enable Semi Auto...")
                    semi_auto = True
                    break
                elif command == "enablefullauto":
                    MessageLog.print_message("[COMBAT] Bot will now attempt to enable Full Auto...")
                    full_auto = Game.find_and_click_button("full_auto")

                    # If the bot failed to find and click the "Full Auto" button, fallback to the "Semi Auto" button.
                    if not full_auto:
                        MessageLog.print_message("[COMBAT] Bot failed to find the \"Full Auto\" button. Falling back to Semi Auto.")
                        semi_auto = True
                    break
                elif "targetenemy" in command:
                    # Select enemy target.
                    CombatMode._select_enemy_target(command)
                elif "back" in command and Game.find_and_click_button("home_back", tries = 1):
                    MessageLog.print_message("[COMBAT] Tapped the Back button.")
                    CombatMode._wait_for_attack()

                    # Advance the Turn number by 1.
                    turn_number += 1
                elif "reload" in command:
                    MessageLog.print_message("[COMBAT] Bot will now attempt to manually reload...")

                    # Press the "Attack" button in order to show the "Cancel" button. Once that disappears, manually reload the page.
                    if Game.find_and_click_button("attack"):
                        if ImageUtils.wait_vanish("combat_cancel", timeout = 10):
                            Game.find_and_click_button("reload")
                            Game.wait(3.0)
                        else:
                            # If the "Cancel" button fails to disappear after 10 tries, reload anyways.
                            Game.find_and_click_button("reload")
                            Game.wait(3.0)
                elif command == "repeatmanualattackandreload":
                    MessageLog.print_message("[COMBAT] Enabling manually pressing the Attack button and reloading (if the mission supports it) until battle ends.")
                    manual_attack_and_reload = True
                elif semi_auto is False and full_auto is False and command == "end":
                    # Click the "Attack" button once every command inside the Turn Block has been processed.
                    MessageLog.print_message(f"[COMBAT] Ending Turn {turn_number}.")
                    Game.find_and_click_button("attack", tries = 10)

                    # Wait until the "Cancel" button vanishes from the screen.
                    if ImageUtils.find_button("combat_cancel", tries = 3) is not None:
                        while ImageUtils.wait_vanish("combat_cancel", timeout = 5) is False:
                            if Settings.debug_mode:
                                MessageLog.print_message("[DEBUG] The \"Cancel\" button has not vanished from the screen yet.")
                            Game.wait(1)

                    CombatMode._reload_for_attack()
                    CombatMode._wait_for_attack()

                    MessageLog.print_message(f"[COMBAT] Turn {turn_number} has ended.")

                    turn_number += 1

                    if CombatMode._retreat_check or ImageUtils.confirm_location("no_loot", tries = 1, suppress_error = True):
                        MessageLog.print_message("\n######################################################################")
                        MessageLog.print_message("######################################################################")
                        MessageLog.print_message("[COMBAT] Combat Mode has ended with no loot")
                        MessageLog.print_message("######################################################################")
                        MessageLog.print_message("######################################################################")
                        return False
                    elif ImageUtils.confirm_location("battle_concluded", tries = 1, suppress_error = True):
                        MessageLog.print_message("\n[COMBAT] Battle concluded suddenly.")
                        MessageLog.print_message("\n######################################################################")
                        MessageLog.print_message("######################################################################")
                        MessageLog.print_message("[COMBAT] Ending Combat Mode.")
                        MessageLog.print_message("######################################################################")
                        MessageLog.print_message("######################################################################")
                        Game.find_and_click_button("reload")
                        return True
                    elif ImageUtils.confirm_location("exp_gained", tries = 1, suppress_error = True):
                        MessageLog.print_message("\n######################################################################")
                        MessageLog.print_message("######################################################################")
                        MessageLog.print_message("[COMBAT] Ending Combat Mode.")
                        MessageLog.print_message("######################################################################")
                        MessageLog.print_message("######################################################################")
                        return True

                    if Game.find_and_click_button("next", tries = 1, suppress_error = True):
                        Game.wait(3)
                elif command == "exit":
                    # End Combat Mode by heading back to the Home screen without retreating.
                    MessageLog.print_message("\n[COMBAT] Leaving this Raid without retreating.")
                    MessageLog.print_message("\n######################################################################")
                    MessageLog.print_message("######################################################################")
                    MessageLog.print_message("[COMBAT] Ending Combat Mode.")
                    MessageLog.print_message("######################################################################")
                    MessageLog.print_message("######################################################################")
                    Game.go_back_home(confirm_location_check = True)
                    return False

            # Handle certain commands that could be present outside of a Turn block.
            if semi_auto is False and full_auto is False and command == "enablesemiauto":
                MessageLog.print_message("[COMBAT] Bot will now attempt to enable Semi Auto...")
                semi_auto = True
                break
            elif semi_auto is False and full_auto is False and command == "enablefullauto":
                MessageLog.print_message("[COMBAT] Bot will now attempt to enable Full Auto...")
                full_auto = Game.find_and_click_button("full_auto")

                # If the bot failed to find and click the "Full Auto" button, fallback to the "Semi Auto" button.
                if not full_auto:
                    MessageLog.print_message("[COMBAT] Bot failed to find the \"Full Auto\" button. Falling back to Semi Auto.")
                    semi_auto = True
                break
            elif command == "repeatmanualattackandreload":
                MessageLog.print_message("[COMBAT] Enabling manually pressing the Attack button and reloading (if the mission supports it) until battle ends.")
                manual_attack_and_reload = True

        # Deal with any the situation where high-profile raids end right when the bot loads in and all it sees is the "Next" button.
        if Settings.farming_mode == "Raid" and Game.find_and_click_button("next", tries = 3):
            MessageLog.print_message("\n######################################################################")
            MessageLog.print_message("######################################################################")
            MessageLog.print_message("[COMBAT] Ending Combat Mode.")
            MessageLog.print_message("######################################################################")
            MessageLog.print_message("######################################################################")
            return True

        ######################################################################
        ######################################################################
        # When the bot reaches here, all the commands in the combat script has been processed.
        MessageLog.print_message("\n[COMBAT] Bot has reached end of script. Automatically attacking until battle ends or Party wipes...")

        if manual_attack_and_reload is False:
            # Attempt to activate Full Auto at the end of the combat script. If not, then attempt to activate Semi Auto.
            if semi_auto is False and full_auto is False:
                full_auto = Game.find_and_click_button("full_auto")

                # If the bot failed to find and click the "Full Auto" button, fallback to the "Semi Auto" button.
                if not full_auto:
                    MessageLog.print_message("[COMBAT] Bot failed to find the \"Full Auto\" button. Falling back to Semi Auto.")
                    semi_auto = True

            # Double check to see if Semi Auto is turned on. Note that the "Semi Auto" button only appears while the Party is attacking.
            if not CombatMode._retreat_check and semi_auto and not full_auto:
                MessageLog.print_message("[COMBAT] Double checking to see if Semi Auto is enabled...")
                enabled_semi_auto = ImageUtils.find_button("semi_auto_enabled")
                if not enabled_semi_auto:
                    # Have the Party attack and then attempt to see if the "Semi Auto" button becomes visible.
                    Game.find_and_click_button("attack")
                    enabled_semi_auto = Game.find_and_click_button("semi_auto", tries = 5)

                    # If the bot still cannot find the "Semi Auto" button, that probably means the user has the "Full Auto" button on the screen instead of the "Semi Auto" button.
                    if not enabled_semi_auto:
                        MessageLog.print_message("[COMBAT] Failed to enable Semi Auto. Falling back to Full Auto...")
                        semi_auto = False
                        full_auto = True

                        # Enable Full Auto.
                        Game.find_and_click_button("full_auto")
                    else:
                        MessageLog.print_message("[COMBAT] Semi Auto is now enabled.")

            # Main workflow loop for both Semi Auto and Full Auto. The bot will progress the Quest/Raid until it ends or the Party wipes.
            while not CombatMode._retreat_check and (full_auto or semi_auto):
                # Back out of the Raid without retreating if the allowed time has been exceeded.
                if Settings.farming_mode == "Raid" and Settings.enable_auto_exit_raid and time.time() - start_time >= Settings.time_allowed_until_auto_exit_raid:
                    MessageLog.print_message("\n######################################################################")
                    MessageLog.print_message("######################################################################")
                    MessageLog.print_message("[COMBAT] Combat Mode ended due to exceeding time allowed.")
                    MessageLog.print_message("######################################################################")
                    MessageLog.print_message("######################################################################")
                    return False

                # Check if the Battle has ended.
                if CombatMode._retreat_check or ImageUtils.confirm_location("no_loot", tries = 1, suppress_error = True):
                    MessageLog.print_message("\n######################################################################")
                    MessageLog.print_message("######################################################################")
                    MessageLog.print_message("[COMBAT] Combat Mode has ended with no loot.")
                    MessageLog.print_message("######################################################################")
                    MessageLog.print_message("######################################################################")
                    return False
                elif ImageUtils.confirm_location("battle_concluded", tries = 1, suppress_error = True):
                    MessageLog.print_message("\n[COMBAT] Battle concluded suddenly.")
                    MessageLog.print_message("\n######################################################################")
                    MessageLog.print_message("######################################################################")
                    MessageLog.print_message("[COMBAT] Ending Combat Mode.")
                    MessageLog.print_message("######################################################################")
                    MessageLog.print_message("######################################################################")
                    Game.find_and_click_button("reload")
                    return True
                elif ImageUtils.confirm_location("exp_gained", tries = 1, suppress_error = True):
                    MessageLog.print_message("\n######################################################################")
                    MessageLog.print_message("######################################################################")
                    MessageLog.print_message("[COMBAT] Ending Combat Mode.")
                    MessageLog.print_message("######################################################################")
                    MessageLog.print_message("######################################################################")
                    return True

                if Game.find_and_click_button("next", tries = 1, suppress_error = True):
                    Game.wait(3)

                CombatMode._party_wipe_check()
        else:
            # Main workflow loop for manually pressing the Attack button and reloading until combat ends.
            while not CombatMode._retreat_check:
                # Back out of the Raid without retreating if the allowed time has been exceeded.
                if Settings.farming_mode == "Raid" and Settings.enable_auto_exit_raid and time.time() - start_time >= Settings.time_allowed_until_auto_exit_raid:
                    MessageLog.print_message("\n######################################################################")
                    MessageLog.print_message("######################################################################")
                    MessageLog.print_message("[COMBAT] Combat Mode ended due to exceeding time allowed.")
                    MessageLog.print_message("######################################################################")
                    MessageLog.print_message("######################################################################")
                    return False

                # Check if the Battle has ended.
                if CombatMode._retreat_check or ImageUtils.confirm_location("no_loot", tries = 1, suppress_error = True):
                    MessageLog.print_message("\n######################################################################")
                    MessageLog.print_message("######################################################################")
                    MessageLog.print_message("[COMBAT] Combat Mode has ended with no loot.")
                    MessageLog.print_message("######################################################################")
                    MessageLog.print_message("######################################################################")
                    return False
                elif ImageUtils.confirm_location("battle_concluded", tries = 1, suppress_error = True):
                    MessageLog.print_message("\n[COMBAT] Battle concluded suddenly.")
                    MessageLog.print_message("\n######################################################################")
                    MessageLog.print_message("######################################################################")
                    MessageLog.print_message("[COMBAT] Ending Combat Mode.")
                    MessageLog.print_message("######################################################################")
                    MessageLog.print_message("######################################################################")
                    Game.find_and_click_button("reload")
                    return True
                elif ImageUtils.confirm_location("exp_gained", tries = 1, suppress_error = True):
                    MessageLog.print_message("\n######################################################################")
                    MessageLog.print_message("######################################################################")
                    MessageLog.print_message("[COMBAT] Ending Combat Mode.")
                    MessageLog.print_message("######################################################################")
                    MessageLog.print_message("######################################################################")
                    return True

                if Game.find_and_click_button("next", tries = 1, suppress_error = True):
                    Game.wait(3)

                Game.find_and_click_button("attack", tries = 10)
                CombatMode._reload_for_attack()
                CombatMode._wait_for_attack()

        ######################################################################
        ######################################################################

        MessageLog.print_message("\n######################################################################")
        MessageLog.print_message("######################################################################")
        MessageLog.print_message("[COMBAT] Ending Combat Mode.")
        MessageLog.print_message("######################################################################")
        MessageLog.print_message("######################################################################")

        if not CombatMode._retreat_check:
            return True
        else:
            return False
