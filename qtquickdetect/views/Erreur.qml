import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15

Rectangle {
    id: erreurRectangle
    visible: true
    width: parent.width
    height: parent.height
    property string errorMessage: ""

    Rectangle {
        id: backgroundParamRectangle
        width: parent.width
        height: parent.height
        color: "#2D2D3A" // Couleur d'arrière-plan

        // Conteneur pour le bouton de fermeture (croix)
        Rectangle {
            id: closeButtonContainer
            width: 30
            height: 30
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.margins: 10
            color: "transparent" // Pas de couleur pour que la croix elle-même reste visible

            Text {
                id: closeButtonText
                text: "✖" // Symbole de la croix
                color: "white"
                font.pixelSize: 24
                anchors.centerIn: parent
            }

            MouseArea {
                id: closeButtonMouseArea
                anchors.fill: parent
                onClicked: {
                    var sharedVar = backend.shared_variable;
                    sharedVar["Erreur"] = false;
                    backend.shared_variable = sharedVar;
                }
            }
        }

        // Conteneur vertical pour l'image, le texte et le bouton
        Column {
            id: contentColumn
            anchors.centerIn: parent
            width: parent.width - 50
            spacing: 25 // Espacement entre les éléments

            // Image du point d'interrogation
            Image {
                id: errorImage
                source: "imgs/erreur.png" // Assurez-vous que cette image existe dans vos ressources
                width: 80
                height: 80
                anchors.horizontalCenter: parent.horizontalCenter
            }

            // Texte du message d'erreur
            Text {
                id: errorMessageText
                text: erreurRectangle.errorMessage // Utilise une propriété pour définir dynamiquement le texte
                color: "red"
                font.pixelSize: 25
                anchors.horizontalCenter: parent.horizontalCenter
                width: parent.width // Ajuste la largeur pour tenir compte des marges
                wrapMode: Text.WordWrap // Permet le retour à la ligne automatique
                horizontalAlignment: Text.AlignHCenter
                visible: erreurRectangle.errorMessage.length > 0 // Visible seulement s'il y a un message d'erreur
            }

            // Bouton de fermeture en bas du message
            Rectangle {
                id: closeButton
                width: 120
                height: 40
                color: "#444" // Couleur du bouton
                radius: 10
                anchors.horizontalCenter: parent.horizontalCenter

                Text {
                    text: "Ok"
                    color: "white"
                    font.pixelSize: 20
                    anchors.centerIn: parent
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        var sharedVar = backend.shared_variable;
                        sharedVar["Erreur"] = false;
                        backend.shared_variable = sharedVar;
                    }
                    onEntered: {
                        closeButton.color = "#666";
                    }

                    onExited: {
                        closeButton.color = "#444";
                    }
                }
            }
        }
    }

    Connections {
        target: backend
        function onInfoSent(message) {
            erreurRectangle.errorMessage = message;
            var sharedVar = backend.shared_variable;
            sharedVar["Erreur"] = true;
            backend.shared_variable = sharedVar;
        }
    }
}
