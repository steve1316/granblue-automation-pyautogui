import multiprocessing
import os
import time

from utils.settings import Settings
from utils import discord_utils
from bot.game import Game


class MainDriver:
    """
    This driver class allows the Game class to be run on a separate Thread.
    """

    def __init__(self):
        super().__init__()
        self._game = None
        self._bot_process = None
        self._discord_process = None

    def _run_bot(self):
        """Starts the main bot process on this Thread.

        Returns:
            None
        """
        # Initialize the Game class and start Farming Mode.
        self._game = Game()
        self._game.start_farming_mode()
        return None

    def start_bot(self):
        """Starts the bot's Game class on a new Thread.

        Returns:
            None
        """
        # #### discord ####
        if Settings.enable_discord and Settings.discord_token != "" and Settings.user_id != 0:
            print("\n[DISCORD] Starting Discord process on a new Thread...")
            self._discord_process = multiprocessing.Process(target = discord_utils.start_now, args = (Settings.discord_token, Settings.user_id, Settings.discord_queue))
            self._discord_process.start()
        else:
            print("\n[DISCORD] Unable to start Discord process. Either you opted not to turn it on or your included token and user id inside the config.ini are invalid.")
        # #### end of discord ####

        print("\n[STATUS] Starting bot on a new Thread...")

        # Create a new Process whose target is the MainDriver's run_bot() method.
        self._bot_process = multiprocessing.Process(target = self._run_bot)

        print("Starting now")

        # Now start the new Process on a new Thread.
        self._bot_process.start()

        return None

    def stop_bot(self):
        """Stops the bot and terminates the Process.

        Returns:
            None
        """
        if self._bot_process is not None:
            print("\n[STATUS] Stopping the bot and terminating its Thread.")
            self._bot_process.terminate()

        if self._discord_process is not None and self._discord_process.is_alive():
            Settings.discord_queue.put(f"```diff\n- Terminated connection to Discord API for Granblue Automation\n```")
            print("\n[DISCORD] Terminated connection to Discord API and terminating its Thread.")
            time.sleep(1.0)
            self._discord_process.terminate()

        return None


if __name__ == "__main__":
    # Generate a config.ini in the root of the folder if it does not exist.
    if os.path.exists(f"{os.getcwd()}/backend/config.ini") is False:
        new_config_file = open("config.ini", "x")
        new_config_file.write("""
############################################################
; Customize the bot's internals by editing the following to your liking.
; Do not enclose anything in double quotes, " ".
############################################################

############################################################
# Read the instructions on the GitHub repository README.md on how to setup Discord notifications.
############################################################
[discord]
enable_discord = False
discord_token = 
user_id = 0

############################################################
# Read the instructions on the GitHub repository README.md on how to get these keys in order to allow the bot to farm Raids via Twitter.
############################################################
[twitter]
api_key = 
api_key_secret = 
access_token = 
access_token_secret = 
set_stream_api_default = True

[refill]
############################################################
# NOTE: Enable the 'enabled_auto_restore' field if you have enabled the 'AP/EP Auto-Restore Settings' under the Misc settings in-game.
# This includes the 'Auto-Restore Notification Settings' being set to Hide. This will shave off about 10s per run.
############################################################
refill_using_full_elixir = False
refill_using_soul_balms = False
enabled_auto_restore = True

[configuration]
############################################################
# Mouse speed in this application is the amount of time in seconds needed to move the mouse from Point A to Point B. Default is 0.2 seconds.
############################################################
mouse_speed = 0.2

############################################################
# Enables the usage of the Bezier Curve to have the bot mimic human-like but slow mouse movements.
# If disabled, the bot will use bot-like but fast linear mouse movement.
############################################################
enable_bezier_curve_mouse_movement = true

############################################################
# Enable delay in seconds between runs to serve as a resting period.
# Default is 15 seconds.
# Note: If both this and randomized delay is turned on, only this delay will be used.
############################################################
enable_delay_between_runs = False
delay_in_seconds = 15

############################################################
# Enable randomized delay in seconds between runs in the range between the lower and upper bounds inclusive to serve as a resting period.
# Default is 15 seconds for the lower bound and 60 seconds for the upper bound.
############################################################
enable_randomized_delay_between_runs = False
delay_in_seconds_lower_bound = 15
delay_in_seconds_upper_bound = 60

############################################################
# The following settings below follow pretty much the same template provided. They default to the settings selected for Farming Mode if nothing is set.

# Enables this fight or skip it if false.
# enable_*** =

# The file name of the combat script to use inside the /scripts/ folder. If set to nothing, defaults to the one selected for Farming Mode. Example: full_auto
# ***_combat_script =

# Select what Summon(s) separated by commas to use in order from highest priority to least. Example: Shiva, Colossus Omega, Varuna, Agni
# https://github.com/steve1316/granblue-automation-pyautogui/wiki/Selectable-Summons
# ***_summon_list =

# Indicate what element(s) the Summon(s) are in order from ***_summon_list separated by commas. Accepted values are: Fire, Water, Earth, Wind, Light, Dark, Misc.
# ***__summon_element_list =

# Set what Party to select and under what Group to run for the specified fight. Accepted values are: Group [1, 2, 3, 4, 5, 6, 7] and Party [1, 2, 3, 4, 5, 6].
# ***_group_number =
# ***_party_number =
############################################################

[dimensional_halo]
enable_dimensional_halo = False
dimensional_halo_combat_script = 
dimensional_halo_summon_list = 
dimensional_halo_summon_element_list = 
dimensional_halo_group_number = 0
dimensional_halo_party_number = 0

[event]
enable_event_nightmare = False
event_nightmare_combat_script = 
event_nightmare_summon_list = 
event_nightmare_summon_element_list = 
event_nightmare_group_number = 0
event_nightmare_party_number = 0

[rise_of_the_beasts]
enable_rotb_extreme_plus = False
rotb_extreme_plus_combat_script = 
rotb_extreme_plus_summon_list = 
rotb_extreme_plus_summon_element_list = 
rotb_extreme_plus_group_number = 0
rotb_extreme_plus_party_number = 0

[xeno_clash]
enable_xeno_clash_nightmare = False
xeno_clash_nightmare_combat_script = 
xeno_clash_nightmare_summon_list = 
xeno_clash_nightmare_summon_element_list = 
xeno_clash_nightmare_group_number = 0
xeno_clash_nightmare_party_number = 0

[arcarum]
enable_stop_on_arcarum_boss = True
""")

        new_config_file.close()
        print("\n[INFO] Generated a new config.ini in the /backend/ folder.")

    # Start the bot.
    bot_object = MainDriver()
    bot_object.start_bot()

    while True:
        if Settings.bot_status_flag.value == 1:
            break

    bot_object.stop_bot()



