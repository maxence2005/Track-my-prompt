import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import Qt5Compat.GraphicalEffects 1.0

RowLayout {
    id: promptRowLayout
    anchors.horizontalCenter: parent.horizontalCenter
    width: parent.width
    height: 50
    spacing: 20

    Rectangle {
        id: wizardIconRectangle
        property bool hovered: false
        property color backgroundColor: (colorManager?.getColor["dark_gray"] ?? "FFFFFF")
        property color backgroundColorHover: (colorManager?.getColor["blue_gray"] ?? "FFFFFF")
        width: 50
        height: 50
        radius: 50
        color: hovered ? backgroundColorHover : backgroundColor

        Image {
            id: wizardIconImage
            source: "../imgs/wizard.png"
            fillMode: Image.PreserveAspectFit
            anchors.centerIn: parent
            width: 30
            height: 30
        }

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            onEntered: {
                wizardIconRectangle.hovered = true;
            }
            onExited: {
                wizardIconRectangle.hovered = false;
            }
        }

        ColorOverlay {
            anchors.fill: wizardIconImage
            source: wizardIconImage
            color: (colorManager?.getColor["default"] ?? "FFFFFF")
        }
    }

    Rectangle {
        id: promptInputRectangle
        Layout.fillWidth: true
        Layout.minimumWidth: 60
        Layout.maximumWidth: parent.width - 80 
        height: 50
        color: (colorManager?.getColor["dark_bluish_gray"] ?? "FFFFFF")
        radius: 10

        TextField {
            id: promptInputField
            placeholderText: "Enter your prompt..."
            font.pixelSize: 18
            anchors.fill: parent 
            color: (colorManager?.getColor["light_gray"] ?? "FFFFFF")
            placeholderTextColor: (colorManager?.getColor["blue_gray"] ?? "FFFFFF")
            background: Rectangle {
                color: "transparent"
            }
        }

        Image {
            id: sendIconImage
            source: "../imgs/send.svg"
            width: 20
            height: 20
            anchors.verticalCenter: parent.verticalCenter
            anchors.right: parent.right
            anchors.rightMargin: 10

            MouseArea {
                id: sendMouseArea
                anchors.fill: parent
                onClicked: {
                    backend.receivePrompt(promptInputField.text);
                }
            }
        }

        ColorOverlay {
            anchors.fill: sendIconImage
            source: sendIconImage
            color: (colorManager?.getColor["light_bluish_gray"] ?? "FFFFFF")
        }
    }
}
