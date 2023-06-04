from PyQt6.QtCore import QUrl, pyqtSlot
from PyQt6.QtQml import QQmlApplicationEngine


class MainWindow(QQmlApplicationEngine):
    def __init__(self):
        super().__init__()

    @pyqtSlot('QString')
    def change_server(self, server):
        print('Server = ', server)
        pass

    @pyqtSlot()
    def refresh(self):
        print('REFREEEEEEEEEEEEEEEEEEEEEEEEEESH')

    def show(self):
        super().load(QUrl('QmlWindows/MainWindow.qml'))
