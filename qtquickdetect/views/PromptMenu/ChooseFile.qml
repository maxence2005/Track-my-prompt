import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15

Rectangle {
    id: chooseFileMainRectangle
    width: 600
    height: 100
    color: "#44464f"
    radius: 10
    Layout.alignment: Qt.AlignHCenter

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
                color: "#D4D4D4"
            }
        }

        Text {
            id: orText
            text: "or"
            font.pixelSize: 36
            color: "#B4B4B4"
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
            console.log("Lien saisi: " + linkInput.text)
        }
    }
}