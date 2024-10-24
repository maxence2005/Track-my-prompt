import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: paramRectangle
    visible: true
    width: parent.width
    height: parent.height

    Rectangle {
        id: backgroundParamRectangle
        width: parent.width
        height: parent.height
        color: "#2D2D3A" // Couleur d'arrière-plan

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
                    sharedVar["settingsMenuShowed"] = false;
                    backend.shared_variable = sharedVar;
                }
            }
        }
        Text {
            id: titleText
            text: "Paramètres"
            font.pixelSize: 40
            color: "white"
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
                                color: "white"
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
                                color: "white"
                            }
                        }

                        Text {
                            id: historySizeText
                            text: "L'historique prend actuellement {TODO: mettre place}."
                            color: "white"
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
                                color: "white"
                            }
                        }

                        Row {
                            id: expertModeToggleRow

                            CheckBox {
                                id: expertModeCheckBox
                                indicator: Rectangle {
                                    width: 20
                                    height: 20
                                    color: expertModeCheckBox.checked ? "#1e1f1e" : "white" // Change la couleur en fonction de l'état
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
