import multiprocessing
import os
import sys
from pathlib import Path
from timeit import default_timer as timer
from typing import Iterable

from PySide2.QtCore import QObject, QUrl, Signal, Slot
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine

from debug import Debug
from game import Game
from map_selection import MapSelection
from twitter_room_finder import TwitterRoomFinder


class MainDriver:
    """
    This driver class allows the Game class to be run on a separate Thread.

    Attributes
    ----------
    None

    """
    def __init__(self):
        super().__init__()
        self.game = None
        self.debug = None
        
    def run_bot(self, item_name: str, item_amount_to_farm: str, farming_mode: str, location_name: str, mission_name: str, summon_element_list: Iterable[str], summon_list: Iterable[str], group_number: int, 
                party_number: int, combat_script: str, queue: multiprocessing.Queue, isBotRunning: int, debug_mode: bool = False):
        """Starts the main bot process on this Thread.

        Args:
            item_name (str): Name of the item to farm.
            item_amount_to_farm (str): Amount of the item to farm.
            farming_mode (str): Mode to look for the specified item and map in.
            location_name (str): Name of the map to look for the specified mission in.
            mission_name (str): Name of the mission to farm the item in.
            summon_element_list (Iterable[str]): List of names of the Summon element image file in the /images/buttons/ folder.
            summon_list (Iterable[str]): List of names of the Summon image's file name in /images/summons/ folder.
            group_number (int): The Group that the specified Party in in.
            party_number (int): The specified Party to start the mission with.
            combat_script (str): The file path to the combat script to use for Combat Mode.
            queue (multiprocessing.Queue): Queue to keep track of logging messages to share between backend and frontend.
            isBotRunning (int): Flag in shared memory that signals the frontend that the bot has finished/exited.
            debug_mode (bool): Optional flag to print relevant debug messages. Defaults to False.

        Returns:
            None
        """
        # Initialize the Game and Debug classes.
        self.game = Game(queue=queue, isBotRunning=isBotRunning, combat_script=combat_script, debug_mode=debug_mode)
        self.debug = Debug(self.game, isBotRunning=isBotRunning, combat_script=combat_script)

        self.game.start_farming_mode(item_name=item_name, item_amount_to_farm=item_amount_to_farm, farming_mode=farming_mode, location_name=location_name, mission_name=mission_name, 
                                     summon_element_list=summon_element_list, summon_list=summon_list, group_number=group_number, party_number=party_number)
        
        # Test finding tweets.
        # self.debug.test_twitter_listener()
        
        # Test finding amounts of all items on the screen.
        # self.debug.test_item_detection()

        # Test the Farming Mode.
        # self.debug.test_farming_mode()

        # Test finding all summon element tabs in Summon Selection Screen.
        # self.debug.test_find_summon_element_tabs()

        # Test Combat Mode.
        # self.debug.test_combat_mode()
        # self.debug.test_combat_mode2()
        
        isBotRunning.value = 1
        return None

class MainWindow(QObject):
    """
    Provides the methods to share information and perform operations between backend and frontend.

    Attributes
    ----------
    None

    """
    def __init__(self):
        QObject.__init__(self)
        
        # Create the Queue for storing logging messages, the flag for the bot's running status, and the amount of seconds that the bot has been running for.
        self.queue = multiprocessing.Queue()
        self.isBotRunning = None
        self.botRunningTimeInSeconds = None
        
        # Create a list in memory to hold all messages in case the frontend wants to save all those messages into a text file.
        self.text_log = []
        
        # Hold the file path to the combat script for use during Combat Mode.
        self.real_file_path = None
                
        # Prep the following objects for multi-processed threading.        
        self.bot_object = MainDriver()
        self.bot_process = None
        
        # Hold the following information for the Game class initialization in a new thread.
        self.farming_mode = ""
        self.item_name = ""
        self.item_amount_to_farm = ""
        self.location_name = ""
        self.mission_name = ""
        self.summon_element_list = []
        self.summon_list = []
        self.group_number = ""
        self.party_number = ""
        
        # Amount of time that the bot is allowed to run for in seconds.
        self.maximum_runtime = "none"
        
        self.debug_mode = False

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
    
    @Slot()
    def reset_values(self):
        """Reset the values for Game class initialization back to default.

        Returns:
            None
        """
        self.farming_mode = ""
        self.item_name = ""
        self.item_amount_to_farm = "0"
        self.location_name = ""
        self.mission_name = ""
        self.summon_element_list = []
        self.summon_list = []
        self.group_number = ""
        self.party_number = ""
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
        if(new_time != "" and new_time != "00:00:00" and len(new_time) != 1):
            self.maximum_runtime = new_time
        else:
            self.maximum_runtime = "none"
            
        self.updateMessage.emit("Farming Mode: " + self.farming_mode + "\nItem Name: " + self.item_name + "\nLocation: " + self.location_name + "\nMission: " + self.mission_name + 
                                "\nItem amount to farm: " + str(self.item_amount_to_farm) + "\nSummons: " + str(self.summon_list) + "\nGroup #: " + str(self.group_number) + "\nParty #: " + 
                                str(self.party_number) + "\nRunning Time: " + str(self.maximum_runtime))
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
        self.debug_mode = flag
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
        self.farming_mode = farming_mode
        self.updateMessage.emit("Farming Mode: " + self.farming_mode + "\nItem Name: " + self.item_name + "\nLocation: " + self.location_name + "\nMission: " + self.mission_name + 
                                "\nItem amount to farm: " + str(self.item_amount_to_farm) + "\nSummons: " + str(self.summon_list) + "\nGroup #: " + str(self.group_number) + "\nParty #: " + 
                                str(self.party_number) + "\nRunning Time: " + str(self.maximum_runtime))
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
        self.item_name = item_name
        self.updateMessage.emit("Farming Mode: " + self.farming_mode + "\nItem Name: " + self.item_name + "\nLocation: " + self.location_name + "\nMission: " + self.mission_name + 
                                "\nItem amount to farm: " + str(self.item_amount_to_farm) + "\nSummons: " + str(self.summon_list) + "\nGroup #: " + str(self.group_number) + "\nParty #: " + 
                                str(self.party_number) + "\nRunning Time: " + str(self.maximum_runtime))
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
        self.item_amount_to_farm = int(item_amount)
        
        self.updateMessage.emit("Farming Mode: " + self.farming_mode + "\nItem Name: " + self.item_name + "\nLocation: " + self.location_name + "\nMission: " + self.mission_name + 
                                "\nItem amount to farm: " + str(self.item_amount_to_farm) + "\nSummons: " + str(self.summon_list) + "\nGroup #: " + str(self.group_number) + "\nParty #: " + 
                                str(self.party_number) + "\nRunning Time: " + str(self.maximum_runtime))
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
        self.mission_name = mission_name
        if(location_name != ""):
            self.location_name = location_name
        else:
            self.location_name = ""
            
        self.updateMessage.emit("Farming Mode: " + self.farming_mode + "\nItem Name: " + self.item_name + "\nLocation: " + self.location_name + "\nMission: " + self.mission_name + 
                                "\nItem amount to farm: " + str(self.item_amount_to_farm) + "\nSummons: " + str(self.summon_list) + "\nGroup #: " + str(self.group_number) + "\nParty #: " + 
                                str(self.party_number) + "\nRunning Time: " + str(self.maximum_runtime))
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
        if(summon_name != ""):
            if (summon_name not in self.summon_list):
                self.summon_list.append(summon_name)
                self.summon_element_list.append(summon_element)
            else:
                # If the user selected a Summon that had been already selected, remove it from the list. Remove its element as well.
                index = self.summon_list.index(summon_name)
                self.summon_list.remove(summon_name)
                self.summon_element_list.pop(index)

            self.updateMessage.emit("Farming Mode: " + self.farming_mode + "\nItem Name: " + self.item_name + "\nLocation: " + self.location_name + "\nMission: " + self.mission_name + 
                                    "\nItem amount to farm: " + str(self.item_amount_to_farm) + "\nSummons: " + str(self.summon_list) + "\nGroup #: " + str(self.group_number) + "\nParty #: " + 
                                    str(self.party_number) + "\nRunning Time: " + str(self.maximum_runtime))
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
        self.group_number = int(split_group_number)
        
        self.updateMessage.emit("Farming Mode: " + self.farming_mode + "\nItem Name: " + self.item_name + "\nLocation: " + self.location_name + "\nMission: " + self.mission_name + 
                                "\nItem amount to farm: " + str(self.item_amount_to_farm) + "\nSummons: " + str(self.summon_list) + "\nGroup #: " + str(self.group_number) + "\nParty #: " + 
                                str(self.party_number) + "\nRunning Time: " + str(self.maximum_runtime))
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
        self.party_number = int(split_party_number)
        
        self.updateMessage.emit("Farming Mode: " + self.farming_mode + "\nItem Name: " + self.item_name + "\nLocation: " + self.location_name + "\nMission: " + self.mission_name + 
                                "\nItem amount to farm: " + str(self.item_amount_to_farm) + "\nSummons: " + str(self.summon_list) + "\nGroup #: " + str(self.group_number) + "\nParty #: " + 
                                str(self.party_number) + "\nRunning Time: " + str(self.maximum_runtime))
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

        for line in self.text_log:
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
        self.real_file_path = QUrl(file_path).toLocalFile()
        file_name = str(Path(self.real_file_path).name)
        self.openFile.emit(file_name)
        return None
    
    @Slot()
    def check_bot_status(self):
        """Checks the status of the bot and returns the status of the bot, whether it is currently running or not. If there is a maximum runtime defined, it will check if the running time of the bot had exceeded that as well.
        
        @Slot()

        Returns:
            None
        """
        if(self.maximum_runtime != "none"):
            # Grab the maximum hours, minutes, and seconds.
            max_hours, max_minutes, max_seconds = self.maximum_runtime.split(":")
            max_seconds = int(max_hours) * 3600 + int(max_minutes) * 60 + int(max_seconds)
            
            # Get the elapsed time since the bot started in seconds.
            elapsed_seconds = timer() - self.botRunningTimeInSeconds

            # Parse the remaining hours, minutes, and seconds.
            remaining_seconds = (int(max_seconds) - elapsed_seconds) % (24 * 3600)
            remaining_hours = remaining_seconds // 3600
            remaining_seconds %= 3600
            remaining_minutes = remaining_seconds // 60
            remaining_seconds %= 60
            
            # Now construct the new time that is remaining.
            remaining_time = "%02d:%02d:%02d" % (remaining_hours, remaining_minutes, remaining_seconds)
        
            if(elapsed_seconds >= max_seconds):
                # Reset the timer back to 00:00:00 to prevent the program from going to 00:00:59 when it stops.
                self.updateTimerTextField.emit("00:00:00")
                self.checkBotStatus.emit(True)
            else:
                self.updateTimerTextField.emit(remaining_time)

        # Transmit True if the bot had stopped running and False otherwise.
        elif(self.isBotRunning.value == 1):
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
        while not self.queue.empty():
            message = self.queue.get()
            self.text_log.append(message)
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

    @Slot()
    def start_bot(self):
        """Starts the bot's Game class on a new Thread.
        
        @Slot()

        Returns:
            None
        """
        print("\n[STATUS] Starting bot on a new Thread...")
        
        # Clear the text log.
        self.text_log.clear()
        
        # Save the isBotRunning flag as an int in memory to be shared across classes. Value of 0 means the bot is currently running and a value of 1 means the bot has stopped.
        self.isBotRunning = multiprocessing.Value("i", 0)
        
        # Start the timer for the running time of the bot.
        self.botRunningTimeInSeconds = timer()
        
        # Create a new Process whose target is the MainDriver's run_bot() method.
        self.bot_process = multiprocessing.Process(target=self.bot_object.run_bot, args=(self.item_name, self.item_amount_to_farm, self.farming_mode, self.location_name,
                                                                                         self.mission_name, self.summon_element_list, self.summon_list, self.group_number,
                                                                                         self.party_number, self.real_file_path, self.queue, self.isBotRunning, self.debug_mode))
        
        # Now start the new Process on a new Thread.
        self.bot_process.start()
        return None
    
    @Slot()
    def stop_bot(self):
        """Stops the bot and terminates the Process.
        
        @Slot()

        Returns:
            None
        """
        if(self.bot_process != None):
            print("\n[STATUS] Stopping the bot and terminating the Thread.")
            self.bot_process.terminate()
        return None


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    app.setOrganizationName("somename")
    app.setOrganizationDomain("somename")
    engine = QQmlApplicationEngine()

    # Get the Context.
    main = MainWindow()
    engine.rootContext().setContextProperty("backend", main)

    # Load the QML File.
    engine.load(os.path.join(os.path.dirname(__file__), "gui/qml/main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
