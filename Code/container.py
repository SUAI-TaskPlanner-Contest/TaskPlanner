from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Code.entities.db_entities import Base
from Code.repositories.server_repo import ServerRepository
from Code.repositories.task_repo import TaskRepository
from Code.services import ServerService, TaskService

engine = create_engine('sqlite:///./database/taskplanner.db', echo=False)  # path to .db
Base.metadata.create_all(engine)  # create tables
session = sessionmaker(bind=engine)()  # create transaction

server_service = ServerService(ServerRepository(session))
task_service = TaskService(TaskRepository(session))
