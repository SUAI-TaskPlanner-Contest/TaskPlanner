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
    modality: (1)
}//Window