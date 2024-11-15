
import QtQuick 2.15
import QtQuick.Controls 2.15

Text {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [titleText, "color", "default"],
            ])
        }
    }
    id: titleText
    text: qsTr("Settings")
    font.pixelSize: 40
    color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
    anchors.horizontalCenter: parent.horizontalCenter
    anchors.top: parent.top
    anchors.topMargin: 20
}