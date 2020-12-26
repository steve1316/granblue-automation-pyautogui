import multiprocessing
import os
import sys

from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine

from debug import Debug
from game import Game
from map_selection import MapSelection

DEBUG = False

class Tester:
    def __init__(self):
        super().__init__()
        
        self.game = None
        self.debug = None
        
    def run_bot(self, queue, isBotRunning):
        self.game = Game(queue=queue, isBotRunning=isBotRunning, custom_mouse_speed=0.5, debug_mode=DEBUG)
        self.map_selection = MapSelection(self.game)
        self.debug = Debug(self.game, isBotRunning=isBotRunning)
        
        # Test finding amounts of all items on the screen.
        self.debug.test_item_detection(4)

        # Test the Farming Mode.
        # self.debug.test_farming_mode()
        
        # Test navigating to all maps supported by MapSelection.
        # self.debug.test_map_selection()

        # Test finding all summon element tabs in Summon Selection Screen.
        # self.debug.test_find_summon_element_tabs()

        # Test Combat Mode.
        # self.debug.test_combat_mode()
        
        isBotRunning.value = 1

class MainWindow(QObject):
    def __init__(self):
        QObject.__init__(self)
        
        # Create the Queue for storing logging messages and the flag for the bot status.
        self.queue = multiprocessing.Queue()
        self.isBotRunning = None
                
        self.bot_object = Tester()
        self.bot_process = None

    # Signal connections connecting the following backend functions to the respective functions in the frontend.
    # The data type inside the Signal indicates the return type from backend to frontend.
    updateConsoleLog = Signal(str)
    checkBotStatus = Signal(bool)
    
    # The data type inside the Slot indicates the return type from frontend to backend. 
    # In this case, this function expects nothing from the frontend.
    @Slot()
    def check_bot_status(self):
        if(self.isBotRunning.value == 1):
            self.checkBotStatus.emit(True)
        else:
            self.checkBotStatus.emit(False)

    @Slot()
    def update_console_log(self):
        while not self.queue.empty():
            message = self.queue.get()
            self.updateConsoleLog.emit(message)

    # Start the bot.
    @Slot()
    def start_bot(self):
        print("\nStarting bot.")
        self.isBotRunning = multiprocessing.Value("i", 0)
        self.bot_process = multiprocessing.Process(target=self.bot_object.run_bot, args=(self.queue, self.isBotRunning,))
        self.bot_process.start()
    
    # Stop the bot.
    @Slot()
    def stop_bot(self):
        print("\nStopping bot.")
        self.bot_process.terminate()


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Get the Context.
    main = MainWindow()
    engine.rootContext().setContextProperty("backend", main)

    # Load the QML File.
    engine.load(os.path.join(os.path.dirname(__file__), "gui/qml/main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
