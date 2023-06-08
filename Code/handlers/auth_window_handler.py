from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QObject, QUrl, pyqtSlot
from PyQt6.QtQuick import QQuickView

from Code.entities.db_entities import Server
from Code.services.caldav_service import CalDavService
from caldav.lib.error import AuthorizationError
from requests.exceptions import MissingSchema
from Code.handlers.main_window_handler import MainWindow
from PyQt6.QtQml import QQmlApplicationEngine
from Code.container import container


class AuthWindow(QObject):
    def __init__(self):
        QObject.__init__(self)

    errorMessage = pyqtSignal(str, arguments=['message'])
    successAuth = pyqtSignal(int, arguments=['number'])

    @pyqtSlot(str, str, str, str)
    def authorize_nextcloud_server(self, user_email, user_password, server_uri, calendar_name):
        try:
            s = Server(user_email=user_email,
                       user_password=user_password,
                       server_uri=server_uri,
                       server_name="nextcloud",
                       calendar_name=calendar_name)

            # http://localhost:8080/remote.php/dav
            caldav_service = CalDavService(s)
            container.set('caldav_service', caldav_service)
            caldav_service.__exit__(None, None, None)

            self.server_service = container.get('server_service')
            self.server_service.add(s)

            self.successAuth.emit(len(self.server_service.get_all()))

        except AuthorizationError as e:
            self.errorMessage.emit("Неверный логин или пароль")
        except MissingSchema as e:
            self.errorMessage.emit("Неверный путь")
        except Exception as e:
            self.errorMessage.emit(e.args[0])
