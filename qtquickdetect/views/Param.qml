import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [backgroundParamRectangle, "color", "very_dark_gray"],
                [closeButtonText, "color", "default"],
                [titleText, "color", "default"],
                [languageLabel, "color", "default"],
                [historyLabel, "color", "default"],
                [historySizeText, "color", "default"],
                [expertModeLabel, "color", "default"]
            ])
        }
    }

    id: paramRectangle
    visible: true
    width: parent.width
    height: parent.height

    Rectangle {
        id: backgroundParamRectangle
        width: parent.width
        height: parent.height
        color: (colorManager?.getColorNoNotify("very_dark_gray") ?? "#000000") // Couleur d'arrière-plan

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
                color: (colorManager?.getColorNoNotify("default") ?? "#000000")
                font.pixelSize: 24
                anchors.centerIn: parent
            }

            MouseArea {
                id: closeButtonMouseArea
                anchors.fill: parent
                onClicked: {
                    backend.toggle_param();
                }
            }
        }
        Text {
            id: titleText
            text: "Paramètres"
            font.pixelSize: 40
            color: (colorManager?.getColorNoNotify("default") ?? "#000000")
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
            anchors.topMargin: 20
        }

        Column {
            id: allSettingsColumn
            anchors.centerIn: parent
            spacing: 20

            Row {
                id: settingsRow
                spacing: 50

                Rectangle {
                    id: languageSettingsContainer
                    width: 300
                    height: 200
                    color: "transparent"

                    Column {
                        id: languageSettingsColumn
                        spacing: 20

                        Row {
                            id: languageRow
                            spacing: 10

                            Text {
                                id: languageLabel
                                text: "Langue de l'application"
                                font.pixelSize: 20
                                color: (colorManager?.getColorNoNotify("default") ?? "#000000")
                            }

                            ComboBox {
                                id: languageComboBox
                                model: ["Français"]
                                width: 100
                            }
                        }

                        Button {
                            id: installLanguageButton
                            text: "Installer un pack de langue"
                            width: 200
                            height: 40
                        }

                        Button {
                            id: applyButton
                            text: "Appliquer"
                            width: 100
                            height: 40
                        }

                        Row {
                            id: historyLabelRow
                            Text {
                                id: historyLabel
                                text: "Historique"
                                font.pixelSize: 20
                                color: (colorManager?.getColorNoNotify("default") ?? "#000000")
                            }
                        }

                        Text {
                            id: historySizeText
                            text: "L'historique prend actuellement {TODO: mettre place}."
                            color: (colorManager?.getColorNoNotify("default") ?? "#000000")
                        }

                        Button {
                            id: clearHistoryButton
                            text: "Supprimer l'historique"
                            width: 200
                            height: 40
                        }
                    }
                }

                Rectangle {
                    id: expertModeContainer
                    width: 200
                    height: 200
                    color: "transparent"

                    Column {
                        id: expertModeColumn
                        spacing: 20

                        Row {
                            id: expertModeLabelRow
                            Text {
                                id: expertModeLabel
                                text: "Mode expert"
                                font.pixelSize: 20
                                color: (colorManager?.getColorNoNotify("default") ?? "#000000")
                            }
                        }

                        Row {
                            id: expertModeToggleRow

                            CheckBox {
                                id: expertModeCheckBox
                                indicator: Rectangle {
                                    width: 20
                                    height: 20
                                    color: expertModeCheckBox.checked ? (colorManager?.getColorNoNotify("black") ?? "#000000") : (colorManager?.getColorNoNotify("default") ?? "#000000") // Change la couleur en fonction de l'état
                                }
                            }

                            Text {
                                id: expertModeToggleText
                                text: "Activer le mode expert"
                                color: "red"
                            }
                        }
                    }
                }
            }
        }
    }
}
