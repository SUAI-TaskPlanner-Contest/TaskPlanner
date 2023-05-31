import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import QtQuick 2.15

ApplicationWindow {
    id: mainWindow
    visible: true
    width: 600
    height: 340
    //color: "#ffffff"
    title: "Окно ошибки"
    color: "transparent"
    flags: Qt.FramelessWindowHint 

    minimumWidth: 600
    minimumHeight: 340
    maximumWidth: 600
    maximumHeight: 340

    
    // название ошибки
    Text {
        id: textEdit1
        color: "#000000"
        text: errorInfo.name
        onTextChanged: errorInfo.name = text
        font.pixelSize: 36
        horizontalAlignment: Text.AlignHCenter
        x: 210
        y: 60
        //anchors.horizontalCenter: parent.horizontalCenter
        //anchors.verticalCenter: parent.verticalCenter * 1.5
        font.family: localFont1.name
    }

    background: Rectangle {
        visible: true
        id: rectangle
        width: parent.width
        height: parent.height

        FontLoader { id: localFont; source: "fonts/Inter-Thin.ttf" }
        FontLoader { id: localFont1; source: "fonts/Inter-ExtraLight.ttf" }

        border.color: "lightgrey"
        border.width: 2
        color: "#ffffff"
        radius: 60

        ColumnLayout {
            width: parent.width
            height: parent.height * 0.6
            spacing: 0
            
        Rectangle {
            id: rectangle1
            width: rectangle.width
            height: rectangle.height*0.35
            radius: 60
            color: "transparent"
        }

        // текст ошибки
        Text {
            id: textEdit

            width: parent.width 
            height: parent.height * 0.5

            text: errorInfo.text
            onTextChanged: errorInfo.text = text
            font.pixelSize: 18
            horizontalAlignment: Text.AlignJustify
            verticalAlignment: Text.AlignTop

            rightPadding: 40
            leftPadding: 40
            font.bold: false
            wrapMode: Text.Wrap
            Layout.fillWidth: true

            font.family: localFont1.name

            Rectangle {
                x: Text.x
                y: Text.y
                width: Text.width
                height: Text.height
                color: "#00fbf9ff"
                anchors.fill: Text

            }
        }
        }
        // левая кнопка
        Button {
            id: button_ok
            text: errorInfo.button_ok
            font.capitalization: Font.MixedCase
            font.bold: false
            font.family: localFont1.name
            checkable: true
            font.pointSize: 14
            flat: false
            display: AbstractButton.TextOnly
            Layout.preferredWidth: 150 // Установка ширины кнопки
            Layout.preferredHeight: 45 // Установка высоты кнопки
            
            hoverEnabled: false

            palette.buttonText: "black"
            x: 100
            y: 270
            rightPadding: 20
            leftPadding: 20
            topPadding: 10
            bottomPadding: 10

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
                    buttonHandler.button_ok_clicked();
                }
            }
        }

        // правая кнопка
        Button {
            id: button_cancel
            text: errorInfo.button_cancel
            font.capitalization: Font.MixedCase
            font.pointSize: 14
            checkable: true
            flat: false
            
            Layout.preferredWidth: 150 // Установка ширины кнопки
            Layout.preferredHeight: 45 // Установка высоты кнопки

            font.bold: false
            font.family: localFont1.name
            display: AbstractButton.TextOnly
            hoverEnabled: false
            palette.buttonText: "black"

            x: 350
            y: 270
            rightPadding: 30
            leftPadding: 30
            topPadding: 10
            bottomPadding: 10
            
            background: Rectangle {
                id: button_2_bg
                color: "#F0F0F0"
                radius: 15
                border.color: "#848484"
            }

            
            MouseArea {
                id: buttonArea2
                anchors.fill: parent
                hoverEnabled: true
                onEntered: {
                    button_2_bg.color = "#C2C2C2"; // Цвет при наведении на кнопку
                }
                onExited: {
                    button_2_bg.color = "#F0F0F0"; // Исходный цвет кнопки
                }
                onPressed: {
                    button_2_bg.color = "#AAAAAA"; // Цвет при нажатии кнопки
                }
                onReleased: {
                    button_2_bg.color = "#F0F0F0"; // Исходный цвет кнопки
                    buttonHandler.button_cancel_clicked();
                }
            }
        }
    }
}
