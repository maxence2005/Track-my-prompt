import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15

Rectangle {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [chooseFileMainRectangle, "backgroundColor", "dark_bluish_gray"],
                [dragDropText, "color", "very_light_gray"],
                [orText, "color", "light_gray"]
            ])
        }
    }

    id: chooseFileMainRectangle
    property bool hovered: false
    property color backgroundColor: (colorManager?.getColorNoNotify("dark_bluish_gray") ?? "#000000")
    property color backgroundColorHover: (colorManager?.getColor["steel_gray"] ?? "#000000")

    width: 600
    height: 100
    color: hovered ? backgroundColorHover : backgroundColor
    radius: 10
    Layout.alignment: Qt.AlignHCenter

    // Propriété pour suivre si un fichier est en cours de glisser-déposer
    property bool isFileOver: false

    // Gérer les événements de drag and drop
    DropArea {
        id: dropArea
        anchors.fill: parent
        onEntered: function(drag) {
            // Vérifier si le drag contient des URLs (fichiers)
            if (drag.hasUrls) {
                drag.accept(Qt.CopyAction);  // Accepter l'action de copier
                chooseFileMainRectangle.hovered = true;  // Mettre en surbrillance le rectangle
            }
        }

        onExited: {
            chooseFileMainRectangle.hovered = false;  // Annuler la surbrillance du rectangle
        }

        onDropped: function(drag) {
            if (drag.hasUrls) {
                var fileUrl = drag.urls[0];  // Récupérer le premier fichier déposé
                backend.receiveFile(fileUrl);  // Envoyer l'URL du fichier au backend
                chooseFileMainRectangle.hovered = false;  // Annuler la surbrillance du rectangle
            }
        }
    }

    RowLayout {
        id: mainRowLayout
        anchors.centerIn: parent
        spacing: 50

        RowLayout {
            id: chooseFileMainRowLayout
            spacing: 10
            Image {
                id: uploadIcon
                source: "../imgs/upload.svg" // icône pour le drag and drop
                width: 40
                height: 40
            }

            Text {
                id: dragDropText
                text: "Drag\nand Drop "
                font.pixelSize: 18
                color: (colorManager?.getColorNoNotify("very_light_gray") ?? "#000000")
            }
        }

        Text {
            id: orText
            text: "or"
            font.pixelSize: 36
            color: (colorManager?.getColorNoNotify("light_gray") ?? "#000000")
        }

        RowLayout {
            id: iconRowLayout
            spacing: 15

            IconRectangle {
                id: camIcon
                imageSource: "../imgs/cam.svg" // Remplace par ton fichier SVG
            }

            IconRectangle {
                id: fileIcon
                imageSource: "../imgs/file.svg" // Remplace par ton fichier SVG
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        backend.openFileExplorer(); // Appeler la méthode pour ouvrir l'explorateur de fichiers
                    }
                }
            }

            IconRectangle {
                id: linkIcon
                imageSource: "../imgs/link.svg" // Remplace par ton fichier SVG
                MouseArea {
                    anchors.fill: parent
                    onClicked: linkDialog.open()
                }
            }
        }
    }

    Dialog {
        id: linkDialog
        title: "Saisir le lien"
        standardButtons: Dialog.Ok | Dialog.Cancel
        modal: true

        ColumnLayout {
            spacing: 10
            TextField {
                id: linkInput
                placeholderText: "Entrez le lien ici"
                Layout.preferredWidth: 500
                Layout.fillWidth: true
            }
        }

        onAccepted: {
            backend.receiveFile(linkInput.text);
        }
    }
}