from utils.message_log import MessageLog as Log
from utils.settings import Settings
from utils.image_utils import ImageUtils
from bot.window import Window
from bot.combat_mode_lite import CombatMode as Combat
from utils.parser import Parser

class GenericLiteUrl:
    """
    Provides more lightweight utility functions with less limitation for more simple mission.
    """

    @staticmethod
    def start(repeat):
        from bot.game import Game

        Log.print_message(f"Name of combat script loaded: {Settings.combat_script_name}")

        raid_seq = Parser.parse_raid_sequence(Settings.combat_script)
        # repeat 1 task
        if len(raid_seq) == 1:
            # first time
            url, summon, actions = raid_seq[0]
            if actions[-1] == "subback":

                Window.goto(url)
                Window.sub_goto(url)
                # remove the 
                Combat.load_actions(actions[:-1])

                if ImageUtils.confirm_location("select_a_summon", tries = 30):
                    if Game.select_summon(Settings.summon_list, summon):
                        if Game.find_and_click_button("ok", tries = 30):
                            if Combat.start_combat_mode():
                                Window.sub_refresh()
                                ImageUtils.find_button("ok", tries = 30, is_sub=True)
                                Game.find_and_click_button("home_back")
                            raise RuntimeError("Failed to skip party selection.")
                else:
                    raise RuntimeError("Failed to arrive at the Summon Selection screen.")

                Combat.load_actions(actions)
                for i in range (1, repeat):
                    GenericLiteUrl.single_raid_with_sub_window(summon)         
                    Game._delay_between_runs()
                    Game._move_mouse_security_check()

        return None
    
    @staticmethod
    def single_raid_with_sub_window(friend_summon: str) -> None:
        """ Method to do single raid only with getting loot in
        the sub window

        friend_summon: string of the support summon
        """
        # Check if the bot is at the Summon Selection screen.
        if ImageUtils.confirm_location("select_a_summon", tries = 30):

            if Game.select_summon(Settings.summon_list, friend_summon):

                if Game.find_and_click_button("ok", tries = 30):

                    # Now start Combat Mode and detect any item drops.
                    if Combat.start_combat_mode():
                        
                        if ImageUtils.find_button("ok", tries = 30, is_sub=True):
                            
                            Game.find_and_click_button("home_back")

                else:
                    raise RuntimeError("Failed to skip party selection.")
        else:
            raise RuntimeError("Failed to arrive at the Summon Selection screen.")
