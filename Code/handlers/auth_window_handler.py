from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QObject, pyqtSlot

from Code.entities.db_entities import Server
from Code.services.caldav_service import CalDavService
from caldav.lib.error import AuthorizationError
from requests.exceptions import MissingSchema


class AuthWindow(QObject):
    def __init__(self, server_service):
        QObject.__init__(self)
        self.server_service = server_service

    errorMessage = pyqtSignal(str, arguments=['message'])
    
    @pyqtSlot()
    def localareaClicked(self):
        pass

    @pyqtSlot(str, str, str, str)
    def authorize_nextcloud_server(self, user_email, user_password, server_uri, calendar_name):
        try:
            s = Server(user_email=user_email,
                       user_password=user_password,
                       server_uri=server_uri,
                       server_name="nextcloud",
                       calendar_name=calendar_name)

            # http://localhost:8080/remote.php/dav
            caldav_service = CalDavService(s)  # check if auth is successful
            self.server_service.add(s)
            # open MainWindow

        except AuthorizationError as e:
            self.errorMessage.emit("Неверный логин или пароль")
        except MissingSchema as e:
            self.errorMessage.emit("Неверный путь")
        except Exception as e:
            self.errorMessage.emit(e.args[0])
       

