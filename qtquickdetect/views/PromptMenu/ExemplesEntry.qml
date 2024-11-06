import QtQuick 2.15

Rectangle {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [entryRectangle, "backgroundColor", "dark_bluish_gray"],
                [entryTextItem, "color", "default"]
            ])
        }
    }

    id: entryRectangle
    property string entryText
    property bool hovered: false
    property color backgroundColor: (colorManager ? colorManager.getColorNoNotify("dark_bluish_gray") : "#000000");
    property color backgroundColorHover: (colorManager ? colorManager.getColor["blue_gray"] : "#000000");
    
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
        color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
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