import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15

RowLayout {
    id: promptRowLayout
    anchors.horizontalCenter: parent.horizontalCenter
    width: 700
    height: 50
    spacing: 20

    Rectangle {
        id: wizardIconRectangle
        width: 50
        height: 50
        radius: 50
        color: "#444654"

        Image {
            id: wizardIconImage
            source: "../imgs/wizard.png" // Remplace par ton fichier SVG
            fillMode: Image.PreserveAspectFit
            anchors.centerIn: parent
            width: 30
            height: 30
        }

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            onEntered: {
                wizardIconRectangle.color = "#66687d";
            }
            onExited: {
                wizardIconRectangle.color = "#444654";
            }
        }
    }

    Rectangle {
        id: promptInputRectangle
        width: 600
        height: 50
        color: "#44464F"
        radius: 10

        TextField {
            id: promptInputField
            placeholderText: "Enter your prompt..."
            font.pixelSize: 18
            width: parent.width - 50 // Réduire la largeur pour faire de la place à l'image
            height: parent.height
            color: "#B0B0B0"
            placeholderTextColor: "#66687D"
            background: Rectangle {
                color: "transparent"
            }
        }

        Image {
            id: sendIconImage
            source: "../imgs/send.svg" // Remplacez par le chemin de votre icône d'envoi
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
    }
}
