import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from errors import errors
from classes import ErrorInfo, ButtonHandler, CustomException

if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    engine.load("window.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())
