import QtQuick 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: customRectangle
    property string iconSource
    property string labelText
    signal clicked

    width: 200
    height: 65
    color: "transparent"

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true

        onEntered: {
            label.color = "#FFFFFF";
        }

        onExited: {
            label.color = "#CCCCCC";
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
            }

            Text {
                id: label
                text: customRectangle.labelText
                font.pixelSize: 20
                color: "#CCCCCC"
            }
        }
    }
}
