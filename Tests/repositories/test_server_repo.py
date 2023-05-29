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


class TestServerRepositoryMethods(unittest.TestCase):
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

    def test_add(self):
        new_server = Server(user_email="astronik00@gmail.com",
                     user_password="jhrryui",
                     server_name="yandex",
                     calendar_name="test8",
                     server_uri="http://localhost:8080")
        new_server = generate_server_labels(new_server)

        server_repo.add(new_server)
        db_server = server_repo.get_by_id(new_server.id)
        self.assertIsNotNone(db_server)

    def test_get_by_server_id(self):
        id_to_get = self.servers[0].id
        self.assertEquals(self.servers[0], server_repo.get_by_id(id_to_get))

    def test_get_all(self):
        self.assertEquals(self.servers.sort(key=lambda server: server.id),
                          server_repo.get_all().sort(key=lambda server: server.id))

    def test_add_servers(self):
        server_repo.add_all(self.servers)
        db_servers = server_repo.get_all()
        self.assertEquals(self.servers.sort(key=lambda server: server.id),
                          db_servers.sort(key=lambda server: server.id))

    def test_cascase_delete_by_id(self):
        id_to_delete = 1
        server_repo.delete_by_id(id_to_delete)
        server_tasks = session.query(Task).filter(Task.server_id == id_to_delete).all()
        server_sizes = session.query(Size).filter(Size.server_id == id_to_delete).all()
        server_types = session.query(Type).filter(Type.server_id == id_to_delete).all()
        server_priorities = session.query(Priority).filter(Priority.server_id == id_to_delete).all()
        server_statuses = session.query(Status).filter(Status.server_id == id_to_delete).all()
        self.assertEquals(len(server_tasks), 0)
        self.assertEquals(len(server_sizes), 0)
        self.assertEquals(len(server_types), 0)
        self.assertEquals(len(server_priorities), 0)
        self.assertEquals(len(server_statuses), 0)

    def test_cascase_delete_by_server(self):
        server_to_delete = self.servers[0]
        id_to_delete = server_to_delete.id
        server_repo.delete(server_to_delete)
        server_tasks = session.query(Task).filter(Task.server_id == id_to_delete).all()
        server_sizes = session.query(Size).filter(Size.server_id == id_to_delete).all()
        server_types = session.query(Type).filter(Type.server_id == id_to_delete).all()
        server_priorities = session.query(Priority).filter(Priority.server_id == id_to_delete).all()
        server_statuses = session.query(Status).filter(Status.server_id == id_to_delete).all()
        self.assertEquals(len(server_tasks), 0)
        self.assertEquals(len(server_sizes), 0)
        self.assertEquals(len(server_types), 0)
        self.assertEquals(len(server_priorities), 0)
        self.assertEquals(len(server_statuses), 0)

    def test_edit(self):
        server_to_edit = self.servers[0]
        server_to_edit.user_password = "new_password"
        server_repo.edit(server_to_edit)
        db_server = server_repo.get_by_id(server_to_edit.id)
        self.assertEquals(server_to_edit, db_server)

    def test_get_many_in_ids(self):
        server_ids = [1, 2]
        result = list(filter(lambda x: x.id in server_ids, self.servers))
        db_servers = server_repo.get_many_by_ids(server_ids)
        self.assertEquals(result, db_servers)

    def test_count(self):
        count = 2
        db_servers_count = server_repo.get_count("astronik00@gmail.com")
        self.assertEquals(count, db_servers_count)
