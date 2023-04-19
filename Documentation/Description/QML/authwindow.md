## Структура объектов
Структура окна  "Авторизация":

```
├── ApplicationWindow
    ├── Rectangle
        ├── GridLayout
            ├── Rectangle // Логин
                ├── TextInput
            ├── Rectangle // Пароль
                ├── TextInput
            ├── Rectangle // Кнопка "Вход"
                ├── Button
                    ├── onClicked
    ├── MainWindow
        ├── onSignalExit
    ├── MainWindow
        ├── InstructionWindow
```

