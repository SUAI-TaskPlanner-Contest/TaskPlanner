import sys

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty
from Code.entities.db_entities import Server
from Code.services.server_service import ServerService


class ItemModel(QObject):
    def __init__(self, value1, value2):
        QObject.__init__(self)
        self.server_name = value1
        self.server_login = value2

    @pyqtProperty(str)
    def server_name(self):
        return self.server_name

    @pyqtProperty(str)
    def server_login(self):
        return self.server_login


class ListModel(QObject):
    def __init__(self, servers_list):
        QObject.__init__(self)
        self.list_of_items = servers_list
        #Необхадимо вызвать дешефратор при чтении из бд

    def add_item(self, value1, value2):
        item = ItemModel(value1, value2)
        print(value1, value2)
        self.list_of_items.append(item)

    @pyqtProperty("QVariantList", constant=True)
    def model(self):
        return self.list_of_items


class SettingWindowClass(QObject):
    def __init__(self):
        QObject.__init__(self, server_service)
        server_service.get_all()
        self._model = ListModel()
        self.server_service = server_service

    @pyqtSlot(str, str)
    def save_pincode(self, oldpin, newpin):
        print(oldpin, newpin)

    @pyqtSlot(str, str, str, str, str)
    def save_server(self, user_email, user_password, server_name, calendar_name, server_uri):
        try:
            # считать переменную pincode текущей сессии
            # user_email = encrypt(user_email, pincode)
            # user_password = encrypt(user_email, pincode)

            s = Server(user_email=user_email,
                       user_password=user_password,
                       server_name=server_name,
                       server_uri=server_uri,
                       calendar_name=calendar_name)

            print(s)

            # caldav_service = CalDavService(s)  # check if auth is successful
            self.server_service.add(s)

            self._model.add_item(server_name, user_email)

        except Invalid as e:  # дефолтная ошибка с сервиса
            print(e.args[0])
        except Exception as e:
            pass

    def test_items1(self):
        self._model.add_item("Nextcloud", "1")

    def test_items2(self):
        self._model.add_item("Google", "2")

    @pyqtProperty("QVariantList", constant=True)
    def model(self):
        return self._model.model
