from datetime import datetime

from PyQt6.QtCore import QUrl, pyqtSlot, QObject, pyqtSignal, pyqtProperty
from PyQt6.QtQml import QQmlApplicationEngine

import threading
from Code.container import container
from Code.entities.db_entities import Task
from Code.services import CalDavService
from Code.utils.time_helper import local_to_utc0


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

    @pyqtProperty(datetime)
    def dtstart(self):
        return self._dtstart

    @pyqtProperty(datetime)
    def due(self):
        return self._due

    @pyqtProperty(datetime)
    def last_mod(self):
        return self._last_mod

    @pyqtProperty(str)
    def summary(self):
        return self._summary

    @pyqtProperty(str)
    def description(self):
        return self._description


class MainWindow(QObject):
    detectedConflicts = pyqtSignal(list, arguments=['conflicted_tasks'])

    def __init__(self, task_service, server_service):
        QObject.__init__(self)
        self.condition = threading.Condition(lock=None)
        self.task_service = task_service
        self.server_service = server_service
        self.result_task = None
        # self.caldav_service = caldav_service
        tasks_list_items = []
        tasks_list = self.task_service.get_all()


    # @pyqtSlot(index)
    # def set_caldav_service(self, index):
        # считали из модели комбобокса по индексу
        # server = ...
        # container.set('caldav_service', CalDavService(server))
        # pass

    @pyqtSlot(int, str, str)
    def update_result_task(self, id, summary, dtstart):
        self.result_task = Task(
            server=self.server_service.get_by_id(1),
            dtstamp=local_to_utc0(datetime.datetime.now()),
            dtstart=local_to_utc0(datetime.datetime.now()),
            due=local_to_utc0(datetime.datetime.now() + datetime.timedelta(days=5)),
            last_mod=local_to_utc0(datetime.datetime.now()),
            summary='Пример задачи',
            description='Для создания новых задач нажмите на +',
            tech_status=0,
            parent=None)
        self.condition.notify()


    @pyqtSlot()
    def sync_tasks(self):
        # tasks_list = self._model.tasks
        tasks_list = self.task_service.get_all()
        conflicted_tasks = []

        server = self.server_service.get_by_id(1)

        container.set('caldav_service', CalDavService(server))
        caldav_service = container.get('caldav_service')

        for task in tasks_list:
            server_task = caldav_service.publish_task(task)[0]
            client_task = caldav_service.publish_task(task)[1]
            conflicted_tasks.append([TaskItem(client_task), TaskItem(server_task)])

        while len(conflicted_tasks) > 0:
            for i in range(len(conflicted_tasks)):
                self.result_task = None
                self.detectedConflicts.emit(conflicted_tasks[i])

                with self.condition:
                    while self.result_task is None:
                        self.condition.wait()

                if caldav_service.publish_task(self.result_task) is None:
                    conflicted_tasks.pop(i)
