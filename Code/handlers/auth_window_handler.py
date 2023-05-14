from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QObject, QUrl, pyqtSlot
from PyQt6.QtQuick import QQuickView

from Code.entities.db_entities import Server
from Code.services.caldav_service import CalDavService
from caldav.lib.error import AuthorizationError
from requests.exceptions import MissingSchema
from Code.handlers.main_window_handler import MainWindow
from PyQt6.QtQml import QQmlApplicationEngine


class AuthWindowHandler(QQmlApplicationEngine):
    def __init__(self):
        QQmlApplicationEngine.__init__(self)
        self.rootContext().setContextProperty("auth_handler", self)
        self.main_window = None
        self.isAuthIsWorking = False

    errorMessage = pyqtSignal(str, arguments=['message'])

    closeWindow = pyqtSignal()

    @pyqtSlot(str, str, str, str)
    def authorize_nextcloud_server(self, user_email, user_password, server_uri, calendar_name):
        if self.isAuthIsWorking:
            return
        try:
            self.isAuthIsWorking = True
            s = Server(user_email=user_email,
                       user_password=user_password,
                       server_uri=server_uri,
                       server_name="nextcloud",
                       calendar_name=calendar_name)

            # http://localhost:8080/remote.php/dav
            CalDavService(s)

            self.main_window = MainWindow()
            self.main_window.show()
            self.close()

        except AuthorizationError as e:
            self.errorMessage.emit("Неверный логин или пароль")
        except MissingSchema as e:
            self.errorMessage.emit("Неверный путь")
        except Exception as e:
            self.errorMessage.emit(e.args[0])

    def show(self):
        super().load('QmlWindows/AuthWindow.qml')

    def close(self):
        self.closeWindow.emit()
