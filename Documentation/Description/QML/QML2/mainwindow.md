## Структура объектов
Структура окна "Список задач" (главное окно):

```
├── Window
    ├── Rectangle
        ├── GridLayout// разделение на 2 области(область кнопок и область задач)
            ├── Rectangle
                ├── GridLayout//5 кнопок
                    ├── Rectangle 
                        ├── Button
                            ├── onClicked
                    ├── Rectangle
                        ├── Button
                            ├── onClicked
                    ├── Rectangle
                        ├── Button
                            ├── onClicked
                    ├── Rectangle
                        ├── Button
                            ├── onClicked
                    ├── Rectangle
                        ├── Button
                            ├── onClicked
            ├── Rectangle // правая кнопка (правая область)
                ├── Button
                    ├── onClicked
    ├── SettingsWindow //окно настроек
```

## Разбор кода

1. Создание окна: 
```
Window {
    id: mainWindow // идентификатор
    signal signalExit // задаем сигнал
    width: screen.width // ширина окна
    height: screen.height // высота окна
    title: ("Список задач")
}
```

Свойства окна:
- Идентификатор (id) - `mainWindow` может пригодиться в дальнейшем;
- Размер (width, height) - ширина и высота в полный размер экрана.
- Название окна (title) - "Список задач".
- Обработчик сигнала (signal signalExit) - при закрытии окна можем задать различные действия.

2. Создание области во все окно:
```
Rectangle{
    width: parent.width
    height: parent.height}
```
Свойства объекта:
- Размер (width, height) - ширина и высота родителя.

3. Сетка (на 2 области):

```
GridLayout{
    id: grid
    width: parent.width; height: parent.height
    columns: 2}
```
Свойства объекта:
- Размер (width, height) - ширина и высота родителя.
- Количество столбцов (columns) равен 2, в первой области будут находиться кнопки, а во второй список задач.

4. Область для кнопок:
```
Rectangle{
    width: screen.width/2 - 500; height: screen.height
    color:"red"
    Layout.column: 2}
```
Свойства объекта:
- Размер (width, height) - ширина объекта чуть левее середины и высота родителя.
- Количество столбцов (columns) равен 2, в первой области будет находиться список задач, счет справа налево.
- Цвет (color) - для визуализации данной области.

5. Сетка (для 5 кнопок):
```
GridLayout{
    width: parent.width; height: parent.height
    rows:5}
```
Свойства объекта:
- Размер (width, height) - ширина и высота родителя.
- Количество строк (rows) - равен 5, так как у нас будет 5 разных кнопок.

6-8,10. Настройка четырех кнопок:

Код аналогичен для кнопок: "Диаграмма Ганта", "Синхронизация с сервером","Смена темы", "Выход". Разбор кода для первой кнопки:
```
Rectangle{
    Layout.row: 1
    width: parent.width; height:100
    Button {
        id: button1
        text: ("Диаграмма Ганта")
        width: parent.width; height: parent.height

        onClicked: {
            mainWindow.signalExit() //вызываем сигнал
        }
    }
}
```
Свойства объекта:
- Нахождение объекта(Layout.row) - прописываем на каком месте находится наша кнопка.
- Размер кнопки(width, height) - ширина родителя, а высота 100 ед.
- Текст (text) - текст на кнопке.
- Обработчик сигнала (onClicked) - после нажатия кнопки закрываем главное окно.

9. Кнопка "Настройки":
```
Rectangle{
    Layout.row: 4
    width:parent.width; height:100
    Button {
        id: button4
        text: ("Настройки")
        width: parent.width; height: parent.height
        onClicked: {
            settingsWindow.show()
        }
    }
}
```
Свойства данного объекта аналогичны 6-8 пункту. Различие лишь в обработчике сигнала, в этом случае открываем окно настроек.

11. Окно "Настройки"

В 9 пункте используется данное окно, для этого необходимо задать id данного окна:
```
SettingsWindow{
    id: settingsWindow
}
```

