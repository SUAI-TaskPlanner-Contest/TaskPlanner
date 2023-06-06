import bcrypt
import os
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Code.entities.db_entities import Base, Task, Server
from Code.repositories.server_repo import ServerRepository
from Code.repositories.task_repo import TaskRepository
from Code.services import ServerService, TaskService, CalDavService
from dotenv import load_dotenv

path_env = os.path.join(os.path.dirname(__file__), '.env')

class Container:
    dict = {}
    setters = ['server_service', 'task_service', 'caldav_service', 'pincode']

    def __init__(self, **kwargs):
        self.dict = kwargs

    @staticmethod
    def get(name):
        return Container.dict[name]

    @staticmethod
    def set(name, value):
        if name in Container.setters:
            Container.dict[name] = value

    @staticmethod
    def check_pincode(pincode) -> bool:
        load_dotenv(path_env)
        if bcrypt.checkpw(pincode.encode('utf-8'), os.getenv('PINCODE').encode('utf-8')):
            return True
        else:
            return False

    def __repr__(self):
        return f"Container(id={self.key}, {self.subkey})"


container = Container


def new_user(pincode):
    with open(path_env, "w") as file:
        container.set('pincode', pincode)
        pincode_hash = bcrypt.hashpw(pincode.encode('utf-8'), bcrypt.gensalt()).decode('utf8')
        file.write(f"PINCODE={pincode_hash}")
        container.set('server_service', ServerService(ServerRepository[Server](session), container.get('pincode')))
        container.set('task_service', TaskService(TaskRepository[Task](session)))
        container.get('server_service').add(Server (
                user_email='local',
                user_password='local',
                server_uri='http://local',
                server_name='локальный',
                calendar_name='local'))


def old_user(pincode):
    container.set('pincode', pincode)
    container.set('server_service', ServerService(ServerRepository[Server](session), container.get('pincode')))
    container.set('task_service', TaskService(TaskRepository[Task](session)))


engine = create_engine('sqlite:///./database/taskplanner.db', echo=False)  # path to .db
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)  # create tables
session = sessionmaker(bind=engine)()  # create transaction

def get_server_service() -> ServerService:
    return container.get('server_service')


def get_caldav_service() -> CalDavService:
    return container.get('caldav_service')

def get_pincode() -> str:
    return container.get('pincode')

def set_pincode(pincode):
    pincode_hash = bcrypt.hashpw(pincode.encode('utf-8'), bcrypt.gensalt()).decode('utf8')
    with open(path_env, "w") as file:
        file.write(f"PINCODE={pincode_hash}")
    container.set('pincode', pincode)
    container.get('server_service').set_pincode(pincode)