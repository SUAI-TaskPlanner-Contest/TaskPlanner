## Структура объектов
Структура окна "Список задач" (главное окно):

```
├── Window
    ├── Rectangle
        ├── GridLayout// разделение на 2 области(область кнопок и область задач)
            ├── Rectangle
                ├── GridLayout//5 кнопок
                    ├── Rectangle // Кнопка "Диаграмма Ганта"
                        ├── Button
                            ├── onClicked
                    ├── Rectangle // Кнопка "Синхронизация с сервером"
                        ├── Button
                            ├── onClicked
                    ├── Rectangle // Кнопка "Смена темы"
                        ├── Button
                            ├── onClicked
                    ├── Rectangle // Кнопка "Настройки"
                        ├── Button
                            ├── onClicked
                    ├── Rectangle // Кнопка "Выход"
                        ├── Button
                            ├── onClicked
            ├── Rectangle // правая кнопка (правая область)
                ├── Button
                    ├── onClicked
    ├── SettingsWindow //окно настроек
```

