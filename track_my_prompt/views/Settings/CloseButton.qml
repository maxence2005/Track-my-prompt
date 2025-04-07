
import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [closeButtonText, "color", "default"],
            ])
        }
    }
    id: closeButtonContainer
    width: 30
    height: 30
    anchors.top: parent.top
    anchors.right: parent.right
    anchors.margins: 10
    color: "transparent"

    Text {
        id: closeButtonText
        text: "✖" 
        color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
        font.pixelSize: 24
        anchors.centerIn: parent
    }

    MouseArea {
        id: closeButtonMouseArea
        anchors.fill: parent
        onClicked: {
            closeButtonMouseArea.forceActiveFocus();
            backend.toggle_param();
        }
    }
}