import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts

Rectangle{
    Layout.column: 0
    width: parent.width/8
    height: task_rect.height
    radius: height / 2
    property string msg: ""
    color: "transparent"
    Text{
        anchors.centerIn: parent
        renderType: Text.NativeRendering
        text: "%1".arg(msg)
    //    %1 - первая позиция, добавить текст, %2 - вторая позиция добавляем *, как для выбранного элемента
    }
    MouseArea {
        anchors.fill: parent
        onClicked: view.currentIndex = model.index
    }
}