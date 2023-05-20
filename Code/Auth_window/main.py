import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from auth_window_handler import AuthWindowHandler


if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    buttonHandler = AuthWindowHandler()
    engine.rootContext().setContextProperty("AuthWindowHandler", AuthWindowHandler)

    engine.load("window.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())
