import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: mainWindow
    width: 640
    height: 480
    visible: true
    title: ("Переключение между окнами")

    Rectangle{
        anchors.fill: parent
        color:  "white"

        GridLayout{
            id: grid
            anchors.fill: parent

            rows: 2
            columns: 1

            Rectangle {
                Layout.fillHeight: true
                Layout.fillWidth: true
                Layout.column: 1
                Layout.row: 1
                //
                Button{
                    text:qsTr("1 окнo")
                    anchors.fill: parent
                    width: 300
                    height: 50

                    onClicked: {
                        firstWindow.show()
                        mainWindow.hide()
                    }
                }
            }
            Rectangle{
                Layout.fillHeight: true
                Layout.fillWidth: true
                Layout.column: 1
                Layout.row: 2
                //
                Button{
                    text:qsTr("2 окнo")
                    anchors.fill: parent


                    onClicked: {
                        secondWindow.show()
                        mainWindow.hide()
                        }
                    }
                }
            }
        }
    AnotherWindow{
        id: firstWindow
        title: qsTr("1 окнo")
        onSignalExit: {
            firstWindow.close()
            mainWindow.show()
        }
    }
    AnotherWindow{
        id: secondWindow
        title: qsTr("2 окнo")
        onSignalExit: {
            secondWindow.close()
            mainWindow.show()
        }
    }


}

