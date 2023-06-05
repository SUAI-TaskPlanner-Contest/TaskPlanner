import sys

from PyQt6.QtCore import pyqtProperty, QObject, pyqtSlot, pyqtSignal

from Code.services import Invalid
from Code.entities.db_entities import Server
from Code.chipher_module.chipher_module import encrypt, decrypt


class ItemModel(QObject):
    def __init__(self, server_id, server_name, user_email, calendar_name, server_uri):
        QObject.__init__(self)
        self._server_id = server_id
        self._server_name = server_name
        self._user_email = user_email
        self._calendar_name = calendar_name
        self._server_uri = server_uri

    @pyqtProperty(int)
    def server_id(self):
        return self._server_id

    @pyqtProperty(str)
    def server_name(self):
        return self._server_name

    @pyqtProperty(str)
    def user_email(self):
        return self._user_email

    @pyqtProperty(str)
    def calendar_name(self):
        return self._calendar_name

    @pyqtProperty(str)
    def server_uri(self):
        return self._server_uri


class ListModel(QObject):
    def __init__(self, servers_list):
        QObject.__init__(self)
        self.servers = servers_list

    def add_item(self, server_id, server_name, user_email, calendar_name, server_uri):
        self.servers.append(ItemModel(server_id, server_name, user_email, calendar_name, server_uri))

    def delete_item(self, index):
        self.servers.pop(index)

    @pyqtProperty(list)
    def model(self):
        return self.servers


class SettingsWindow(QObject):
    updateListView = pyqtSignal(ListModel, arguments=['new_model'])

    def __init__(self, server_service):
        QObject.__init__(self)
        self.server_service = server_service
        servers_list_items = []
        servers_list = self.server_service.get_all()

        for server in servers_list:
            servers_list_items.append(ItemModel(server.id,
                                                server.server_name,
                                                server.user_email,
                                                server.calendar_name,
                                                server.server_uri))

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
            s = Server(user_email=user_email,
                       user_password=user_password,
                       server_name=server_name,
                       server_uri=server_uri,
                       calendar_name=calendar_name)

            self.server_service.add(s)
            self._model.add_item(s.id, s.server_name, s.user_email, s.calendar_name, s.server_uri)

            self.updateListView.emit(self._model)

        except Invalid as e:  # дефолтная ошибка с сервиса
            print(e.args[0])
        except Exception as e:
            print(e.args[0])

    @pyqtSlot(int)
    def delete(self, index):
        # нужно вызвать окно предупреждения с ServerDeleteError
        # придумать способ обработки кнопок "ок" и "отмена"
        server_to_delete = self._model.servers[index]
        self.server_service.delete_by_id(server_to_delete.server_id)
        self._model.delete_item(index)
        self.updateListView.emit(self._model)

    @pyqtProperty(list, notify=updateListView)
    def model(self):
        return self._model.model
