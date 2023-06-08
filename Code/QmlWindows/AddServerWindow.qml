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
    flags: Qt.FramelessWindowHint
    color: "transparent"
    modality: Qt.NonModal

    property int previousX
    property int previousY
    property int empty_imput_score

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
        //radius: 60
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
            id: emptyRectangle
            color: "transparent"
            anchors.top:addserversTxt.bottom
            width: 35; height: 40

        }
        Rectangle {
            id: serverurlTxtRectangle
            anchors.top:emptyRectangle.bottom
            width: parent.width-40; height: 30
            anchors.left: emptyRectangle.right
            color: "transparent"
            anchors.margins: 5
            Text {
                id: serverurlTxt
                text: "URL сервера"
                anchors.verticalCenter: parent.verticalCenter
                color: "#232323"
                font.family: localFont1.name
                font.pointSize: 14; font.bold: true
                font.weight: 150
            }
        }
        Rectangle {
            id: serverurlInputara
            anchors.top:serverurlTxtRectangle.bottom
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
                onPressed: {
                    serverurlTxt.color = "#232323"
                }
            }
        }
        Rectangle {
            id: server_nameTxtRectangle
            anchors.top:serverurlInputara.bottom
            width: parent.width-40; height: 30
            anchors.left: emptyRectangle.right
            color: "transparent"
            anchors.margins: 5
            Text {
                id: server_nameTxt
                text: "Название сервера"
                anchors.verticalCenter: parent.verticalCenter
                color: "#232323"
                font.family: localFont1.name
                font.pointSize: 14; font.bold: true
                font.weight: 150
            }
        }
        Rectangle {
            id: server_nameInputara
            anchors.top:server_nameTxtRectangle.bottom
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
                onPressed: {
                    server_nameTxt.color = "#232323"
                }
            }
        }
        Rectangle {
            id: user_emailTxtRectangle
            anchors.top:server_nameInputara.bottom
            width: parent.width-40; height: 30
            anchors.left: emptyRectangle.right
            color: "transparent"
            anchors.margins: 5
            Text {
                id: user_emailTxt
                text: "Почта"
                anchors.verticalCenter: parent.verticalCenter
                color: "#232323"
                font.family: localFont1.name
                font.pointSize: 14; font.bold: true
                font.weight: 150
            }
        }
        Rectangle {
            id: user_emailInputara
            anchors.top:user_emailTxtRectangle.bottom
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
                onPressed: {
                    user_emailTxt.color = "#232323"
                }
            }
        }

        Rectangle {
            id: user_passwordTxtRectangle
            anchors.top:user_emailInputara.bottom
            width: parent.width-40; height: 30
            anchors.left: emptyRectangle.right
            color: "transparent"
            anchors.margins: 5
            Text {
                id: user_passwordTxt
                text: "Пароль"
                anchors.verticalCenter: parent.verticalCenter
                color: "#232323"
                font.family: localFont1.name
                font.pointSize: 14; font.bold: true
                font.weight: 150
            }
        }
        Rectangle {
            id: user_passwordInputara
            anchors.top:user_passwordTxtRectangle.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width-40; height: 30
            anchors.margins: 5
            NumberAnimation on x{ // создание анимации "трясущихся" полей ввода
                id: user_password_shake_animation
                running: false
                from: 1
                to: 5
                loops: 5
                duration: 200
            }
            Timer {
                id: user_password_shake_timer
                interval: 5000  // Интервал в 5 секунд (в миллисекундах)
                repeat: false  // Остановиться после одного срабатывания

                onTriggered: {
                    user_password_shake_animation.stop()  // Остановить анимацию
                }
            }
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
                onPressed: {
                    user_passwordTxt.color = "#232323"
                }
            }
        }
        Rectangle {
            id: calendar_nameTxtRectangle
            anchors.top:user_passwordInputara.bottom
            anchors.left: emptyRectangle.right
            color: "transparent"
            width: parent.width-40; height: 30
            anchors.margins: 5
            Text {
                id: calendar_nameTxt
                text: "Название календаря"
                anchors.verticalCenter: parent.verticalCenter
                color: "#232323"
                font.family: localFont1.name
                font.pointSize: 14; font.bold: true
                font.weight: 150
            }
        }
        Rectangle {
            id: calendar_nameInputara
            anchors.top:calendar_nameTxtRectangle.bottom
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
                onPressed: {
                    calendar_nameTxt.color = "#232323"
                }
            }
        }
    }
    Rectangle {

        width:120; height:30
        anchors.bottom:parent.bottom
        anchors.left: parent.left
        anchors.margins: 20

        Button{
            text:("Добавить")
            width: parent.width; height: parent.height
            font.family: localFont1.name
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
                    addserverButton.color = "#AAAAAA" // Цвет при нажатии кнопки\addserverWindow.close()
                    empty_imput_score = 0
                    if(serverurl.text.length === 0){
                        serverurlTxt.color = "red"
                        empty_imput_score++
                    }
                    if(server_name.text.length === 0){server_nameTxt.color = "red"; empty_imput_score++}
                    if(user_email.text.length === 0){user_emailTxt.color = "red"; empty_imput_score++}
                    if(user_password.text.length === 0){
                        user_passwordTxt.color = "red";
                        empty_imput_score++
                    }
                    if(calendar_name.text.length === 0){calendar_nameTxt.color = "red"; empty_imput_score++}
                    if(empty_imput_score==0){
                        settings_handler.save_server (user_email.text, user_password.text, server_name.text, calendar_name.text, serverurl.text)
                        addserverWindow.close()
                        settingsWindow.show()
                    }
                }
                onReleased: {
                    addserverButton.color = "#D3D3D3" // Исходный цвет кнопки
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
                    addserverWindow.close()
                    settingsWindow.show()
                    calendar_nameTxt.color = "#232323"
                    user_passwordTxt.color = "#232323"
                    user_emailTxt.color = "#232323"
                    server_nameTxt.color = "#232323"
                    serverurlTxt.color = "#232323"

                }
                onReleased: {
                    closeButton.color = "#D3D3D3" // Исходный цвет кнопки
                }
            }
        }
    }

}