import QtQuick 2.15
import QtQuick.Layouts 1.15
import Qt5Compat.GraphicalEffects 1.0

Rectangle {
    id: customRectangle
    property string iconSource
    property string labelText
    property bool hovered: false
    property color textColor: (colorManager?.getColor["silver_gray"] ?? "FFFFFF")
    property color textColorHover: (colorManager?.getColor["default"] ?? "FFFFFF")
    signal clicked

    width: 200
    height: 65
    color: "transparent"

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true

        onEntered: {
            customRectangle.hovered = true;
        }

        onExited: {
            customRectangle.hovered = false;
        }

        onClicked: {
            customRectangle.clicked();
        }

        RowLayout {
            id: rowLayout
            anchors.fill: parent

            Image {
                id: icon
                source: customRectangle.iconSource
                sourceSize.width: 30
                sourceSize.height: 30

                ColorOverlay {
                    anchors.fill: parent
                    source: parent
                    color: (colorManager?.getColor["default"] ?? "FFFFFF")
                }
            }

            Text {
                id: label
                text: customRectangle.labelText
                font.pixelSize: 20
                color: customRectangle.hovered ? customRectangle.textColorHover : customRectangle.textColor
            }
        }
    }
}
