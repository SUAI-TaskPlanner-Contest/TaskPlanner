import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: authWindow
    width: screen.width
    height: screen.height
    visible: true
    title: ("Окно авторизации")

    Rectangle{
            width: 500
            height: 300
            anchors.centerIn:parent
            color:  "grey"

        GridLayout{
            id: grid
            anchors.fill: parent

            x:screen.width/2 - width
            y:screen.height/2 -height

            anchors.margins:30
            rows: 3
            columns: 1

            //Login
            Rectangle{
                Layout.column: 1
                Layout.row: 1
                width:parent.width
                height:25

                TextInput{
                    id: loginId
                    text: "Login"
                    cursorVisible: false
                }
            }

            //Password
            Rectangle{
                Layout.column: 1
                Layout.row: 2
                width:parent.width
                height:25
                anchors.margins:10

                TextInput{
                    id: passwordId
                    text: "Password"
                    cursorVisible: false
                }
            }
            Rectangle {
                Layout.column: 1
                Layout.row: 3

                width:parent.width
                height:40
                anchors.margins:10
                Button{
                    text:("Вход")
                    width: parent.width
                    height: parent.height

                    onClicked: {
                        firstWindow.show()
                        instructionWindow.show()
                        authWindow.hide()
                    }
                }
            }
        }
    }
    MainWindow{
        id: firstWindow
        onSignalExit: {
            firstWindow.close()
            authWindow.show()
        }
    }
    InstructionWindow{
        id: instructionWindow
    }
}