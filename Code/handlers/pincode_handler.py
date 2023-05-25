from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from Code.chipher_module.chipher_module import encrypt, decrypt


class PincodeWindow(QObject):
    def __init__(self, server_service):
        QObject.__init__(self)
        self.server_service = server_service

    @pyqtSlot(str)
    def set_pincode(self, pincode):
        print(pincode)
        servers = self.server_service.get_all()
        for s in servers:
            s.user_name = encrypt(s.user_name, pincode)
            s.server_password = decrypt(s.server_password, pincode)
            self.server_service.edit(s)
