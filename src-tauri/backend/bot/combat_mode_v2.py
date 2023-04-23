from typing import List, Optional
from time import sleep
from numpy import random
import pyautogui as pya

# from bot.game import Game
from utils.settings import Settings
from utils.message_log import MessageLog as Log
from utils.image_utils import ImageUtils
from utils.mouse_utils import MouseUtils
from bot.combat_mode import CombatMode
from bot.window import Window

class CombatModeV2:
    """ This is a class that manager everything inside a battle
    """

    actions = []

    @staticmethod
    def _enable_auto() -> bool:
        """Enable Full/Semi auto for this battle.

        Returns:
            (bool): True if Full/Semi auto is enabled.
        """
        from bot.game import Game

        if Settings.enable_refresh_during_combat and Settings.enable_auto_quick_summon:
            Log.print_message(f"[COMBAT] Automatically attempting to use Quick Summon...")
            CombatModeV2._quick_summon()

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
        """Click on the character on combact screen. Idx start at 0
        """
        x,y = ImageUtils.find_button("attack", tries = 50, bypass_general_adjustment = True)

        if Settings.use_first_notch is False:
            x_offset = 280
            x_inc = 80
        else:
            x_offset = 215
            x_inc = 55
        
        x = x - x_offset + (x_inc * idx-2)
        y = y + 92
        MouseUtils.move_and_click_point(x, y, "template_character")

    @staticmethod
    def _change_select_char(idx: int):
        """Given that a character is select, change to select another char
        """
        from bot.game import Game
        Game.find_and_click_button("back")
        CombatModeV2._select_char(idx)

    @staticmethod
    def _deselect_char():
        """Click on the back button
        """
        from bot.game import Game
        Game.find_and_click_button("back")

    @staticmethod
    def _use_skill(idx: int):

        if Settings.use_first_notch is False:
            # calibrated
            x_offset = 138
            x_inc = 84
            y_offset = 546
        else:
            x_offset = 145
            x_inc = 55
            y_offset = 115

        x = Window.start + x_offset + (x_inc * idx)
        y = Window.top + y_offset

        MouseUtils.move_and_click_point(x, y, "template_skill", custom_wait=random.uniform(0.03, 0.1))
        Log.print_message(f"[COMBAT] Use Skill {idx}.")
    
    @staticmethod
    def _skill_target(idx: int):

        x_offset = 115
        x_inc = 93
        y_offset = 251
        y_inc = 164

        x = Window.start + x_offset + (x_inc * (idx%3))
        y = Window.top + y_offset + (y_inc * (idx//3))

        Log.print_message(f"[COMBAT] Targeting Character {idx+1} for Skill.")
        MouseUtils.move_and_click_point(x, y, "template_target", custom_wait=random.uniform(0.03, 0.1))

    @staticmethod
    def _quick_summon() -> bool:
        """Activate a Quick Summon.
        Returns:
            (bool): if success
        """
        Log.print_message("[COMBAT] Quick Summoning now...")
        pt = ImageUtils.find_button("quick_summon2")
        if pt is not None:
            x,y=pt
            MouseUtils.move_and_click_point(x,y, "quick_summon1", custom_wait=random.uniform(0.03, 0.1))
            return True
        
        pt = ImageUtils.find_button("quick_summon1")
        if pt is not None:
            x,y=pt
            MouseUtils.move_and_click_point(x,y, "quick_summon2", custom_wait=random.uniform(0.03, 0.1))
            return True

        Log.print_message("[COMBAT] Was not able to quick summon this Turn.")
        return False
    
    @staticmethod
    def _enable_semi_auto():
        """Enable Semi Auto and if it fails, try to enable Full Auto.
        """
        from bot.game import Game
        Log.print_message("[COMBAT] Bot will now attempt to enable Semi Auto...")
        pt = ImageUtils.find_button("semi_auto_enabled")
        if pt is None:
             # check if the user has the "Full Auto" button
            if Game.find_and_click_button("full_auto", tries=1):
                return
            # Have the Party attack and then attempt to see if the "Semi Auto" button becomes visible.
            Game.find_and_click_button("attack")

            if Game.find_and_click_button("semi_auto"):
                Log.print_message("[COMBAT] Failed to enable Semi Auto.")
            else:
                Log.print_message("[COMBAT] Semi Auto is now enabled.")

    @staticmethod
    def _use_summon(idx: int) -> bool:
 
        from bot.game import Game

        if not Game.find_and_click_button("summon", clicks=2):
            return False

        x_offset = 15
        x_inc = 77
        y_offset = 468
        x = Window.start + x_offset + (x_inc * idx)
        y = Window.top + y_offset
        #animation
        sleep(0.3)
        Log.print_message(f"[COMBAT] Using Summon #{idx+1}.")
        # check if accidentally click on a summon
        if ImageUtils.confirm_location("summon_details",tries=1):
            Game.find_and_click_button("cancel")

        MouseUtils.move_and_click_point(x,y, "template_summon")
        # Check if it is able to be summoned.
        if not Game.find_and_click_button("ok"):
            Log.print_message(f"[COMBAT] Summon #{idx+1} cannot be used.")
            Game.find_and_click_button("cancel")
            return False
        return True

    @staticmethod
    def _enable_full_auto():
        """Enable Full Auto and if it fails, try to enable Semi Auto.

        """
        from bot.game import Game

        Log.print_message("[COMBAT] Bot will now attempt to enable Full Auto...")

        # If the bot failed to find and click the "Full Auto" button, fallback to the "Semi Auto" button.
        if not Game.find_and_click_button("full_auto"):
            Log.print_message("[COMBAT] Bot failed to find the \"Full Auto\" button. Falling back to Semi Auto.")
            CombatModeV2._enable_semi_auto()
        else:
            Log.print_message("[COMBAT] Full Auto is now enabled.")

    @staticmethod
    def _back():
        """Attacks and then presses the Back button to quickly end animations.
        """
        CombatMode._back(False)

    @staticmethod
    def _sub_back():
        """Presses the Back button.
        """
        x, y = ImageUtils.find_button("home_back", tries = 30, is_sub=True)    
        MouseUtils.move_and_click_point(
            x, y, "home_back"
        )
    
        Log.print_message("[COMBAT] Tapped the Back button of sub Window.")
    
    @staticmethod
    def _sub_reload():
        Window.reload(is_sub=True, is_focus=False)

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
    def _attack():
        """Attacks and if there is a wait command attached, execute that as well.
        """
        from bot.game import Game

        if Game.find_and_click_button("attack", tries = 30):
            if ImageUtils.wait_vanish("combat_cancel", timeout = 10):
                Log.print_message("[COMBAT] Successfully executed a manual attack.")
            else:
                Log.print_message("[COMBAT] Successfully executed a manual attack that resolved instantly.")
        else:
            Log.print_message("[WARNING] Failed to execute a manual attack.")
    
    @staticmethod
    def _wait(time: int):
        from bot.game import Game
        Game._move_mouse_security_check()
        Log.print_message(f"[COMBAT] Sleeping for {time} seconds")
        sleep(time)
    
    @staticmethod
    def load_actions(actions):
        """ Check the string list and load the actions chain into the combat mode

        actions: list of tuple of function name and parameter
        """
        fun = {
            "quicksummon": CombatModeV2._quick_summon,
            "usesummon": CombatModeV2._use_summon,
            "enablefullauto": CombatModeV2._enable_full_auto,
            "enablesemiauto": CombatModeV2._enable_semi_auto,
            "back": CombatModeV2._back,
            "selectchar": CombatModeV2._select_char,
            "changechar": CombatModeV2._change_select_char,
            "useskill": CombatModeV2._use_skill,
            "target": CombatModeV2._skill_target,
            "subback": CombatModeV2._sub_back,
            "deselectchar": CombatModeV2._deselect_char,
            "reload": CombatModeV2._reload,
            "attack": CombatModeV2._attack,
            "wait": CombatModeV2._wait,
            "_sub_reload": CombatModeV2._sub_reload,
            "_wait_for_end": CombatModeV2._wait_for_end,
            "requestbackup": CombatMode._request_backup,
            "tweetbackup": CombatMode._tweet_backup,
        }
        CombatModeV2.actions = []
        for action in actions:
            CombatModeV2.actions.append(
                (fun[action[0]] , action[1])
            )
        Log.print_message(
            f"[COMBAT] Action Loaded: Size {len(CombatModeV2.actions)}")

    @staticmethod
    def _is_battle_end() -> bool:
        """checks to see if the battle ended or not.

        Returns:
            (str): Return "Nothing" if combat is still continuing. Otherwise, raise a CombatModeV2Exception whose message is the event name that caused the battle to end.
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
        while not CombatModeV2._is_battle_end():
            sleep(5)
        
    @staticmethod
    def start_combat_mode() -> bool:
        """Start Combat Mode.

        Returns:
           if Combat Mode successful start
        """
        Log.print_message("\n######################################################################")
        Log.print_message("######################################################################")
        Log.print_message(f"[COMBAT] Starting Combat Mode.")
        Log.print_message("######################################################################")
        Log.print_message("######################################################################\n")

        first_action = CombatModeV2.actions[0]
       
        if first_action[0] == CombatModeV2._enable_semi_auto:
            attempt_to_click = 1
        elif first_action[0] == CombatModeV2._enable_full_auto:
            attempt_to_click = 2
        else:
            attempt_to_click = 0 # enum, 0 for nothin, 1 for semi, 2 for full
        
        if ImageUtils.confirm_location("auto_ready", tries=15):
            Log.print_message(f"[Combat] Entering Ready Page")

            if attempt_to_click != 0:
                sleep(random.uniform(0.02, 0.12))
                pya.mouseDown()
                sleep(random.uniform(0.02, 0.12))
                pya.mouseUp()

                if ImageUtils.confirm_location("auto_enabled", tries=5):
                    Log.print_message(f"[Combat] Auto enabled")
                    attempt_to_click = 3
        
        if ImageUtils.find_button("heal", tries=50):
            Log.print_message(f"[Combat] Entering combact page")
        else:
            return False
        
        if attempt_to_click == 1:
            if ImageUtils.find_button("semi_auto_enabled", tries=20):
                Log.print_message(f"[Combat] Semi Auto successfully start")
                ImageUtils.find_button("heal_disabled", tries=50)
                Log.print_message(f"[Combat] attacked in Semi Auto ")
                sleep(random.uniform(0.1,1))
            else:
                CombatModeV2._attack()
        elif attempt_to_click == 2:
            if ImageUtils.find_button("full_auto_enabled", tries=20):
                Log.print_message(f"[Combat] Full Auto successfully start")
            else:
                attempt_to_click = 0
        # reuse the variable to decide if first enable auto should be skip
        attempt_to_click = min(attempt_to_click, 1)
        # excute chain actions
        for action in CombatModeV2.actions[attempt_to_click:]:
            action[0](**action[1])

        Log.print_message("\n######################################################################")
        Log.print_message("######################################################################")
        Log.print_message("[COMBAT] Ending Combat Mode.")
        Log.print_message("######################################################################")
        Log.print_message("######################################################################")

        return True