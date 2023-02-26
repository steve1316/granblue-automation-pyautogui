import copy
import os
from typing import List
import time

from utils.settings import Settings
from utils.message_log import MessageLog
from utils.image_utils import ImageUtils
from utils.mouse_utils import MouseUtils


class CombatModeException(Exception):
    def __init__(self, message):
        super().__init__(message)


class CombatMode:
    """
    Provides the utility functions needed for Combat Mode.
    """

    # Save a reference to the original current working directory.
    _owd = os.getcwd()

    _healing_item_commands = ["usegreenpotion.target(1)", "usegreenpotion.target(2)", "usegreenpotion.target(3)", "usegreenpotion.target(4)", "usebluepotion", "usefullelixir",
                              "usesupportpotion", "useclarityherb.target(1)", "useclarityherb.target(2)", "useclarityherb.target(3)", "useclarityherb.target(4)", "userevivalpotion"]

    # Save some variables for use throughout the class.
    _semi_auto = False
    _full_auto = False
    _attack_button_location = None
    _retreat_check = False
    _start_time: float = None
    _list_of_exit_events_for_false = ["Time Exceeded", "No Loot"]
    _list_of_exit_events_for_true = ["Battle Concluded", "Exp Gained", "Loot Collected"]
    _command_turn_number = 1
    _turn_number = 1  # Current turn for the script execution.

    ######################################################################
    ######################################################################
    # Checks
    ######################################################################
    ######################################################################

    @staticmethod
    def _check_for_wipe():
        """Check to see if the Party has wiped during Combat Mode. Update the retreat check flag if so.

        Returns:
            None
        """
        from bot.game import Game

        # Check to see if Party has wiped.
        if Settings.debug_mode:
            MessageLog.print_message(f"\n[DEBUG] Checking to see if the Party wiped...")

        party_wipe_indicator = ImageUtils.find_button("party_wipe_indicator", tries = 3, suppress_error = True)
        if party_wipe_indicator is not None or ImageUtils.confirm_location("salute_participants", tries = 3, suppress_error = True):
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
    def _check_for_dialog():
        """Check if there are dialog popups from either Lyria or Vyrn and click them away.

        Returns:
            None
        """
        dialog_location = ImageUtils.find_button("dialog_lyria", tries = 2, suppress_error = True, bypass_general_adjustment = True)
        if dialog_location is None:
            dialog_location = ImageUtils.find_button("dialog_vyrn", tries = 2, suppress_error = True, bypass_general_adjustment = True)

        if dialog_location is not None:
            if Settings.use_first_notch is False:
                MouseUtils.move_and_click_point(dialog_location[0] + 180, dialog_location[1] - 50, "template_dialog")
            else:
                MouseUtils.move_and_click_point(dialog_location[0] + 130, dialog_location[1] - 40, "template_dialog")

        return None

    @staticmethod
    def _check_for_battle_end() -> str:
        """Perform checks to see if the battle ended or not.

        Returns:
            (str): Return "Nothing" if combat is still continuing. Otherwise, raise a CombatModeException whose message is the event name that caused the battle to end.
        """
        from bot.game import Game

        # Check if the Battle has ended.
        if Settings.farming_mode == "Raid" and Settings.enable_auto_exit_raid and time.time() - CombatMode._start_time >= Settings.time_allowed_until_auto_exit_raid:
            MessageLog.print_message("\n######################################################################")
            MessageLog.print_message("######################################################################")
            MessageLog.print_message("[COMBAT] Combat Mode ended due to exceeding time allowed.")
            MessageLog.print_message("######################################################################")
            MessageLog.print_message("######################################################################")
            raise CombatModeException("Time Exceeded")
        elif CombatMode._retreat_check or ImageUtils.confirm_location("no_loot", tries = 1, suppress_error = True, bypass_general_adjustment = True):
            MessageLog.print_message("\n######################################################################")
            MessageLog.print_message("######################################################################")
            MessageLog.print_message("[COMBAT] Combat Mode has ended with no loot.")
            MessageLog.print_message("######################################################################")
            MessageLog.print_message("######################################################################")
            raise CombatModeException("No Loot")
        elif ImageUtils.confirm_location("battle_concluded", tries = 1, suppress_error = True, bypass_general_adjustment = True):
            MessageLog.print_message("\n[COMBAT] Battle concluded suddenly.")
            MessageLog.print_message("\n######################################################################")
            MessageLog.print_message("######################################################################")
            MessageLog.print_message("[COMBAT] Ending Combat Mode.")
            MessageLog.print_message("######################################################################")
            MessageLog.print_message("######################################################################")
            Game.find_and_click_button("reload")
            raise CombatModeException("Battle Concluded")
        elif ImageUtils.confirm_location("exp_gained", tries = 1, suppress_error = True, bypass_general_adjustment = True):
            MessageLog.print_message("\n######################################################################")
            MessageLog.print_message("######################################################################")
            MessageLog.print_message("[COMBAT] Ending Combat Mode.")
            MessageLog.print_message("######################################################################")
            MessageLog.print_message("######################################################################")
            raise CombatModeException("Exp Gained")
        elif ImageUtils.confirm_location("loot_collected", tries = 1, suppress_error = True, bypass_general_adjustment = True):
            MessageLog.print_message("\n######################################################################")
            MessageLog.print_message("######################################################################")
            MessageLog.print_message("[COMBAT] Ending Combat Mode.")
            MessageLog.print_message("######################################################################")
            MessageLog.print_message("######################################################################")
            raise CombatModeException("Loot Collected")
        else:
            return "Nothing"

    @staticmethod
    def _check_raid() -> bool:
        """Check if the current battle is a raid-like battle.

        Returns:
            (bool): True if the current battle is a raid-like battle.
        """
        event_raids = ["VH Event Raid", "EX Event Raid", "IM Event Raid"]
        rotb_raids = ["EX Zhuque", "EX Xuanwu", "EX Baihu", "EX Qinglong", "Lvl 100 Shenxian"]
        dread_barrage_raids = ["1 Star", "2 Star", "3 Star", "4 Star", "5 Star"]
        proving_grounds_raids = ["Extreme", "Extreme+"]
        guild_wars_raids = ["Very Hard", "Extreme", "Extreme+", "NM90", "NM95", "NM100", "NM150"]
        xeno_clash_raids = ["Xeno Clash Raid"]

        if Settings.farming_mode == "Raid" or \
                event_raids.__contains__(Settings.mission_name) or \
                rotb_raids.__contains__(Settings.mission_name) or \
                dread_barrage_raids.__contains__(Settings.mission_name) or \
                (Settings.farming_mode == "Proving Grounds" and proving_grounds_raids.__contains__(Settings.mission_name)) or \
                (Settings.farming_mode == "Guild Wars" and guild_wars_raids.__contains__(Settings.mission_name)) or \
                xeno_clash_raids.__contains__(Settings.mission_name) or Settings.farming_mode == "Arcarum" or Settings.farming_mode == "Arcarum Sandbox":
            return True
        else:
            return False

    ######################################################################
    ######################################################################
    # Helper Methods
    ######################################################################
    ######################################################################

    @staticmethod
    def _select_character(character_number: int):
        """Selects the portrait of the character specified on the Combat screen.

        Args:
            character_number (int): The character that needs to be selected on the Combat screen.

        Returns:
            None
        """
        if Settings.use_first_notch is False:
            x_offset = 320
            x_inc = 80
        else:
            x_offset = 215
            x_inc = 55

        if character_number == 1:
            x = CombatMode._attack_button_location[0] - x_offset + (x_inc * 0)
        elif character_number == 2:
            x = CombatMode._attack_button_location[0] - x_offset + (x_inc * 1)
        elif character_number == 3:
            x = CombatMode._attack_button_location[0] - x_offset + (x_inc * 2)
        elif character_number == 4:
            x = CombatMode._attack_button_location[0] - x_offset + (x_inc * 3)
        else:
            MessageLog.print_message(f"[WARNING] Invalid command received for selecting a Character. User wanted to select Character #{character_number}.")
            return

        y = CombatMode._attack_button_location[1] + 123

        # Double-clicking the character portrait to avoid any non-invasive popups from other Raid participants.
        MouseUtils.move_and_click_point(x, y, "template_character", mouse_clicks = 2)

        return None

    @staticmethod
    def _reload_for_attack(override: bool = False) -> bool:
        """Determine whether or not to reload after an Attack.

        Args:
            override (bool): Override the set checks and reload anyways. Defaults to false.

        Returns:
            (bool): True if the bot reloaded the page. False otherwise.
        """
        # If the "Cancel" button vanishes, that means the attack is in-progress. Now reload the page and wait for either the attack to finish or Battle ended.
        if Settings.enable_refresh_during_combat and (CombatMode._check_raid() or override or (Settings.farming_mode == "Generic" and Settings.enable_force_reload)):
            from bot.game import Game

            if CombatMode._check_for_battle_end() == "Nothing":
                MessageLog.print_message("[COMBAT] Reloading now.")
                Game.find_and_click_button("reload")

                if Settings.enable_combat_mode_adjustment:
                    Game.wait(Settings.adjust_waiting_for_reload)
                else:
                    Game.wait(3.0)

                return True

        return False

    @staticmethod
    def _process_incorrect_turn():
        """Processes the current turn manually in order to get the bot to the expected turn number.

        Returns:
            None
        """
        from bot.game import Game

        # Clear any detected dialog popups that might obstruct the "Attack" button.
        CombatMode._check_for_dialog()

        # Wait for the Attack to process.
        MessageLog.print_message(f"[COMBAT] Ending Turn {CombatMode._turn_number}...")
        if CombatMode._full_auto is False and CombatMode._semi_auto is False:
            Game.find_and_click_button("attack", tries = 30)
            while ImageUtils.find_button("cancel", suppress_error = True) is not None:
                if Settings.debug_mode:
                    MessageLog.print_message("[DEBUG] While waiting for the incorrect turn to process, the \"Cancel\" button has not vanished from the screen yet.")
                Game.wait(1.0)
        else:
            while ImageUtils.find_button("attack", suppress_error = True) is not None:
                if Settings.debug_mode:
                    MessageLog.print_message("[DEBUG] While waiting for the incorrect turn to process, the \"Attack\" button has not vanished from the screen yet.")
                Game.wait(1.0)

        reload_check = False

        # If the next Turn is the current Turn block, turn off auto.
        if CombatMode._turn_number + 1 == CombatMode._command_turn_number:
            reload_check = CombatMode._reload_for_attack()
            if reload_check is False:
                if CombatMode._full_auto:
                    MouseUtils.scroll_screen_from_home_button(0)  # Move the cursor if it is hovering over the Full/Semi Auto button.
                    Game.find_and_click_button("full_auto_enabled", tries = 10)
                elif CombatMode._semi_auto:
                    MouseUtils.scroll_screen_from_home_button(0)  # Move the cursor if it is hovering over the Full/Semi Auto button.
                    Game.find_and_click_button("semi_auto_enabled", tries = 10)

            CombatMode._full_auto = False
            CombatMode._semi_auto = False

        Game.wait(1.0)

        # If the bot reloaded the page, determine if bot needs to enable Full/Semi Auto again.
        if reload_check is False:
            reload_check = CombatMode._reload_for_attack()
            if reload_check and CombatMode._full_auto:
                CombatMode._enable_full_auto()
            elif reload_check and CombatMode._semi_auto:
                CombatMode._enable_semi_auto()

        CombatMode._wait_for_attack()

        MessageLog.print_message(f"[COMBAT] Turn {CombatMode._turn_number} has ended.")

        if Game.find_and_click_button("next", tries = 3, suppress_error = True):
            Game.wait(3)

        CombatMode._turn_number += 1

        MessageLog.print_message(f"\n[COMBAT] Starting Turn {CombatMode._turn_number}.")

        return None

    @staticmethod
    def _wait_for_attack() -> bool:
        """Wait for several tries until the bot sees either the Attack or the Next button before starting a new turn.

        Returns:
            (bool): True if Attack ended into the next Turn. False if Attack ended but combat also ended as well.
        """
        MessageLog.print_message("[COMBAT] Now waiting for attack to end...")
        if Settings.enable_combat_mode_adjustment:
            tries = Settings.adjust_waiting_for_attack
        else:
            tries = 100

        while tries > 0 and not CombatMode._retreat_check and ImageUtils.find_button("attack", tries = 1, suppress_error = True) is None and \
                ImageUtils.find_button("next", tries = 1, suppress_error = True) is None:
            CombatMode._check_for_dialog()

            # Check if the Party wiped after attacking.
            CombatMode._check_for_wipe()

            CombatMode._check_for_battle_end()

            tries -= 1

        MessageLog.print_message("[COMBAT] Attack ended.")

        return True

    @staticmethod
    def _enable_auto() -> bool:
        """Enable Full/Semi auto for this battle.

        Returns:
            (bool): True if Full/Semi auto is enabled.
        """
        from bot.game import Game

        if Settings.enable_refresh_during_combat and Settings.enable_auto_quick_summon:
            MessageLog.print_message(f"[COMBAT] Automatically attempting to use Quick Summon...")
            CombatMode._quick_summon()

        enable_auto = Game.find_and_click_button("full_auto") or ImageUtils.find_button("full_auto_enabled")

        # If the bot failed to find and click the "Full Auto" button, fallback to the "Semi Auto" button.
        if enable_auto is False:
            MessageLog.print_message(f"[COMBAT] Failed to find the \"Full Auto\" button. Falling back to Semi Auto.")
            MessageLog.print_message(f"[COMBAT] Double checking to see if Semi Auto is enabled.")

            enabled_semi_auto_button_location = ImageUtils.find_button("semi_button_enabled")
            if enabled_semi_auto_button_location is None:
                # Have the Party attack and then attempt to see if the "Semi Auto" button becomes visible.
                Game.find_and_click_button("attack")

                Game.wait(2.0)

                enable_auto = Game.find_and_click_button("semi_auto", tries = 10)
                if enable_auto:
                    MessageLog.print_message("[COMBAT] Semi Auto is now enabled.")
        else:
            MessageLog.print_message(f"[COMBAT] Enabled Full Auto.")

        return enable_auto

    ######################################################################
    ######################################################################
    # Commands
    ######################################################################
    ######################################################################

    @staticmethod
    def _start_turn(command: str):
        """Start the Turn based on the read command and move the internal Turn count forward to match the command.

        Args:
            command (str): The command to execute.

        Returns:
            None
        """
        # Clear any detected dialog popups that might obstruct the "Attack" button.
        CombatMode._check_for_dialog()

        # Parse the Turn's number.
        CombatMode._command_turn_number = int(command.split(":")[0].split(" ")[1])

        # If the command is a "Turn #:" and it is currently not the correct Turn, attack until the Turn numbers match.
        if CombatMode._retreat_check is False and CombatMode._turn_number != CombatMode._command_turn_number:
            MessageLog.print_message(f"[COMBAT] Attacking until the bot reaches Turn {CombatMode._command_turn_number}.")
            while CombatMode._turn_number != CombatMode._command_turn_number:
                CombatMode._process_incorrect_turn()
        else:
            MessageLog.print_message(f"\n[COMBAT] Starting Turn {CombatMode._turn_number}.")

        return None

    @staticmethod
    def _end_turn():
        """Ends the Turn by clicking the Attack button.

        Returns:
            None
        """
        from bot.game import Game

        # Click the "Attack" button once every command inside the Turn Block has been processed.
        MessageLog.print_message(f"[COMBAT] Ending Turn {CombatMode._turn_number}...")

        if CombatMode._full_auto or CombatMode._semi_auto:
            while ImageUtils.find_button("attack") is not None:
                Game.wait(1.0)
        else:
            Game.find_and_click_button("attack", tries = 10)

            # Wait until the "Cancel" button vanishes from the screen.
            if ImageUtils.find_button("combat_cancel", tries = 10) is not None:
                while ImageUtils.wait_vanish("combat_cancel", timeout = 5, suppress_error = True) is False:
                    if Settings.debug_mode:
                        MessageLog.print_message("[DEBUG] The \"Cancel\" button has not vanished from the screen yet.")
                    Game.wait(1.0)

        # Check for exit conditions.
        CombatMode._check_for_battle_end()

        if Game.find_and_click_button("next", tries = 3, suppress_error = True):
            Game.wait(3)

        return None

    @staticmethod
    def _wait_execute(command_list: List[str], fallback_delay: float = 1.0):
        """Execute a wait command.

        Args:
            command_list (List[str]): A split list of the command by its "." delimiter with the "wait" command being the first element.
            fallback_delay (float): A default delay if the wait command was invalid. Defaults to 1.0 second.

        Returns:
            None
        """
        from bot.game import Game

        # Isolate the seconds inside the command.
        if command_list[0].__contains__(")"):
            wait_command: str = command_list[0].split("(")[1].replace(")", "")
        else:
            wait_command: str = command_list[0].split("(")[1] + "." + command_list[1].replace(")", "")

        try:
            wait_seconds: float = float(wait_command)
            MessageLog.print_message(f"[COMBAT] Now waiting {wait_seconds} second(s).")
            Game.wait(wait_seconds)
        except ValueError:
            MessageLog.print_message(f"[COMBAT] Could not parse out the seconds in the wait command. Waiting {fallback_delay} second(s) as fallback.")
            Game.wait(fallback_delay)

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

                if Settings.use_first_notch is False:
                    x_offset = 270
                    x_inc = 160
                    y_offset = 285
                else:
                    x_offset = 175
                    x_inc = 100
                    y_offset = 190

                if target == 1:
                    x = CombatMode._attack_button_location[0] - x_offset + (x_inc * 0)
                elif target == 2:
                    x = CombatMode._attack_button_location[0] - x_offset + (x_inc * 1)
                else:
                    x = CombatMode._attack_button_location[0] - x_offset + (x_inc * 2)

                y = CombatMode._attack_button_location[1] - y_offset

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
            (bool): Return True if the Turn will end due to a chained "attack" command. False otherwise.
        """
        from bot.game import Game

        # Execute every skill command in the list.
        while len(skill_command_list) > 0:
            # Stop if the Next button is present.
            if ImageUtils.find_button("next", tries = 1, suppress_error = True):
                return False

            if skill_command_list[0].__contains__("wait"):
                CombatMode._wait_execute(skill_command_list)
                skill_command_list.pop(0)
            elif skill_command_list[0].__contains__("attack"):
                CombatMode._end()
                return True
            else:
                skill = skill_command_list.pop(0)

                if Settings.use_first_notch is False:
                    x_offset = 220
                    x_inc = 85
                    y_offset = 170
                else:
                    x_offset = 145
                    x_inc = 55
                    y_offset = 115

                if skill == "useskill(1)":
                    MessageLog.print_message(f"[COMBAT] Character {character_selected} uses Skill 1.")
                    x = CombatMode._attack_button_location[0] - x_offset + (x_inc * 0)
                elif skill == "useskill(2)":
                    MessageLog.print_message(f"[COMBAT] Character {character_selected} uses Skill 2.")
                    x = CombatMode._attack_button_location[0] - x_offset + (x_inc * 1)
                elif skill == "useskill(3)":
                    MessageLog.print_message(f"[COMBAT] Character {character_selected} uses Skill 3.")
                    x = CombatMode._attack_button_location[0] - x_offset + (x_inc * 2)
                elif skill == "useskill(4)":
                    MessageLog.print_message(f"[COMBAT] Character {character_selected} uses Skill 4.")
                    x = CombatMode._attack_button_location[0] - x_offset + (x_inc * 3)
                else:
                    MessageLog.print_message(f"[WARNING] Invalid command received for using the Character's Skill. User wanted: {skill}.")
                    Game.find_and_click_button("back")
                    return False

                y = CombatMode._attack_button_location[1] + y_offset

                MouseUtils.move_and_click_point(x, y, "template_skill")

                # Check if the skill requires a target.
                if len(skill_command_list) > 0 and ImageUtils.confirm_location("use_skill", bypass_general_adjustment = True):
                    MessageLog.print_message(f"[COMBAT] Skill is awaiting a target...")
                    target = skill_command_list.pop(0)

                    if Settings.use_first_notch is False:
                        x_offset = 225
                        x_inc = 95
                        y_offset = 55
                        y_inc = 70
                    else:
                        x_offset = 150
                        x_inc = 60
                        y_offset = 35
                        y_inc = 110

                    if target == 1:
                        x = CombatMode._attack_button_location[0] - x_offset + (x_inc * 0)
                    elif target == 2:
                        x = CombatMode._attack_button_location[0] - x_offset + (x_inc * 1)
                    else:
                        x = CombatMode._attack_button_location[0] - x_offset + (x_inc * 2)

                    if target == 1 or target == 2 or target == 3:
                        y = CombatMode._attack_button_location[1] - y_offset + (y_inc * 0)
                    else:
                        y = CombatMode._attack_button_location[1] - y_offset + (y_inc * 1)

                    if target == "target(1)":
                        MessageLog.print_message("[COMBAT] Targeting Character 1 for Skill.")
                        MouseUtils.move_and_click_point(x, y, "template_target")
                    elif "target(2)" in target:
                        MessageLog.print_message("[COMBAT] Targeting Character 2 for Skill.")
                        MouseUtils.move_and_click_point(x, y, "template_target")
                    elif "target(3)" in target:
                        MessageLog.print_message("[COMBAT] Targeting Character 3 for Skill.")
                        MouseUtils.move_and_click_point(x, y, "template_target")
                    elif "target(4)" in target:
                        MessageLog.print_message("[COMBAT] Targeting Character 4 for Skill.")
                        MouseUtils.move_and_click_point(x, y, "template_target")
                    elif "target(5)" in target:
                        MessageLog.print_message("[COMBAT] Targeting Character 5 for Skill.")
                        MouseUtils.move_and_click_point(x, y, "template_target")
                    elif "target(6)" in target:
                        MessageLog.print_message("[COMBAT] Targeting Character 6 for Skill.")
                        MouseUtils.move_and_click_point(x, y, "template_target")
                    elif "wait" in target:
                        CombatMode._wait_execute(list(target))
                    else:
                        MessageLog.print_message("[WARNING] Invalid command received for Skill targeting.")
                        Game.find_and_click_button("cancel")

                # Else, check if the character is skill-sealed.
                elif ImageUtils.confirm_location("skill_unusable", bypass_general_adjustment = True):
                    MessageLog.print_message("[COMBAT] Character is currently skill-sealed. Unable to execute command.")
                    Game.find_and_click_button("cancel")

        # Once all the commands for the selected Character have been processed, click the "Back" button to return.
        Game.find_and_click_button("back")

        return False

    @staticmethod
    def _use_summon(command: str):
        """Activate the specified Summon.

        Args:
            command (str): The command to be executed.

        Returns:
            (bool): Return True if the Turn will end due to a chained "attack" command. False otherwise.
        """
        for summon_index in range(1, 7):
            if f"summon({summon_index})" in command:
                from bot.game import Game

                # Click the "Summon" button to bring up the available Summons.
                MessageLog.print_message(f"[COMBAT] Invoking Summon #{summon_index}.")
                Game.find_and_click_button("summon")

                if Settings.use_first_notch is False:
                    x_offset = 320
                    x_inc = 75
                    y_offset = 140
                else:
                    x_offset = 215
                    x_inc = 50
                    y_offset = 90

                # Click on the specified Summon.
                tries = 3
                while ImageUtils.confirm_location("summon_details") is False:
                    if summon_index == 1:
                        MouseUtils.move_and_click_point(CombatMode._attack_button_location[0] - x_offset + (x_inc * 0), CombatMode._attack_button_location[1] + y_offset, "template_summon")
                    elif summon_index == 2:
                        MouseUtils.move_and_click_point(CombatMode._attack_button_location[0] - x_offset + (x_inc * 1), CombatMode._attack_button_location[1] + y_offset, "template_summon")
                    elif summon_index == 3:
                        MouseUtils.move_and_click_point(CombatMode._attack_button_location[0] - x_offset + (x_inc * 2), CombatMode._attack_button_location[1] + y_offset, "template_summon")
                    elif summon_index == 4:
                        MouseUtils.move_and_click_point(CombatMode._attack_button_location[0] - x_offset + (x_inc * 3), CombatMode._attack_button_location[1] + y_offset, "template_summon")
                    elif summon_index == 5:
                        MouseUtils.move_and_click_point(CombatMode._attack_button_location[0] - x_offset + (x_inc * 4), CombatMode._attack_button_location[1] + y_offset, "template_summon")
                    else:
                        MouseUtils.move_and_click_point(CombatMode._attack_button_location[0] - x_offset + (x_inc * 5), CombatMode._attack_button_location[1] + y_offset, "template_summon")

                    tries -= 1

                # Check if it is able to be summoned.
                if ImageUtils.confirm_location("summon_details", bypass_general_adjustment = True):
                    if Game.find_and_click_button("ok") is False:
                        MessageLog.print_message(f"[COMBAT] Summon #{summon_index} cannot be invoked due to current restrictions.")
                        Game.find_and_click_button("cancel")

                # Click the "Back" button to return.
                Game.find_and_click_button("back")

        if "wait" in command:
            split_command = command.split(".")
            split_command.pop(0)
            CombatMode._wait_execute(split_command)

        if "attack" in command:
            CombatMode._end()
            return True

        return False

    @staticmethod
    def _quick_summon(command: str = ""):
        """Activate a Quick Summon.

        Args:
            command (str, optional): The command to be executed. Defaults to the regular quick summon command.

        Returns:
            (bool): Return True if the Turn will end due to a chained "attack" command. False otherwise.
        """
        from bot.game import Game

        MessageLog.print_message("[COMBAT] Quick Summoning now...")
        if ImageUtils.find_button("quick_summon_not_ready", bypass_general_adjustment = True) is None and \
                (Game.find_and_click_button("quick_summon1", bypass_general_adjustment = True) or Game.find_and_click_button("quick_summon2", bypass_general_adjustment = True)):
            MessageLog.print_message("[COMBAT] Successfully quick summoned!")

            if "wait" in command:
                split_command = command.split(".")
                split_command.pop(0)
                CombatMode._wait_execute(split_command)

            if "attack" in command:
                CombatMode._end()
                return True
        else:
            MessageLog.print_message("[COMBAT] Was not able to quick summon this Turn.")

        return False

    @staticmethod
    def _enable_semi_auto():
        """Enable Semi Auto and if it fails, try to enable Full Auto.

        Returns:
            None
        """
        from bot.game import Game

        MessageLog.print_message("[COMBAT] Bot will now attempt to enable Semi Auto...")
        CombatMode._semi_auto = ImageUtils.find_button("semi_auto_enabled")
        if not CombatMode._semi_auto:
            # Have the Party attack and then attempt to see if the "Semi Auto" button becomes visible.
            Game.find_and_click_button("attack")
            CombatMode._semi_auto = Game.find_and_click_button("semi_auto")

            # If the bot still cannot find the "Semi Auto" button, that probably means the user has the "Full Auto" button on the screen instead of the "Semi Auto" button.
            if not CombatMode._semi_auto:
                MessageLog.print_message("[COMBAT] Failed to enable Semi Auto. Falling back to Full Auto...")

                # Enable Full Auto.
                CombatMode._full_auto = Game.find_and_click_button("full_auto")
            else:
                MessageLog.print_message("[COMBAT] Semi Auto is now enabled.")

        return None

    @staticmethod
    def _enable_full_auto():
        """Enable Full Auto and if it fails, try to enable Semi Auto.

        Returns:
            None
        """
        from bot.game import Game

        MessageLog.print_message("[COMBAT] Bot will now attempt to enable Full Auto...")
        CombatMode._full_auto = Game.find_and_click_button("full_auto")

        # If the bot failed to find and click the "Full Auto" button, fallback to the "Semi Auto" button.
        if not CombatMode._full_auto:
            MessageLog.print_message("[COMBAT] Bot failed to find the \"Full Auto\" button. Falling back to Semi Auto.")
            CombatMode._enable_semi_auto()
        else:
            MessageLog.print_message("[COMBAT] Full Auto is now enabled.")

        return None

    @staticmethod
    def _attack_back():
        """Attacks and then presses the Back button to quickly end animations.

        Returns:
            None
        """
        from bot.game import Game

        if Game.find_and_click_button("attack"):
            if ImageUtils.wait_vanish("combat_cancel", timeout = 10):
                MessageLog.print_message("[COMBAT] Attacked and pressing the Back button now...")
                CombatMode._back(increment_turn = False)

            # Advance the Turn number by 1.
            CombatMode._turn_number += 1
        else:
            MessageLog.print_message("[WARNING] Failed to execute the \"attackback\" command...")

        return None

    @staticmethod
    def _attack(command: str):
        """Attacks and if there is a wait command attached, execute that as well.

        Args:
            command (str): The command to be executed.

        Returns:
            None
        """
        from bot.game import Game

        if Game.find_and_click_button("attack", tries = 30):
            if ImageUtils.wait_vanish("combat_cancel", timeout = 10):
                MessageLog.print_message("[COMBAT] Successfully executed a manual attack.")
            else:
                MessageLog.print_message("[COMBAT] Successfully executed a manual attack that resolved instantly.")
        else:
            MessageLog.print_message("[WARNING] Failed to execute a manual attack.")

        if "wait" in command:
            split_command = command.split(".")
            split_command.pop(0)
            CombatMode._wait_execute(list(split_command))

        return None

    @staticmethod
    def _back(increment_turn: bool = True):
        """Presses the Back button. Increments the Turn number if specified otherwise.

        Args:
            increment_turn (bool, optional): Increments the Turn number. Defaults to True.

        Returns:
            None
        """
        from bot.game import Game

        if Game.find_and_click_button("home_back"):
            MessageLog.print_message("[COMBAT] Tapped the Back button.")
            CombatMode._wait_for_attack()

            if increment_turn:
                # Advance the Turn number by 1.
                CombatMode._turn_number += 1
        else:
            MessageLog.print_message("[WARNING] Failed to find and tap the Back button.")

        return None

    @staticmethod
    def _reload():
        """Reloads the page.

        Returns:
            None
        """
        from bot.game import Game

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

        return None

    @staticmethod
    def _end():
        """Ends the Turn.

        Returns:
            None
        """
        CombatMode._end_turn()

        CombatMode._reload_for_attack()
        CombatMode._wait_for_attack()

        MessageLog.print_message(f"[COMBAT] Turn {CombatMode._turn_number} has ended.")

        CombatMode._turn_number += 1
        return None

    ######################################################################
    ######################################################################
    # Looping Workflows for the End
    ######################################################################
    ######################################################################

    @staticmethod
    def _loop_auto():
        """Main workflow loop for both Semi Auto and Full Auto. The bot will progress the Quest/Raid until it ends or the Party wipes.

        Returns:
            None
        """
        from bot.game import Game

        while not CombatMode._retreat_check and (CombatMode._full_auto or CombatMode._semi_auto):
            # Check for exit conditions.
            CombatMode._check_for_battle_end()

            if Game.find_and_click_button("next", tries = 1, suppress_error = True):
                Game.wait(3)

            CombatMode._check_for_wipe()

            if CombatMode._check_raid():
                # Click Next if it is available and enable automation again if combat continues.
                if Game.find_and_click_button("next", tries = 1, suppress_error = True):
                    Game.wait(3.0)

                    # Check for exit conditions and restart auto.
                    if CombatMode._check_for_battle_end() == "Nothing":
                        CombatMode._enable_auto()
                elif ImageUtils.find_button("attack", tries = 1, suppress_error = True) is None and ImageUtils.find_button("next", tries = 1, suppress_error = True) is None and \
                        CombatMode._check_for_battle_end() == "Nothing":
                    Game.wait(1.0)

                    CombatMode._reload_for_attack(override = True)
                    CombatMode._wait_for_attack()

                    # Check for exit conditions and restart auto.
                    if CombatMode._check_for_battle_end() == "Nothing":
                        if Settings.debug_mode:
                            MessageLog.print_message("[DEBUG] Clicked the Next button to move to the next wave. Attempting to restart Full/Semi Auto...")

                        CombatMode._enable_auto()
            elif ImageUtils.find_button("attack", tries = 1, suppress_error = True) is None and ImageUtils.find_button("next", tries = 1, suppress_error = True) is None:
                if Settings.debug_mode:
                    MessageLog.print_message("[DEBUG] Attack and Next buttons have vanished. Determining if bot should reload...")

                if CombatMode._reload_for_attack():
                    # Enable Full/Semi Auto again if the bot reloaded.
                    if CombatMode._full_auto:
                        CombatMode._enable_full_auto()
                    elif CombatMode._semi_auto:
                        CombatMode._enable_semi_auto()

        return None

    @staticmethod
    def _loop_manual():
        """Main workflow loop for manually pressing the Attack button and reloading until combat ends.

        Returns:
            None
        """
        from bot.game import Game

        while not CombatMode._retreat_check:
            # Check for exit conditions.
            CombatMode._check_for_battle_end()

            if Game.find_and_click_button("next", tries = 1, suppress_error = True):
                Game.wait(3)

                # Check for exit conditions.
                CombatMode._check_for_battle_end()

            Game.find_and_click_button("attack", tries = 10)
            CombatMode._reload_for_attack()
            CombatMode._wait_for_attack()

        return None

    ######################################################################
    ######################################################################
    # Entry Point
    ######################################################################
    ######################################################################

    @staticmethod
    def start_combat_mode(script_commands: List[str] = None, is_nightmare: bool = False, is_defender: bool = False):
        """Start Combat Mode with the given script file path. Start reading through the text file line by line and have the bot proceed with the commands accordingly.

        Args:
            script_commands (List[str]): List of script commands to use instead of reading from a text file. Defaults to None.
            is_nightmare (bool, optional): If Combat Mode is being used for a Nightmare, determines the method of reading the script file.
            is_defender (bool, optional): If Combat Mode is being used for a Defender, determines the method of reading the script file.

        Returns:
            (bool): Return True if Combat Mode was successful. Else, return False if the Party wiped or backed out without retreating.
        """
        from bot.game import Game

        CombatMode._start_time = time.time()

        # Reset flags and Attack button location.
        CombatMode._retreat_check = False
        CombatMode._semi_auto = False
        CombatMode._full_auto = False
        manual_attack_and_reload = False
        skip_end = False
        CombatMode._attack_button_location = None
        CombatMode._command_turn_number = 1
        CombatMode._turn_number = 1  # Current turn for the script execution.

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
            elif is_defender:
                MessageLog.print_message(f"Name of Defender combat script loaded: {Settings.defender_combat_script_name}")
                command_list = copy.deepcopy(Settings.defender_combat_script)
            else:
                MessageLog.print_message(f"Name of combat script loaded: {Settings.combat_script_name}")
                command_list = copy.deepcopy(Settings.combat_script)

        MessageLog.print_message(f"[COMBAT] Size of script commands: {len(command_list)}")

        # If current Farming Mode is Arcarum, attempt to dismiss potential stage effect popup like "Can't use Charge Attacks".
        if Settings.farming_mode == "Arcarum":
            Game.find_and_click_button("arcarum_stage_effect_active", tries = 10, bypass_general_adjustment = True)

        # Save the position of the Attack button.
        CombatMode._attack_button_location = ImageUtils.find_button("attack", tries = 50, bypass_general_adjustment = True)

        if CombatMode._attack_button_location is None:
            MessageLog.print_message(f"\n[ERROR] Cannot find Attack button. Raid must have just ended.")
            return False

        ######################################################################
        ######################################################################
        # This is where the main workflow of Combat Mode is located.
        try:
            while len(command_list) > 0 and CombatMode._retreat_check is False:
                # All the logic that follows assumes that the command string is lowercase to allow case-insensitive commands.
                command = command_list.pop(0).strip().lower()
                if command == "" or command[0] == "#" or command[0] == "/":
                    continue
                elif command.__contains__("/") or command.__contains__("#"):
                    # Remove comments in the same line.
                    command = command[0:command.find("#")][0:command.find("/")].strip()

                MessageLog.print_message(f"\n[COMBAT] Reading command: \"{command}\"")

                if command.__contains__("turn"):
                    CombatMode._start_turn(command)
                elif CombatMode._turn_number == CombatMode._command_turn_number:
                    # Process all commands here that belong inside a Turn block.

                    # Check for exit conditions.
                    CombatMode._check_for_battle_end()

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
                        if CombatMode._use_character_skill(character_selected, skill_command_list):
                            skip_end = True

                    # Handle any other supported command.
                    elif command == "requestbackup":
                        CombatMode._request_backup()
                    elif command == "tweetbackup":
                        CombatMode._tweet_backup()
                    elif CombatMode._healing_item_commands.__contains__(command):
                        CombatMode._use_combat_healing_item(command)
                    elif command.__contains__("summon") and command.__contains__("quicksummon") is False:
                        if CombatMode._use_summon(command):
                            skip_end = True
                    elif command.__contains__("quicksummon"):
                        if CombatMode._quick_summon(command):
                            skip_end = True
                    elif command == "enablesemiauto":
                        CombatMode._enable_semi_auto()
                    elif command == "enablefullauto":
                        CombatMode._enable_full_auto()
                    elif "targetenemy" in command:
                        # Select enemy target.
                        CombatMode._select_enemy_target(command)
                    elif "attackback" in command:
                        CombatMode._attack_back()
                    elif "attack" in command:
                        CombatMode._attack(command)
                    elif "back" in command:
                        CombatMode._back()
                    elif "reload" in command:
                        CombatMode._reload()
                    elif command == "repeatmanualattackandreload":
                        MessageLog.print_message("[COMBAT] Enabling manually pressing the Attack button and reloading (if the mission supports it) until battle ends.")
                        manual_attack_and_reload = True
                    elif CombatMode._semi_auto is False and CombatMode._full_auto is False and command == "end" and skip_end is False:
                        CombatMode._end()
                    elif command.find("wait") == 0:
                        CombatMode._wait_execute(list(command))
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

                ######################################################################
                ######################################################################
                # Handle certain commands that could be present outside a Turn block.
                if CombatMode._semi_auto is False and CombatMode._full_auto is False and command == "enablesemiauto":
                    CombatMode._enable_semi_auto()
                elif CombatMode._semi_auto is False and CombatMode._full_auto is False and command == "enablefullauto":
                    CombatMode._enable_full_auto()
                elif command == "repeatmanualattackandreload":
                    MessageLog.print_message("[COMBAT] Enabling manually pressing the Attack button and reloading (if the mission supports it) until battle ends.")
                    manual_attack_and_reload = True
                elif command.find("wait") == 0:
                    CombatMode._wait_execute(list(command))

            # Deal with the situation where high-profile raids end right when the bot loads in and all it sees is the "Next" button.
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
                if CombatMode._full_auto is False and CombatMode._semi_auto is False:
                    CombatMode._enable_full_auto()

                # Counteract slower instances when the battle finished right when the bot finished executing the script.
                if Game.find_and_click_button("next", tries = 1, suppress_error = True):
                    Game.wait(3)
                    CombatMode._check_for_battle_end()

                # Main workflow loop for both Semi Auto and Full Auto. The bot will progress the Quest/Raid until it ends or the Party wipes.
                CombatMode._loop_auto()
            else:
                # Main workflow loop for manually pressing the Attack button and reloading until combat ends.
                CombatMode._loop_manual()
        except CombatModeException as e:
            if CombatMode._list_of_exit_events_for_false.__contains__(e.__str__()):
                return False
            elif CombatMode._list_of_exit_events_for_true.__contains__(e.__str__()):
                # Calculate elapsed time for the API.
                if Settings.enable_opt_in_api:
                    Settings.combat_elapsed_time = time.time() - CombatMode._start_time

                return True

        ######################################################################
        ######################################################################

        MessageLog.print_message("\n######################################################################")
        MessageLog.print_message("######################################################################")
        MessageLog.print_message("[COMBAT] Ending Combat Mode.")
        MessageLog.print_message("######################################################################")
        MessageLog.print_message("######################################################################")

        # Calculate elapsed time for the API.
        if Settings.enable_opt_in_api:
            Settings.combat_elapsed_time = time.time() - CombatMode._start_time

        if not CombatMode._retreat_check:
            return True
        else:
            return False
