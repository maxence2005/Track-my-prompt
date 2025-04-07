import QtQuick 2.15
import QtQuick.Controls 2.15
import Qt5Compat.GraphicalEffects 1.0

Rectangle {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [container, "color", "anthracite_gray"],
                [promptHistorique, "color", "silver_gray"],
                [promptInput, "color", "silver_gray"],
                [backgroundRectangle, "borderColor", "dark_bluish_gray"],
                [colorOverlayModifyIcon, "color", "default"],
                [colorOverlayTrashIcon, "color", "default"],
                [colorOverlayImageIcon, "color", "default"]
            ]);
        }
    }

    id: container
    width: parent.width * 0.8
    height: 40
    color: (colorManager ? colorManager.getColorNoNotify("anthracite_gray") : "#000000")
    border.width: 1
    radius: 8
    anchors.horizontalCenter: parent.horizontalCenter
    property string promptText: ""
    property int caseID: model.pageID
    property bool isEditing: false

    Rectangle {
        id: backgroundRectangle
        anchors.fill: parent
        property bool hovered: hoverArea.containsMouse
        property color borderColor: colorManager ? colorManager.getColorNoNotify("dark_bluish_gray") : "#000000"

        color: hovered ? (colorManager ? colorManager.getColor["dark_gray"] : "#333333") : "transparent"
        border.color: borderColor
        border.width: 3
        radius: 8
    }

    MouseArea {
        id: hoverArea
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
        onClicked: {
            if (backend.shared_variable["Chargement"] == false) {
                backend.startOnFalse()
                
                backend.retrievePage(container.caseID); // Appelle la méthode du backend
            }
            else {
                backend.infoSent("history_cannot_change_on_loading");
            }
        }
    }

    Row {
        anchors.fill: parent
        padding: 10
        spacing: 10
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.left: parent.left
        
        // Image à gauche
        Rectangle {
            width: imageIcon.width
            height: imageIcon.height
            color: "transparent"
            Image {
                id: imageIcon
                width: 20
                height: 20
                source: "../imgs/Message.png"
            }

            ColorOverlay {
                id: colorOverlayImageIcon
                anchors.fill: imageIcon
                source: imageIcon
                color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
            }
        }

        // Item qui contient le texte et le champ de saisie pour la superposition
        Item {
            width: container.width * 0.45
            height: parent.height

            // Texte normal
            Text {
                id: promptHistorique
                text: promptText !== "" ? promptText : "pas de prompt"
                font.pixelSize: 18
                color: (colorManager?.getColorNoNotify("silver_gray") ?? "#000000")
                anchors.fill: parent
                visible: !isEditing
                elide: Text.ElideRight
                wrapMode: Text.NoWrap
            }

            // Champ de saisie pour la modification
            TextInput {
                id: promptInput
                text: promptText
                font.pixelSize: 18
                color: (colorManager?.getColorNoNotify("silver_gray") ?? "#000000")
                anchors.fill: parent
                visible: isEditing
                focus: isEditing
                maximumLength: 100
                onAccepted: {
                    backend.modifyPromptText(caseID, text);
                    promptText = text;
                    isEditing = false;
                }
            }

        }

        Item {
            width: container.width * 0.4
            height: parent.height

            Row {
                anchors.fill: parent
                spacing: 10
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.right: parent.right

                Rectangle {
                    width: 18
                    height: 18
                    color: "transparent"
                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        onClicked: {
                            if (isEditing) {
                                // Appel de la méthode pour modifier le texte
                                backend.modifyPromptText(caseID, promptInput.text);
                                promptText = promptInput.text;
                                isEditing = false;
                            } else {
                                isEditing = true;
                                promptInput.forceActiveFocus();
                            }
                        }
                    }
                    Rectangle {
                        width: parent.width
                        height: parent.height
                        color: "transparent"
                        Image {
                            id: modifyIcon
                            width: parent.width
                            height: parent.height
                            source: "../imgs/modify.svg"
                        }

                        ColorOverlay {
                            id: colorOverlayModifyIcon
                            anchors.fill: modifyIcon
                            source: modifyIcon
                            color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
                        }
                    }
                }

                Rectangle {
                    width: 18
                    height: 18
                    color: "transparent"
                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        onClicked: {
                            backend.deleteHistorique(caseID);
                        }
                    }

                    Rectangle {
                        width: parent.width
                        height: parent.height
                        color: "transparent"
                        Image {
                            id: trashIcon
                            width: parent.width
                            height: parent.height
                            source: "../imgs/poubelle.svg"
                        }

                        ColorOverlay {
                            id: colorOverlayTrashIcon
                            anchors.fill: trashIcon
                            source: trashIcon
                            color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
                        }
                    }
                }
            }
        }
    }
} 