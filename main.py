import sys
import os

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QObject, Slot, Signal

from game import Game
from debug import Debug

DEBUG = False


class MainWindow(QObject):
    def __init__(self):
        QObject.__init__(self)

        self.myLine = "HELLO"

    # Signal connection to the log.
    updateConsoleLog = Signal(str)

    # Function to interact with the scrolling view's text log.
    @Slot(str)
    def update_console_log(self, line):
        self.updateConsoleLog.emit("\nLine: " + self.myLine)

    # Start the bot.
    def start_bot(self):
        self.mygame = Game(custom_mouse_speed=0.3, debug_mode=DEBUG)
        self.mydebug = Debug(self.mygame)

# def main():
#     my_game = Game(custom_mouse_speed=0.3, debug_mode=DEBUG)
#     my_debug = Debug(my_game)

#     # Test finding all summon element tabs in Summon Selection Screen.
#     my_debug.test_find_summon_element_tabs()

#     # Test Combat Mode.
#     # my_debug.test_combat_mode()


if __name__ == "__main__":
    # main()

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
