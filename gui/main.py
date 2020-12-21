# # This Python file uses the following encoding: utf-8
# import sys
# import os

# from PySide2.QtGui import QGuiApplication
# from PySide2.QtQml import QQmlApplicationEngine
# from PySide2.QtCore import QObject, Slot, Signal


# class MainWindow(QObject):
#     def __init__(self):
#         QObject.__init__(self)

#     # Signal variable to the log.
#     updateConsoleLog = Signal(str)

#     # Function set the log to the scrolling view's text.
#     @Slot(str)
#     def update_console_log(self, line):
#         self.updateConsoleLog.emit("Line: " + line)


# if __name__ == "__main__":
#     app = QGuiApplication(sys.argv)
#     engine = QQmlApplicationEngine()

#     # Get the Context.
#     main = MainWindow()
#     engine.rootContext().setContextProperty("backend", main)

#     # Load the QML File.
#     engine.load(os.path.join(os.path.dirname(__file__), "qml/main.qml"))

#     if not engine.rootObjects():
#         sys.exit(-1)
#     sys.exit(app.exec_())
