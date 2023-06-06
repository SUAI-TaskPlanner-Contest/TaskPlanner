import os
import sys

from Code.handlers.auth_window_handler import AuthWindow
from Code.handlers.pincode_handler import PincodeWindow
from utils.add_data_db import add_data
from Code.container import container, session
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from Code.handlers.main_window_handler import MainWindow
from Code.handlers.settings_window_handler import SettingsWindow


if __name__ == '__main__':

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # сохранить pincode с окна авторизаций
    # if len(container.get('server_service').get_all()) == 0:
    #     add_data(session)

    pincode_handler = PincodeWindow(container.get('server_service'))
    settings_windows = SettingsWindow(container.get('server_service'))
    auth_window = AuthWindow(container.get('server_service'))
    main_window = MainWindow(container.get('task_service'), container.get('server_service'))

    engine.rootContext().setContextProperty("main_handler", main_window)
    engine.rootContext().setContextProperty("settings_handler", settings_windows)
    engine.rootContext().setContextProperty("auth_handler", auth_window)
    engine.rootContext().setContextProperty("pincode_handler", pincode_handler)

    cur_dir = os.path.dirname(__file__)

    if len(container.get('server_service').get_all()) > 1:
        engine.load(os.path.join(cur_dir, "QmlWindows/ChekPincodeWindow.qml"))
    else:
        engine.load(os.path.join(cur_dir, "QmlWindows/AuthWindow.qml"))

    # engine.load(os.path.join(cur_dir, "QmlWindows/MainWindow.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
