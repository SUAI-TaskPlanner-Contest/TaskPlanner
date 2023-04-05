# This Python file uses the following encoding: utf-8
import sys
from pathlib import Path

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()
    qml_file = Path(__file__).resolve().parent / "main.qml"
    engine.load("main.qml")


    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
