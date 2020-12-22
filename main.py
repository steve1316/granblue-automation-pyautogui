import datetime
import os
import sys
from multiprocessing import Process
from timeit import default_timer as timer

from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine

from debug import Debug
from game import Game

DEBUG = False

class Tester:
    def __init__(self):
        super().__init__()
        
        self.my_game = None
        self.my_debug = None
        
    def run_bot(self):
        self.my_game = Game(custom_mouse_speed=0.3, debug_mode=DEBUG)
        self.my_debug = Debug(self.my_game)

        # Test finding all summon element tabs in Summon Selection Screen.
        #my_debug.test_find_summon_element_tabs()

        # Test Combat Mode.
        self.my_debug.test_combat_mode()
        
    def logger(self):
        pass

class MainWindow(QObject):
    def __init__(self):
        QObject.__init__(self)

        self.myLine = "\nHELLO"
        
        self.bot_object = Tester()
        self.bot_process = None
        
        self.log_reader = None
        self.log_list = []

    # Signal connection connecting the backend function update_console_log() to the onUpdateConsoleLog function in the frontend.
    updateConsoleLog = Signal()

    # Function to interact with the scrolling view's text log.
    @Slot()
    def update_console_log(self):
        self.updateConsoleLog.emit(self.myLine)

    # Start the bot.
    @Slot()
    def start_bot(self):
        self.bot_process = Process(target=self.bot_object.run_bot)
        self.bot_process.start()
    
    # Stop the bot.
    @Slot()
    def stop_bot(self):
        self.bot_process.terminate()


if __name__ == "__main__":
    # run_bot()

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
