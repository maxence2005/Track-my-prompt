import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Button {
    id: buttonWithHover
    width: 180
    height: 50
    text: ""
    property string iconSource: ""
    property int topMargin: 0

    background: Rectangle {
        property bool hovered: false
        id: buttonBackground
        color: hovered ? (colorManager?.getColor["dark_gray"] ?? "FFFFFF") : "transparent"
        border.color: (colorManager?.getColor["very_dark_gray"] ?? "FFFFFF")
        border.width: 3
        radius: 8

        MouseArea {
            id: buttonMouseArea
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

    contentItem: ColumnLayout {
        id: buttonContent
        anchors.fill: parent
        Layout.alignment: Qt.AlignVCenter

        RowLayout {
            id: buttonRow
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: 10

            Image {
                id: buttonImage
                sourceSize.width: 30
                sourceSize.height: 30
                source: buttonWithHover.iconSource
                fillMode: Image.PreserveAspectFit
                Layout.alignment: Qt.AlignVCenter
                visible: buttonWithHover.iconSource !== ""
            }

            Text {
                id: buttonText
                height: 40
                text: buttonWithHover.text
                Layout.alignment: Qt.AlignVCenter
                color: (colorManager?.getColor["silver_gray"] ?? "FFFFFF")
                font.pixelSize: 16
                verticalAlignment: Text.AlignVCenter
            }
        }
    }
}