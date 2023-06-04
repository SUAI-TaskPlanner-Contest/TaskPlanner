import sys

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine

class PincodeHandler(QObject):
    def __init__(self):
        QObject.__init__(self)

    @pyqtSlot(str, str, str, str)
    def set_pincode(self, pinInput0, pinInput1, pinInput2, pinInput3):
        pin = pinInput0 + pinInput1 + pinInput2 + pinInput3
        print(pin)


if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    pincode_save = PincodeHandler()
    engine.rootContext().setContextProperty("pincode_save", pincode_save)

    engine.load('QmlWindows/PincodeWindow.qml')  # файл с кодом QML окна инструкций
    sys.exit(app.exec())  # запустить цикл события