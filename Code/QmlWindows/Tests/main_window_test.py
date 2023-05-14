import sys
import os
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Получаем абсолютный путь к текущему скрипту и строим путь к файлу MainWindow.qml
    script_path = os.path.abspath(__file__)
    qml_file_path = os.path.join(os.path.dirname(script_path), '../MainWindow.qml')

    engine.load(QUrl.fromLocalFile(qml_file_path))  # Загрузка QML-файла
    sys.exit(app.exec())  # Запуск цикла события