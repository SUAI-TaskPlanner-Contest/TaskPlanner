import QtQuick 2.0
import QtQuick.Controls 6.4
import TaskPlanner

// Основное окно
Rectangle {
    id: rectangle
    width: 400
    height: 480
    color: "#ffffff"

    // Логин
    TextInput {
        id: textInput3
        x: 75
        y: 107
        width: 250
        height: 41
        visible: true
        text: qsTr("Логин")
        font.pixelSize: 16
        horizontalAlignment: Text.AlignLeft
        color: "#757575"
        verticalAlignment: Text.AlignVCenter
        leftPadding: 20
        font.bold: true
        clip: false

        Rectangle {
            x: 120
            y: 107
            width: textInput3.width
            height: textInput3.height
            color: "#00979699"
            border.color: "#b2a7a7a7"
            border.width: 1
            anchors.fill: textInput3
            radius: 4
        }
    }

    // Password
    TextInput {
        id: textInput1
        x: 75
        y: 171
        width: 250
        height: 41
        visible: true
        text: qsTr("Пароль")
        font.pixelSize: 16
        horizontalAlignment: Text.AlignLeft
        verticalAlignment: Text.AlignVCenter
        leftPadding: 20
        echoMode: TextInput.Normal
        font.bold: true
        color: "#757575"
        clip: false

        Rectangle {
            x: 120
            y: 107
            width: textInput1.width
            height: textInput1.height
            color: "#00ffffff"
            border.color: "#b2a7a7a7"
            border.width: 1
            anchors.fill: textInput1
            radius: 4
        }
    }

    // Адрес календаря
    TextInput {
        id: textInput2
        x: 75
        y: 235
        width: 250
        height: 41
        visible: true
        color: "#757575"
        text: qsTr("Адрес календаря")
        font.pixelSize: 16
        verticalAlignment: Text.AlignVCenter
        leftPadding: 20
        font.bold: true
        clip: false

        Rectangle {
            x: 120
            y: 107
            width: textInput2.width
            height: textInput2.height
            color: "#00fbf9ff"
            border.color: "#b2a7a7a7"
            border.width: 1
            anchors.fill: textInput2
            radius: 4
        }
    }

    Button {
        id: button
        x: 75
        y: 306
        width: 250
        height: 39
        text: qsTr("Войти")
        font.capitalization: Font.Capitalize
        font.italic: false
        font.bold: true
        checkable: false
        font.pointSize: 14
        flat: false
        display: AbstractButton.TextOnly

        background: Rectangle {
            color: "#8282F6"
            radius: 5
        }
    }

    Text {
        id: text4
        x: 97
        y: 35
        width: 206
        height: 46
        color: "#252040"
        text: qsTr("TaskPlanner")
        font.pixelSize: 36
        horizontalAlignment: Text.AlignHCenter
        font.bold: true
    }

    Text {
        id: text1
        x: 163
        y: 355

        width: 162
        height: 20
        color: "#000000"

        font.pixelSize: 15
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignTop
        font.strikeout: false
        font.italic: false
        font.bold: false
        styleColor: "#0600ff"

        text: "Продолжить локально"
        MouseArea {
            anchors.fill: parent
            anchors.rightMargin: 0
            anchors.bottomMargin: 0
            anchors.leftMargin: 0
            anchors.topMargin: 0
            cursorShape: Qt.PointingHandCursor
        }
    }

    TextEdit {
        id: textEdit
        x: 64
        y: 400
        width: 273
        height: 55
        text: qsTr("Поле для ошибок")
        font.pixelSize: 14
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }

    states: [
        State {
            name: "clicked"
            when: button.checked
        }
    ]
}
