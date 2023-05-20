from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot


class AuthWindowHandler(QObject):
    errorTextChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._errorText = " "

    @pyqtProperty(str, notify=errorTextChanged)
    def errorText(self):
        return self._errorText

    @errorText.setter
    def errorText(self, value):
        if self._errorText != value:
            self._errorText = value
            self.errorTextChanged.emit(value)

    @pyqtSlot()
    def localareaClicked(self):
        pass

    @pyqtSlot(str, str, str, str)
    def loginClicked(self, login, password, calendarAddress, serverLink):
        pass
