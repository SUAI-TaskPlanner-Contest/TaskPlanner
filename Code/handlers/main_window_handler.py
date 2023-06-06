from datetime import datetime
from PyQt6.QtCore import pyqtSlot, pyqtProperty, pyqtSignal, QObject, QUrl
from Code.entities.db_entities import Server, Task, Label, Priority, Status, Type, Size
from Code.container import get_server_service
from PyQt6.QtCore import pyqtSlot, pyqtProperty, pyqtSignal, QObject
from Code.entities.db_entities import Server
from Code.container import get_server_service
from Code.container import container, session
from Code.services import CalDavService
from Code.utils.time_helper import utc_now, local_to_utc0
from Code.utils.time_helper import utc_now
from Code.container import container
from Code.services import TaskService, ServerService
from Code.entities.db_entities import Task, Server
from Code.repositories.server_repo import ServerRepository
from Code.repositories.task_repo import TaskRepository


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
        self._dtstamp = dtstamp.strftime('%Y.%m.%d %H:%M')
        self._dtstart = dtstart.strftime('%Y.%m.%d %H:%M')
        self._due = due.strftime('%Y.%m.%d %H:%M')
        self._last_mod = last_mod.strftime('%Y.%m.%d %H:%M')
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
        return self._client_task.dtstart.strftime('%Y.%m.%d %H:%M')

    @pyqtProperty(str)
    def client_due(self):
        return self._client_task.due.strftime('%Y.%m.%d %H:%M')

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
        return self._server_task.dtstart.strftime('%Y.%m.%d %H:%M')

    @pyqtProperty(str)
    def server_due(self):
        return self._server_task.due.strftime('%Y.%m.%d %H:%M')

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

    def add_task(self, task):
        self.tasks.append(ItemModelTasks(
            id=task.id,
            server_id=task.server.id,
            parent_id=task.parent_id,
            server=task.server,
            label=task.label,
            children=task.children,
            dtstamp=task.dtstamp,
            dtstart=task.dtstart,
            due=task.due,
            last_mod=task.last_mod,
            summary=task.summary,
            description=task.description,
            tech_status=task.tech_status,
            size=task.label.size,
            type=task.label.type,
            priority=task.label.priority,
            status=task.label.status,
            # last_mod=utc_now())
        ))

    def save_task(self, index, task):
        self.tasks[index] = ItemModelTasks(id=task.id,
                                           server_id=task.server.id,
                                           parent_id=task.parent_id,
                                           server=task.server,
                                           label=task.label,
                                           children=task.children,
                                           dtstamp=task.dtstamp,
                                           dtstart=task.dtstart,
                                           due=task.due,
                                           last_mod=task.last_mod,
                                           summary=task.summary,
                                           description=task.description,
                                           tech_status=task.tech_status,
                                           size=task.label.size,
                                           type=task.label.type,
                                           priority=task.label.priority,
                                           status=task.label.status,
                                           # last_mod=utc_now())
                                           )
        # self.tasks[index].summary = task.summary
        # self.tasks[index].description = task.description
        # self.tasks[index].dtstart = task.dtstart
        # self.tasks[index].dtstamp = task.dtstamp
        # self.tasks[index].due = task.due
        # self.tasks[index].label = task.label
        # self.tasks[index].last_mod = utc_now()

    def delete_task(self, index):
        self.tasks.pop(index)

    @pyqtProperty(list)
    def model(self):
        return self.tasks


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
        self._item = None

    @pyqtProperty(TaskLabelItemModel, notify=itemChanged)
    def item(self):
        return self._item

    @pyqtProperty(list, notify=itemsChanged)
    def model(self):
        return self._labels


class ComboBoxModel(QObject):
    itemChanged = pyqtSignal()
    itemsChanged = pyqtSignal()

    def __init__(self, servers):
        QObject.__init__(self)
        self._servers = servers
        self._server = None

    @pyqtProperty(ServerItem, notify=itemChanged)
    def server(self):
        return self._server

    @pyqtProperty(list, notify=itemsChanged)
    def servers(self):
        return self._servers


class MainWindow(QObject):
    detectedConflicts = pyqtSignal(ConflictedTasks, arguments=['conflicted_tasks'])
    updateListView = pyqtSignal(ListModelTasks, arguments=['tasks'])

    def __init__(self):
        QObject.__init__(self)
        self._servers_combobox_model = ComboBoxModel([])
        self._priority_model = TaskLabelListModel([])
        self._status_model = TaskLabelListModel([])
        self._type_model = TaskLabelListModel([])
        self._size_model = TaskLabelListModel([])
        self._tasks_list_model = ListModelTasks([])
        self.conflicted_tasks = []
        self.result_task = None

    @pyqtSlot()
    def set_services(self):
        self.conflicted_tasks = []
        self.task_service = container.set('task_service', TaskService(TaskRepository[Task](session)))
        self.server_service = container.set('server_service',
                                            ServerService(ServerRepository[Server](session), container.get('pincode')))
        self.result_task = None

        self._servers_combobox_model = ComboBoxModel(list(map(lambda server:
                                                              ServerItem(server),
                                                              self.server_service.get_all())))

        server_id = self._servers_combobox_model.servers[0].server.id

        types = self.server_service.get_types(server_id)
        sizes = self.server_service.get_sizes(server_id)
        statuses = self.server_service.get_statuses(server_id)
        priorities = self.server_service.get_priorities(server_id)

        self._priority_model = TaskLabelListModel(list(map(lambda priority: TaskLabelItemModel(priority), priorities)))
        self._status_model = TaskLabelListModel(list(map(lambda status: TaskLabelItemModel(status), statuses)))
        self._type_model = TaskLabelListModel(list(map(lambda task_type: TaskLabelItemModel(task_type), types)))
        self._size_model = TaskLabelListModel(list(map(lambda size: TaskLabelItemModel(size), sizes)))

        tasks = self.server_service.get_tasks(server_id)
        self._tasks_list_model = ListModelTasks(list(map(lambda task:
                                                         ItemModelTasks(
                                                             id=task.id,
                                                             server_id=task.server.id,
                                                             parent_id=task.parent_id,
                                                             server=task.server,
                                                             label=task.label,
                                                             children=task.children,
                                                             dtstamp=task.dtstamp,
                                                             dtstart=task.dtstart,
                                                             due=task.due,
                                                             last_mod=task.last_mod,
                                                             summary=task.summary,
                                                             description=task.description,
                                                             tech_status=task.tech_status,
                                                             size=task.label.size,
                                                             type=task.label.type,
                                                             priority=task.label.priority,
                                                             status=task.label.status,
                                                             # last_mod=utc_now())
                                                         ),
                                                         tasks)))

    @pyqtSlot()
    def update_combobox(self):
        servers = get_server_service().get_all()
        if len(servers) != len(self._servers_combobox_model.servers):
            self._servers_combobox_model = ComboBoxModel(list(map(lambda server:
                                                                  ServerItem(server),
                                                                  servers)))

    def global_add(self, server_index, task_id, parent_id, type_index, size_index, priority_index,
                   status_index, summary, description, dtstart, due):

        parent = None

        server_id = self._servers_combobox_model.servers[server_index].server.id
        # server = self.server_service.get_by_id(server_id)

        size = self.size_model[size_index].label
        status = self.status_model[status_index].label
        type = self.type_model[type_index].label
        priority = self.priority_model[priority_index].label

        task = Task(server_id=server_id,
                    summary=summary,
                    description=description,
                    dtstamp=utc_now(),
                    dtstart=local_to_utc0(datetime.strptime(dtstart, '%Y.%m.%d %H:%M')),
                    due=local_to_utc0(datetime.strptime(due, '%Y.%m.%d %H:%M')),
                    last_mod=utc_now(),
                    tech_status=0,
                    parent=parent)

        # TODO : fill labels
        label = Label(task=task,
                      size=size,
                      status=status,
                      type=type,
                      priority=priority)

        task.label = label
        self.task_service.add(task)
        self._tasks_list_model.add_task(task)
        self.updateListView.emit(self._tasks_list_model)

    def local_add(self, server_index, task_id, parent_id, type_index, size_index, priority_index,
                  status_index, summary, description, dtstart, due):
        parent = self.task_service.get_by_id(parent_id)

        server_id = self._servers_combobox_model.servers[server_index].server.id
        server = self.server_service.get_by_id(server_id)

        size = self.size_model[size_index].label
        status = self.status_model[status_index].label
        type = self.type_model[type_index].label
        priority = self.priority_model[priority_index].label

        task = Task(server=server,
                    summary=summary,
                    description=description,
                    dtstamp=utc_now(),
                    dtstart=local_to_utc0(datetime.strptime(dtstart, '%Y.%m.%d %H:%M')),
                    due=local_to_utc0(datetime.strptime(due, '%Y.%m.%d %H:%M')),
                    last_mod=utc_now(),
                    tech_status=0,
                    parent=parent)

        # TODO : fill labels
        label = Label(task=task,
                      size=size,
                      status=status,
                      type=type,
                      priority=priority)

        task.label = label
        self.task_service.add(task)
        self._tasks_list_model.add_task(task)
        self.updateListView.emit(self._tasks_list_model)

    def edit(self, server_index, task_id, parent_id, type_index, size_index, priority_index,
             status_index, summary, description, dtstart, due):

        parent = self.task_service.get_by_id(parent_id)

        task = next(filter(lambda task: task.id == task_id, self._tasks_list_model.tasks))
        task_index = self._tasks_list_model.tasks.index(task)

        server_id = self._servers_combobox_model.servers[server_index].server.id
        server = self.server_service.get_by_id(server_id)

        # TODO : create combobox
        size_id = self.size_model[size_index].label_id
        status_id = self.status_model[status_index].label_id
        type_id = self.type_model[type_index].label_id
        priority_id = self.priority_model[priority_index].label_id

        # обновили ее поля
        task.summary = summary
        task.description = description
        task.dtstart = local_to_utc0(datetime.strptime(dtstart, '%Y.%m.%d %H:%M'))
        task.due = local_to_utc0(datetime.strptime(due, '%Y.%m.%d %H:%M'))
        task.last_mod = utc_now()

        task.label.size_id = size_id
        task.label.status_id = status_id
        task.label.type_id = type_id
        task.label.priority_id = priority_id

        # обновили задачу в БД и изменили модель
        self.task_service.edit(task)
        self._tasks_list_model.save_task(task_index, task)

    @pyqtSlot(int, int, int, int, int, int, int, str, str, str, str)
    def add_task(self, server_index, task_id, parent_id, type_index, size_index, priority_index,
                 status_index, summary, description, dtstart, due):

        if parent_id == -1 and task_id == -1:
            self.global_add(server_index, task_id, parent_id, type_index, size_index, priority_index,
                            status_index, summary, description, dtstart, due)

        if parent_id != -1 and task_id == -1:
            self.local_add(server_index, task_id, parent_id, type_index, size_index, priority_index,
                           status_index, summary, description, dtstart, due)

        if parent_id != -1 and task_id != -1:
            self.edit(server_index, task_id, parent_id, type_index, size_index, priority_index,
                      status_index, summary, description, dtstart, due)

    @pyqtSlot(int)
    def delete_task(self, index):
        id_to_delete = self._tasks_list_model.tasks[index].id
        self.task_service.delete_by_id(id_to_delete)
        self._tasks_list_model.delete_task(index)
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
        result_task.dtstart = local_to_utc0(datetime.strptime(dtstart, '%Y.%m.%d %H:%M'))
        result_task.due = local_to_utc0(datetime.strptime(due, '%Y.%m.%d %H:%M'))
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

    @pyqtProperty(list, notify=updateListView)
    def task_list_model(self):
        return self._tasks_list_model.model

    @pyqtProperty(ServerItem)
    def server_combobox_item(self):
        return self._servers_combobox_model.server

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
