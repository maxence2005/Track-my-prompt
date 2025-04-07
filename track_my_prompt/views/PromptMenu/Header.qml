import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [headerLabel, "color", "default"]
            ])
        }
    }

    id: headerRectangle
    width: parent.width
    height: 60
    color: "transparent"
    anchors.margins: 15

    Label {
        id: headerLabel
        anchors.centerIn: parent
        text: "Track My Prompts"
        font.pixelSize: parent.width / 15
        color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")

        horizontalAlignment: Text.AlignHCenter
        Layout.alignment: Qt.AlignHCenter
    }
}