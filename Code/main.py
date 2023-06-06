import os
import sys

from Code.handlers.auth_window_handler import AuthWindow
from Code.handlers.pincode_handler import PincodeWindow, ChangePincodeWindow
from Code.container import container, path_env, new_user
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from Code.handlers.main_window_handler import MainWindow
from Code.handlers.settings_window_handler import SettingsWindow


if __name__ == '__main__':

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    cur_dir = os.path.dirname(__file__)

    settings_windows = SettingsWindow()
    main_window = MainWindow()
    engine.rootContext().setContextProperty("main_handler", main_window)
    engine.rootContext().setContextProperty("settings_handler", settings_windows)
    auth_window = AuthWindow()
    engine.rootContext().setContextProperty("auth_handler", auth_window)
    change_pincode_handler = ChangePincodeWindow()
    engine.rootContext().setContextProperty('change_pincode_handler', change_pincode_handler)

    # проверка существует ли записанный пинкод
    if os.path.exists(path_env):
        pincode_handler = PincodeWindow(novice=False)
        engine.rootContext().setContextProperty("pincode_handler", pincode_handler)

        engine.load(os.path.join(cur_dir, "QmlWindows/ChekPincodeWindow.qml"))

    else:
        new_user('0000')
        pincode_handler = PincodeWindow(novice=True)
        engine.rootContext().setContextProperty("pincode_handler", pincode_handler)
        engine.load(os.path.join(cur_dir, "QmlWindows/AuthWindow.qml"))

    # engine.load(os.path.join(cur_dir, "QmlWindows/MainWindow.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
