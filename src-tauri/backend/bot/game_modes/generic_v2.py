from utils.message_log import MessageLog as Log
from utils.settings import Settings
from utils.image_utils_v2 import ImageUtils
from bot.window import Window
from bot.combat_mode_v2 import CombatMode as Combat
from utils.parser import Parser
import numpy as np
from time import sleep

class GenericV2:
    """
    Provides more lightweight utility functions with less limitation for more simple mission.
    """

    @staticmethod
    def start():

        from bot.game import Game
        ImageUtils._summon_selection_first_run = False

        Log.print_message(f"[GenericV2] Parsing combat script: {Settings.combat_script_name}")
        battles_seq = Parser.parse_battles(Settings.combat_script)

        for battle in battles_seq:

            config, actions = battle
            url, summon, repeat = config
        
            Log.print_message(f"[GenericV2] Start battle:{url}, total of {repeat} times")

            if actions[-1][0] == "subback":
                # first time
                Log.print_message(f"[GenericV2] First run with support window")
                if Window.sub_start == None:
                    raise RuntimeError("There are no support Window.")

                Window.goto(url)
                Window.sub_prepare_loot()
                # reload instead of back for first time
                Combat.load_actions(actions[:-1] + [("_sub_reload",{})])
                # start first time
                GenericV2.single_battle_sub_back(summon)         
                # load the original script
                Combat.load_actions(actions)

                for i in range (1, repeat):
                    Log.print_message(f"[GenericV2] Repeat for {i} times")
                    GenericV2.single_battle_sub_back(summon)         
                    Game._delay_between_runs()
                    if (np.random.rand() > .9):
                        Game._move_mouse_security_check()
    
            else:
                if ("enablefullauto",{}) in actions:
                    actions.append(('_wait_for_end' ,{}))
                Combat.load_actions(actions)
                
                for i in range (0, repeat):

                    Log.print_message(f"[GenericV2] Repeat for {i+1} times")
                    Window.goto(url)
                    
                    GenericV2.single_raid(summon)
                    Game._delay_between_runs()

                    if (np.random.rand() > .9):
                        Game._move_mouse_security_check()


        Log.print_message(f"GenericV2 successfully finish!")

    
    @staticmethod
    def single_battle_sub_back(support_summon: str):
        from bot.game import Game
        """ Method to do single raid only with getting loot in the sub window

        support_summon: string of the support summon
        """
        # Check if the bot is at the Summon Selection screen.
        if ImageUtils.confirm_location("select_a_summon", tries = 30):
            if Game.select_summon([support_summon], Settings.summon_element_list):
                if Game.find_and_click_button("ok", tries = 30):
                    # Now start Combat Mode and detect any item drops.
                    if Combat.start_combat_mode():
                        if ImageUtils.find_button("ok", tries = 30, is_sub=True):
                            Game.find_and_click_button("home_back")
                else:
                    raise RuntimeError("Failed to skip party selection.")
        else:
            raise RuntimeError("Failed to arrive at the Summon Selection screen.")



    @staticmethod
    def single_raid(support_summon: str):
        from bot.game import Game
        """ Standart method to do a battle
        """
        if ImageUtils.confirm_location("select_a_summon", tries = 30):
            if Game.select_summon([support_summon], Settings.summon_element_list):
                if Game.find_and_click_button("ok", tries = 30):
                    Combat.start_combat_mode()
                else:
                    raise RuntimeError("Failed to find ok button.")
        else:
            raise RuntimeError("Failed to arrive at the Summon Selection screen.")