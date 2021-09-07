import multiprocessing
import os
import sys
import time
from configparser import ConfigParser
from pathlib import Path
from timeit import default_timer as timer
from typing import List

from PySide2.QtCore import QObject, QUrl, Signal, Slot
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine

import utils.discord_utils
from bot.game import Game


class MainDriver:
    """
    This driver class allows the Game class to be run on a separate Thread.
    """

    def __init__(self):
        super().__init__()
        self._game = None
        self._debug = None

    def run_bot(self, item_name: str, item_amount_to_farm: str, farming_mode: str, location_name: str, mission_name: str, summon_element_list: List[str], summon_list: List[str],
                group_number: int, party_number: int, combat_script: str, queue: multiprocessing.Queue, discord_queue: multiprocessing.Queue, is_bot_running: int, debug_mode: bool = False,
                test_mode: bool = False):
        """Starts the main bot process on this Thread.

        Args:
            item_name (str): Name of the item to farm.
            item_amount_to_farm (str): Amount of the item to farm.
            farming_mode (str): Mode to look for the specified item and map in.
            location_name (str): Name of the map to look for the specified mission in.
            mission_name (str): Name of the mission to farm the item in.
            summon_element_list (List[str]): List of names of the Summon element image file in the /images/buttons/ folder.
            summon_list (List[str]): List of names of the Summon image's file name in /images/summons/ folder.
            group_number (int): The Group that the specified Party in in.
            party_number (int): The specified Party to start the mission with.
            combat_script (str): The file path to the combat script to use for Combat Mode.
            queue (multiprocessing.Queue): Queue to keep track of logging messages to share between backend and frontend.
            discord_queue (multiprocessing.Queue): Queue to keep track of status messages to inform the user via Discord DMs.
            is_bot_running (int): Flag in shared memory that signals the frontend that the bot has finished/exited.
            debug_mode (bool): Optional flag to print relevant debug messages. Defaults to False.
            test_mode (bool): Optional flag to turn on debugging testing mode. Defaults to False.

        Returns:
            None
        """
        # Initialize the Game class and start Farming Mode.
        self._game = Game(queue = queue, discord_queue = discord_queue, is_bot_running = is_bot_running, item_name = item_name, item_amount_to_farm = int(item_amount_to_farm),
                          farming_mode = farming_mode, map_name = location_name, mission_name = mission_name, summon_element_list = summon_element_list, summon_list = summon_list,
                          group_number = group_number, party_number = party_number, combat_script = combat_script, debug_mode = debug_mode, test_mode = test_mode)

        self._game.start_farming_mode()

        is_bot_running.value = 1
        return None


# noinspection PyUnresolvedReferences
# ^ This is for suppressing warnings in PyCharm that it cannot recognize the emit() method.
class MainWindow(QObject):
    """
    Provides the methods to share information and perform operations between backend and frontend.
    """

    def __init__(self):
        QObject.__init__(self)

        # Create the Queue for storing logging messages, the flag for the bot's running status, and the amount of seconds that the bot has been running for.
        self._queue = multiprocessing.Queue()
        self._is_bot_running = None
        self._botRunningTimeInSeconds = None

        # Create the Queue and process for the Discord functionality.
        self.discord_queue = None
        self._discord_process = None

        # Create a list in memory to hold all messages in case the frontend wants to save all those messages into a text file.
        self._text_log: list = []

        # Hold the file path to the combat script for use during Combat Mode.
        self._real_file_path: str = ""

        # Prep the following objects for multi-processed threading.        
        self._bot_object = MainDriver()
        self._bot_process = None

        # Hold the following information for the Game class initialization in a new thread.
        self._farming_mode: str = ""
        self._item_name: str = ""
        self._item_amount_to_farm: int = 0
        self._location_name: str = ""
        self._mission_name: str = ""
        self._summon_element_list: list = []
        self._summon_list: list = []
        self._group_number: int = 0
        self._party_number: int = 0

        # Amount of time that the bot is allowed to run for in seconds.
        self._maximum_runtime = "none"

        self._debug_mode = False

        self._test_mode = False

    # These signal connections connects the following backend functions to their respective functions in the frontend via the Connections type in the Signal and Handler Event System in Qt QML.
    # The data type inside the Signal indicates the return type going from backend to frontend. All of the functions that are connected to the frontend needs to use the emit() functionality 
    # to transmit their return information so that the frontend can receive it.
    updateConsoleLog = Signal(str)
    checkBotStatus = Signal(bool)
    checkBotReady = Signal(bool)
    openFile = Signal(str)
    updateMessage = Signal(str)
    enableGroupAndPartySelectors = Signal()
    updateTimerTextField = Signal(str)
    getSummonListLength = Signal(int)

    @Slot()
    def reset_values(self):
        """Reset the values for Game class initialization back to default.
        
        @Slot()

        Returns:
            None
        """
        self._farming_mode = ""
        self._item_name = ""
        self._item_amount_to_farm = 0
        self._location_name = ""
        self._mission_name = ""
        self._summon_element_list = []
        self._summon_list = []
        self._group_number = 0
        self._party_number = 0
        return None

    @Slot(str)
    def update_timer(self, new_time: str):
        """Update the amount of time that the bot is allowed to run for. If no time was provided, bot will run until it achieves its main objective.
        
        @Slot(str)

        Args:
            new_time (str): The updated max time that the bot is allowed to run.

        Returns:
            None
        """
        if new_time != "" and new_time != "00:00:00" and len(new_time) != 1:
            self._maximum_runtime = new_time
        else:
            self._maximum_runtime = "none"

        self.updateMessage.emit("Farming Mode: " + self._farming_mode + "\nItem Name: " + self._item_name + "\nLocation: " + self._location_name + "\nMission: " + self._mission_name +
                                "\nItem amount to farm: " + str(self._item_amount_to_farm) + "\nSummons: " + str(self._summon_list) + "\nGroup #: " + str(self._group_number) + "\nParty #: " +
                                str(self._party_number) + "\nRunning Time: " + str(self._maximum_runtime))
        return None

    @Slot(bool)
    def update_debug_mode(self, flag: bool):
        """Update the debug mode flag for Game class initialization.
        
        @Slot(bool)

        Args:
            flag (bool): True if Debug Mode should be turned on and False otherwise.

        Returns:
            None
        """
        self._debug_mode = flag
        return None

    @Slot(str)
    def update_farming_mode(self, farming_mode: str):
        """Updates the Farming Mode for Game class initialization.
        
        @Slot(str)

        Args:
            farming_mode (str): Mode to look for the specified item and map in.

        Returns:
            None
        """
        self._farming_mode = farming_mode
        self.updateMessage.emit("Farming Mode: " + self._farming_mode + "\nItem Name: " + self._item_name + "\nLocation: " + self._location_name + "\nMission: " + self._mission_name +
                                "\nItem amount to farm: " + str(self._item_amount_to_farm) + "\nSummons: " + str(self._summon_list) + "\nGroup #: " + str(self._group_number) + "\nParty #: " +
                                str(self._party_number) + "\nRunning Time: " + str(self._maximum_runtime))
        return None

    @Slot(str)
    def update_item_name(self, item_name: str):
        """Updates the item name to farm for Farming Mode.
        
        @Slot(str)

        Args:
            item_name (str): Name of the item to farm.

        Returns:
            None
        """
        self._item_name = item_name
        self.updateMessage.emit("Farming Mode: " + self._farming_mode + "\nItem Name: " + self._item_name + "\nLocation: " + self._location_name + "\nMission: " + self._mission_name +
                                "\nItem amount to farm: " + str(self._item_amount_to_farm) + "\nSummons: " + str(self._summon_list) + "\nGroup #: " + str(self._group_number) + "\nParty #: " +
                                str(self._party_number) + "\nRunning Time: " + str(self._maximum_runtime))
        return None

    @Slot(str)
    def update_item_amount(self, item_amount: str):
        """Updates the item amount to farm for Farming Mode.
        
        @Slot(str)

        Args:
            item_amount (str): Amount of the item to farm.

        Returns:
            None
        """
        self._item_amount_to_farm = int(item_amount)

        self.updateMessage.emit("Farming Mode: " + self._farming_mode + "\nItem Name: " + self._item_name + "\nLocation: " + self._location_name + "\nMission: " + self._mission_name +
                                "\nItem amount to farm: " + str(self._item_amount_to_farm) + "\nSummons: " + str(self._summon_list) + "\nGroup #: " + str(self._group_number) + "\nParty #: " +
                                str(self._party_number) + "\nRunning Time: " + str(self._maximum_runtime))
        return None

    @Slot(str, str)
    def update_mission_name(self, mission_name: str, location_name: str):
        """Updates the mission name for Farming Mode.
        
        @Slot(str, str)

        Args:
            mission_name (str): Name of the mission to farm the item in.
            location_name (str): Name of the map to look for the specified mission in.

        Returns:
            None
        """
        self._mission_name = mission_name
        if location_name != "":
            self._location_name = location_name
        else:
            self._location_name = ""

        self.updateMessage.emit("Farming Mode: " + self._farming_mode + "\nItem Name: " + self._item_name + "\nLocation: " + self._location_name + "\nMission: " + self._mission_name +
                                "\nItem amount to farm: " + str(self._item_amount_to_farm) + "\nSummons: " + str(self._summon_list) + "\nGroup #: " + str(self._group_number) + "\nParty #: " +
                                str(self._party_number) + "\nRunning Time: " + str(self._maximum_runtime))
        return None

    @Slot(str, str)
    def update_summon_list(self, summon_name: str, summon_element: str):
        """Appends the specified Summon name and element to their respective lists for Farming Mode.

        @Slot(str, str)

        Args:
            summon_name (str): Exact name of the Summon image's file name in /images/summons/ folder.
            summon_element (str): Name of the Summon element image file in the /images/buttons/ folder.

        Returns:
            None
        """
        if summon_name != "":
            if summon_name not in self._summon_list:
                self._summon_list.append(summon_name)
                self._summon_element_list.append(summon_element)
            else:
                # If the user selected a Summon that had already been selected, remove it from the list. Remove its element as well.
                index = self._summon_list.index(summon_name)
                self._summon_list.remove(summon_name)
                self._summon_element_list.pop(index)

            self.updateMessage.emit("Farming Mode: " + self._farming_mode + "\nItem Name: " + self._item_name + "\nLocation: " + self._location_name + "\nMission: " + self._mission_name +
                                    "\nItem amount to farm: " + str(self._item_amount_to_farm) + "\nSummons: " + str(self._summon_list) + "\nGroup #: " + str(self._group_number) + "\nParty #: " +
                                    str(self._party_number) + "\nRunning Time: " + str(self._maximum_runtime))

        # Send the current length of the Summon list to the frontend.
        self.getSummonListLength.emit(len(self._summon_list))

        return None

    @Slot()
    def clear_summon_list(self):
        """Clears the Summon and Summon Element lists for the frontend.

        @Slot()

        Returns:
            None
        """
        self._summon_element_list.clear()
        self._summon_list.clear()

        return None

    @Slot(str)
    def update_group_number(self, group_number: str):
        """Updates the Group number for Farming Mode.
        
        @Slot(str)

        Args:
            group_number (str): The specified Group to use for Farming Mode.

        Returns:
            None
        """
        # Parse the Group number and then convert it to int.
        split_group_number = group_number.split(" ")[1]
        self._group_number = int(split_group_number)

        self.updateMessage.emit("Farming Mode: " + self._farming_mode + "\nItem Name: " + self._item_name + "\nLocation: " + self._location_name + "\nMission: " + self._mission_name +
                                "\nItem amount to farm: " + str(self._item_amount_to_farm) + "\nSummons: " + str(self._summon_list) + "\nGroup #: " + str(self._group_number) + "\nParty #: " +
                                str(self._party_number) + "\nRunning Time: " + str(self._maximum_runtime))
        return None

    @Slot(str)
    def update_party_number(self, party_number: str):
        """Updates the Party number for Farming Mode.
        
        @Slot(str)

        Args:
            party_number (str): The specified Party to use for Farming Mode.

        Returns:
            None
        """
        # Parse the Party number and then convert it to int.
        split_party_number = party_number.split(" ")[1]
        self._party_number = int(split_party_number)

        self.updateMessage.emit("Farming Mode: " + self._farming_mode + "\nItem Name: " + self._item_name + "\nLocation: " + self._location_name + "\nMission: " + self._mission_name +
                                "\nItem amount to farm: " + str(self._item_amount_to_farm) + "\nSummons: " + str(self._summon_list) + "\nGroup #: " + str(self._group_number) + "\nParty #: " +
                                str(self._party_number) + "\nRunning Time: " + str(self._maximum_runtime))
        return None

    @Slot(str)
    def save_file(self, file_path: str):
        """Save the text_log to the specified text file.
        
        @Slot(str)

        Args:
            file_path (str): The location of where to save the text file to.

        Returns:
            None
        """
        # Parse the file path from Qt QML and then either open an existing file or create a new one otherwise.
        file_path = QUrl(file_path).toLocalFile()
        opened_file = open(file_path, "w")

        for line in self._text_log:
            opened_file.write("\n" + line)

        opened_file.close()
        return None

    @Slot(str)
    def open_file(self, file_path: str):
        """Obtain the file path to the combat script that the user selected. After saving the real file path, return the full file name of the script back to frontend.
        
        @Slot(str)

        Args:
            file_path (str): The file path to the combat script for Combat Mode.

        Returns:
            None
        """
        # Parse the file path to the specified file from Qt QML, grab the file name and then transmit it to the frontend.
        self._real_file_path = QUrl(file_path).toLocalFile()
        file_name = str(Path(self._real_file_path).name)
        self.openFile.emit(file_name)
        return None

    @Slot()
    def check_bot_status(self):
        """Checks the status of the bot and returns the status of the bot, whether it is currently running or not. If there is a maximum runtime defined, it will check if the running time of the bot had exceeded that as well.
        
        @Slot()

        Returns:
            None
        """
        if self._maximum_runtime != "none":
            # Grab the maximum hours, minutes, and seconds.
            max_hours, max_minutes, max_seconds = self._maximum_runtime.split(":")
            max_seconds = int(max_hours) * 3600 + int(max_minutes) * 60 + int(max_seconds)

            # Get the elapsed time since the bot started in seconds.
            elapsed_seconds = timer() - self._botRunningTimeInSeconds

            # Parse the remaining hours, minutes, and seconds.
            remaining_seconds = (int(max_seconds) - elapsed_seconds) % (24 * 3600)
            remaining_hours = remaining_seconds // 3600
            remaining_seconds %= 3600
            remaining_minutes = remaining_seconds // 60
            remaining_seconds %= 60

            # Now construct the new time that is remaining.
            remaining_time = "%02d:%02d:%02d" % (remaining_hours, remaining_minutes, remaining_seconds)

            if elapsed_seconds >= max_seconds:
                # Reset the timer back to 00:00:00 to prevent the program from going to 00:00:59 when it stops.
                self.updateTimerTextField.emit("00:00:00")
                self.checkBotStatus.emit(True)
            else:
                self.updateTimerTextField.emit(remaining_time)

        # Transmit True if the bot had stopped running and False otherwise.
        elif self._is_bot_running.value == 1:
            self.checkBotStatus.emit(True)
        else:
            self.checkBotStatus.emit(False)

        return None

    @Slot()
    def update_console_log(self):
        """Grab logging messages from the Queue and then output to the frontend's log.

        @Slot()
        
        Returns:
            None
        """
        # While the Queue is not empty, grab a message from it, append it to the log, and then transmit the message to the frontend.
        while not self._queue.empty():
            message = self._queue.get()
            self._text_log.append(message)
            self.updateConsoleLog.emit(message)

        return None

    @Slot(bool)
    def check_bot_ready(self, ready_flag: bool):
        """Update the flag on whether or not the bot is ready to start.
        
        @Slot(bool)

        Args:
            ready_flag (bool): True if the bot has all the information it needs to start running and False otherwise.

        Returns:
            None
        """
        self.checkBotReady.emit(ready_flag)
        return None

    @Slot(str)
    def update_test_mode(self, flag: bool):
        """Grab logging messages from the Queue and then output to the frontend's log.

        @Slot(str)

        Args:
            flag (bool): True if the bot will start in a debugging testing mode and False for normal operations.

        Returns:
            None
        """
        print(f"Testing mode is {flag}")
        self._test_mode = not self._test_mode

        if self._test_mode:
            self._farming_mode = "test"
            self._item_name = "test"
            self._item_amount_to_farm = 1
            self._location_name = "test"
            self._mission_name = "test"
            self._summon_element_list = ["fire"]
            self._summon_list = ["colossus omega"]
            self._group_number = 1
            self._party_number = 1
            self.updateMessage.emit("Testing Mode turned on.")
        else:
            self.reset_values()
            self.updateMessage.emit("Testing Mode turned off.")

        return None

    @Slot()
    def start_bot(self):
        """Starts the bot's Game class on a new Thread.
        
        @Slot()

        Returns:
            None
        """
        print("\n[STATUS] Starting bot on a new Thread...")

        # Clear the text log.
        self._text_log.clear()

        # Save the bot status flag as an int in memory to be shared across classes. Value of 0 means the bot is currently running and a value of 1 means the bot has stopped.
        self._is_bot_running = multiprocessing.Value("i", 0)

        # Start the timer for the running time of the bot.
        self._botRunningTimeInSeconds = timer()

        # #### discord ####
        config = ConfigParser()
        config.read("config.ini")
        enable_discord: bool = config.getboolean("discord", "enable_discord")
        discord_token: str = config.get("discord", "discord_token")
        user_id: int = config.getint("discord", "user_id")
        self.discord_queue = multiprocessing.Queue()
        if enable_discord and discord_token != "" and user_id != 0:
            print("\n[DISCORD] Starting Discord process on a new Thread...")
            self._discord_process = multiprocessing.Process(target = utils.discord_utils.start_now, args = (discord_token, user_id, self.discord_queue))
            self._discord_process.start()
        else:
            print("\n[DISCORD] Unable to start Discord process. Either you opted not to turn it on or your included token and user id inside the config.ini are invalid.")
        # #### end of discord ####

        # Create a new Process whose target is the MainDriver's run_bot() method.
        self._bot_process = multiprocessing.Process(target = self._bot_object.run_bot, args = (self._item_name, self._item_amount_to_farm, self._farming_mode, self._location_name,
                                                                                               self._mission_name, self._summon_element_list, self._summon_list, self._group_number,
                                                                                               self._party_number, self._real_file_path, self._queue, self.discord_queue, self._is_bot_running,
                                                                                               self._debug_mode, self._test_mode))

        # Now start the new Process on a new Thread.
        self._bot_process.start()
        return None

    @Slot()
    def stop_bot(self):
        """Stops the bot and terminates the Process.
        
        @Slot()

        Returns:
            None
        """
        if self._bot_process is not None:
            print("\n[STATUS] Stopping the bot and terminating its Thread.")
            self._bot_process.terminate()

        if self._discord_process is not None and self._discord_process.is_alive():
            self.discord_queue.put(f"```diff\n- Terminated connection to Discord API for Granblue Automation\n```")
            print("\n[DISCORD] Terminated connection to Discord API and terminating its Thread.")
            time.sleep(1.0)
            self._discord_process.terminate()
        return None


if __name__ == "__main__":
    # Generate a config.ini in the root of the folder if it does not exist.
    if os.path.exists("config.ini") is False:
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
        print("\n[INFO] Generated a new config.ini in the root of the project folder.")

    app = QGuiApplication(sys.argv)
    app.setOrganizationName("steve1316_Organization")
    app.setOrganizationDomain("steve1316_Domain")
    engine = QQmlApplicationEngine()

    # Get the Context.
    main = MainWindow()
    engine.rootContext().setContextProperty("backend", main)

    # Load the QML File.
    engine.load(os.path.join(os.path.dirname(__file__), "gui/qml/main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
