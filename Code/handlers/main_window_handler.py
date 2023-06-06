from PyQt6.QtCore import pyqtSlot, pyqtProperty, pyqtSignal, QObject
from Code.entities.db_entities import Server, Priority, Status, Size, Type
from Code.container import get_server_service
from Code.container import container
from Code.services import CalDavService
from Code.utils.time_helper import utc_now


class TaskItem(QObject):
    def __init__(self, task):
        QObject.__init__(self)
        self._id = task.id
        self._server_id = task.server_id
        self._parent_id = task.parent_id
        self._server = task.server
        self._label = task.label
        self._children = task.children
        self._dtstamp = task.dtstamp
        self._dtstart = task.dtstart
        self._due = task.due
        self._last_mod = task.last_mod
        self._summary = task.summary
        self._description = task.description
        self._tech_status = task.tech_status

    @pyqtProperty(int)
    def id(self):
        return self._id

    @pyqtProperty(int)
    def server_id(self):
        return self._server_id

    @pyqtProperty(int)
    def parent_id(self):
        return self._parent_id

    @pyqtProperty(str)
    def dtstart(self):
        return self._dtstart

    @pyqtProperty(str)
    def due(self):
        return self._due

    @pyqtProperty(str)
    def last_mod(self):
        return self._last_mod

    @pyqtProperty(str)
    def summary(self):
        return self._summary

    @pyqtProperty(str)
    def description(self):
        return self._description


class ConflictedTasks(QObject):
    def __init__(self, client_task, server_task):
        QObject.__init__(self)
        self._client_task = client_task
        self._server_task = server_task

    @pyqtProperty(int)
    def client_id(self):
        return self._client_task.id

    @pyqtProperty(TaskItem)
    def client_task(self):
        return self._client_task

    @pyqtProperty(str)
    def client_dtstart(self):
        return self._client_task.dtstart.strftime('%Y-%m-%d %H:%M:%S')

    @pyqtProperty(str)
    def client_due(self):
        return self._client_task.due.strftime('%Y-%m-%d %H:%M:%S')

    @pyqtProperty(str)
    def client_summary(self):
        return self._client_task.summary

    @pyqtProperty(str)
    def client_description(self):
        return self._client_task.description

    @pyqtProperty(int)
    def server_id(self):
        return self._server_task.id

    @pyqtProperty(str)
    def server_dtstart(self):
        return self._server_task.dtstart.strftime('%Y-%m-%d %H:%M:%S')

    @pyqtProperty(str)
    def server_due(self):
        return self._server_task.due.strftime('%Y-%m-%d %H:%M:%S')

    @pyqtProperty(str)
    def server_summary(self):
        return self._server_task.summary

    @pyqtProperty(str)
    def server_description(self):
        return self._server_task.description


    @pyqtProperty(TaskItem)
    def client_task(self):
        return self._client_task

    @pyqtProperty(TaskItem)
    def server_task(self):
        return self._server_task


class ItemModel(QObject):
    nameChanged = pyqtSignal()

    def __init__(self, server: Server):
        QObject.__init__(self)
        self.server = server

    @pyqtProperty("QString", notify=nameChanged)
    def server_name(self):
        return self.server.server_name


class ListModel(QObject):
    itemChanged = pyqtSignal()
    itemsChanged = pyqtSignal()

    def __init__(self, servers):
        QObject.__init__(self)
        self._servers = servers
        self._item = servers[0]
        # container.set('caldav_service', CalDavService(self._item.server))

    @pyqtProperty(ItemModel, notify=itemChanged)
    def item(self):
        return self._item

    @pyqtProperty(list, notify=itemsChanged)
    def model(self):
        return self._servers


class TaskLabelItemModel(QObject):
    nameChanged = pyqtSignal()
    idChanged = pyqtSignal()

    def __init__(self, label: Priority | Status | Type | Size):
        QObject.__init__(self)
        self.label = label

    @pyqtProperty("QString", notify=nameChanged)
    def label_text(self):
        return self.label.name

    @pyqtProperty(int, notify=idChanged)
    def label_id(self):
        return self.label.id


class TaskLabelListModel(QObject):
    itemChanged = pyqtSignal()
    itemsChanged = pyqtSignal()

    def __init__(self, labels):
        QObject.__init__(self)
        self._labels = labels
        self._item = labels[0]

    @pyqtProperty(TaskLabelItemModel, notify=itemChanged)
    def item(self):
        return self._item

    @pyqtProperty(list, notify=itemsChanged)
    def model(self):
        return self._labels


class MainWindow(QObject):
    detectedConflicts = pyqtSignal(ConflictedTasks, arguments=['conflicted_tasks'])

    def __init__(self, task_service, server_service):
        QObject.__init__(self)
        self.conflicted_tasks = []
        self.task_service = task_service
        self.server_service = server_service
        self.result_task = None
        self._model = ListModel(list(map(lambda server: ItemModel(server), get_server_service().get_all())))
        server_id = self._model.item.server.id
        self._priority_model = TaskLabelListModel(list(map(lambda priority: TaskLabelItemModel(priority), get_server_service().get_priorities(server_id))))
        self._status_model = TaskLabelListModel(list(map(lambda status: TaskLabelItemModel(status), get_server_service().get_statuses(server_id))))
        self._type_model = TaskLabelListModel(list(map(lambda task_type: TaskLabelItemModel(task_type), get_server_service().get_types(server_id))))
        self._size_model = TaskLabelListModel(list(map(lambda size: TaskLabelItemModel(size), get_server_service().get_sizes(server_id))))

    @pyqtSlot(int)
    def change_server(self, index):
        if index != 0:
            container.set('caldav_service', CalDavService(self._model.model[index].server))
        # main window reload logic

    @pyqtSlot(int, str, str)
    def update_result_task(self, id, summary, description):
        caldav_service = container.get('caldav_service')

        # нашли задачу
        self.result_task = self.task_service.get_by_id(id)

        # обновили ее
        self.result_task.summary = summary
        self.result_task.description = description
        self.result_task.last_mod = utc_now()
        self.result_task.sync_time = utc_now()

        # self.result_task = self.task_service.get_by_id(id)

        if caldav_service.publish_task(self.result_task) is None:
            self.conflicted_tasks.pop(-1)
            self.task_service.edit(self.result_task)

        if len(self.conflicted_tasks) > 0:
            conflicted_task = self.conflicted_tasks[-1]

            qml_conflicted_tasks = ConflictedTasks(
                TaskItem(conflicted_task[0]),
                TaskItem(conflicted_task[1])
            )

            # print(qml_conflicted_tasks.client_task)

            self.detectedConflicts.emit(qml_conflicted_tasks)

    @pyqtSlot()
    def sync_tasks(self):
        # tasks_list = self._model.tasks
        tasks_list = self.task_service.get_all()

        server = self.server_service.get_by_id(1)

        container.set('caldav_service', CalDavService(server))
        caldav_service = container.get('caldav_service')

        for task in tasks_list:
            result = caldav_service.publish_task(task)
            if result is not None:
                server_task = result[0]
                client_task = result[1]
                self.conflicted_tasks.append([client_task, server_task])

        if len(self.conflicted_tasks) > 0:
            conflicted_task = self.conflicted_tasks[-1]

            qml_conflicted_tasks = ConflictedTasks(
                TaskItem(conflicted_task[0]),
                TaskItem(conflicted_task[1])
            )

            # print(qml_conflicted_tasks.client_task)

            self.detectedConflicts.emit(qml_conflicted_tasks)

    @pyqtProperty(list)
    def model(self):
        return self._model.model

    @pyqtProperty(ItemModel)
    def item(self):
        return self._model.item

    @pyqtProperty(list)
    def priority_model(self):
        return self._priority_model.model

    @pyqtProperty(TaskLabelItemModel)
    def priority_item(self):
        return self._priority_model.item

    @pyqtProperty(list)
    def status_model(self):
        return self._status_model.model

    @pyqtProperty(TaskLabelItemModel)
    def status_item(self):
        return self._status_model.item

    @pyqtProperty(list)
    def type_model(self):
        return self._type_model.model

    @pyqtProperty(TaskLabelItemModel)
    def type_item(self):
        return self._type_model.item

    @pyqtProperty(list)
    def size_model(self):
        return self._size_model.model

    @pyqtProperty(TaskLabelItemModel)
    def size_item(self):
        return self._size_model.item
