import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt5Compat.GraphicalEffects 1.0

Button {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [buttonBackground, "borderColor", "dark_bluish_gray"],
                [colorOverlay, "color", "default"],
                [buttonText, "color", "silver_gray"]
            ])
        }
    }
    id: buttonWithHover
    width: 180
    height: 50
    text: ""
    property string iconSource: ""
    property int topMargin: 0

    background: Rectangle {
        id: buttonBackground
        property bool hovered: false
        property color borderColor: colorManager?.getColorNoNotify("dark_bluish_gray") ?? "#000000"

        color: hovered ? (colorManager?.getColor["dark_gray"] ?? "#000000") : "transparent"
        border.color: borderColor
        border.width: 3
        radius: 8

        MouseArea {
            id: buttonMouseArea
            anchors.fill: parent
            hoverEnabled: true

            onEntered: {
                parent.hovered = true;
            }

            onExited: {
                parent.hovered = false;
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

            Row {
                width: buttonImage.width
                height: buttonImage.height
                Image {
                    id: buttonImage
                    sourceSize.width: 30
                    sourceSize.height: 30
                    source: buttonWithHover.iconSource
                    fillMode: Image.PreserveAspectFit
                    Layout.alignment: Qt.AlignVCenter
                    visible: buttonWithHover.iconSource !== ""
                }

                ColorOverlay {
                    id: colorOverlay
                    anchors.fill: buttonImage
                    source: buttonImage
                    color: (colorManager?.getColorNoNotify("default") ?? "#000000")
                }
            }

            Text {
                id: buttonText
                height: 40
                text: buttonWithHover.text
                Layout.alignment: Qt.AlignVCenter
                color: (colorManager?.getColorNoNotify("silver_gray") ?? "#000000")
                font.pixelSize: 16
                verticalAlignment: Text.AlignVCenter
            }
        }
    }
}
