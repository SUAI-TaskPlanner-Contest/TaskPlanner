import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts
//Автоматизация через функции !
Window {
    id: mainWindow // идентификатор
    signal signalExit // задаем сигнал
    width: screen.width // ширина окна
    height: screen.height // высота окна
    title: ("Список задач")
    Rectangle{
    width: parent.width
    height: parent.height
        GridLayout{
            id: grid
            width: parent.width; height: parent.height
            columns: 2
            Rectangle{
                width: screen.width/2 - 500; height: screen.height
                color:"red"
                Layout.column: 2
                GridLayout{
                    width: parent.width; height: parent.height
                    rows:5
                    Rectangle{
                        Layout.row: 1
                        width: parent.width; height:100
                        Button {
                            id: button1
                            text: ("Диаграмма Ганта")
                            width: parent.width
                            height: parent.height

                            onClicked: {
                                mainWindow.signalExit() //вызываем сигнал
                            }
                        }
                    }
                    Rectangle{
                        Layout.row: 2
                        width: parent.width; height:100
                        Button {
                            id: button2
                            text: ("Синхронизация с сервером")
                            width: parent.width; height: parent.height

                            onClicked: {
                                mainWindow.signalExit() //вызываем сигнал
                            }
                        }
                    }
                    Rectangle{
                        Layout.row: 3
                        width: parent.width; height:100

                        Button {
                            id: button3
                            text: ("Смена темы")
                            width: parent.width; height: parent.height

                            onClicked: {
                                mainWindow.signalExit() //вызываем сигнал
                            }
                        }
                    }
                    Rectangle{
                        Layout.row: 4
                        width:parent.width; height:100

                        Button {
                            id: button4
                            text: ("Настройки")
                            width: parent.width; height: parent.height

                            onClicked: {
                                settingsWindow.show()
                            }
                        }
                    }
                    Rectangle{
                        Layout.row: 5
                        width:parent.width; height:100

                        Button {
                            id: button5
                            text: ("Выход")
                            width: parent.width; height: parent.height

                            onClicked: {
                                mainWindow.signalExit() //вызываем сигнал
                            }
                        }
                    }
                }
            }
            Rectangle{
                width: 100
                height: 100
                Layout.column: 1

                Button {
                    text: ("Правый")
                    width: parent.width; height: parent.height
                    anchors.centerIn: parent

                    onClicked: {
                        mainWindow.signalExit() //вызываем сигнал
                    }
                }
            }
        }
    }
    SettingsWindow{
    id: settingsWindow
    }
}
