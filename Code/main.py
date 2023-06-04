import os
import sys
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from Code.container import container
from Code.handlers.settings_window_handler import SettingsWindow


if __name__ == '__main__':
    settings = SettingsWindow(container.get('server_service'))
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("settings", settings)

    cur_dir = os.path.dirname(__file__)
    engine.load(os.path.join(cur_dir, "QmlWindows/SettingsWindow.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
