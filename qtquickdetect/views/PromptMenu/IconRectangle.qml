import QtQuick 2.0

Rectangle {
    property string imageSource: ""

    width: 64
    height: 64
    color: "#9A9B9F"
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
            parent.color = "#B0B0B0"
        }

        onExited: {
            parent.color = "#9A9B9F"
        }
    }
}