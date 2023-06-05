import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: addserverWindow // идентификатор
    // signal signalExit // задаем сигнал
    x: Screen.width / 2 - width / 2
    y: Screen.height / 2 - height / 2
    FontLoader { id: localFont; source: "fonts/Inter-Thin.ttf" }
    FontLoader { id: localFont1; source: "fonts/Inter-ExtraLight.ttf" }
    width: 400// ширина окна
    height: 700// высота окна
    // flags: Qt.FramelessWindowHint
    // color: "transparent"
    modality: Qt.NonModal

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
            addserverWindow.setX(addserverWindow.x + dx)
        }

        onMouseYChanged: {
            var dy = mouseY - previousY
            addserverWindow.setY(addserverWindow.y + dy)
        }
    }
    Rectangle{
        width: parent.width; height: parent.height
        anchors.top:parent.top // позиционирование
        anchors.left: parent.left
        anchors.right: parent.right
        border.width: 2
        border.color: "lightgrey"
        radius: 60
        Rectangle{
            id: addserversTxt
            width: parent.width-40; height: 40

            anchors.margins: 20
            anchors.top:parent.top
            anchors.horizontalCenter: parent.horizontalCenter

            Text {
                text: "Добавление сервера"
                anchors.verticalCenter: parent.verticalCenter
                color: "#232323"
                font.family: localFont1.name
                anchors.horizontalCenter: parent.horizontalCenter
                font.pointSize: 24; font.bold: true
                font.weight: 150
            }
        }
        Rectangle {
            id: serverurlTxt
            anchors.top:addserversTxt.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width-40; height: 30
            anchors.margins: 5
            Text {
                text: "URL сервера"
                anchors.verticalCenter: parent.verticalCenter
                color: "#232323"
                font.family: localFont1.name
                anchors.horizontalCenter: parent.horizontalCenter
                font.pointSize: 14; font.bold: true
                font.weight: 150
            }
        }
        Rectangle {
            id: serverurlInputara
            anchors.top:serverurlTxt.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width-40; height: 30
            anchors.margins: 5
            TextField {
                id: serverurl
                anchors.horizontalCenter: parent.horizontalCenter
                width: parent.width-40
                height: parent.height
                placeholderText: qsTr("Введите URL сервера")
                horizontalAlignment: TextInput.AlignHCenter
                verticalAlignment: TextInput.AlignVCenter
                font.family: localFont1.name
                font.weight: 400
                font.pointSize: 14
                color: "#000000"
                font.pixelSize: 16
            }
        }
        Rectangle {
            id: server_nameTxt
            anchors.top:serverurlInputara.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width-40; height: 30
            anchors.margins: 5
            Text {
                text: "Название сервера"
                anchors.verticalCenter: parent.verticalCenter
                color: "#232323"
                font.family: localFont1.name
                anchors.horizontalCenter: parent.horizontalCenter
                font.pointSize: 14; font.bold: true
                font.weight: 150
            }
        }
        Rectangle {
            id: server_nameInputara
            anchors.top:server_nameTxt.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width-40; height: 30
            anchors.margins: 5
            TextField {
                id: server_name
                anchors.horizontalCenter: parent.horizontalCenter
                width: parent.width-40
                height: parent.height
                placeholderText: qsTr("Введите название сервера")
                horizontalAlignment: TextInput.AlignHCenter
                verticalAlignment: TextInput.AlignVCenter
                font.family: localFont1.name
                font.weight: 400
                font.pointSize: 14
                color: "#000000"
                font.pixelSize: 16
            }
        }
        Rectangle {
            id: user_emailTxt
            anchors.top:server_nameInputara.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width-40; height: 30
            anchors.margins: 5
            Text {
                text: "Почта"
                anchors.verticalCenter: parent.verticalCenter
                color: "#232323"
                font.family: localFont1.name
                anchors.horizontalCenter: parent.horizontalCenter
                font.pointSize: 14; font.bold: true
                font.weight: 150
            }
        }
        Rectangle {
            id: user_emailInputara
            anchors.top:user_emailTxt.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width-40; height: 30
            anchors.margins: 5
            TextField {
                id: user_email
                anchors.horizontalCenter: parent.horizontalCenter
                width: parent.width-40
                height: parent.height
                placeholderText: qsTr("Введите почту")
                horizontalAlignment: TextInput.AlignHCenter
                verticalAlignment: TextInput.AlignVCenter
                font.family: localFont1.name
                font.weight: 400
                font.pointSize: 14
                color: "#000000"
                font.pixelSize: 16
            }
        }

        Rectangle {
            id: user_passwordTxt
            anchors.top:user_emailInputara.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width-40; height: 30
            anchors.margins: 5
            Text {
                text: "Пароль"
                anchors.verticalCenter: parent.verticalCenter
                color: "#232323"
                font.family: localFont1.name
                anchors.horizontalCenter: parent.horizontalCenter
                font.pointSize: 14; font.bold: true
                font.weight: 150
            }
        }
        Rectangle {
            id: user_passwordInputara
            anchors.top:user_passwordTxt.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width-40; height: 30
            anchors.margins: 5
            TextField {
                id: user_password
                anchors.horizontalCenter: parent.horizontalCenter
                width: parent.width-40
                placeholderText: qsTr("Введите пароль")
                height: parent.height
                horizontalAlignment: TextInput.AlignHCenter
                verticalAlignment: TextInput.AlignVCenter
                font.family: localFont1.name
                font.weight: 400
                font.pointSize: 14
                color: "#000000"
                font.pixelSize: 16
            }
        }
        Rectangle {
            id: calendar_nameTxt
            anchors.top:user_passwordInputara.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width-40; height: 30
            anchors.margins: 5
            Text {
                text: "Название календаря"
                anchors.verticalCenter: parent.verticalCenter
                color: "#232323"
                font.family: localFont1.name
                anchors.horizontalCenter: parent.horizontalCenter
                font.pointSize: 14; font.bold: true
                font.weight: 150
            }
        }
        Rectangle {
            id: calendar_nameInputara
            anchors.top:calendar_nameTxt.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width-40; height: 30
            anchors.margins: 5
            TextField {
                id: calendar_name
                anchors.horizontalCenter: parent.horizontalCenter
                width: parent.width-40
                placeholderText: qsTr("Введите название календаря")
                height: parent.height
                horizontalAlignment: TextInput.AlignHCenter
                verticalAlignment: TextInput.AlignVCenter
                font.family: localFont1.name
                font.weight: 400
                font.pointSize: 14
                color: "#000000"
                font.pixelSize: 16
            }
        }
    }
    Rectangle {

        width:120; height:30
        anchors.bottom:parent.bottom
        anchors.left: parent.left
        anchors.margins: 20

        Button{
            id: addserverButton
            text:("Добавить")
            width: parent.width; height: parent.height
            font.family: localFont1.name

            onClicked: { //действия при нажатии кнопки
                addserverWindow.close()
                settingsWindow.show()
                settings.save_server (user_email.text, user_password.text, server_name.text, calendar_name.text, serverurl.text)

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
                addserverWindow.close()
                settingsWindow.show()
            }
        }
    }

}