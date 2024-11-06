import QtQuick 2.15
import QtQuick.Layouts 1.15
import Qt5Compat.GraphicalEffects 1.0

Rectangle {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [colorOverlayIcon, "color", "default"]
            ])
        }
    }

    id: customRectangle
    property string iconSource
    property string labelText
    property bool hovered: false
    property color textColor: colorManager ? colorManager.getColorNoNotify("silver_gray") : "#000000"
    property color textColorHover: (colorManager ? colorManager.getColor["default"] : "#000000")
    
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

            Rectangle {
                width: icon.width
                height: icon.height
                color: "transparent"
                Image {
                    id: icon
                    source: customRectangle.iconSource
                    sourceSize.width: 30
                    sourceSize.height: 30
                }

                ColorOverlay {
                    id: colorOverlayIcon
                    anchors.fill: icon
                    source: icon
                    color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
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
