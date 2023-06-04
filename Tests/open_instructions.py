import sys
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Code.entities.db_entities import Base
from Code.handlers.pincode_handler import PincodeWindow
from Code.repositories.server_repo import ServerRepository
from Code.services import ServerService

if __name__ == '__main__':
    engine = create_engine('sqlite:///../Code/database/taskplanner.db', echo=False)  # path to .db
    Base.metadata.create_all(engine)  # create tables
    session = sessionmaker(bind=engine)()

    server_service = ServerService(ServerRepository(session))
    pincode_window = PincodeWindow(server_service)

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("pincode_save", pincode_window)
    engine.load('../Code/QmlWindows/PincodeWindow.qml')
    sys.exit(app.exec())
