from datetime import datetime, timedelta

from PyQt6.QtCore import QUrl, pyqtSlot, QObject, pyqtSignal, pyqtProperty
from PyQt6.QtQml import QQmlApplicationEngine

import threading
from Code.container import container
from Code.entities.db_entities import Task
from Code.services import CalDavService
from Code.utils.time_helper import local_to_utc0, utc_now


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


class MainWindow(QObject):
    detectedConflicts = pyqtSignal(ConflictedTasks, arguments=['conflicted_tasks'])

    def __init__(self, task_service, server_service):
        QObject.__init__(self)
        self.conflicted_tasks = []
        self.task_service = task_service
        self.server_service = server_service
        self.result_task = None

    # @pyqtSlot(index)
    # def set_caldav_service(self, index):
        # считали из модели комбобокса по индексу
        # server = ...
        # container.set('caldav_service', CalDavService(server))
        # pass

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

            qml_conflicted_tasks = ConflictedTasks \
                    (
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

            qml_conflicted_tasks = ConflictedTasks \
                    (
                        TaskItem(conflicted_task[0]),
                        TaskItem(conflicted_task[1])
                    )

            # print(qml_conflicted_tasks.client_task)

            self.detectedConflicts.emit(qml_conflicted_tasks)
