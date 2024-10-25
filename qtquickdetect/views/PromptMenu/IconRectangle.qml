import QtQuick 2.0

Rectangle {
    property string imageSource: ""
    property bool hovered: false
    property color backgroundColor: (colorManager?.getColor["light_bluish_gray"] ?? "FFFFFF")
    property color backgroundColorHover: (colorManager?.getColor["light_gray"] ?? "FFFFFF")

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