from PyQt6.QtCore import pyqtSlot, pyqtProperty, pyqtSignal, QObject, QUrl
from Code.entities.db_entities import Server, Task, Label
from Code.container import get_server_service
from Code.container import container
from Code.services import CalDavService
from Code.utils.time_helper import utc_now, local_to_utc0
from datetime import datetime


class ItemModelTasks(QObject):
    def __init__(self, id, server_id, parent_id, server, label, children, dtstamp, dtstart, due, last_mod, summary,
                 description, tech_status, size, type, priority, status):
        QObject.__init__(self)
        self._id = id
        self._server_id = server_id
        self._parent_id = parent_id
        self._server = server
        self._label = label
        self._children = children
        self._dtstamp = dtstamp.strftime('%Y-%m-%d %H:%M:%S')
        self._dtstart = dtstart.strftime('%Y-%m-%d %H:%M:%S')
        self._due = due.strftime('%Y-%m-%d %H:%M:%S')
        self._last_mod = last_mod.strftime('%Y-%m-%d %H:%M:%S')
        self._summary = summary
        self._description = description
        self._tech_status = tech_status
        self._size = size.name
        self._type = type.name
        self._priority = priority.name
        self._status = status.name

    @pyqtProperty(int)
    def id(self):
        return self._id

    @pyqtProperty(int)
    def server_id(self):
        return self._server_id

    @pyqtProperty(int)
    def parent_id(self):
        return self._parent_id

    @pyqtProperty(list)
    def server(self):
        return self._server

    # ItemLabel.name
    @pyqtProperty(str)
    def label(self):
        return self.label.name

    @pyqtProperty(list)
    def children(self):
        return self._children

    @pyqtProperty(str)
    def dtstamp(self):
        return self._dtstamp

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

    @pyqtProperty(int)
    def tech_status(self):
        return self._tech_status

    @pyqtProperty(str)
    def size(self):
        return self._size

    @pyqtProperty(str)
    def type(self):
        return self._type

    @pyqtProperty(str)
    def status(self):
        return self._status

    @pyqtProperty(str)
    def priority(self):
        return self._priority


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

    @pyqtProperty(str)
    def priority_name(self):
        return self._label.priority.name

    @pyqtProperty(str)
    def size_name(self):
        return self._label.size.name

    @pyqtProperty(str)
    def type_name(self):
        return self._label.type.name

    @pyqtProperty(str)
    def status_name(self):
        return self._label.status.name

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
    def __init__(self, client_task: TaskItem, server_task: TaskItem):
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
    def client_size(self):
        return self._client_task.size_name

    @pyqtProperty(str)
    def client_priority(self):
        return self._client_task.priority_name

    @pyqtProperty(str)
    def client_type(self):
        return self._client_task.type_name

    @pyqtProperty(str)
    def client_status(self):
        return self._client_task.status_name

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

    @pyqtProperty(str)
    def server_size(self):
        return self._server_task.size_name

    @pyqtProperty(str)
    def server_priority(self):
        return self._server_task.priority_name

    @pyqtProperty(str)
    def server_type(self):
        return self._server_task.type_name

    @pyqtProperty(str)
    def server_status(self):
        return self._server_task.status_name

    @pyqtProperty(TaskItem)
    def client_task(self):
        return self._client_task

    @pyqtProperty(TaskItem)
    def server_task(self):
        return self._server_task


class ServerItem(QObject):
    nameChanged = pyqtSignal()

    def __init__(self, server: Server):
        QObject.__init__(self)
        self.server = server

    @pyqtProperty("QString", notify=nameChanged)
    def server_name(self):
        return self.server.server_name


class ListModelTasks(QObject):
    def __init__(self, task_list):
        QObject.__init__(self)
        self.tasks = task_list

    def add_item(self, id, server_id, parent_id, server, children,
                 summary, description, dtstart, dtstamp, tech_status, due, label):
        self.tasks.append(ItemModelTasks(
            summary=summary,
            id=id,
            server_id=server_id,
            parent_id=parent_id,
            server=server,
            children=children,
            description=description,
            dtstart=dtstart,
            dtstamp=dtstamp,
            tech_status=tech_status,
            due=due,
            label=label,
            last_mod=utc_now())
        )

    def save_item(self, index, task):
        self.tasks[index].summary = task.summary
        self.tasks[index].description = task.description
        self.tasks[index].dtstart = task.dtstart
        self.tasks[index].dtstamp = task.dtstamp
        self.tasks[index].due = task.due
        self.tasks[index].label = task.label
        self.tasks[index].last_mod = utc_now()

    def delete_item(self, index):
        self.tasks.pop(index)

    @pyqtProperty(list)
    def model(self):
        return self.tasks


class ComboBoxModel(QObject):
    itemChanged = pyqtSignal()
    itemsChanged = pyqtSignal()

    def __init__(self, servers):
        QObject.__init__(self)
        self._servers = servers
        self._server = servers[0]

    @pyqtProperty(ServerItem, notify=itemChanged)
    def server(self):
        return self._server

    @pyqtProperty(list, notify=itemsChanged)
    def servers(self):
        return self._servers


class MainWindow(QObject):
    detectedConflicts = pyqtSignal(ConflictedTasks, arguments=['conflicted_tasks'])
    updateListView = pyqtSignal(ListModelTasks, arguments=['tasks'])

    def __init__(self, task_service, server_service):
        QObject.__init__(self)
        self.conflicted_tasks = []
        self.task_service = task_service
        self.server_service = server_service
        self.result_task = None
        self._servers_combobox_model = ComboBoxModel(list(map(lambda server:
                                                              ServerItem(server),
                                                              self.server_service.get_all())))

        self._tasks_list_model = ListModelTasks(list(map(lambda task:
                                                         TaskItem(task),
                                                         self.task_service.get_all())))

    @pyqtSlot(str, str, datetime, datetime, int)
    def save_item(self, index, id, summary, description, dtstart, due, label):
        # нашли задачу
        task = self.task_service.get_by_id(id)

        # обновили ее поля
        task.summary = summary
        task.description = description
        # Если надо ещё и время выводить, надо стереть .date()
        task.dtstart = local_to_utc0(dtstart.strptime('%Y-%m-%d %H:%M:%S'))
        task.due = local_to_utc0(due.strptime('%Y-%m-%d %H:%M:%S'))
        # task.label.size = ItemSizeLabel
        # task.label.type = ItemTypeLabel
        # task.label.priority = ItemPriorityLabel
        # task.label.status = ItemStatusLabel
        task.last_mod = local_to_utc0(utc_now())

        self.task_service.edit(task)
        self._tasks_list_model.save_item(task)

    @pyqtSlot(str, str, datetime, datetime, str, list, datetime)
    def add_item(self, summary, description, dtstart, dtstamp, tech_status, server, due):
        task = Task(server=server, summary=summary, description=description, dtstamp=dtstamp, dtstart=dtstart,
                    due=due, last_mod=utc_now(), tech_status=tech_status, parent=None)
        self.task_service.add(task)
        self.add_item(task.id, task.server_id, task.parent_id, task.server,
                                                task.label, task.children, task.dtstamp, task.dtstart,
                                                task.due, task.last_mod, task.summary, task.description,
                                                task.tech_status, task.label.size,
                                                task.label.type, task.label.priority, task.label.status)
        self.updateListView.emit(self._model)

    @pyqtSlot(int)
    def delete_item(self, index):
        id_to_delete = self._tasks_list_model.tasks[index].id
        self.task_service.delete_by_id(id_to_delete)
        self._tasks_list_model.delete_item(index)
        self.updateListView.emit(self._model)


    @pyqtSlot(int)
    def change_server(self, index):
        if index != 0:
            container.set('caldav_service', CalDavService(self._servers_combobox_model.servers[index].server))

    # потом еще надо будет послать 4 индекса для лейблов
    @pyqtSlot(int, str, str, str, str)
    def update_result_task(self, id, dtstart, due, summary, description):
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
        tasks_list = self.task_service.get_all()  # tasks_list = self._model.tasks
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

            self.detectedConflicts.emit(qml_conflicted_tasks)

    @pyqtProperty(list)
    def server_combobox_model(self):
        return self._servers_combobox_model.servers

    @pyqtProperty(list)
    def task_list_model(self):
        return self._tasks_list_model.model

    @pyqtProperty(ServerItem)
    def server_combobox_item(self):
        return self._servers_combobox_model.server
