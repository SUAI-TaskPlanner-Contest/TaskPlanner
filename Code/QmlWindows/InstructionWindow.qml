import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts

Window {
    id: instructionWindow // идентификатор
    signal signalExit // задаем сигнал
    width: 300 // ширина окна
    height: 300 // высота окна
    title: ("Инструкция")
    modality: (1)

}