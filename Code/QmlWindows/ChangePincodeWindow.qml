import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: pincodeWindow // идентификатор
    signal signalExit // задаем сигнал
    x: Screen.width / 2 - width / 2
    y: Screen.height / 2 - height / 2
    FontLoader { id: localFont; source: "fonts/Inter-Thin.ttf" }
    FontLoader { id: localFont1; source: "fonts/Inter-ExtraLight.ttf" }
    width: 400// ширина окна
    height: 700// высота окна
    flags: Qt.FramelessWindowHint
    color: "transparent"

    property int empty_imput_score
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
            pincodeWindow.setX(pincodeWindow.x + dx)
        }

        onMouseYChanged: {
            var dy = mouseY - previousY
            pincodeWindow.setY(pincodeWindow.y + dy)
        }
    }
    background: Rectangle{
        width: parent.width; height: parent.height
        anchors.top:parent.top // позиционирование
        anchors.left: parent.left
        anchors.right: parent.right
        border.width: 2
        border.color: "lightgrey"
        //radius: 60
    }
        Rectangle {
            id: emptyRectangle3
            color: "transparent"
            anchors.top:parent.top
            width: 35; height: 30

        }
        Rectangle{
            id: pinTxt
            width: parent.width-40; height: 40

            anchors.margins: 20
            anchors.top:emptyRectangle3.bottom
            anchors.horizontalCenter: parent.horizontalCenter

            Text {
                text: "Изменение PIN-кода"
                anchors.verticalCenter: parent.verticalCenter
                color: "#232323"
                font.family: localFont1.name
                anchors.horizontalCenter: parent.horizontalCenter
                font.pointSize: 24; font.bold: true
                font.weight: 150
            }
        }
        Rectangle {
            id: emptyRectangle1
            color: "transparent"
            anchors.top:pinTxt.bottom
            width: 35; height: 80

        }
        Rectangle {
            id: oldpinTxtRectangle
            anchors.top:emptyRectangle1.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width-40; height: 40
            anchors.margins: 20
            Text {
                text: "Введите старый PIN-кода"
                id: oldpinTxt
                anchors.verticalCenter: parent.verticalCenter
                color: "#232323"
                font.family: localFont1.name
                anchors.horizontalCenter: parent.horizontalCenter
                font.pointSize: 18; font.bold: true
                font.weight: 150
            }
        }
        Rectangle {
            id: oldpinInputara
            anchors.top:oldpinTxtRectangle.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width-40; height: 40
            anchors.margins: 20
            TextField {
                id: oldpin
                anchors.horizontalCenter: parent.horizontalCenter
                width: 160
                height: parent.height
                horizontalAlignment: TextInput.AlignHCenter
                verticalAlignment: TextInput.AlignVCenter
                font.family: localFont1.name
                font.weight: 400
                font.pointSize: 18
                color: "#000000"
                font.pixelSize: 32
                onPressed: {
                    oldpinTxt.color = "#232323"
                }
            }
        }
        Rectangle {
            id: emptyRectangle2
            color: "transparent"
            anchors.top:oldpinInputara.bottom
            width: 35; height: 40

        }
        Rectangle {
            id: newpinTxtRectangle
            anchors.top:emptyRectangle2.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width-40; height: 40
            anchors.margins: 20
            Text {
                id: newpinTxt
                text: "Введите новый PIN-кода"
                anchors.verticalCenter: parent.verticalCenter
                color: "#232323"
                font.family: localFont1.name
                anchors.horizontalCenter: parent.horizontalCenter
                font.pointSize: 18; font.bold: true
                font.weight: 150
            }
        }
        Rectangle {
            id: newpinInputara
            anchors.top:newpinTxtRectangle.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width-40; height: 40
            anchors.margins: 20
            TextField {
                id: newpin
                anchors.horizontalCenter: parent.horizontalCenter
                width: 160
                height: parent.height
                horizontalAlignment: TextInput.AlignHCenter
                verticalAlignment: TextInput.AlignVCenter
                font.family: localFont1.name
                font.weight: 400
                font.pointSize: 18
                color: "#000000"
                font.pixelSize: 32
                onPressed: {
                    newpinTxt.color = "#232323"
                }
            }
        }



    Rectangle {

        width:120; height:30
        anchors.bottom:parent.bottom
        anchors.left: parent.left
        anchors.margins: 20

        Button{
            text:("Сохранить PIN-код")
            width: parent.width; height: parent.height
            font.family: localFont1.name
            hoverEnabled: false
            background: Rectangle {
                id: savepinButton
                color: "#F0F0F0"
                border.color: "#848484"
                border.width: 1
                radius: 8
            }
            MouseArea{
                anchors.fill: parent
                hoverEnabled: true
                onEntered: {
                    savepinButton.color = "#C2C2C2" // Цвет при наведении на кнопку
                }
                onExited: {
                    savepinButton.color = "#F0F0F0" // Исходный цвет кнопки
                }
                onPressed: {
                    savepinButton.color = "#AAAAAA" // Цвет при нажатии кнопки\addserverWindow.close()
                    empty_imput_score = 0
                    if(oldpin.text.length != 4){oldpinTxt.color = "red"; empty_imput_score++}
                    if(newpin.text.length != 4){newpinTxt.color = "red"; empty_imput_score++}
                    if(empty_imput_score==0){
                        settings_handler.save_pincode(oldpin.text, newpin.text)
                        pincodeWindow.close()
                        settingsWindow.show()
                    }

                }
                onReleased: {
                    savepinButton.color = "#D3D3D3" // Исходный цвет кнопки
                }
            }
        }
    }
    Rectangle {
        width:120; height:30
        anchors.bottom:parent.bottom
        anchors.right: parent.right
        anchors.margins: 20
        Button {
            anchors.fill: parent
            text: "Закрыть"
            font.family: localFont1.name
            width: (parent.width / 3)
            height: parent.height
            hoverEnabled: false
            background: Rectangle {
                id: closeButton
                color: "#F0F0F0"
                border.color: "#848484"
                border.width: 1
                radius: 8
            }
            MouseArea{
                anchors.fill: parent
                hoverEnabled: true
                onEntered: {
                    closeButton.color = "#C2C2C2" // Цвет при наведении на кнопку
                }
                onExited: {
                    closeButton.color = "#F0F0F0" // Исходный цвет кнопки
                }
                onPressed: {
                    closeButton.color = "#AAAAAA" // Цвет при нажатии кнопки\addserverWindow.close()
                    pincodeWindow.close()
                    settingsWindow.show()
                    newpinTxt.color = "#232323"
                    oldpinTxt.color = "#232323"

                }
                onReleased: {
                    closeButton.color = "#D3D3D3" // Исходный цвет кнопки
                }
            }
        }
    }
}