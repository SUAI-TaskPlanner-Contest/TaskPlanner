import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

//Автоматизация через функции !
Window {
    id: mainWindow
    signal signalExit
    visible: true

    width: 1400; height: 700
    title: ("Task Planner")

    //предотвратить изменение размеров окна пользователем
    maximumHeight: height; maximumWidth: width
    minimumHeight: height; minimumWidth: width

    //по центру экрана
    x: (Screen.width - width) / 2
    y: (Screen.height - height) / 2

    //Загрузка шрифтов
    FontLoader { id: localFont; source: "fonts/Inter-Thin.ttf" }
    FontLoader { id: localFont1; source: "fonts/Inter-ExtraLight.ttf" }

    //рабочее место для Списка задач
    Rectangle{
        id: workplace
        width: 1200; height: parent.height
        visible: true
        // Название страницы "Список задач"
        Text{
            x:10; y:10
            text: "Список задач"
            font.family: localFont.name; font.weight: 400;color: "#232323"
            font.pointSize: 45
        }

        //комбобокс серверов + кнопка обн(мерж)
        Rectangle{
            width: 170; height: 45
            x: 420; y: 30
            // combobox выбор сервера
            ComboBox {
                anchors.verticalCenter: parent.verticalCenter
                id: control
                font.family: localFont.name; font.weight: 400;
                font.pointSize: 12
                model: ["NextCloud", "Second", "Third"]
                onActivated: {
                    // обработки выбора элемента здесь
                    console.log("Выбран элемент:", model[index]);//вывод только в консоль qml
                }
                delegate: ItemDelegate {
                    width: control.width
                    contentItem: Text {
                        text: control.textRole
                            ? (Array.isArray(control.model) ? modelData[control.textRole] : model[control.textRole]) : modelData
                        color: "black"
                        font: control.font
                        elide: Text.ElideRight
                        verticalAlignment: Text.AlignVCenter
                    }
                    highlighted: control.highlightedIndex === index
                }

                indicator: Canvas { //треуг справа
                    x: control.width - width - control.rightPadding
                    y: control.topPadding + (control.availableHeight - height) / 2
                    width: 12;  height: 8
                    contextType: "2d"

                    Connections {
                        target: control; function onPressedChanged() { canvas.requestPaint(); }
                    }

                    onPaint: {
                        context.reset();  context.moveTo(0, 0);
                        context.lineTo(width, 0); context.lineTo(width / 2, height);
                        context.closePath(); context.fillStyle = control.pressed ? "black" : "lightgrey";
                        context.fill();
                    }
                }

                contentItem: Text { //текст в строке
                    leftPadding: 0; rightPadding: control.indicator.width + control.spacing

                    text: control.displayText
                    font: control.font;  color: control.pressed ? "black" : "black"
                    verticalAlignment: Text.AlignVCenter
                    elide: Text.ElideRight
                }

                background: Rectangle {
                    implicitWidth: 120; implicitHeight: 40
                    border.color: control.pressed ? "lightgrey" : "lightgrey"
                    border.width: control.visualFocus ? 2 : 1
                    radius: 5
                }

                popup: Popup {
                    y: control.height - 1;  width: control.width
                    implicitHeight: contentItem.implicitHeight
                    padding: 1
                    contentItem: ListView {
                        clip: true; implicitHeight: contentHeight
                        model: control.popup.visible ? control.delegateModel : null
                        currentIndex: control.highlightedIndex
                        ScrollIndicator.vertical: ScrollIndicator { }
                    }

                    background: Rectangle {border.color: "lightgrey";radius: 2}
                }
            }

            Button{
                id: but_refresh_server
                width: 45; height: 45; x: 125
                anchors.verticalCenter: parent.verticalCenter
                background: Rectangle{color: "white"}
                contentItem: Image{source: "Resources/refresh.svg"}
                hoverEnabled: false //не будет выделяться кнопка

                onClicked:{
                    console.log("I'm working!")
                    main_window.sync_tasks()
                    // tab_merge_task.visible=!tab_merge_task.visible
                }
            }
        }

        //кнопка плюс
        Rectangle{
            width: 45; height: 45
            x: 1150; y: 20
            color: "grey"
            //плюс
            Button{
                id: but_add_task
                width: 45 // ширина окна
                height: 45
                background: Rectangle{color: "white"}
                contentItem: Image{source: "Resources/add.svg"}
                hoverEnabled: false //не будет выделяться кнопка

                onClicked:{
                    patentsearch_text.visible=false
                    patentsearch_combobox.visible=false
                    newtask.visible=!newtask.visible
                }
            }

        }


        //таблица задач
        Rectangle{
            width: 1180; height: 610
            x:10; y:80
            border.color: "lightgrey"
            border.width: 4
            radius: 20 // устанавливаем общий радиус для всех углов
        }

        Button {
            id: but_setting_task
            width: 50; height: 50
            x:1000; y:120
            visible: true
            contentItem: Image{source: "Resources/dots.svg"}
            hoverEnabled: false
            background: Rectangle{color: "white"}
            onClicked: {
                settingsList.visible = !settingsList.visible
            }
            Popup {//открытия окна редактирования добавления и удаление задачи
                id: settingsList
                width: 135
                height: 90
                visible: false

                Column {
                    spacing: 1
                    Button {
                        id: but_add_subtask
                        width: 125
                        background: Rectangle{color: "white"}
                        text: "Добавить подзадачу"
                        font.family: localFont.name; font.weight: 500
                        onClicked: {
                            newtask.visible=!newtask.visible
                            settingsList.visible=!settingsList.visible
                            patentsearch_text.visible=true
                            patentsearch_combobox.visible=true
                            // Действия при нажатии кнопки "Добавить подзадачу"
                            }
                    }
                    Button {
                        id: but_edit_task
                        width: 125
                        text: "Редактировать"
                        font.family: localFont.name; font.weight: 500
                        background: Rectangle{color: "white"}
                        onClicked: {
                            newtask.visible=!newtask.visible
                            settingsList.visible=!settingsList.visible

                            // Действия при нажатии кнопки "Редактировать"
                            }
                    }
                    Button {
                        id: but_delete_task
                        width: 125
                        text: "Удалить"
                        font.family: localFont.name; font.weight: 500
                        background: Rectangle{color: "white"}
                        onClicked: {
                            // Действия при нажатии кнопки "Удалить"
                            }
                    }
                }
            }
        }
    }
    //ДОСКА ГАНТА
    Rectangle{
        id: workplace_gant
        width: 1200; height: parent.height
        visible: false
        // Список задач текст
        Text{
            x:10; y:10
            text: "Диаграмма Ганта"
            font.family: localFont.name; font.weight: 400;color: "#232323"
            font.pointSize: 45}
    }
    //мердж
    Rectangle{
        id: tab_merge_task
        width: workplace.width; height: mainWindow.height
        visible: false

        Rectangle{
            id: ver_server//Версия сервера
            width: parent.width/3; height: parent.height
            Text{
                text: "Версия сервера"
                font.family: localFont.name; font.weight: 400
                anchors.horizontalCenter: parent.horizontalCenter
                font.pointSize: 20; y:20
            }
            Rectangle{
                width: parent.width-10
                height: 550
                y:60
                anchors.horizontalCenter: parent.horizontalCenter
                border.color: 'lightgrey'
                border.width: 3; radius: 40
                Text{
                    id: ver_server_name
                    text: 'Написать доку'
                    font.family: localFont.name; font.weight: 400;color: "#232323"
                    font.pointSize: 20
                    anchors.horizontalCenter: parent.horizontalCenter; y:5
                }
                ScrollView {
                    y:50
                    x:10
                    Text{
                        id: ver_server_description
                        wrapMode: Text.Wrap
                        font.family: localFont1.name; font.weight: 400;color: "#232323"
                        font.pointSize: 16
                        width: ver_server.width-20
                        height: 70
                        text: 'Описание задачи содержит описание задачи, описывающий необходимую информацию о задаче. Возьми еще этих мягких французских булок, да выпей чаю.'
                    }
                }

                Rectangle{//делаем таблицу 6*2
                    x: 10
                    y: 250
                    GridLayout{ rows: 7; columns: 2;
                        Text{ Layout.column: 2; Layout.row: 1; text: "Дата начала:"
                             font.pointSize: 12;font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{ Layout.column: 2; Layout.row: 2; text: "Дата завершения:"
                            font.pointSize: 12;font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{ Layout.column: 2; Layout.row: 3; text: "Категория:"
                            font.pointSize: 12;font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{ Layout.column: 2; Layout.row: 4; text: "Статус:"
                            font.pointSize: 12;font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{ Layout.column: 2; Layout.row: 5; text: "Размер:"
                            font.pointSize: 12;font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{ Layout.column: 2; Layout.row: 6; text: "Приоритет:"
                            font.pointSize: 12;font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{ Layout.column: 2; Layout.row: 7; text: "Родитель:"
                            font.pointSize: 12;font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{
                            id: ver_server_data_start
                            Layout.column: 1; Layout.row: 1
                            text: "20.20.2020"; font.pointSize: 12
                            font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{
                            id: ver_server_data_end
                            Layout.column: 1; Layout.row: 2
                            text: "20.20.2020"; font.pointSize: 12
                            font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{
                            id: ver_server_category
                            Layout.column: 1; Layout.row: 3
                            text: "Design"; font.pointSize:12
                            font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{
                            id: ver_server_status
                            Layout.column: 1; Layout.row: 4
                            text: "Нет исполнителя";  font.pointSize:12
                            font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{
                            id: ver_server_size
                            Layout.column: 1; Layout.row: 5; text: "Легкая"
                            font.pointSize:12
                            font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{
                            id: ver_server_priority
                            Layout.column: 1; Layout.row: 6; text: "1"
                            font.pointSize:12
                            font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{
                            id: ver_server_parent
                            Layout.column: 1; Layout.row: 7; text: "Какая-то задача"
                            font.pointSize:12
                            font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                    }
                }
            }
            Button{
                text: "Принять это"
                font.pointSize: 18
                y:640
                font.family: localFont.name; font.weight: 400;
                width: 200;height: 50
                hoverEnabled: false
                anchors.horizontalCenter: parent.horizontalCenter

                background: Rectangle {
                     id:but_ver_server
                     color: "lightgreen"
                     border.color: "green"
                     radius: 17
                     border.width: 1
                }
                MouseArea{
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: {
                        but_ver_server.color = "#8BFF18" // Цвет при наведении на кнопку
                    }
                    onExited: {but_ver_server.color = "lightgreen" // Исходный цвет кнопки
                    }
                    onPressed: {but_ver_server.color = "#8BFF18" // Цвет при нажатии кнопки
                    }
                    onReleased: {
                        but_ver_server.color = "#D3D3D3" // Исходный цвет кнопки
                        tab_merge_task.visible=!tab_merge_task.visible
                    }
                }
            }
        }
        Rectangle{
            id: ver_intermediate//Промежуточная версия
            width: parent.width/3; height: parent.height
            anchors.left: ver_server.right
            Text{
                text: "Промежуточная версия"
                font.family: localFont.name; font.weight: 400;color: "#232323"
                anchors.horizontalCenter: parent.horizontalCenter
                font.pointSize: 20; y:20
            }
            Rectangle{
                width: parent.width-10; height: 550
                y:60
                anchors.horizontalCenter: parent.horizontalCenter
                color: 'white'
                border.color: 'lightgrey'
                border.width: 3; radius: 40
                TextField {
                    id: ver_intermediate_name
                    text: 'Переписать доку'
                    font.family: localFont.name; font.weight: 400;color: "#232323"
                    font.pointSize: 20
                    anchors.horizontalCenter: parent.horizontalCenter; y:5
                    width: 300
                }
                TextField {
                    y:50
                    id: ver_intermediate_description
                    anchors.horizontalCenter: parent.horizontalCenter;
                    font.family: localFont1.name; font.weight: 400;color: "#232323"
                    wrapMode: Text.Wrap
                    font.pointSize: 16
                    width: 360
                    height: 180
                    text: 'Описание задачи содержит описание задачи, описывающий необходимую информацию о задаче. Возьми еще этих мягких французских булок, да выпей чаю.'
                }
                Rectangle{//делаем таблицу 6*2
                    x: 20
                    y: 250

                    GridLayout{ rows: 7; columns: 2
                        Text{ Layout.column: 2; Layout.row: 1; text: "Дата начала:"
                             font.pointSize: 12
                             font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{ Layout.column: 2; Layout.row: 2; text: "Дата завершения:"
                            font.pointSize: 12
                            font.family: localFont.name; font.weight: 400;color: "#232323"
                        }

                        Text{ Layout.column: 2; Layout.row: 3; text: "Категория:"
                            font.pointSize: 12
                            font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{ Layout.column: 2; Layout.row: 4; text: "Статус:"
                            font.pointSize: 12
                            font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{ Layout.column: 2; Layout.row: 5; text: "Размер:"
                            font.pointSize: 12
                            font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{ Layout.column: 2; Layout.row: 6; text: "Приоритет:"
                            font.pointSize: 12
                            font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{ Layout.column: 2; Layout.row: 7; text: "Родитель:"
                            font.pointSize: 12
                            font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        TextField {
                            id: ver_intermediate_data_start
                            Layout.column: 1; Layout.row: 1
                            text: "20.20.2020"; font.pointSize: 12
                            inputMask: " 99.99.9999";
                            font.family: localFont.name; font.weight: 400;
                        }
                        TextField {
                            id: ver_intermediate_data_end
                            inputMask: " 99.99.9999";
                            Layout.column: 1; Layout.row: 2
                            text: "20.20.2020"; font.pointSize: 12
                            font.family: localFont.name; font.weight: 400;
                        }
                        ComboBox{
                            id: ver_intermediate_category
                            Layout.column: 1; Layout.row: 3
                            model: ["Design", "UX", "UI", "Backend"]
                            font.pointSize:12
                            font.family: localFont.name; font.weight: 400;
                        }
                        ComboBox{
                            id: ver_intermediate_status
                            Layout.column: 1; Layout.row: 4
                            model: ["Нет исполнителя", "В работе", "Завершена", "Конфликт"]
                            onActivated: {}
                            font.pointSize:12
                            font.family: localFont.name; font.weight: 400;
                        }
                        ComboBox{
                            id: ver_intermediate_size
                            model: ["Легкая", "Средняя", "Тяжелая"]
                            onActivated: {}
                            Layout.column: 1; Layout.row: 5;
                            font.pointSize:12
                            font.family: localFont.name; font.weight: 400;
                        }
                        ComboBox{
                            id: ver_intermediate_priority
                            model: ["1", "2", "3", "4"]
                            onActivated: {}
                            Layout.column: 1; Layout.row: 6;
                            font.pointSize:12
                            font.family: localFont.name; font.weight: 400;
                        }
                        Text{
                            id: ver_intermediate_parent
                            Layout.column: 1; Layout.row: 7; text: "Какая-то задача"
                            font.pointSize:12
                            font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                    }
                }
            }

            Button{
                text: "Принять это"
                font.pointSize: 18
                y:640
                font.family: localFont.name; font.weight: 400;
                width: 200;height: 50
                hoverEnabled: false
                anchors.horizontalCenter: parent.horizontalCenter

                background: Rectangle {
                     id:but_ver_intermediate
                     color: "lightgreen"
                     border.color: "green"
                     radius: 17
                     border.width: 1
                }
                MouseArea{
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: {but_ver_intermediate.color = "#8BFF18" // Цвет при наведении на кнопку
                    }
                    onExited: {but_ver_intermediate.color = "lightgreen" // Исходный цвет кнопки
                    }
                    onPressed: {but_ver_intermediate.color = "#8BFF18" // Цвет при нажатии кнопки
                    }
                    onReleased: {
                        but_ver_intermediate.color = "#D3D3D3" // Исходный цвет кнопки
                        tab_merge_task.visible=!tab_merge_task.visible
                    }
                }
            }
        }
        Rectangle{
            id: ver_client//Версия клиента
            width: parent.width/3; height: parent.height
            anchors.left: ver_intermediate.right
            Text{
                text: "Версия клиента"
                font.family: localFont.name; font.weight: 400;color: "#232323"
                anchors.horizontalCenter: parent.horizontalCenter
                font.pointSize: 20; y:20
            }
            Rectangle{
                width: parent.width-10; height: 550
                y:60
                anchors.horizontalCenter: parent.horizontalCenter
                color: 'white'
                border.color: 'lightgrey'
                border.width: 3; radius: 40
                Text{
                    id:ver_client_name
                    text: 'Написать доку'
                    font.pointSize: 20
                    font.family: localFont.name; font.weight: 400;color: "#232323"
                    anchors.horizontalCenter: parent.horizontalCenter; y:5
                }
                ScrollView {
                    y:50
                    x:10
                    Text{
                        id: ver_client_description
                        wrapMode: Text.Wrap
                        font.family: localFont1.name; font.weight: 400;color: "#232323"
                        font.pointSize: 16
                        width: ver_server.width-20
                        height: 70
                        text: 'Описание задачи содержит описание задачи, описывающий необходимую информацию о задаче. Возьми еще этих мягких французских булок, да выпей чаю.'
                    }
                }

                Rectangle{//делаем таблицу 6*2
                    x: 20
                    y: 250
                    GridLayout{ rows: 7; columns: 2
                        Text{ Layout.column: 2; Layout.row: 1; text: "Дата начала:"
                             font.pointSize: 12
                             font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{ Layout.column: 2; Layout.row: 2; text: "Дата завершения:"
                            font.pointSize: 12
                            font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{ Layout.column: 2; Layout.row: 3; text: "Категория:"
                            font.pointSize: 12
                            font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{ Layout.column: 2; Layout.row: 4; text: "Статус:"
                            font.pointSize: 12
                            font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{ Layout.column: 2; Layout.row: 5; text: "Размер:"
                            font.pointSize: 12
                            font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{ Layout.column: 2; Layout.row: 6; text: "Приоритет:"
                            font.pointSize: 12
                            font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{ Layout.column: 2; Layout.row: 7; text: "Родитель:"
                            font.pointSize: 12
                            font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{
                            id:ver_client_data_start
                            Layout.column: 1; Layout.row: 1
                            text: "20.20.2020"; font.pointSize: 12
                            font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{
                            id: ver_client_data_end
                            Layout.column: 1; Layout.row: 2
                            text: "20.20.2020"; font.pointSize: 12
                            font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{
                            id:ver_client_category
                            Layout.column: 1; Layout.row: 3
                            text: "Design"; font.pointSize:12
                            font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{
                            id: ver_client_status
                            Layout.column: 1; Layout.row: 4
                            text: "Нет исполнителя";  font.pointSize:12
                            font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{
                            id: ver_client_size
                            Layout.column: 1; Layout.row: 5; text: "Легкая"
                            font.pointSize:12
                            font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{
                            id: ver_client_priority
                            Layout.column: 1; Layout.row: 6; text: "1"
                            font.pointSize:12
                            font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                        Text{
                            id: ver_client_parent
                            Layout.column: 1; Layout.row: 7; text: "Какая-то задача"
                            font.pointSize:12
                            font.family: localFont.name; font.weight: 400;color: "#232323"
                        }
                    }
                }
            }

            Button{
                text: "Принять это"
                font.family: localFont.name; font.weight: 400;
                font.pointSize: 18
                y:640
                width: 200;height: 50
                hoverEnabled: false
                anchors.horizontalCenter: parent.horizontalCenter

                background: Rectangle {
                     id:but_ver_client
                     color: "lightgreen"
                     border.color: "green"
                     radius: 17
                     border.width: 1
                }
                MouseArea{
                    anchors.fill: parent
                    hoverEnabled: true

                    onEntered: { but_ver_client.color = "#8BFF18" // Цвет при наведении на кнопку
                    }
                    onExited: {but_ver_client.color = "lightgreen" // Исходный цвет кнопки
                    }
                    onPressed: {but_ver_client.color = "#8BFF18" // Цвет при нажатии кнопки
                    }
                    onReleased: {
                        but_ver_client.color = "#D3D3D3" // Исходный цвет кнопки
                        tab_merge_task.visible=!tab_merge_task.visible
                    }
                }
            }
        }

         Button{//кнопка закрыть мердж
            id: closemerge
            width: 50; height: 50
            y: 5; x:1150
            contentItem: Image{source: "Resources/close.svg"}
            hoverEnabled: false
            background: Rectangle{color: "white"}
            onClicked:{tab_merge_task.visible=!tab_merge_task.visible}
        }
    }
    // о пользователе
    Rectangle{
        id: info
        width: mainWindow.width-workplace.width
        height: parent.height
        anchors.left: workplace.right
        color: "lightgrey"

        Button {
            id: info_but
            width: parent.width; height: parent.height/15
            y:10
            anchors.horizontalCenter: parent.horizontalCenter
            visible: true
            text: "Task Planner"; font.pointSize: 25
            font.family: localFont.name; font.weight: 500;
            hoverEnabled: false
            background: Rectangle{color: "lightgrey"}
            onClicked: {
                popinfo.visible = !popinfo.visible
            }
            Popup {
                id: popinfo
                width: parent.width
                height: 190
                visible: false

                Column {
                    spacing: 0
                    Text {
                        text: "Версия приложения: v0.1.09062023"
                        font.family: localFont.name; font.weight: 600;color: "#232323"
                        font.pointSize: 8
                    }
                    Text {
                        text: "Над проектом работали:\n1. 4230М Кузнецов Никита\n2. 4230М Сидоренко Денис\n3. 4231М Гилёв Ярослав\n4. 4231М Горбунов Александр\n5. 4231М Кустова Екатерина\n6. 4231М Кырлан Вячеслав\n7. 4231М Савельева Дарья\n8. 4231М Щеголева Александра\n9. 4232М Климонтов Никита\n10. 4232М Парфишов Павел"
                        font.pointSize: 8
                        font.family: localFont.name; font.weight: 600;color: "#232323"
                    }
                    Text {
                        text: "<a href='https://github.com/SUAI-TaskPlanner-Contest'>Репозиторий</a>"
                        font.pointSize: 8
                        font.family: localFont.name; font.weight: 600;color: "#232323"
                        MouseArea {
                            anchors.fill: parent
                            onClicked: Qt.openUrlExternally("https://github.com/SUAI-TaskPlanner-Contest")
                            hoverEnabled: true
                            cursorShape: Qt.PointingHandCursor
                        }
                    }
                }
            }
        }
        //ФИ
        Rectangle{
            anchors.top: info_but.bottom
            width: parent.width;
            color: parent.color
            Text{
                id: username
                font.pointSize: 17
                text: "Username"
                font.family: localFont.name; font.weight: 400;color: "#232323"
                anchors.horizontalCenter: parent.horizontalCenter;
            }
        }
        // кнопки диаграмма Ганта настройки и полоса сверху
        Rectangle{
            y:620
            width: parent.width; height: 70
            color: parent.color
            Rectangle{//полоса
                anchors.horizontalCenter: parent.horizontalCenter
                width: 180;  height: 3; radius: 20
                color: "white"
            }
            //кнопки
            Button{
                id: butdiagram
                width: 60; height: 60
                y:10; x:10
                visible: true
                contentItem: Image{source: "Resources/diagram.svg"}
                hoverEnabled: true
                background: Rectangle{color: "lightgrey"}
                onClicked: {
                    butdiagram.visible=!butdiagram.visible
                    butdosk.visible=!butdosk.visible

                    workplace.visible=!workplace.visible
                    workplace_gant.visible=!workplace_gant.visible
                }
            }
            Button{
                id: butdosk
                width: 60
                height: 60
                y:10
                x:10
                visible: false
                contentItem: Image{source: "Resources/alltask.svg"}
                hoverEnabled: true
                background: Rectangle{color: "lightgrey"}
                onClicked: {
                    butdiagram.visible=!butdiagram.visible
                    butdosk.visible=!butdosk.visible

                    workplace.visible=!workplace.visible
                    workplace_gant.visible=!workplace_gant.visible
                }
            }
            Button{
                id: but_setting_window
                width: 60
                height: 60
                y: 10
                x: 140
                contentItem: Image{source: "Resources/setting.svg"}
                hoverEnabled: false
                background: Rectangle{color: "lightgrey"}
                onClicked: {
                    //settingsWindow.show()//вызываем сигнал
                }
            }
        }
    }// о пользователе

    //окно создание задачи
    Rectangle{
        id: newtask
        width: 500; height: parent.height
        x:900
        color: "white"
        visible: false
        border.width: 2
        border.color: "lightgrey"
        Button{//кнопка закрыть окно создания задачи
            id: butclose
            width: 45;  height: 45
            y: 3;  x: 450
            contentItem: Image{source: "Resources/close.svg"}
            hoverEnabled: false
            background: Rectangle{color: "white"}
            onClicked:{newtask.visible=false}
        }
        //название задачи
        TextField{
            x: 10; y: 50
            id: task_name
            width:440
            //maximumLength: 50
            font.pointSize: 25
            text: "Новая  задача"
            font.family: localFont.name; font.weight: 500;color: "#232323"
        }
        //описание задачи
        TextField{
            id: task_description
            x:10; y:100
            width: 440; height: 150
            wrapMode: TextInput.Wrap
            //maximumLength: 200
            font.pointSize: 17
            font.family: localFont.name; font.weight: 500;color: "#232323"
            text: "Введите описание задачи"
        }

        Rectangle{//делаем таблицу 6*2
            x: 10; y: 260
            width: 440; height: 500
            GridLayout{ // разбиваем на сетку
                rows: 8; columns: 2
                Text{Layout.column: 2; Layout.row:1; text: "Дата начала:"
                    font.pointSize: 14
                    font.family: localFont.name; font.weight: 400;color: "#232323"
                    }
                Text{ Layout.column: 2; Layout.row: 2; text: "Дата завершения:"
                    font.pointSize: 14
                    font.family: localFont.name; font.weight: 400;color: "#232323"
                    }
                Text{Layout.column: 2; Layout.row: 3; text: "Категория:"
                    font.pointSize: 14
                    font.family: localFont.name; font.weight: 400;color: "#232323"
                    }
                Text{ Layout.column: 2; Layout.row: 4; text: "Статус:"
                    font.pointSize: 14
                    font.family: localFont.name; font.weight: 400;color: "#232323"
                    }
                Text{ Layout.column: 2; Layout.row: 5; text: "Размер:"
                    font.pointSize: 14
                    font.family: localFont.name; font.weight: 400;color: "#232323"
                    }
                Text{ Layout.column: 2; Layout.row: 6; text: "Приоритет:"
                    font.pointSize: 14
                    font.family: localFont.name; font.weight: 400;color: "#232323"
                    }
                Text{ id: patentsearch_text
                    visible: true
                    Layout.column: 2; Layout.row: 7; text: "Родитель:"
                    font.pointSize: 14
                    font.family: localFont.name; font.weight: 400;color: "#232323"
                }
                TextField {
                    font.family: localFont.name; font.weight: 400;color: "#232323"
                    Layout.column: 1; Layout.row: 1
                    id: task_data_start
                    inputMask: " 99.99.9999"; text: "20.20.2020"
                    font.pointSize: 14
                }
                TextField {
                    font.family: localFont.name; font.weight: 400;color: "#232323"
                    Layout.column: 1; Layout.row: 2
                    id: task_data_end
                    inputMask: " 99.99.9999"; text: "20.20.2020"
                    font.pointSize: 14
                }
                ComboBox{
                    id: task_category
                    Layout.column: 1; Layout.row: 3
                    width: 200
                    height: 45
                    font.pointSize:14
                    model: ["Design", "UX", "UI", "Backend"]
                    onActivated: {}
                    font.family: localFont.name; font.weight: 400;
                }
                ComboBox{
                    id: task_status
                    Layout.column: 1; Layout.row: 4
                    width: 200
                    height: 45
                    font.pointSize:14
                    model: ["Нет исполнителя", "В работе", "Завершена", "Конфликт"]
                    onActivated: {}
                    font.family: localFont.name; font.weight: 400;
                }
                ComboBox{
                    id: task_size
                    Layout.column: 1; Layout.row: 5
                    width: 200
                    height: 45
                    font.pointSize:14
                    model: ["Легкая", "Средняя", "Тяжелая"]
                    onActivated: {}
                    font.family: localFont.name; font.weight: 400;
                }
                ComboBox{
                    id: task_priority
                    Layout.column: 1; Layout.row: 6
                    width: 200
                    height: 45
                    font.pointSize:14
                    model: ["1", "2", "3", "4"]
                    onActivated: {}
                    font.family: localFont.name; font.weight: 400;
                }
                ComboBox{
                    id: patentsearch_combobox
                    Layout.column: 1; Layout.row: 7
                    width: 200
                    height: 45
                    visible: true
                    font.pointSize:14
                    model: ["Не выбрано", "Одиночная задача", "Вторая", "Работа"]
                    onActivated: {}
                    font.family: localFont.name; font.weight: 400;
                }
            }
        }
        Button{
            id: but_add_newtask
            text: "Добавить"
            onClicked: newtask.visible=false
            x:10; y:630
            width: 200;height: 50
            font.family: localFont.name; font.weight: 400;

            background: Rectangle {
                 color: "lightgreen"
                 border.color: "green"
                 radius: 5
            }
        }
        Button{
            id: but_cancel
            text: "Отменить"
            onClicked: {newtask.visible=false}
            x:270; y:630
            width: 200;height: 50
            font.family: localFont.name; font.weight: 400;
            background: Rectangle {
                color: "#F15A5A"; border.color: "#D64141"; radius: 5}
        }
    }

    Connections {
        target: main_window

        onDetectedConflicts: {
            let client_task = conficted_tasks[0]
            let server_task = conficted_tasks[1]

            tab_merge_task.visible = !tab_merge_task.visible

            // tab_merge_task.ver_server.Text

        }

        onCloseWindow: {
            auth_window.hide()
        }
    }

}
