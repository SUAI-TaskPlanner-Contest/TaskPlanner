import os
import sys
from utils.add_data_db import add_data
from container import session, pincode
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from Code.container import container
from Code.handlers.main_window_handler import MainWindow
from Code.handlers.settings_window_handler import SettingsWindow


if __name__ == '__main__':

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    add_data(session, pincode)

    settings = SettingsWindow(container.get('server_service'))
    main_window = MainWindow(container.get('task_service'), container.get('server_service'))

    engine.rootContext().setContextProperty("main_window", main_window)
    engine.rootContext().setContextProperty("settings", settings)

    # QFont fon("Helvetica", 40);
    # app.setFont(fon);

    cur_dir = os.path.dirname(__file__)
    engine.load(os.path.join(cur_dir, "QmlWindows/SettingsWindow.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
