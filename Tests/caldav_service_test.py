from datetime import timedelta
from unittest import TestCase
from caldav import DAVClient, Calendar
from Code.services.caldav_service import CalDavService
from caldav.lib.error import NotFoundError
from Tests.test_helpers import *


class CaldavTests(TestCase):
    login = 'user'
    password = 'user'
    url = 'http://localhost:8080/remote.php/dav'
    calendar_name = 'dav'
    server_name = 'test_server'

    task: Task
    service: CalDavService
    testCalendar: Calendar
    server: Server

    def setUp(self) -> None:
        self.server = Server(user_email=self.login, user_password=self.password,
                             calendar_name=self.calendar_name, server_uri=self.url, server_name=self.server_name)
        with DAVClient(username=self.login, password=self.password, url=self.url) as client:
            for calendar in client.principal().calendars():
                if calendar.name == self.calendar_name:
                    calendar.delete()
        self.task = generate_task(self.server)
        self.service = CalDavService(server=self.server)

    def tearDown(self) -> None:
        self.service.__exit__(None, None, None)

    def test_create_and_get(self) -> None:
        self.service.publish_task(self.task)
        published = self.service.get_task_by_int_uid(self.task.task_id)
        assert published is not None

    def test_delete(self) -> None:
        assert self.service.publish_task(self.task) is None
        assert self.service.delete_task_by_int_id(self.task.task_id)
        with self.assertRaises(NotFoundError):
            self.service.get_event_by_int_id(self.task.task_id)

    def test_update(self) -> None:
        assert self.service.publish_task(self.task) is None
        self.task.dtstart = self.task.dtstart + timedelta(days=1)
        self.task.dtstamp = self.task.dtstamp + timedelta(days=1)
        self.task.due = self.task.due + timedelta(days=1)
        self.task.sync_time = self.task.sync_time + timedelta(days=1)
        self.task.summary = 'new summary'
        self.task.description = 'new description'
        self.task.server_id = '2'
        self.task.parent_id = '2'
        self.task.label = generate_labels(self.server, self.task)
        assert self.service.update_task(self.task) is None
        updated = self.service.get_task_by_int_uid(self.task.task_id)
        assert updated is not None
        assert self.task.summary == updated.summary
        assert self.task.description == updated.description
        assert self.task.server_id == updated.server_id
        assert self.task.parent_id == updated.parent_id
        assert self.task.label.priority_id == updated.label.priority_id
        assert self.task.label.size_id == updated.label.size_id
        assert self.task.label.type_id == updated.label.type_id
        assert self.task.label.status_id == updated.label.status_id
        assert self.task.dtstart == updated.dtstart
        assert self.task.due == updated.due

    def test_get_all(self) -> None:
        assert self.service.publish_task(generate_task(self.server)) is None
        assert self.service.publish_task(generate_task(self.server)) is None
        assert self.service.publish_task(generate_task(self.server)) is None
        assert self.service.publish_task(generate_task(self.server)) is None
        assert len(self.service.get_all_tasks()) == 4
