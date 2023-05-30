from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot


class WarningWindowHandler(QObject):
    name_changed = pyqtSignal()
    text_changed = pyqtSignal()
    button_ok_changed = pyqtSignal()
    button_cancel_changed = pyqtSignal()

    def __init__(self, _name: str, _text: str, _button_ok: str, _button_cancel: str) -> None:
        super().__init__()
        self._name = _name
        self._text = _text
        self._button_ok = _button_ok
        self._button_cancel = _button_cancel

    @pyqtProperty(str, notify=name_changed)
    def name(self):
        return self._name

    @pyqtProperty(str, notify=text_changed)
    def text(self):
        return self._text

    @pyqtProperty(str, notify=button_ok_changed)
    def button_ok(self):
        return self._button_ok

    @pyqtProperty(str, notify=button_cancel_changed)
    def button_cancel(self):
        return self._button_cancel

    @name.setter
    def name(self, value):
        self._name = value
        self.name_changed.emit()

    @text.setter
    def text(self, value):
        self._text = value
        self.text_changed.emit()

    @button_ok.setter
    def button_ok(self, value):
        self._button_ok = value
        self.button_ok_changed.emit()

    @button_cancel.setter
    def button_cancel(self, value):
        self._button_cancel = value
        self.button_cancel_changed.emit()


class WarningButtonHandler(QObject):
    @pyqtSlot()
    def button_ok_clicked(self):
        pass

    @pyqtSlot()
    def button_cancel_clicked(self):
        pass
