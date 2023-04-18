import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow { // окно
    id: authWindow;
    width: screen.width; height: screen.height
    visible: true // отображение
    title: ("Окно авторизации")

    Rectangle{ // область для авторизации
            width: 500; height: 300
            anchors.centerIn:parent // позиционирование
            color:  "grey"

        GridLayout{ // разбиваем на сетку
            id: grid
            anchors.fill: parent // заполняем сетку во весь объект указанного выше
            anchors.margins:30 //смещения объекта с 4 сторон
            rows: 3; columns: 1

            //Login
            Rectangle{
                Layout.column: 1; Layout.row: 1
                width:parent.width; height:25

                TextInput{
                    id: loginId
                    text: "Login"
                }
            }

            //Password
            Rectangle{
                Layout.column: 1; Layout.row: 2
                width:parent.width; height:25

                TextInput{
                    id: passwordId
                    text: "Password"
                }
            }
            //кнопка входа
            Rectangle {
                Layout.column: 1; Layout.row: 3

                width:parent.width; height:40

                Button{
                    text:("Вход")
                    width: parent.width; height: parent.height

                    onClicked: { //действия при нажатии кнопки
                        mainWindow.show()
                        instructionWindow.show()
                        authWindow.hide() //окно авторизации сворачиваем
                    }
                }
            }
        }
    }
    MainWindow{ //окно список задач
        id: mainWindow
        onSignalExit: {
            mainWindow.close()
            authWindow.show()
        }
    }
    InstructionWindow{ //окно инструкции
        id: instructionWindow
    }
}