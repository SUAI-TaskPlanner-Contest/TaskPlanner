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
    modality: (1)

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
        radius: 60
    }
        Rectangle{
            id: pinTxt
            width: parent.width-40; height: 40

            anchors.margins: 20
            anchors.top:parent.top
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
            id: oldpinTxt
            anchors.top:pinTxt.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width-40; height: 40
            anchors.margins: 20
            Text {
                text: "Введите старый PIN-кода"
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
            anchors.top:oldpinTxt.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width-40; height: 40
            anchors.margins: 20
            TextField {
                id: oldpin
                anchors.horizontalCenter: parent.horizontalCenter
                width: 160
                height: parent.height
                validator: IntValidator {
                    bottom: 0
                    top: 9999
                }
                horizontalAlignment: TextInput.AlignHCenter
                verticalAlignment: TextInput.AlignVCenter
                font.family: localFont1.name
                font.weight: 400
                font.pointSize: 18
                color: "#000000"
                font.pixelSize: 32
            }
        }
        Rectangle {
            id: newpinTxt
            anchors.top:oldpinInputara.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width-40; height: 40
            anchors.margins: 20
            Text {
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
            anchors.top:newpinTxt.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width-40; height: 40
            anchors.margins: 20
            TextField {
                id: newpin
                anchors.horizontalCenter: parent.horizontalCenter
                width: 160
                height: parent.height
                validator: IntValidator {
                    bottom: 0
                    top: 9999
                }
                horizontalAlignment: TextInput.AlignHCenter
                verticalAlignment: TextInput.AlignVCenter
                font.family: localFont1.name
                font.weight: 400
                font.pointSize: 18
                color: "#000000"
                font.pixelSize: 32
            }
        }



    Rectangle {

        width:120; height:30
        anchors.bottom:parent.bottom
        anchors.left: parent.left
        anchors.margins: 20

        Button{
            id: savepinButton
            text:("Сохранить PIN-код")
            width: parent.width; height: parent.height
            font.family: localFont1.name

            onClicked: { //действия при нажатии кнопки
                pincodeWindow.close()
                settingsWindow.show()
                settings.save_pincode(oldpin.text, newpin.text)
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
            width: (parent.width / 3)
            height: parent.height

            onClicked: {
                pincodeWindow.close()
                settingsWindow.show()
            }
        }
    }
}