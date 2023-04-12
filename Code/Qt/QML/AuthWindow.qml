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
//            x:screen.width/2 - width
//            y:screen.height/2 -height

//            color:  "red"
            color:  "grey"

        GridLayout{
            id: grid
            anchors.fill: parent
//          width: 10
//          height: 10
            x:screen.width/2 - width
            y:screen.height/2 -height
//          anchors.topMargin:30
//          anchors.bottomMargin:30
            anchors.margins:30
            rows: 3
            columns: 1
             //Login
            Rectangle{
//                Layout.fillHeight: true
//                Layout.fillWidth: true
                Layout.column: 1
                Layout.row: 1
                width:parent.width
                height:25
//                anchors.margins:40
//                anchors.bottom:40
                TextInput{

                    id: loginId
                    text: "Login"
                    cursorVisible: false
                }
            }
            //Password
            Rectangle{
//                Layout.fillHeight: true
//                Layout.fillWidth: true
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
//                Layout.fillHeight: true
//                Layout.fillWidth: true
                Layout.column: 1
                Layout.row: 3
//                color: "red"
                //
                width:parent.width
                height:40
                anchors.margins:10
                Button{
                    text:("Вход")
//                    anchors.fill: parent
//                    x:100
//                    y:100
                    width: parent.width
                    height: parent.height

                    onClicked: {
                        firstWindow.show()
                        authWindow.hide()
                    }
                }
            }
        }
    }
    MainWindow{
        id: firstWindow
//        title: ("Список задач")
            onSignalExit: {
                firstWindow.close()
                authWindow.show()
        }
    }
}