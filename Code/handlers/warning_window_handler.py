from PyQt6.QtCore import QObject, pyqtProperty, pyqtSignal, QVariant, pyqtSlot


class WarningWindow(QObject):
    nameChanged = pyqtSignal()
    textChanged = pyqtSignal()
    buttonOkChanged = pyqtSignal()
    buttonCancelChanged = pyqtSignal()

    def __init__(self, _name: str, _text: str, _button_ok: str, _button_cancel: str) -> None:
        super().__init__()
        self._name = _name
        self._text = _text
        self._button_ok = _button_ok
        self._button_cancel = _button_cancel

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

    @pyqtProperty(str, notify=buttonOkChanged)
    def button_ok(self):
        return self._button_ok

    @button_ok.setter
    def button_ok(self, value):
        self._button_ok = value
        self.buttonOkChanged.emit()

    @pyqtProperty(str, notify=buttonCancelChanged)
    def button_cancel(self):
        return self._button_cancel

    @button_cancel.setter
    def button_cancel(self, value):
        self._button_cancel = value
        self.buttonCancelChanged.emit()


class WarningButtonHandler(QObject):
    @pyqtSlot()
    # Нажатие на левую кнопку
    def button_ok_clicked(self):
        pass

    # Нажатие на правую кнопку
    @pyqtSlot()
    def button_cancel_clicked(self):
        pass
