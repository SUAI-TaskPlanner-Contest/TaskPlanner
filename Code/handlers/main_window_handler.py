from PyQt6.QtCore import QUrl, pyqtSlot, QObject, pyqtSignal
from PyQt6.QtQml import QQmlApplicationEngine

from Code.container import container
from Code.services import CalDavService


class MainWindow(QObject):
    detectedConflicts = pyqtSignal(list, arguments=['conficted_tasks'])

    def __init__(self, task_service, server_service):
        QObject.__init__(self)
        self.task_service = task_service
        self.server_service = server_service
        # self.caldav_service = caldav_service
        tasks_list_items = []
        tasks_list = self.task_service.get_all()

    @pyqtSlot()
    async def sync_tasks(self):
        # tasks_list = self._model.tasks
        tasks_list = self.task_service.get_all()
        conficted_tasks = []

        server = self.server_service.get_by_id(1)

        container.set('caldav_service', CalDavService(server))
        caldav_service = container.get('caldav_service')

        for task in tasks_list:
            conficted_tasks.append(caldav_service.publish_tasks(task))
        while len(conficted_tasks) > 0:
            for i in range(len(conficted_tasks)):

                @pyqtSlot(str)
                def get_result_task(id, summary):
                    return summary

                # по этому сигналу нужно открыть окно Merge
                # слева все значения заполнить conficted_tasks[0], справа conficted_tasks[1], в центре вывести conficted_tasks[0]
                # result_task (на основании нажатой кнопки решения конфликта)
                result_task = await self.detectedConflicts.emit(conficted_tasks)
                if caldav_service.publish_tasks(result_task) == None:
                    conficted_tasks.pop(i)

