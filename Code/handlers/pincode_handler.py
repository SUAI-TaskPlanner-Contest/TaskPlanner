from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty
from Code.container import container, set_pincode, new_user, old_user


class PincodeWindow(QObject):
    def __init__(self, novice: bool):
        QObject.__init__(self)
        self._novice = novice

    @pyqtSlot(str)
    def set_pincode(self, pincode):
        """
            установка пинкода для нового пользователя
            создание сервисов
        """
        set_pincode(pincode)

    @pyqtSlot(str)
    def check_pincode(self, pincode):
        if container.check_pincode(pincode):
            old_user(pincode)
            self._check_pin = True
        else:
            self._check_pin = False

    @pyqtProperty(bool)
    def novice(self):
        return self._novice

    @pyqtProperty(bool)
    def verify_pin(self):
        return self._check_pin


class ChangePincodeWindow(QObject):
    def __init__(self):
        QObject.__init__(self)

    @pyqtSlot(str, str)
    def set_new_pincode(self, old_pin, new_pin):
        """
            изменение пинкода для пользователя
            обновление сервисов
        """
        if container.check_pincode(old_pin):
            self._check_pin = True
            set_pincode(new_pin)
        else:
            self._check_pin = False

    @pyqtProperty(bool)
    def verify_pin(self):
        return self._check_pin
