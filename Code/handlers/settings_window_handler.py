import sys

from PyQt6.QtCore import pyqtProperty, QObject, pyqtSlot, pyqtSignal

from Code.services import Invalid
from Code.entities.db_entities import Server
from Code.chipher_module.chipher_module import encrypt, decrypt


class ItemModel(QObject):
    def __init__(self, server_name, user_email):
        QObject.__init__(self)
        self._text_value = server_name
        self._text_value2 = user_email

    @pyqtProperty(str)
    def text_value(self):
        return self._text_value

    @pyqtProperty(str)
    def text_value2(self):
        return self._text_value2


class ListModel(QObject):
    def __init__(self, servers_list):
        QObject.__init__(self)
        self.list_of_items = servers_list

    def add_item(self, server_name, user_email):
        self.list_of_items.append(ItemModel(server_name, user_email))

    @pyqtProperty(list, constant=True)
    def model(self):
        return self.list_of_items


class SettingsWindow(QObject):
    updateListView = pyqtSignal(list, arguments=['new_model'])

    def __init__(self, server_service):
        QObject.__init__(self)
        self.server_service = server_service
        servers_list_items = []
        servers_list = self.server_service.get_all()

        for server in servers_list:
            servers_list_items.append(ItemModel(server.server_name, server.user_email))

        self._model = ListModel(servers_list_items)

    @pyqtSlot(str, str)
    def save_pincode(self, oldpin, newpin):
        servers_list = self.server_service.get_all()

        for server in servers_list:
            server.user_email = encrypt(decrypt(server.user_email, oldpin), newpin)
            server.user_password = encrypt(decrypt(server.user_password, oldpin), newpin)
            self.server_service.edit(server)

    @pyqtSlot(str, str, str, str, str)
    def save_server(self, user_email, user_password, server_name, calendar_name, server_uri):
        try:
            pincode = "djgf"  # заглушка, считать откуда-то текущий пин

            # s = Server(user_email=user_email,
            #            user_password=user_password,
            #            server_name=server_name,
            #            server_uri=server_uri,
            #            calendar_name=calendar_name)

            s = Server(user_email="astronik00@gmail.com",
                       user_password="qwerty",
                       server_name="google",
                       server_uri="http://localhost:8080/dav",
                       calendar_name="test")

            print(s)

            # caldav_service = CalDavService(s)  # check if auth is successful
            self.server_service.add(s)
            self._model.add_item(s.server_name, s.user_email)

            self.updateListView.emit(self._model.list_of_items)


        except Invalid as e:  # дефолтная ошибка с сервиса
            print(e.args[0])
        except Exception as e:
            print(e.args[0])

    @pyqtProperty(list, constant=True, notify=updateListView)
    def model(self):
        return self._model.model
