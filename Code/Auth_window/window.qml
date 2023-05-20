import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

// Основное окно
ApplicationWindow {
    visible: true
    id: rectangle
    width: 400
    height: 530
    color: "transparent"
    title: "Окно авторизации"
    
    flags: Qt.FramelessWindowHint
    
    minimumWidth: rectangle.width
    minimumHeight: rectangle.height
    maximumWidth: rectangle.width
    maximumHeight: rectangle.height

    FontLoader { id: localFont; source: "fonts/Inter-Thin.ttf" }
    FontLoader { id: localFont1; source: "fonts/Inter-ExtraLight.ttf" }

    background: Rectangle {
        visible: true
        id: rectangle1
        width: parent.width
        height: parent.height
        border.color: "lightgrey"
        border.width: 2
        color: "#ffffff"
        radius: 60
    }

    Text {
        id: text4
        x: 97
        y: 35
        width: 206
        height: 46
        color: "black"
        text: qsTr("TaskPlanner")
        horizontalAlignment: Text.AlignHCenter

        font.bold: false
        font.family: localFont1.name
        font.pixelSize: 36
    }

    // Логин
    TextField {
        id: textInput3
        x: 75
        y: 107
        width: 250
        height: 41
        visible: true
        placeholderText: qsTr("Nextcloud логин")
        horizontalAlignment: Text.AlignLeft
        color: "#000000"
        verticalAlignment: Text.AlignVCenter
        leftPadding: 20
        clip: false
    
        font.pixelSize: 18
        font.bold: false
        font.family: localFont1.name

        background: Rectangle {
            x: 120
            y: 107
            width: textInput3.width
            height: textInput3.height
            color: "#00979699"
            border.color: "#848484"
            border.width: 1
            anchors.fill: textInput3
            radius: 15
        }
    

    }

    // Password
    TextField {
        id: textInput1
        x: 75
        y: 171
        width: 250
        height: 41
        visible: true
        placeholderText: qsTr("Nextcloud пароль")
        horizontalAlignment: Text.AlignLeft
        verticalAlignment: Text.AlignVCenter
        leftPadding: 20
        color: "#000000"
        clip: false

        echoMode : TextInput.Password
        
        font.pixelSize: 18
        font.bold: false
        font.family: localFont1.name

        background: Rectangle {
            x: 120
            y: 107
            width: textInput1.width
            height: textInput1.height
            color: "#00ffffff"
            border.color: "#848484"
            border.width: 1
            anchors.fill: textInput1
            radius: 15
        }
    }

    // Адрес календаря
    TextField {
        id: textInput2
        x: 75
        y: 235
        width: 250
        height: 41
        visible: true
        color: "#000000"
        placeholderText: qsTr("Адрес календаря")
        verticalAlignment: Text.AlignVCenter
        leftPadding: 20
        clip: false

        font.pixelSize: 18
        font.bold: false
        font.family: localFont1.name

        background: Rectangle {
            x: 120
            y: 107
            width: textInput2.width
            height: textInput2.height
            color: "#00fbf9ff"
            border.color: "#848484"
            border.width: 1
            anchors.fill: textInput2
            radius: 15
        }
    }

    // Ссылка на сервер
    TextField {
        id: textInput4
        x: 75
        y: 299
        width: 250
        height: 41
        visible: true
        color: "#000000"
        placeholderText: qsTr("Ссылка на сервер")
        verticalAlignment: Text.AlignVCenter
        leftPadding: 20
        clip: false

        font.pixelSize: 18
        font.bold: false
        font.family: localFont1.name

        background: Rectangle {
            x: 120
            y: 107
            width: textInput4.width
            height: textInput4.height
            color: "#00fbf9ff"
            border.color: "#848484"
            border.width: 1
            anchors.fill: textInput4
            radius: 15
        }
    }

    Button {
        id: button
        x: 75
        y: 369
        width: 250
        height: 39
        text: qsTr("Войти")
       
        checkable: true
        palette.buttonText: "black"

        font.pixelSize: 20
        font.bold: false
        font.family: localFont1.name

        signal loginClicked(string login, string password, string calendarAddress, string serverLink)

        background: Rectangle {
            id: button_1_bg
            color: "#F0F0F0"
            radius: 15
            border.color: "#848484"
        }

        MouseArea {
            id: buttonArea1
            anchors.fill: parent
            hoverEnabled: true
            onEntered: {
                button_1_bg.color = "#C2C2C2"; // Цвет при наведении на кнопку
            }
            onExited: {
                button_1_bg.color = "#F0F0F0"; // Исходный цвет кнопки
            }
            onPressed: {
                button_1_bg.color = "#AAAAAA"; // Цвет при нажатии кнопки
            }
            onReleased: {
                button_1_bg.color = "#F0F0F0"; // Исходный цвет кнопки
                buttonHandler.loginClicked(textInput3.text, textInput1.text, textInput2.text, textInput4.text)
            }
        }
        
    }

    Text {
        id: text1
        x: 163
        y: 419

        width: 162
        height: 20
        color: "#000000"

        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignTop
        styleColor: "#000000"

        font.bold: false
        font.family: localFont1.name
        font.pixelSize: 15
        
        text: qsTr("Продолжить локально")
        MouseArea {
            id: buttonArea2
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
            
            onEntered: {
                text1.color = "#C2C2C2"; // Цвет при наведении на кнопку
            }
            onExited: {
                text1.color = "#000000"; // Исходный цвет кнопки
            }
            onPressed: {
                text1.color = "#AAAAAA"; // Цвет при нажатии кнопки
            }
            onReleased: {
                text1.color = "#000000"; // Исходный цвет кнопки
                buttonHandler.localareaClicked();
            }
        }
    }

    Text {
        id: text_for_errors
        x: 64
        y: 464
        width: 273
        height: 55
        text: buttonHandler.errorText
        font.pixelSize: 14
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        font.bold: false
        font.family: localFont1.name
    }
}
