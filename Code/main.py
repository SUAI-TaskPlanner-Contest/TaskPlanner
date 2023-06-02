import os
import sys

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Code.handlers.settings_window_handler import SettingsWindow
from entities.db_entities import Base
from services.server_service import ServerService
from services.task_service import TaskService
from repositories.server_repo import ServerRepository
from repositories.task_repo import TaskRepository


# from pathlib import Path

if __name__ == '__main__':
    # create database
    engine = create_engine('sqlite:///./database/taskplanner.db', echo=False)  # path to .db
    Base.metadata.create_all(engine)  # create tables
    session = sessionmaker(bind=engine)()  # create transaction

    server_service = ServerService(ServerRepository(session))
    task_service = TaskService(TaskRepository(session))

    main = SettingsWindow(server_service)
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("backend", main)

    cur_dir = os.path.dirname(__file__)
    engine.load(os.path.join(cur_dir, "QmlWindows/SettingsWindow.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
