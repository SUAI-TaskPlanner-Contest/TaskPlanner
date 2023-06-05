import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Code.entities.db_entities import Base
from Tests.repositories.test_server_repo import generate_data
from Code.handlers.auth_window_handler import AuthWindowHandler
from Code.services import Invalid, ServerService, TaskService
from Code.repositories.server_repo import ServerRepository
from Code.repositories.task_repo import TaskRepository

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine

# from pathlib import Path

if __name__ == '__main__':
    # create database
    engine = create_engine('sqlite:///./test.db', echo=False)  # path to .db
    Base.metadata.create_all(engine)  # create tables
    session = sessionmaker(bind=engine)()  # create transaction

    servers, tasks = generate_data()
    server_repo = ServerRepository(session)
    server_service = ServerService(server_repo, "1234")

    server_service.add_all(servers)
    print(server_service.get_count("astronik00@gmail.com"))
    print(server_service.get_by_id(1).user_email)
    print(server_service.get_many_by_ids([1, 2]))

    # app = QGuiApplication(sys.argv)
    # engine = QQmlApplicationEngine()
    # auth_handler = AuthWindowHandler()
    # engine.rootContext().setContextProperty("auth_handler", auth_handler)
    # engine.load('QmlWindows/AuthWindow.qml')  # файл с кодом QML основного окна
    # sys.exit(app.exec())  # запустить цикл события
