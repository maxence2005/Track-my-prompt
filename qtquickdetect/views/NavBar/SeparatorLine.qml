import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [separatorLine, "color", "dark_gray"]
            ])
        }
    }

    id: separatorRectangle
    width: parent.width
    height: 20
    color: "transparent"

    Rectangle {
        id: separatorLine
        height: 2
        width: parent.width * 0.8
        color: (colorManager?.getColorNoNotify("dark_gray") ?? "#000000")
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 10
    }
}