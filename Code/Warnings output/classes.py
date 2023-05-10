from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, QVariant, pyqtSlot
from typing import Tuple


class ErrorInfo(QObject):
    nameChanged = pyqtSignal()
    textChanged = pyqtSignal()
    button1Changed = pyqtSignal()
    button2Changed = pyqtSignal()

    def __init__(self, _name: str, _text: str, _button1: str, _button2: str) -> None:
        super().__init__()
        self._name = _name
        self._text = _text
        self._button1 = _button1
        self._button2 = _button2

    @pyqtProperty(str, notify=nameChanged)
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.nameChanged.emit()

    @pyqtProperty(str, notify=textChanged)
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.textChanged.emit()

    @pyqtProperty(str, notify=button1Changed)
    def button1(self):
        return self._button1

    @button1.setter
    def button1(self, value):
        self._button1 = value
        self.button1Changed.emit()

    @pyqtProperty(str, notify=button2Changed)
    def button2(self):
        return self._button2

    @button2.setter
    def button2(self, value):
        self._button2 = value
        self.button2Changed.emit()


class ButtonHandler(QObject):
    @pyqtSlot()
    def button1Clicked(self):
        pass

    @pyqtSlot()
    def button2Clicked(self):
        pass


class CustomException(Exception):
    def __init__(self, error_info: Tuple[str, str, str, str]) -> None:
        super().__init__(error_info[1])
        self.error_info = ErrorInfo(*error_info)
