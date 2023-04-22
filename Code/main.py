import sys

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine

# from pathlib import Path

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.load('QmlWindows/AuthWindow.qml')  # файл с кодом QML основного окна
    sys.exit(app.exec())  # запустить цикл события
