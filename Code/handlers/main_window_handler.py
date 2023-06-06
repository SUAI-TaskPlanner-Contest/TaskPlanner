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
        self._task = task

    @pyqtProperty(str)
    def priority_name(self):
        return self._task.label.priority.name

    @pyqtProperty(str)
    def size_name(self):
        return self._task.label.size.name

    @pyqtProperty(str)
    def type_name(self):
        return self._task.label.type.name

    @pyqtProperty(str)
    def status_name(self):
        return self._task.label.status.name

    @pyqtProperty(int)
    def id(self):
        return self._task.id

    @pyqtProperty(int)
    def server_id(self):
        return self._task.server_id

    @pyqtProperty(int)
    def parent_id(self):
        return self._task.parent_id

    @pyqtProperty(str)
    def dtstart(self):
        return self._task.dtstart

    @pyqtProperty(str)
    def due(self):
        return self._task.due

    @pyqtProperty(str)
    def last_mod(self):
        return self._task.last_mod

    @pyqtProperty(str)
    def summary(self):
        return self._task.summary

    @pyqtProperty(str)
    def description(self):
        return self._task.description


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

    @pyqtProperty(str)
    def server_name(self):
        return self.server.server_name


class ListModelTasks(QObject):
    def __init__(self, task_list):
        QObject.__init__(self)
        self.tasks = task_list

    def add_item(self, task):
        self.tasks.append(ItemModelTasks(
            summary=task.summary,
            id=task.id,
            server_id=task.server_id,
            parent_id=task.parent_id,
            server=task.server,
            children=task.children,
            description=task.description,
            dtstart=task.dtstart,
            dtstamp=task.dtstamp,
            tech_status=task.tech_status,
            due=task.due,
            label=task.label,
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
                                                              get_server_service().get_all())))

        # TODO : tasks should load by current server
        self._tasks_list_model = ListModelTasks(list(map(lambda task:
                                                         TaskItem(task),
                                                         self.task_service.get_all())))

    @pyqtSlot()
    def update_combobox(self):
        servers = get_server_service().get_all()
        if len(servers) != len(self._servers_combobox_model.servers):
            self._servers_combobox_model = ComboBoxModel(list(map(lambda server:
                                                                  ServerItem(server),
                                                                  servers)))

    @pyqtSlot(int, int, int, int, int, str, str, str, str)
    def edit_task(self, task_index, size_index, status_index, type_index,
                  priority_index, summary, description, dtstart, due):
        # нашли задачу
        task = self.task_service.get_by_id(self._tasks_list_model.tasks[task_index].id)

        # достали id выбранных лейблов
        # TODO : create combobox
        size_id = 0 #self._size_combobox_model.sizes[size_index].size.id
        status_id = 0 #self._status_combobox_model.statuses[status_index].status.id
        type_id = 0 #self._type_combobox_model.types[type_index].type.id
        priority_id = 0 #self._priority_combobox_model.priorities[priority_index].priority.id

        # обновили ее поля
        task.summary = summary
        task.description = description
        task.dtstart = local_to_utc0(dtstart.strptime('%Y-%m-%d %H:%M:%S'))
        task.due = local_to_utc0(due.strptime('%Y-%m-%d %H:%M:%S'))
        task.label.size_id = size_id
        task.label.status_id = status_id
        task.label.type_id = type_id
        task.label.priority_id = priority_id
        task.last_mod = utc_now()

        # обновили задачу в БД и изменили модель
        self.task_service.edit(task)
        self._tasks_list_model.save_item(task_index, task)

    @pyqtSlot(int, int, int, int, int, int, str, str, str, str)
    def add_task(self, server_index, parent_index, size_index, status_index, type_index,
                 priority_index, summary, description, dtstart, due):

        if parent_index == -1:
            parent = None
        else:
            parent = self.task_service.get_by_id(self._tasks_list_model.tasks[parent_index].id)

        server_id = self._servers_combobox_model.servers[server_index].server.id

        # TODO : create combobox
        size_id = 0 #self._size_combobox_model.sizes[size_index].size.id
        status_id = 0 #self._status_combobox_model.statuses[status_index].status.id
        type_id = 0 #self._type_combobox_model.types[type_index].type.id
        priority_id = 0 #self._priority_combobox_model.priorities[priority_index].priority.id

        # TODO: fix everythere data format to Y.m.d H: M
        task = Task(server_id=server_id,
                    summary=summary,
                    description=description,
                    dtstamp=utc_now(),
                    dtstart=local_to_utc0(dtstart.strptime('%Y.%m.%d %H:%M')),
                    due=local_to_utc0(due.strptime('%Y-%m-%d %H:%M:%S')),
                    last_mod=utc_now(),
                    tech_status=0,
                    parent=parent)

        # TODO : fill labels
        # task.label.size_id = size_id
        # task.label.status_id = status_id
        # task.label.type_id = type_id
        # task.label.priority_id = priority_id

        self.task_service.add(task)
        self.add_task(task)
        self.updateListView.emit(self._tasks_list_model)

    @pyqtSlot(int)
    def delete_task(self, index):
        id_to_delete = self._tasks_list_model.tasks[index].id
        self.task_service.delete_by_id(id_to_delete)
        self._tasks_list_model.delete_item(index)
        self.updateListView.emit(self._tasks_list_model)

    # TODO : change tasks model also in QML by this slot
    @pyqtSlot(int)
    def change_server(self, index):
        server = self._servers_combobox_model.servers[index].server
        if index != 0:
            container.set('caldav_service', CalDavService(server))
        self._tasks_list_model.tasks = self.task_service.get_all_by_server_id(server.id)

    def resolve_conflict(self, result_task):
        caldav_service = container.get('caldav_service')

        if caldav_service.publish_task(result_task) is None:
            self.conflicted_tasks.pop(-1)
            self.task_service.edit(result_task)

        if len(self.conflicted_tasks) > 0:
            conflicted_task = self.conflicted_tasks[-1]
            self.detectedConflicts.emit(ConflictedTasks(conflicted_task[0], conflicted_task[1]))

    @pyqtSlot()
    def accept_server(self):
        self.resolve_conflict(self.conflicted_tasks[-1][1].task)

    @pyqtSlot()
    def accept_client(self):
        self.conflicted_tasks[-1][0].task.sync_time = utc_now()
        self.conflicted_tasks[-1][0].task.last_mod = utc_now()
        self.resolve_conflict(self.conflicted_tasks[-1][0].task)

    @pyqtSlot(int, str, str, str, str)
    def merge_tasks(self, id, dtstart, due, summary, description,
                    size_item, status_item, type_item, priority_item):
        # size_id = size_item.
        result_task = self.task_service.get_by_id(id)
        result_task.summary = summary
        result_task.dtstart = dtstart.strftime('%Y-%m-%d %H:%M:%S')
        result_task.due = due.strftime('%Y-%m-%d %H:%M:%S')
        result_task.description = description
        result_task.last_mod = utc_now()
        result_task.sync_time = utc_now()
        # self.result_task.label
        self.resolve_conflict(result_task)

    @pyqtSlot()
    def sync_tasks(self):
        tasks_list = self.task_service.get_all()  # tasks_list = self._model.tasks
        caldav_service = container.get('caldav_service')

        for task in tasks_list:
            result = caldav_service.publish_task(task)
            if result is not None:
                server_task = result[0]
                client_task = result[1]
                self.conflicted_tasks.append([TaskItem(client_task), TaskItem(server_task)])

        if len(self.conflicted_tasks) > 0:
            conflicted_task = self.conflicted_tasks[-1]
            self.detectedConflicts.emit(conflicted_task[0], conflicted_task[1])

    @pyqtProperty(list)
    def server_combobox_model(self):
        return self._servers_combobox_model.servers

    @pyqtProperty(list)
    def task_list_model(self):
        return self._tasks_list_model.model

    @pyqtProperty(ServerItem)
    def server_combobox_item(self):
        return self._servers_combobox_model.server
