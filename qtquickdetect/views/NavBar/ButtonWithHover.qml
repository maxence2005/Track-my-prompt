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
        id: buttonBackground
        color: "transparent"
        border.color: "#343541"
        border.width: 3
        radius: 8

        MouseArea {
            id: buttonMouseArea
            anchors.fill: parent
            hoverEnabled: true

            onEntered: {
                buttonBackground.color = "#444654";  // Couleur de fond au survol
            }

            onExited: {
                buttonBackground.color = "transparent";  // Couleur de fond par défaut
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
                color: "#CCCCCC"
                font.pixelSize: 16
                verticalAlignment: Text.AlignVCenter
            }
        }
    }
}