import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    width: 800
    height: 600
    color: "#33343b" // Couleur de fond similaire à celle de l'image

    // Layout principal
    ColumnLayout {
        anchors.centerIn: parent
        spacing: 50

        // Section des exemples
        ColumnLayout {
            anchors.top: parent.top
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: 10

            Label {
                text: "Exemples"
                font.pixelSize: 24
                color: "white"
                horizontalAlignment: Text.AlignHCenter
                Layout.alignment: Qt.AlignHCenter
            }

            RowLayout {
                Layout.alignment: Qt.AlignHCenter
                spacing: 30

                Rectangle {
                    width: 200
                    height: 100
                    color: "#44464f"
                    radius: 10
                    Text {
                        anchors.centerIn: parent
                        width: parent.width - 20
                        text: "Trouver toutes les images de chiens parmi un ensemble d'images"
                        font.pixelSize: 16
                        color: "white"
                        horizontalAlignment: Text.AlignHCenter
                        wrapMode: Text.WordWrap
                    }
                }

                Rectangle {
                    width: 200
                    height: 100
                    color: "#44464f"
                    radius: 10
                    Text {
                        anchors.centerIn: parent
                        width: parent.width - 20
                        text: "Détecter le nombre de chats sur une vidéo en simultané"
                        font.pixelSize: 16
                        color: "white"
                        horizontalAlignment: Text.AlignHCenter
                        wrapMode: Text.WordWrap
                    }
                }
            }
        }
        // Section de Drag and Drop
        Rectangle {
            width: 600
            height: 100
            color: "#44464f"
            radius: 10
            Layout.alignment: Qt.AlignHCenter
            RowLayout {
                anchors.centerIn: parent
                spacing: 50
                RowLayout {
                    spacing: 10
                    Image {
                        source: "./imgs/upload.svg" // icône pour le drag and drop
                        width: 40
                        height: 40
                    }

                    Text {
                        text: "Drag\nand Drop "
                        font.pixelSize: 18
                        color: "#D4D4D4"
                    }
                }

                Text {
                    text: "or"
                    font.pixelSize: 36
                    color: "#B4B4B4"
                }

                RowLayout {
                    spacing: 15
                    Rectangle {
                        width: 64
                        height: 64
                        color: "#9A9B9F" // Couleur du carré de fond
                        radius: 10
                        Image {
                            source: "./imgs/cam.svg" // Remplace par ton fichier SVG
                            fillMode: Image.PreserveAspectFit
                            anchors.centerIn: parent
                            width: 40
                            height: 40
                        }
                    }

                    Rectangle {
                        width: 64
                        height: 64
                        color: "#9A9B9F" // Couleur du carré de fond
                        radius: 10
                        Image {
                            source: "./imgs/file.svg" // Remplace par ton fichier SVG
                            fillMode: Image.PreserveAspectFit
                            anchors.centerIn: parent
                            width: 40
                            height: 40
                        }
                    }

                    Rectangle {
                        width: 64
                        height: 64
                        color: "#9A9B9F" // Couleur du carré de fond
                        radius: 10
                        Image {
                            source: "./imgs/link.svg" // Remplace par ton fichier SVG
                            fillMode: Image.PreserveAspectFit
                            anchors.centerIn: parent
                            width: 40
                            height: 40
                        }
                    }
                }
            }
        }

        // Champ de saisie de prompt
        RowLayout {
            anchors.horizontalCenter: parent.horizontalCenter
            width: 700
            height: 50
            spacing: 20

            Rectangle {
                width: 50
                height: 50
                radius: 50
                color: "#40414E"

                Image {
                    source: "./imgs/wizard.png" // Remplace par ton fichier SVG
                    fillMode: Image.PreserveAspectFit
                    anchors.centerIn: parent
                    width: 30
                    height: 30
                }
            }

            Rectangle {
                width: 600
                height: 50
                color: "#44464f"
                radius: 10

                TextField {
                    id: promptInput
                    placeholderText: "Enter your prompt..."
                    font.pixelSize: 18
                    width: parent.width - 50 // Réduire la largeur pour faire de la place à l'image
                    height: parent.height
                    color: "#C5C5D1"
                    placeholderTextColor: "#C5C5D1"
                    background: Rectangle {
                        color: "transparent"
                    }
                }

                Image {
                    source: "./imgs/send.svg" // Remplacez par le chemin de votre icône d'envoi
                    width: 20
                    height: 20
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: parent.right
                    anchors.rightMargin: 10

                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            backend.receivePrompt(promptInput.text);
                        }
                    }
                }
            }
        }
    }

    // Titre principal
    Rectangle {
        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter
        width: parent.width
        height: 60
        color: "transparent"
        anchors.margins: 15

        Label {
            anchors.centerIn: parent
            text: "Track My Prompts"
            font.pixelSize: 32
            color: "white"
            horizontalAlignment: Text.AlignHCenter
            Layout.alignment: Qt.AlignHCenter
        }
    }
}
