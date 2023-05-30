import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from entities.db_entities import Base
from Code.handlers.auth_window_handler import AuthWindowHandler

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine

# from pathlib import Path

if __name__ == '__main__':
    # create database
    engine = create_engine('sqlite:///./database/taskplanner.db', echo=False)  # path to .db
    Base.metadata.create_all(engine)  # create tables
    session = sessionmaker(bind=engine)()  # create transaction

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    auth_handler = AuthWindowHandler()
    engine.rootContext().setContextProperty("auth_handler", auth_handler)
    engine.load('QmlWindows/AuthWindow.qml')  # файл с кодом QML основного окна
    sys.exit(app.exec())  # запустить цикл события
