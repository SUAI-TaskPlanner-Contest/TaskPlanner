import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts

Window {
    id: settingsWindow // идентификатор
    signal signalExit // задаем сигнал
    visible: true // отображение
    FontLoader { id: localFont; source: "pics/Inter-Thin.ttf" }
    FontLoader { id: localFont1; source: "pics/Inter-ExtraLight.ttf" }
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
    Rectangle{

        width: parent.width; height: parent.height
        anchors.bottom:parent.bottom // позиционирование
        border.width: 2
        border.color: "lightgrey"
        //radius: 60

        Rectangle{
            id: servertxt
            width: parent.width-40; height: 50

            anchors.margins: 20
            anchors.top:parent.top
            anchors.horizontalCenter: parent.horizontalCenter

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
            id: severListview
            anchors.top: servertxt.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            height: 40*serverModel.count
            anchors.margins: 5



            Component {
                id: serverDelegate
                Item {
                    width: parent.width; height: 40

                        Rectangle {
                            id:serverNameRec
                            width: (parent.width / 3)
                            height: parent.height
                            anchors.left: severListview.left

                            // Устанавливаем текстовое поле для размещения индекса кнопки
                            Text {
                                id: textServername
                                anchors.fill: parent
                                text: '<b>Сервер:</b> ' + model.modelData.server_name
                                font.family: localFont.name
                                verticalAlignment: Text.AlignVCenter
                                horizontalAlignment: Text.AlignHCenter
                            }
                        }
                        Rectangle {
                            id:serverLoginRec
                            anchors.left: serverNameRec.right
                            width: (parent.width / 3)
                            height: parent.height

                            // Устанавливаем текстовое поле для размещения индекса кнопки
                            Text {
                                id: textSeverlogin
                                anchors.fill: parent
                                text: '<b>Логин:</b> ' + model.modelData.server_login
                                font.family: localFont.name
                                verticalAlignment: Text.AlignVCenter
                                horizontalAlignment: Text.AlignHCenter
                            }
                        }
                        Button {
                            id: delitserver
                            anchors.right: parent.right
                            text: "Удалить сервер"
                            font.family: localFont1.name
                            width: (parent.width / 3)
                            height: parent.height

                            onClicked: {
                            if(serverModel.get(index).servername!="Nextcloud")
                                {
//                                    serverModel.remove(index)
                                }
                            }
                        }

                }
            }

            ListView {
                anchors.fill: parent
                model: settings.model
                delegate: serverDelegate
                focus: true
            }
        }
    }
    Rectangle {
        width:120; height:30
        anchors.bottom:parent.bottom
        anchors.right: parent.right
        anchors.margins: 20
        Button {
            id: clousButton
            anchors.fill: parent
            text: "Закрыть"
            font.family: localFont1.name
            width: parent.width
            height: parent.height

            onClicked: {
                onClicked: {
                    settingsWindow.close()
                }
            }
        }
    }
    Rectangle {
        width:120; height:30
        anchors.bottom:parent.bottom
        anchors.left: parent.left
        anchors.margins: 20
        Button {
            id: pincodeButton
            anchors.fill: parent
            text: "Изменить PIN-код"
            font.family: localFont1.name
            width: (parent.width / 3)
            height: parent.height

            onClicked: {
                onClicked: {
                    pincodeWindow.show()
                    settingsWindow.hide()
                }
            }
        }
    }

    Rectangle {
        width:120; height:30
        anchors.bottom:parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.margins: 20
        Button {
            id: addserverButton
            anchors.fill: parent
            text: "Добавить сервер"
            font.family: localFont1.name
            width: (parent.width / 3)
            height: parent.height

            onClicked: {
                onClicked: {
                    addserverWindow.show()
                    settingsWindow.hide()
                }
            }
        }
    }

    PincodeWindow{
        id: pincodeWindow
    }
    AddserverWindow{
        id: addserverWindow
    }
}//Window