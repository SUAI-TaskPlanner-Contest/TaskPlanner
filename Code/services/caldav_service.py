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

        def save_task(t: Task):
            self.calendar.save_event(uid=t.id, dtstamp=t.dtstamp, dtstart=t.dtstart, DATE_START=t.dtstart,
                                     DATE_STAMP=t.dtstamp, SUMMARY=t.summary, SIZE_ID=t.label.size_id, 
                                     STATUS_ID=t.label.status_id,  TYPE_ID=t.label.type_id, 
                                     PRIORITY_ID=t.label.priority_id, DATE_DUE=t.due, DUE=t.due,
                                     SERVER_ID=t.server_id, LAST_MOD=t.last_mod, DESCRIPTION=t.description,
                                     PARENT_ID=t.parent_id, CATEGORIES=[t.label.priority.name, t.label.size.name,
                                                                        t.label.status.name, t.label.type.name])

        try:
            existing_task = self.get_task_by_id(task.id)
            assert existing_task.last_mod.tzinfo == timezone.utc
            assert task.sync_time.tzinfo == timezone.utc
            if existing_task.last_mod > task.sync_time:
                return existing_task, task
            if not self.delete_task_by_int_id(task.id):
                raise 'Update Exception'
            task.last_mod = utc_now()
            save_task(task)
            return None
        except NotFoundError:
            save_task(task)
        return None

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
        try:
            response = self.calendar.event_by_uid(uid=str(uid))
            response.delete()
            return True
        except NotFoundError:
            return False

    def get_task_by_id(self, uid: int) -> Task:
        """
            Get Task by int id

            parameters:
                uid: task int id
            returns:
                Task entity
            raise:
                NotFoundError, if task with this id is not exists
        """
        event = self.calendar.event_by_uid(uid=str(uid))
        return self.__task_from_event(event)

    def __task_from_event(self, event: Event) -> Task:
        """
            Convert caldav event to task entity

            parameters:
                event: caldav event
            returns:
                task entity
        """
        def get_value_or_none(e: Event, value: str) -> str | None:
            try:
                return str(e.icalendar_component[value])
            except Exception:
                return None

        def time_from_string(time_string: str) -> datetime:
            return None if time_string is None else datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S.%f%z')

        task = Task(
            server=self.server,
            dtstart=time_from_string(get_value_or_none(event, 'DATE-START')),
            dtstamp=time_from_string(get_value_or_none(event, 'DATE-STAMP')),
            summary=get_value_or_none(event, 'SUMMARY'),
            due=time_from_string(get_value_or_none(event, 'DATE-DUE')),
            last_mod=time_from_string(get_value_or_none(event, 'LAST-MOD')),  # check for build in later
            description=get_value_or_none(event, 'DESCRIPTION'),
            tech_status=0
        )

        label = Label(task=task)
        label.type_id = int(get_value_or_none(event, 'TYPE-ID'))
        label.size_id = int(get_value_or_none(event, 'SIZE-ID'))
        label.status_id = int(get_value_or_none(event, 'STATUS-ID'))
        label.priority_id = int(get_value_or_none(event, 'PRIORITY-ID'))
        task.label = label

        task.id = get_value_or_none(event, 'UID')
        task.server_id = get_value_or_none(event, 'SERVER-ID')
        task.parent_id = get_value_or_none(event, 'PARENT-ID')
        task.sync_time = utc_now()
        return task

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.__exit__(exc_type, exc_value, traceback)
