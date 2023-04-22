from typing import Tuple
from caldav import DAVClient, Principal, Calendar, Event
from caldav.lib.error import NotFoundError
from Code.entities.db_entities import Task, Label, Server
from Code.utils.time_helper import *


class CalDavService:
    client: DAVClient
    principal: Principal
    calendar: Calendar
    server: Server

    def __init__(self, server: Server):
        """
            Returns all task from server

            raise: 
                Exception: Unauthorized
        """
        self.server = server
        self.client = DAVClient(url=server.server_uri, username=server.user_email, password=server.user_password)
        self.principal = self.client.principal()
        calendar_not_found = True
        for calendar in self.principal.calendars():
            if calendar.name == server.calendar_name:
                self.calendar = calendar
                calendar_not_found = False
        if calendar_not_found:
            self.calendar = self.principal.make_calendar(name=server.calendar_name)

    def get_all_tasks(self) -> list[Task]:
        """
            Returns all task from server

            returns:
                Task list
            raise:
                Server exception: Unauthorized
        """
        tasks = []
        for event in self.calendar.events():
            task = self.__task_from_event(event)
            task.sync_time = utc_now()
            tasks.append(task)
        return tasks

    def publish_task(self, task: Task) -> Tuple[Task, Task] | None:
        """
            Publish task

            parameters:
                task: task entity
            returns:
                None if publish was successful, or merge conflicted tasks
            raise:
                Update exception, this exception is system and indicates logic problem
                Publish exception: Unauthorized
        """
        assert task.last_mod.tzinfo == timezone.utc
        assert task.sync_time.tzinfo == timezone.utc
        assert task.dtstamp.tzinfo == timezone.utc
        assert task.dtstart.tzinfo == timezone.utc
        try:
            self.get_event_by_id(str(task.task_id))
            self.update_task(task)
        except NotFoundError:
            self.calendar.save_event(
                uid=task.task_id,
                dtstamp=task.dtstamp,
                dtstart=task.dtstart,
                DATE_START=task.dtstart,
                DATE_STAMP=task.dtstamp,
                SUMMARY=task.summary,
                CATEGORIES=[task.label.priority.name, task.label.size.name, task.label.status.name, task.label.type.name],
                STATUS_ID=task.label.status_id,
                TYPE_ID=task.label.type_id,
                SIZE_ID=task.label.size_id,
                PRIORITY_ID=task.label.priority_id,
                DUE=task.due,
                DATE_DUE=task.due,
                SERVER_ID=task.server_id,
                LAST_MOD=task.last_mod,
                DESCRIPTION=task.description,
                PARENT_ID=task.parent_id,
            )

    def update_task(self, task: Task) -> Tuple[Task, Task] | None:
        """
            Updates task with ID

            parameters:
                task: new task data
            returns:
                None if update was successful, or merge conflicted tasks
            raise:
                Update exception, this exception is system and indicates logic problem
                Publish exception: Unauthorized
        """
        existing_task = self.get_task_by_int_uid(task.task_id)
        assert existing_task.last_mod.tzinfo == timezone.utc
        assert task.sync_time.tzinfo == timezone.utc
        if existing_task.last_mod > task.sync_time:
            return existing_task, task
        if not self.delete_task_by_int_id(task.task_id):
            raise 'Update Exception'
        task.last_mod = utc_now()
        self.publish_task(task)

    def delete_task_by_id(self, uid: str) -> bool:
        """
            Delete task by ID

            parameters:
                uid: task string id
            returns:
                True if delete was successful, or false
            raise:
                Delete exception: Unauthorized
        """
        response = self.get_event_by_id(uid)
        if response is not None:
            response.delete()
            return True
        else:
            return False

    def delete_task_by_int_id(self, uid: int) -> bool:
        """
            Delete task by int ID

            parameters:
                uid: task int id
            returns:
                True if delete was successful, or false
            rais
            e:
                Delete exception: Unauthorized
        """
        return self.delete_task_by_id(str(uid))

    def get_task_by_uid(self, uid: str) -> Task:
        """
            Get Task by string id

            parameters:
                uid: task string id
            returns:
                Task entity
            raise:
                NotFoundError, if task with this id is not exists
        """
        event = self.calendar.event_by_uid(uid=uid)
        return self.__task_from_event(event)

    def get_task_by_int_uid(self, uid: int) -> Task:
        """
            Get Task by int id

            parameters:
                uid: task int id
            returns:
                Task entity
            raise:
                NotFoundError, if task with this id is not exists
        """
        return self.get_task_by_uid(str(uid))

    def get_event_by_id(self, uid: str) -> Event:
        """
            Get event by string id

            parameters:
                uid: task string id
            returns:
                Caldav event
            raise:
                NotFoundError, if event with this id is not exists
        """
        return self.calendar.event_by_uid(uid=uid)

    def get_event_by_int_id(self, uid: int) -> Event:
        """
            Get event by int id

            parameters:
                uid: task int id
            returns:
                Caldav event
            raise:
                NotFoundError, if event with this id is not exists
        """
        return self.get_event_by_id(str(uid))

    def __task_from_event(self, event: Event) -> Task:
        """
            Convert caldav event to task entity

            parameters:
                event: caldav event
            returns:
                task entity
        """
        def get_value_or_none(event: Event, value: str) -> str | None:
            try:
                return str(event.icalendar_component[value])
            except Exception:
                return None
        task = Task(
            server=self.server,
            dtstart=self.time_from_string(get_value_or_none(event, 'DATE-START')),
            dtstamp=self.time_from_string(get_value_or_none(event, 'DATE-STAMP')),
            summary=get_value_or_none(event, 'SUMMARY'),
            due=self.time_from_string(get_value_or_none(event, 'DATE-DUE')),
            last_mod=self.time_from_string(get_value_or_none(event, 'LAST-MOD')),  # check for build in later
            description=get_value_or_none(event, 'DESCRIPTION'),
            tech_status=0
        )

        label = Label(task=task)
        label.type_id = int(get_value_or_none(event, 'TYPE-ID'))
        label.size_id = int(get_value_or_none(event, 'SIZE-ID'))
        label.status_id = int(get_value_or_none(event, 'STATUS-ID'))
        label.priority_id = int(get_value_or_none(event, 'PRIORITY-ID'))
        task.label = label

        task.task_id = get_value_or_none(event, 'UID')
        task.server_id = get_value_or_none(event, 'SERVER-ID')
        task.parent_id = get_value_or_none(event, 'PARENT-ID')
        task.sync_time = utc_now()
        return task

    @staticmethod
    def time_from_string(time_string: str) -> datetime:
        return None if time_string is None else datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S.%f%z')

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.__exit__(exc_type, exc_value, traceback)
