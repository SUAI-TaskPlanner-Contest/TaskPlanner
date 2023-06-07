import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

ApplicationWindow { // окно
    id: pincode_window
    title: "Инструкция по работе в приложении"
    width: 720; height: 480
    visible: true // отображение
    color: "transparent"
    flags: Qt.FramelessWindowHint // Отключаем обрамление окна

    Rectangle {
    visible: true
    id: rect_for_invis_border
    width: parent.width
    height: parent.height
    border.color: "lightgrey"
    border.width: 2
    radius: 60
    color: "transparent"
    }


    background: Rectangle {
        id: rect_for_workspace
        width: parent.width
        height: parent.height

        border.color: "lightgrey"
        border.width: 2
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        radius: 60

        FontLoader { id: localFont; source: "fonts/Inter-Thin.ttf" }
        FontLoader { id: localFont1; source: "fonts/Inter-ExtraLight.ttf" }

        Text {
            text: "Введите пинкод"
            font.family: localFont.name
            font.pointSize: 32
            font.weight: 500
            font.letterSpacing: 11.2
            color: "#232323"
            leftPadding: 28
            topPadding: 30
            bottomPadding: 20
            anchors.horizontalCenter: parent.horizontalCenter
            x: 50; y: 10
        }

        Text {
            text: "Введите пинкод"
            width: parent.width // задаем максимальную ширину текста
            wrapMode: Text.Wrap // включаем перенос текста на новую строку
            font.family: localFont1.name
            font.weight: 400
            font.pointSize: 18
            color: "#000000"
            leftPadding: 60
            rightPadding: 50
            topPadding: 20
            anchors.horizontalCenter: parent.horizontalCenter
            padding: 10
            x: 0; y: 100
        }
        Rectangle {

        width: parent.width; height: parent.height
        color: "transparent"

             NumberAnimation on x{ // создание анимации "трясущихся" полей ввода
                id: shake_animation
                running: false
                from: 1
                to: 5
                loops: 5
                duration: 200
            }

            Timer {
                id: shake_timer
                interval: 5000  // Интервал в 5 секунд (в миллисекундах)
                repeat: false  // Остановиться после одного срабатывания

                onTriggered: {
                    shake_animation.stop()  // Остановить анимацию
                }
            }

        Row {
            y: 220
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: 25

                TextField {
                    id: pinInput0
                    width: 60
                    height: 80
                    background: Rectangle {
                                    color: "#F0F0F0"
                                    radius: 17
                                    border.color: "#848484"
                                    border.width: 1
                                }
                    horizontalAlignment: TextInput.AlignHCenter
                    verticalAlignment: TextInput.AlignVCenter
                    font.family: localFont1.name
                    font.weight: 400
                    font.pointSize: 18
                    color: "#000000"
                    font.pixelSize: 32
                    maximumLength: 1
                    onTextChanged: {
                        if (text.length === 1) { // перевод фокуса на следующий TextField при заполнении предыдущего
                            pinInput1.forceActiveFocus()
                        }
                    }
                    KeyNavigation.right: pinInput1 // переход на следующий TextField при нажатии клавиши влево
                }

                TextField {
                    id: pinInput1
                    width: 60; height: 80
                    background: Rectangle {
                                    color: "#F0F0F0"
                                    radius: 17
                                    border.color: "#848484"
                                    border.width: 1
                                }
                    horizontalAlignment: TextInput.AlignHCenter
                    verticalAlignment: TextInput.AlignVCenter
                    font.family: localFont1.name
                    font.weight: 400
                    font.pointSize: 18
                    color: "#000000"
                    font.pixelSize: 32
                    maximumLength: 1
                    onTextChanged: {
                        if (text.length === 1) { // перевод фокуса на следующий TextField при заполнении предыдущего
                            pinInput2.forceActiveFocus()
                        }
                    }
                    KeyNavigation.right: pinInput2 // переход на следующий TextField при нажатии клавиши влево
                }

                TextField {
                    id: pinInput2
                    width: 60
                    height: 80
                    background: Rectangle {
                                    color: "#F0F0F0"
                                    radius: 17
                                    border.color: "#848484"
                                    border.width: 1
                                }
                    horizontalAlignment: TextInput.AlignHCenter
                    verticalAlignment: TextInput.AlignVCenter
                    font.family: localFont1.name
                    font.weight: 400
                    font.pointSize: 18
                    color: "#000000"
                    font.pixelSize: 32
                    maximumLength: 1
                    onTextChanged: {
                        if (text.length === 1) { // перевод фокуса на следующий TextField при заполнении предыдущего
                            pinInput3.forceActiveFocus()
                        }
                    }
                    KeyNavigation.right: pinInput3 // переход на следующий TextField при нажатии клавиши влево
                }

                TextField {
                    id: pinInput3
                    width: 60
                    height: 80
                    background: Rectangle {
                                    color: "#F0F0F0"
                                    radius: 17
                                    border.color: "#848484"
                                    border.width: 1
                                }
                    horizontalAlignment: TextInput.AlignHCenter
                    verticalAlignment: TextInput.AlignVCenter
                    font.family: localFont1.name
                    font.weight: 400
                    font.pointSize: 18
                    color: "#000000"
                    font.pixelSize: 32
                    maximumLength: 1
                    onTextChanged: {

                    }
                }
}
        }

        Text {
            text: "Вы сможете изменить свой pin-код в любой момент в меню Настроек."
            width: parent.width // задаем максимальную ширину текста
            wrapMode: Text.Wrap // включаем перенос текста на новую строку
            font.family: localFont1.name
            font.weight: 300
            font.pointSize: 12
            color: "#000000"
            leftPadding: 90
            rightPadding: 50
            topPadding: 10
            padding: 10
            anchors.horizontalCenter: parent.horizontalCenter
            x: 0; y: 320
        }

        Button{
            text: "Далее"
            font.family: localFont1.name
            font.pointSize: 18
            font.weight: 200
            x: 465; y: 380
            width: 180;height: 50
            hoverEnabled: false

            background: Rectangle {
                id: createPinButton
                color: "#F0F0F0"
                border.color: "#848484"
                border.width: 1
                radius: 13
            }
            MouseArea{
            anchors.fill: parent
            hoverEnabled: true
                    onEntered: {
                        createPinButton.color = "#C2C2C2" // Цвет при наведении на кнопку
                    }
                    onExited: {
                        createPinButton.color = "#D3D3D3" // Исходный цвет кнопки
                    }
                    onPressed: {
                        createPinButton.color = "#AAAAAA" // Цвет при нажатии кнопки

                        if (pinInput0.text.length === 0 ||
                            pinInput1.text.length === 0 ||
                            pinInput2.text.length === 0 ||
                            pinInput3.text.length === 0) {

                            shake_animation.start()
                            shake_timer.start()
                        }
                        else {
                            if (pincode_handler.novice) {
                                pincode_handler.set_pincode(pinInput0.text +
                                                         pinInput1.text +
                                                         pinInput2.text +
                                                         pinInput3.text)
                                main_handler.set_services()
                                mainWindow.show()
                                pincode_window.hide()
                            }
                            else {
                                pincode_handler.check_pincode(pinInput0.text +
                                                         pinInput1.text +
                                                         pinInput2.text +
                                                         pinInput3.text)
                                if (pincode_handler.verify_pin) {
                                    main_handler.set_services()
                                    mainWindow.show()
                                    pincode_window.hide()
                                }
                                else {
                                    shake_animation.start()
                                    shake_timer.start()
                                }
                            }

                        }
                    }
                    onReleased: {
                        createPinButton.color = "#D3D3D3" // Исходный цвет кнопки
                    }
            }

        }


    }

    MainWindow {
        id: mainWindow
    }
}