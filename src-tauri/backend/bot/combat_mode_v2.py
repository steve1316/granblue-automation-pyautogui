import copy
import os
from typing import List
import time
from time import sleep
from numpy import random


# from bot.game import Game
from utils.settings import Settings
from utils.message_log import MessageLog as Log
from utils.image_utils_v2 import ImageUtils
from utils.mouse_utils import MouseUtils
from bot.window import Window

class CombatMode:
    """ This is a class that manager everything inside a battle
    """

    actions = []
    _attack_button_location = None


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
    def _select_char(idx: int):
        """Click on the character on combact screen.
        """
        x,y = ImageUtils.find_button("attack", tries = 50, bypass_general_adjustment = True)

        if Settings.use_first_notch is False:
            # calibrated
            x_offset = 280
            x_inc = 80
        else:
            x_offset = 215
            x_inc = 55
        
        x = x - x_offset + (x_inc * idx-2)
        # calibrated
        y = y + 92
        # Double-clicking the character portrait to avoid any non-invasive popups from other Raid participants.
        # Double-click can select skill by accident
        MouseUtils.move_and_click_point(x, y, "template_character")


    @staticmethod
    def _use_skill(idx: int):
        """This function should only be called by select character"""
        from bot.game import Game

        x,y = ImageUtils.find_button("attack", tries = 50, bypass_general_adjustment = True)

        if Settings.use_first_notch is False:
            # calibrated
            x_offset = -243
            x_inc = 84
            y_offset = 178
        else:
            x_offset = 145
            x_inc = 55
            y_offset = 115

        x = x + x_offset + (x_inc * idx-1)
        y = y + y_offset

        MouseUtils.move_and_click_point(x, y, "template_skill")
        Log.print_message(f"[COMBAT] Use Skill {idx}.")



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

        # If the bot failed to find and click the "Full Auto" button, fallback to the "Semi Auto" button.
        if not Game.find_and_click_button("full_auto"):
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

        else:
            Log.print_message("[WARNING] Failed to execute the \"attackback\" command...")

        return None

    @staticmethod
    def _sub_back():
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
    def _sub_reload():
        Window.reload(is_sub=True)

    @staticmethod
    def _reload():
        from bot.game import Game
        Log.print_message("[COMBAT] Bot will now attempt to manually reload...")

        if (random.rand() > 0.1):
            Window.reload()
        else:
            Game.find_and_click_button("reload")
        
        Game.wait(3.0)



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

        return None
    
    @staticmethod
    def load_actions(actions):
        """ Check the string list and load the actions chain into the combat mode

        actions: list of tuple of function name and parameter
        """
        fun = {
            "quicksummon": CombatMode._quick_summon,
            "enablefullauto": CombatMode._enable_full_auto,
            "enablesemiauto": CombatMode._enable_semi_auto,
            "back": CombatMode._back,
            "selectchar": CombatMode._select_char,
            "useskill": CombatMode._use_skill,
            "subback": CombatMode._sub_back,
            "reload": CombatMode._reload,
            "attack": CombatMode._attack,
            "_sub_reload": CombatMode._sub_reload,
            "_wait_for_end": CombatMode._wait_for_end
        }
        CombatMode.actions = []
        for action in actions:
            CombatMode.actions.append(
                (fun[action[0]] , action[1])
            )
        Log.print_message(
            f"[COMBAT] Action Load: Size {len(CombatMode.actions)}")


    @staticmethod
    def _is_battle_end() -> bool:
        """checks to see if the battle ended or not.

        Returns:
            (str): Return "Nothing" if combat is still continuing. Otherwise, raise a CombatModeException whose message is the event name that caused the battle to end.
        """
        from bot.game import Game

        # Check if the Battle has ended.
        if ImageUtils.confirm_location("battle_concluded", tries = 1, suppress_error = True, bypass_general_adjustment = True):
            Log.print_message("\n[COMBAT] Battle concluded suddenly.")
            Log.print_message("\n######################################################################")
            Log.print_message("######################################################################")
            Log.print_message("[COMBAT] Ending Combat Mode.")
            Log.print_message("######################################################################")
            Log.print_message("######################################################################")
            return True

        if ImageUtils.confirm_location("exp_gained", tries = 1, suppress_error = True, bypass_general_adjustment = True):
            Log.print_message("\n######################################################################")
            Log.print_message("######################################################################")
            Log.print_message("[COMBAT] Ending Combat Mode.")
            Log.print_message("######################################################################")
            Log.print_message("######################################################################")
            return True

        if ImageUtils.confirm_location("loot_collected", tries = 1, suppress_error = True, bypass_general_adjustment = True):
            Log.print_message("\n######################################################################")
            Log.print_message("######################################################################")
            Log.print_message("[COMBAT] Ending Combat Mode.")
            Log.print_message("######################################################################")
            Log.print_message("######################################################################")
            return True

        return False
        
    @staticmethod
    def _wait_for_end():
        from bot.game import Game
        Game._move_mouse_security_check()
        while not CombatMode._is_battle_end():
            time.sleep(5)
        
    @staticmethod
    def start_combat_mode():

        # CombatMode._start_time = time.time()
        # CombatMode._turn_number = 1  # Current turn for the script execution.

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
            action[0](**action[1])

        Log.print_message("\n######################################################################")
        Log.print_message("######################################################################")
        Log.print_message("[COMBAT] Ending Combat Mode.")
        Log.print_message("######################################################################")
        Log.print_message("######################################################################")

        # Calculate elapsed time for the API.
        if Settings.enable_opt_in_api:
            Settings.combat_elapsed_time = time.time() - CombatMode._start_time

        return True