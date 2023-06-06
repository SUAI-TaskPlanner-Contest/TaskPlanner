import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

Window {
    id: settingsWindow // идентификатор
    signal signalExit // задаем сигнал
    // visible: true // отображение
    FontLoader { id: localFont; source: "fonts/Inter-Thin.ttf" }
    FontLoader { id: localFont1; source: "fonts/Inter-ExtraLight.ttf" }
    x: Screen.width / 2 - width / 2
    y: Screen.height / 2 - height / 2
    width: 400// ширина окна
    height: 700// высота окна
    flags: Qt.FramelessWindowHint
    color: "transparent"
    property int previousX
    property int previousY

    MouseArea {
        anchors.fill: parent

        onPressed: {
            previousX = mouseX
            previousY = mouseY
        }

        onMouseXChanged: {
            var dx = mouseX - previousX
            settingsWindow.setX(settingsWindow.x + dx)
        }

        onMouseYChanged: {
            var dy = mouseY - previousY
            settingsWindow.setY(settingsWindow.y + dy)
        }
    }
    Rectangle {
        width: parent.width; height: parent.height
        anchors.bottom:parent.bottom // позиционирование
        border.width: 2
        border.color: "lightgrey"
        //radius: 60

        Rectangle {
            id: servertxt
            width: parent.width-40; height: 50

            anchors.margins: 20
            anchors.top:parent.top
            anchors.horizontalCenter: parent.horizontalCenter
            color: "transparent"

            Text {
                text: "Список серверов"
                color: "#232323"
                font.family: localFont1.name
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
                font.pointSize: 24; font.bold: true
                font.weight: 150
            }
        }
        Rectangle {
            id: emptyRectangle
            width: parent.width; height: 40
            anchors.top:servertxt.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            color: "transparent"

        }
        Rectangle {
            id: textServernametitle
            width: parent.width/3; height: 10
            anchors.left: parent.left

            anchors.margins: 5
            anchors.top:emptyRectangle.bottom
            color: "transparent"

            Text {
                text: "Сервер"
                color: "#232323"
                font.family: localFont1.name
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
                font.pointSize: 10; font.bold: true
                font.weight: 150
            }
        }

        Rectangle {
            id: textServerlogintitle
            width: parent.width/3-10; height: 10
            anchors.left: textServernametitle.right

            anchors.margins: 5
            anchors.top:emptyRectangle.bottom
            color: "transparent"

            Text {
                text: "Логин"
                color: "#232323"
                font.family: localFont1.name
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
                font.pointSize: 10; font.bold: true
                font.weight: 150
            }
        }
        Rectangle {
            id: severListviewRectangle
            anchors.top: textServernametitle.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.margins: 5
            color: "transparent"

            ListView {
                id: severListview
                anchors.fill: parent
                anchors.margins: 5
                model: settings_handler.model
                focus: true
                delegate: Item {
                        property int indexOfThisDelegate: index
                        width: parent.width; height: 60
                        Rectangle {
                            id:serverNameRec
                            anchors.verticalCenter: parent.verticalCenter
                            width: (parent.width / 3)
                            height: parent.height-10
                            anchors.left: severListview.left

                            // Устанавливаем текстовое поле для размещения индекса кнопки
                            Text {
                                id: textServername
                                anchors.fill: parent
                                text: model.modelData.server_name
                                font.family: localFont.name
                                verticalAlignment: Text.AlignVCenter
                                horizontalAlignment: Text.AlignHCenter
                            }
                        }
                        Rectangle {
                            id:serverLoginRec
                            anchors.left: serverNameRec.right
                            anchors.verticalCenter: parent.verticalCenter
                            width: (parent.width / 3) + 10
                            height: parent.height-10

                            // Устанавливаем текстовое поле для размещения индекса кнопки
                            Text {
                                id: textSeverlogin
                                anchors.fill: parent
                                text: model.modelData.user_email
                                font.family: localFont.name
                                verticalAlignment: Text.AlignVCenter
                                horizontalAlignment: Text.AlignHCenter
                            }
                        }
                        Button {
                            anchors.right: parent.right
                            text: "Удалить сервер"
                            font.family: localFont1.name
                            anchors.verticalCenter: parent.verticalCenter
                            width: (parent.width / 3) - 20
                            height: parent.height-25
                            hoverEnabled: false
                            background: Rectangle {
                                id: delitserver
                                color: "#F0F0F0"
                                border.color: "#848484"
                                border.width: 1
                                anchors.margins: 5
                                radius: 8
                            }
                            MouseArea{
                            anchors.fill: parent
                            hoverEnabled: true
                                    onEntered: {
                                        delitserver.color = "#C2C2C2" // Цвет при наведении на кнопку
                                    }
                                    onExited: {
                                        delitserver.color = "#F0F0F0" // Исходный цвет кнопки
                                    }
                                    onPressed: {
                                        delitserver.color = "#AAAAAA" // Цвет при нажатии кнопки\
                                        severListview.currentIndex = index;
                                        messageDialog.title = "Удаление сервера"
                                        messageDialog.informativeText = "В случае удаления сервера, все задачи на нем также будут удалены."
                                        messageDialog.open()
                                        //settings_handler.delete(index)
                                    }
                                    onReleased: {
                                        delitserver.color = "#D3D3D3" // Исходный цвет кнопки
                                    }
                            }
                        }
                }
            }
        }
    }
    Rectangle {
        width:100; height:30
        anchors.bottom:parent.bottom
        anchors.right: parent.right
        anchors.margins: 20
        Button {
            anchors.fill: parent
            text: "Закрыть"
            font.pointSize: 7
            font.weight: 150
            font.family: localFont1.name
            width: parent.width
            height: parent.height
            hoverEnabled: false
            background: Rectangle {
                id: clousButton
                color: "#F0F0F0"
                border.color: "#848484"
                border.width: 1
                radius: 8
            }
            MouseArea{
            anchors.fill: parent
            hoverEnabled: true
                    onEntered: {
                        clousButton.color = "#C2C2C2" // Цвет при наведении на кнопку
                    }
                    onExited: {
                        clousButton.color = "#F0F0F0" // Исходный цвет кнопки
                    }
                    onPressed: {
                        clousButton.color = "#AAAAAA" // Цвет при нажатии кнопки\
                        settingsWindow.close()
                    }
                    onReleased: {
                        clousButton.color = "#D3D3D3" // Исходный цвет кнопки
                    }
            }
        }
    }
    Rectangle {
        width:100; height:30
        anchors.bottom:parent.bottom
        anchors.left: parent.left
        anchors.margins: 20
        Button {
            anchors.fill: parent
            text: "Изменить PIN-код"
            font.pointSize: 7
            font.weight: 150
            font.family: localFont1.name
            width: (parent.width / 3)
            height: parent.height
            hoverEnabled: false
            background: Rectangle {
                id: pincodeButton
                color: "#F0F0F0"
                border.color: "#848484"
                border.width: 1
                radius: 8
            }
            MouseArea{
            anchors.fill: parent
            hoverEnabled: true
                    onEntered: {
                        pincodeButton.color = "#C2C2C2" // Цвет при наведении на кнопку
                    }
                    onExited: {
                        pincodeButton.color = "#F0F0F0" // Исходный цвет кнопки
                    }
                    onPressed: {
                        pincodeButton.color = "#AAAAAA" // Цвет при нажатии кнопки\
                        pincodeWindow.show()
                        settingsWindow.hide()
                    }
                    onReleased: {
                        pincodeButton.color = "#D3D3D3" // Исходный цвет кнопки
                    }
            }
        }
    }

    Rectangle {
        width:100; height:30
        anchors.bottom:parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.margins: 20
        Button {
            anchors.fill: parent
            text: "Добавить сервер"
            font.pointSize: 7
            font.weight: 150
            font.family: localFont1.name
            width: (parent.width / 3)
            height: parent.height
            hoverEnabled: false
            background: Rectangle {
                id: addserverButton
                color: "#F0F0F0"
                border.color: "#848484"
                border.width: 1
                radius: 8
            }
            MouseArea{
            anchors.fill: parent
            hoverEnabled: true
                    onEntered: {
                        addserverButton.color = "#C2C2C2" // Цвет при наведении на кнопку
                    }
                    onExited: {
                        addserverButton.color = "#F0F0F0" // Исходный цвет кнопки
                    }
                    onPressed: {
                        addserverButton.color = "#AAAAAA" // Цвет при нажатии кнопки\
                        addServerWindow.show()
                        settingsWindow.hide()
                    }
                    onReleased: {
                        addserverButton.color = "#D3D3D3" // Исходный цвет кнопки
                    }
            }
        }
    }

    MessageDialog {
        id: messageDialog
        modality: Qt.WindowModal
        buttons: MessageDialog.Ok | MessageDialog.Cancel
        onAccepted: {
            settings_handler.delete(severListview.currentIndex)
        }
        onRejected: messageDialog.close()
        Component.onCompleted: {
            messageDialog.standardButton(MessageDialog.Ok).text = "Продолжить"
            // messageDialog.standardButton(MessageDialog.Ok).font
        }
    }

    ChangePincodeWindow{
        id: pincodeWindow
    }

    AddServerWindow{
        id: addServerWindow
    }
}//Window