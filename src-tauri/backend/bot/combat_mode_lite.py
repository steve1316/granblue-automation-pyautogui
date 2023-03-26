import copy
import os
from typing import List
import time

# from bot.game import Game
from utils.settings import Settings
from utils.message_log import MessageLog as Log
from utils.image_utils import ImageUtils
from utils.mouse_utils import MouseUtils
from utils.parser import Parser


class CombatMode:
    """
    Provides a liter version of utility functions for Combat Mode
    Which execute faster but with less features. It is essentially a state
    manager while the game enter a raid/battle
    """

    actions = []

    @property
    def command_dict(self) :
        return {
            "quicksummon": CombatMode._quick_summon,
            "enablefullauto": CombatMode._enable_full_auto,
            "enablesemiauto": CombatMode._enable_semi_auto,
            "back": CombatMode._back,
            "subback": CombatMode._sub_back,
            "reload": CombatMode._reload,
            "attack": CombatMode._attack
        }



    @staticmethod
    def _check_for_battle_end() -> str:
        """Perform checks to see if the battle ended or not.

        Returns:
            (str): Return "Nothing" if combat is still continuing. Otherwise, raise a CombatModeException whose message is the event name that caused the battle to end.
        """
        from bot.game import Game

    @staticmethod
    def _reload():
        """Determine whether or not to reload after an Attack.

        Args:
            override (bool): Override the set checks and reload anyways. Defaults to false.

        Returns:
            (bool): True if the bot reloaded the page. False otherwise.
        """

    @staticmethod
    def _wait_for_attack() -> bool:
        """Wait for several tries until the bot sees either the Attack or the Next button before starting a new turn.

        Returns:
            (bool): True if Attack ended into the next Turn. False if Attack ended but combat also ended as well.
        """
        Log.print_message("[COMBAT] Now waiting for attack to end...")
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

        Log.print_message("[COMBAT] Attack ended.")

        return True

    @staticmethod
    def _enable_auto() -> bool:
        """Enable Full/Semi auto for this battle.

        Returns:
            (bool): True if Full/Semi auto is enabled.
        """
        from bot.game import Game

        if Settings.enable_refresh_during_combat and Settings.enable_auto_quick_summon:
            Log.print_message(f"[COMBAT] Automatically attempting to use Quick Summon...")
            CombatMode._quick_summon()

        enable_auto = Game.find_and_click_button("full_auto") or ImageUtils.find_button("full_auto_enabled")

        # If the bot failed to find and click the "Full Auto" button, fallback to the "Semi Auto" button.
        if enable_auto is False:
            Log.print_message(f"[COMBAT] Failed to find the \"Full Auto\" button. Falling back to Semi Auto.")
            Log.print_message(f"[COMBAT] Double checking to see if Semi Auto is enabled.")

            enabled_semi_auto_button_location = ImageUtils.find_button("semi_button_enabled")
            if enabled_semi_auto_button_location is None:
                # Have the Party attack and then attempt to see if the "Semi Auto" button becomes visible.
                Game.find_and_click_button("attack")

                Game.wait(2.0)

                enable_auto = Game.find_and_click_button("semi_auto", tries = 10)
                if enable_auto:
                    Log.print_message("[COMBAT] Semi Auto is now enabled.")
        else:
            Log.print_message(f"[COMBAT] Enabled Full Auto.")

        return enable_auto



    @staticmethod
    def _quick_summon(command: str = ""):
        """Activate a Quick Summon.

        Args:
            command (str, optional): The command to be executed. Defaults to the regular quick summon command.

        Returns:
            (bool): Return True if the Turn will end due to a chained "attack" command. False otherwise.
        """
        from bot.game import Game

        Log.print_message("[COMBAT] Quick Summoning now...")
        if ImageUtils.find_button("quick_summon_not_ready", bypass_general_adjustment = True) is None and \
                (Game.find_and_click_button("quick_summon1", bypass_general_adjustment = True) or Game.find_and_click_button("quick_summon2", bypass_general_adjustment = True)):
            Log.print_message("[COMBAT] Successfully quick summoned!")

            if "wait" in command:
                split_command = command.split(".")
                split_command.pop(0)
                CombatMode._wait_execute(split_command)

            if "attack" in command:
                CombatMode._end()
                return True
        else:
            Log.print_message("[COMBAT] Was not able to quick summon this Turn.")

        return False

    @staticmethod
    def _enable_semi_auto():
        """Enable Semi Auto and if it fails, try to enable Full Auto.

        Returns:
            None
        """
        from bot.game import Game

        Log.print_message("[COMBAT] Bot will now attempt to enable Semi Auto...")
        CombatMode._semi_auto = ImageUtils.find_button("semi_auto_enabled")
        if not CombatMode._semi_auto:
            # Have the Party attack and then attempt to see if the "Semi Auto" button becomes visible.
            Game.find_and_click_button("attack")
            CombatMode._semi_auto = Game.find_and_click_button("semi_auto")

            # If the bot still cannot find the "Semi Auto" button, that probably means the user has the "Full Auto" button on the screen instead of the "Semi Auto" button.
            if not CombatMode._semi_auto:
                Log.print_message("[COMBAT] Failed to enable Semi Auto. Falling back to Full Auto...")

                # Enable Full Auto.
                CombatMode._full_auto = Game.find_and_click_button("full_auto")
            else:
                Log.print_message("[COMBAT] Semi Auto is now enabled.")

        return None

    @staticmethod
    def _enable_full_auto():
        """Enable Full Auto and if it fails, try to enable Semi Auto.

        Returns:
            None
        """
        from bot.game import Game

        Log.print_message("[COMBAT] Bot will now attempt to enable Full Auto...")
        CombatMode._full_auto = Game.find_and_click_button("full_auto")

        # If the bot failed to find and click the "Full Auto" button, fallback to the "Semi Auto" button.
        if not CombatMode._full_auto:
            Log.print_message("[COMBAT] Bot failed to find the \"Full Auto\" button. Falling back to Semi Auto.")
            CombatMode._enable_semi_auto()
        else:
            Log.print_message("[COMBAT] Full Auto is now enabled.")

        return None

    @staticmethod
    def _back():
        """Attacks and then presses the Back button to quickly end animations.

        Returns:
            None
        """
        from bot.game import Game

        if Game.find_and_click_button("attack"):
            if ImageUtils.wait_vanish("combat_cancel", timeout = 10):
                Log.print_message("[COMBAT] Attacked and pressing the Back button now...")
                CombatMode._back(increment_turn = False)

            # Advance the Turn number by 1.
            CombatMode._turn_number += 1
        else:
            Log.print_message("[WARNING] Failed to execute the \"attackback\" command...")

        return None

    @staticmethod
    def sub_back():
        """Presses the Back button.
        """
        from bot.game import Game

        x, y = ImageUtils.find_button("home_back", tries = 30, is_sub=True)    
        MouseUtils.move_and_click_point(
            x, y, "home_back"
        )
    
        Log.print_message("[COMBAT] Tapped the Back button of sub Window.")

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
                Log.print_message("[COMBAT] Successfully executed a manual attack.")
            else:
                Log.print_message("[COMBAT] Successfully executed a manual attack that resolved instantly.")
        else:
            Log.print_message("[WARNING] Failed to execute a manual attack.")

        if "wait" in command:
            split_command = command.split(".")
            split_command.pop(0)
            CombatMode._wait_execute(list(split_command))

        return None
    
    @staticmethod
    def load_actions(str_actions: List[str]):
        """ Check the string list and load the actions chain into the combat mode

        Args:
            list of string from user script
        """
        CombatMode.actions = [CombatMode.command_dict[action] for action in str_actions]
        Log.print_message(f"[COMBAT] Size of script commands: {len(CombatMode.actions)}")

    @staticmethod
    def start_combat_mode(str_actions: List[str]):

        CombatMode._start_time = time.time()
        CombatMode._turn_number = 1  # Current turn for the script execution.

        Log.print_message("\n######################################################################")
        Log.print_message("######################################################################")
        Log.print_message(f"[COMBAT] Starting Combat Mode.")
        Log.print_message("######################################################################")
        Log.print_message("######################################################################\n")


        # Save the position of the Attack button.
        CombatMode._attack_button_location = ImageUtils.find_button("attack", tries = 50, bypass_general_adjustment = True)

        if CombatMode._attack_button_location is None:
            Log.print_message(f"\n[ERROR] Cannot find Attack button. Raid must have just ended.")
            return False

        # excute chain actions
        for action in CombatMode.actions:
            action()

        Log.print_message("\n######################################################################")
        Log.print_message("######################################################################")
        Log.print_message("[COMBAT] Ending Combat Mode.")
        Log.print_message("######################################################################")
        Log.print_message("######################################################################")

        # Calculate elapsed time for the API.
        if Settings.enable_opt_in_api:
            Settings.combat_elapsed_time = time.time() - CombatMode._start_time

        if not CombatMode._retreat_check:
            return True
        else:
            return False
