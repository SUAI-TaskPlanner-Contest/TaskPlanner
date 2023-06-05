from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Code.entities.db_entities import Base, Task, Server
from Code.repositories.server_repo import ServerRepository
from Code.repositories.task_repo import TaskRepository
from Code.services import ServerService, TaskService


class Container:
    dict = {}
    setters = ['server_service', 'task_service', 'caldav_service']

    def __init__(self, **kwargs):
        self.dict = kwargs

    @staticmethod
    def get(name):
        return Container.dict[name]

    @staticmethod
    def set(name, value):
        if name in Container.setters:
            Container.dict[name] = value

    def __repr__(self):
        return f"Container(id={self.key}, {self.subkey})"


engine = create_engine('sqlite:///./database/taskplanner.db', echo=False)  # path to .db
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)  # create tables
session = sessionmaker(bind=engine)()  # create transaction


container = Container
container.set('server_service', '0000')
container.set('server_service', ServerService(ServerRepository[Server](session)))
container.set('task_service', TaskService(TaskRepository[Task](session)))
