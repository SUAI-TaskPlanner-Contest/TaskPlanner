# Пример вызова ошибки
```
if __name__ == "__main__":
    try:
        a = 1
        if a == 1:
            raise CustomException(tuple(errors["ServerDeleteError"].values()))
    except CustomException as e:
        app = QApplication(sys.argv)
        engine = QQmlApplicationEngine()

        buttonHandler = ButtonHandler()
        engine.rootContext().setContextProperty("buttonHandler", buttonHandler)

        error_info = ErrorInfo(e.error_info.name, e.error_info.text, e.error_info.button1, e.error_info.button2)
        context = engine.rootContext()
        context.setContextProperty("errorInfo", error_info)

        engine.load("window.qml")

        if not engine.rootObjects():
            sys.exit(-1)

        sys.exit(app.exec_())
```
![image](https://github.com/SUAI-TaskPlanner-Contest/TaskPlanner/assets/78814540/073dcc82-00f6-466a-b64f-0e96ff45c96c)
