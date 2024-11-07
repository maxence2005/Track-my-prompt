import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Image {
    anchors.fill: parent
    visible: model.type === "image"
    fillMode: Image.PreserveAspectFit

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        onEntered: overlay.visible = true
        onExited: overlay.visible = false
    }

    Item {
        id: overlay
        anchors.top: parent.top
        anchors.left: parent.left
        visible: false

        Row {
            spacing: 5

            Button {
                text: "Bouton 1"
                onClicked: {
                    // Fonction à exécuter pour le bouton 1
                }
            }

            Button {
                text: "Bouton 2"
                onClicked: {
                    // Fonction à exécuter pour le bouton 2
                }
            }
            // Ajouter d'autres boutons si nécessaire
        }
    }
}