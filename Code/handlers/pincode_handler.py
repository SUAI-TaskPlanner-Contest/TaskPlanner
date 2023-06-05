from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from Code.container import container


class PincodeWindow(QObject):
    def __init__(self, server_service):
        QObject.__init__(self)
        self.server_service = server_service

    @pyqtSlot(str)
    def set_pincode(self, pincode):
        container.set('pincode', pincode)
