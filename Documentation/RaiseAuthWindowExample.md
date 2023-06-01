## Пример вызова окна Авторизации
```
import sys
import os

from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication
from PyQt6.QtQml import QQmlApplicationEngine

from Code.handlers.auth_window_handler import AuthWindowHandler


if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    authwindowHandler = AuthWindowHandler()
    engine.rootContext().setContextProperty("authwindowHandler", authwindowHandler)

    current_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    qml_file_path = os.path.join(current_dir, "Code\QmlWindows\AuthWindow.qml")
    engine.load(QUrl.fromLocalFile(qml_file_path))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
 ```
 ![image](https://github.com/SUAI-TaskPlanner-Contest/TaskPlanner/assets/78814540/6305347e-f1ac-42af-a4f5-f784c5ca8ce9)
