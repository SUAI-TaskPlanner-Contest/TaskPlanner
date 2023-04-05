import QtQuick
import QtQuick.Window
import QtQuick.Controls

Window {
    id: anotherWindow // идентификатор
    signal signalExit // задаем сигнал
    width: 480 // ширина окна
    height: 320 // высота окна

    //кнопка для открывания главного окна приложения
    Button {
        // id: button1
        text: ("Главное окно")
        width: 480
        height: 320
        anchors.centerIn: parent
        onClicked: {
           anotherWindow.signalExit() //вызываем сигнал
        }

    }

}
