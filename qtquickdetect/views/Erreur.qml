import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([[backgroundParamRectangle, "color", "very_dark_gray"], [closeButton, "color", "gray"], [closeButtonText, "color", "default"]])
        }
    }

    id: erreurRectangle
    visible: true
    width: parent.width
    height: parent.height
    property string errorMessage: ""

    Rectangle {
        id: backgroundParamRectangle
        width: parent.width
        height: parent.height
        color: (colorManager ? colorManager.getColorNoNotify("very_dark_gray") : "#000000") // Couleur d'arrière-plan

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
                color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
                font.pixelSize: 24
                anchors.centerIn: parent
            }

            MouseArea {
                id: closeButtonMouseArea
                anchors.fill: parent
                onClicked: {
                    backend.toggle_erreur();
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
                color: (colorManager ? colorManager.getColorNoNotify("gray") : "#000000") // Couleur du bouton
                radius: 10
                anchors.horizontalCenter: parent.horizontalCenter

                Text {
                    text: "Ok"
                    color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
                    font.pixelSize: 20
                    anchors.centerIn: parent
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        backend.toggle_erreur();
                    }
                    onEntered: {
                        closeButton.color = (colorManager ? colorManager.getColorNoNotify("medium_gray") : "#000000");
                    }

                    onExited: {
                        closeButton.color = (colorManager ? colorManager.getColorNoNotify("gray") : "#000000");
                    }
                }
            }
        }
    }

    Connections {
        target: backend
        function onInfoSent(message) {
            let msg = {
                "no_data_saved" : qsTr("Error: No image/video saved."),
                "missing_mistral_api_key" : qsTr("Error: Please provide an API key for Mistral."),
                "wrong_file_type" : qsTr("Error: The file is not an image or a video."),
                "prompt_err" : qsTr("Error processing the prompt, try again, check your internet connection, rewrite the prompt, check your API key, or change the method.")
            }

            erreurRectangle.errorMessage = msg[message] !== undefined ? msg[message] : message;
            backend.toggle_erreur();
        }
    }
}
