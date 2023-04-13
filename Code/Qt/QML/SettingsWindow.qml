import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts

Window {
    id: settingsWindow // идентификатор
    signal signalExit // задаем сигнал
    width: 400 // ширина окна
    height: 400 // высота окна
    title: ("Настройки")
    Rectangle{
        width: parent.width
        height: parent.height
        GridLayout{
            id: gridSetting
            width: parent.width
            height: parent.height
            columns: 4



        }
    }//Rectangle
}//Window