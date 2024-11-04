import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import Qt5Compat.GraphicalEffects 1.0

RowLayout {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [wizardIconRectangle, "backgroundColor", "dark_gray"],
                [promptInputRectangle, "color", "dark_bluish_gray"],
                [promptInputField, "color", "light_gray"],
                [promptInputField, "placeholderTextColor", "blue_gray"],
                [sendColorOverlay, "color", "light_bluish_gray"]
            ])
        }
    }

    id: promptRowLayout
    anchors.horizontalCenter: parent.horizontalCenter
    width: 700
    height: 50
    spacing: 20

    Rectangle {
        id: wizardIconRectangle
        property bool hovered: false
        property color backgroundColor: (colorManager?.getColorNoNotify("dark_gray") ?? "#000000")
        property color backgroundColorHover: (colorManager?.getColor["blue_gray"] ?? "#000000")
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
            color: (colorManager?.getColorNoNotify("default") ?? "#000000")
        }
    }

    Rectangle {
        id: promptInputRectangle
        width: 600
        height: 50
        color: (colorManager?.getColorNoNotify("dark_bluish_gray") ?? "#000000")
        radius: 10

        TextField {
            id: promptInputField
            placeholderText: "Enter your prompt..."
            font.pixelSize: 18
            width: parent.width - 50 // Réduire la largeur pour faire de la place à l'image
            height: parent.height
            color: (colorManager?.getColorNoNotify("light_gray") ?? "#000000")
            placeholderTextColor: (colorManager?.getColorNoNotify("blue_gray") ?? "#000000")
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
            id: sendColorOverlay
            anchors.fill: sendIconImage
            source: sendIconImage
            color: (colorManager?.getColorNoNotify("light_bluish_gray") ?? "#000000")
        }
    }
}
