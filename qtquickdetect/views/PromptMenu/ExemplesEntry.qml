import QtQuick 2.15

Rectangle {
    id: entryRectangle
    property string entryText
    property bool hovered: false
    property color backgroundColor: (colorManager?.getColor["dark_bluish_gray"] ?? "FFFFFF");
    property color backgroundColorHover: (colorManager?.getColor["blue_gray"] ?? "FFFFFF");
    
    width: 200
    height: 100
    color: hovered ? backgroundColorHover : backgroundColor
    radius: 10

    Text {
        id: entryTextItem
        anchors.centerIn: parent
        width: parent.width - 20
        text: entryText
        font.pixelSize: 16
        color: (colorManager?.getColor["default"] ?? "FFFFFF")
        horizontalAlignment: Text.AlignHCenter
        wrapMode: Text.WordWrap
    }

    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        onEntered: {
            entryRectangle.hovered = true;
        }
        onExited: {
            entryRectangle.hovered = false;
        }
    }
}