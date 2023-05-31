# Пример вызова ошибки
```
import sys
import os

from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication
from PyQt6.QtQml import QQmlApplicationEngine

from TaskPlanner.Code.errors_dict.errors import errors
from TaskPlanner.Code.exceptions.custom_exceptions import CustomException
from TaskPlanner.Code.handlers.warning_window_handler import WarningWindowHandler, WarningButtonHandler

if __name__ == "__main__":
    try:
        a = 1
        if a == 1:
            raise CustomException(tuple(errors["ServerDeleteError"].values()))
    except CustomException as e:
        app = QApplication(sys.argv)
        engine = QQmlApplicationEngine()

        buttonHandler = WarningButtonHandler()
        engine.rootContext().setContextProperty("buttonHandler", buttonHandler)

        error_info = WarningWindowHandler("", "", "", "")
        context = engine.rootContext()
        context.setContextProperty("errorInfo", error_info)

        error_info.setProperty("name", e.error_info.name)
        error_info.setProperty("text", e.error_info.text)
        error_info.setProperty("button_ok", e.error_info.button_ok)
        error_info.setProperty("button_cancel", e.error_info.button_cancel)

        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        qml_file_path = os.path.join(current_dir, "Code\QmlWindows", "WarningWindow.qml")
        engine.load(QUrl.fromLocalFile(qml_file_path))

        if not engine.rootObjects():
            sys.exit(-1)

        sys.exit(app.exec())
```
![image](https://github.com/SUAI-TaskPlanner-Contest/TaskPlanner/assets/78814540/a0e2e6e8-bc61-435f-9fb9-7c958595a612)
