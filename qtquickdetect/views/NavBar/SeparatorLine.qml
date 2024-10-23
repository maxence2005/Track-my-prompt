import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: separatorRectangle
    width: parent.width
    height: 20
    color: "transparent"

    Rectangle {
        id: separatorLine
        height: 2
        width: parent.width * 0.8
        color: "#40414F"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 10
    }
}