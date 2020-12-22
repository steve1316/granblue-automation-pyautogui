import datetime
import os
import sys
import multiprocessing
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
        
    def run_bot(self, queue):
        self.my_game = Game(queue=queue, custom_mouse_speed=0.3, debug_mode=DEBUG)
        self.my_debug = Debug(self.my_game)

        # Test finding all summon element tabs in Summon Selection Screen.
        self.my_debug.test_find_summon_element_tabs()

        # Test Combat Mode.
        # self.my_debug.test_combat_mode()
        
    def logger(self):
        pass

class MainWindow(QObject):
    def __init__(self):
        QObject.__init__(self)
        
        self.queue = multiprocessing.Queue()
        
        self.bot_object = Tester()
        self.bot_process = None

    # Signal connections connecting the following backend functions to the respective functions in the frontend.
    updateConsoleLog = Signal(str)

    @Slot(str)
    def update_console_log(self, line):
        while not self.queue.empty():
            message = self.queue.get()
            self.updateConsoleLog.emit("\n" + message)

    # Start the bot.
    @Slot()
    def start_bot(self):
        print("\nStarting bot.")
        self.bot_process = multiprocessing.Process(target=self.bot_object.run_bot, args=(self.queue,))
        self.bot_process.start()
    
    # Stop the bot.
    @Slot()
    def stop_bot(self):
        print("\nStopping bot.")
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
