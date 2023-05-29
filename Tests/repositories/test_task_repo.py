import unittest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Code.repositories.task_repo import TaskRepository
from Code.utils.time_helper import utc0_to_local, local_to_utc0
from Code.repositories.server_repo import ServerRepository
from Code.entities.db_entities import Server, Task, Label, Priority, Size, Type, Status, Base


engine = create_engine('sqlite:///test.db', echo=False)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()

server_repo = ServerRepository[Server](session)
task_repo = TaskRepository[Task](session)


def generate_server_labels(s: Server) -> Server:
    priority1_test = Priority(server=s, name="Низкий")
    priority2_test = Priority(server=s, name="Средний")
    priority3_test = Priority(server=s, name="Высокий")

    size1_test = Size(server=s, name="Маленький")
    size2_test = Size(server=s, name="Средний")
    size3_test = Size(server=s, name="Большой")

    type1_test = Type(server=s, name="Разработка")
    type2_test = Type(server=s, name="Исследование")
    type3_test = Type(server=s, name="Баг")
    type4_test = Type(server=s, name="UI")

    status1_test = Status(server=s, name="Нет исполнителя")
    status2_test = Status(server=s, name="Нужна помощь")
    status3_test = Status(server=s, name="Выполняется")
    status4_test = Status(server=s, name="Дополняется")

    return s


def generate_data():
    s1_test = Server(user_email="astronik00@gmail.com",
                     user_password="qwerty",
                     server_name="nextcloud",
                     calendar_name="test1",
                     server_uri="http://localhost:8080")

    s2_test = Server(user_email="astronik00@gmail.com",
                     user_password="12345",
                     server_name="google",
                     calendar_name="test2",
                     server_uri="http://localhost:8081")

    s1_test = generate_server_labels(s1_test)
    s2_test = generate_server_labels(s2_test)

    local_creation_time = datetime.now()
    local_start_time = datetime(2023, 5, 24, 14, 33, 0, 0)
    local_end_time = datetime(2023, 5, 24, 17, 0, 0, 0)

    utc0_creation_time = local_to_utc0(local_creation_time)
    utc0_start_time = local_to_utc0(local_start_time)
    utc0_end_time = local_to_utc0(local_end_time)

    t1_test = Task(server=s1_test,
                   summary="My first task",
                   description="Need to test smth really quick",
                   dtstamp=utc0_creation_time,
                   dtstart=utc0_start_time,
                   due=utc0_end_time,
                   last_mod=utc0_creation_time,
                   tech_status=201,
                   parent=None)

    t2_test = Task(server=s1_test,
                   summary="My second task",
                   description="Need to test smth really quick",
                   dtstamp=utc0_creation_time,
                   dtstart=utc0_start_time,
                   due=utc0_end_time,
                   last_mod=utc0_creation_time,
                   tech_status=201,
                   parent=t1_test)

    t3_test = Task(server=s2_test,
                   summary="My third task",
                   description="Need to test smth really quick",
                   dtstamp=utc0_creation_time,
                   dtstart=utc0_start_time,
                   due=utc0_end_time,
                   last_mod=utc0_creation_time,
                   tech_status=201,
                   parent=None)

    t1_test.label = Label(task=t1_test)
    t2_test.label = Label(task=t2_test)
    t3_test.label = Label(task=t3_test)

    return [s1_test, s2_test], [t1_test, t2_test, t3_test]


class TestTaskRepositoryMethods(unittest.TestCase):
    def tearDown(self) -> None:
        session.query(Server).delete()
        session.query(Task).delete()
        session.query(Label).delete()
        session.query(Size).delete()
        session.query(Status).delete()
        session.query(Priority).delete()
        session.query(Type).delete()

    def setUp(self) -> None:
        self.servers, self.tasks = generate_data()
        server_repo.add_all(self.servers)
        task_repo.add_all(self.tasks)

    def test_add(self) -> None:
        local_creation_time = datetime.now()
        local_start_time = datetime.now()
        local_end_time = datetime(2023, 5, 25, 17, 0, 0, 0)

        utc0_creation_time = local_to_utc0(local_creation_time)
        utc0_start_time = local_to_utc0(local_start_time)
        utc0_end_time = local_to_utc0(local_end_time)

        t4_test = Task(server=self.servers[1],
                       summary="My third task",
                       description="Need to test smth really quick",
                       dtstamp=utc0_creation_time,
                       dtstart=utc0_start_time,
                       due=utc0_end_time,
                       last_mod=utc0_creation_time,
                       tech_status=201,
                       parent=None)

        t4_test.label = Label(task=t4_test)

        task_repo.add(t4_test)
        db_task = task_repo.get_by_id(t4_test.id)
        self.assertIsNotNone(db_task)

    def test_get_by_task_id(self):
        id_to_get = self.tasks[0].id
        self.assertEquals(self.tasks[0], task_repo.get_by_id(id_to_get))

    def test_delete_by_id(self):
        id_to_delete = 2  # нет детей
        task_repo.delete_by_id(id_to_delete)
        db_tasks = task_repo.get_by_id(id_to_delete)
        self.assertIsNone(db_tasks)

    def test_delete_by_task(self):
        task_to_delete = self.tasks[1]  # нет детей
        task_repo.delete(task_to_delete)
        db_tasks = task_repo.get_by_id(task_to_delete.id)
        self.assertIsNone(db_tasks)

    def test_delete_task_and_children_by_id(self):
        id_to_delete = 1
        task_repo.delete_by_id(id_to_delete)
        task_to_delete_children = task_repo.get_children_by_parent_id(id_to_delete)
        db_tasks = task_repo.get_by_id(id_to_delete)
        self.assertIsNone(db_tasks)
        self.assertEquals(len(task_to_delete_children), 0)

    def test_delete_task_and_children_by_task(self):
        task_to_delete = self.tasks[0]
        task_repo.delete(task_to_delete)
        task_to_delete_children = task_repo.get_children_by_parent_id(task_to_delete.id)
        db_tasks = task_repo.get_by_id(task_to_delete.id)
        self.assertIsNone(db_tasks)
        self.assertEquals(len(task_to_delete_children), 0)

    def test_edit(self):
        task_to_edit = self.tasks[0]
        task_to_edit.summary = "I was edited! Please look at me!"
        task_repo.edit(task_to_edit)
        db_tasks = task_repo.get_by_id(task_to_edit.id)
        self.assertEquals(task_to_edit, db_tasks)

    def test_get_all_by_server_id(self):
        server_id = 1
        result = [x for x in self.tasks if x.server_id == server_id]
        db_tasks = task_repo.get_all_by_server_id(server_id)
        self.assertEquals(result, db_tasks)

    def test_get_many_in_ids(self):
        task_ids = [1, 2]
        result = list(filter(lambda x: x.id in task_ids, self.tasks))
        db_tasks = task_repo.get_many_by_ids(task_ids)
        self.assertEquals(result, db_tasks)
