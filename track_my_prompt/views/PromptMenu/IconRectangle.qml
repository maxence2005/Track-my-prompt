import QtQuick 2.0

Rectangle {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [iconRectangle, "backgroundColor", "light_bluish_gray"]
            ])
        }
    }

    id: iconRectangle
    property string imageSource: ""
    property bool hovered: false
    property color backgroundColor: (colorManager ? colorManager.getColorNoNotify("light_bluish_gray") : "#000000")
    property color backgroundColorHover: (colorManager ? colorManager.getColor["light_gray"] : "#000000")

    width: 64
    height: 64
    color: hovered ? backgroundColorHover : backgroundColor
    radius: 10

    Image {
        source: imageSource
        fillMode: Image.PreserveAspectFit
        anchors.centerIn: parent
        width: 40
        height: 40
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true

        onEntered: {
            parent.hovered = true
        }

        onExited: {
            parent.hovered = false
        }
    }
}