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
        color: (colorManager ? colorManager.getColorNoNotify("very_dark_gray") : "#000000") // Background color

        Rectangle {
            id: closeButtonContainer
            width: 30
            height: 30
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.margins: 10
            color: "transparent" // No color so the cross itself remains visible

            Text {
                id: closeButtonText
                text: "✖" // Cross symbol
                color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
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
            text: qsTr("Settings")
            font.pixelSize: 40
            color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
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
                                text: qsTr("Application Language")
                                font.pixelSize: 20
                                color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
                            }

                            ComboBox {
                                id: languageComboBox
                                model: languageManager ? languageManager.getLanguages : []
                                width: 100
                                onActivated : {
                                    languageManager.setLanguage(languageComboBox.currentText)
                                }
                            }
                        }

                        Button {
                            id: installLanguageButton
                            text: qsTr("Install a Language Pack")
                            width: 200
                            height: 40
                            onClicked: {
                                languageManager.install_new_language()
                            }
                        }

                        Row {
                            id: historyLabelRow
                            Text {
                                id: historyLabel
                                text: qsTr("History")
                                font.pixelSize: 20
                                color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
                            }
                        }

                        Text {
                            id: historySizeText
                            text: qsTr("The history currently takes up ") + backend ? backend.getSizeOfHistory : "0B"
                            color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
                        }

                        Button {
                            id: clearHistoryButton
                            text: qsTr("Clear History")
                            width: 200
                            height: 40

                            onClicked: {
                                backend.deleteHistory()
                            }
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
                                text: qsTr("Expert Mode")
                                font.pixelSize: 20
                                color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
                            }
                        }

                        Row {
                            id: expertModeToggleRow

                            CheckBox {
                                id: expertModeCheckBox
                                enabled: false
                                indicator: Rectangle {
                                    width: 20
                                    height: 20
                                    color: expertModeCheckBox.checked ? (colorManager ? colorManager.getColorNoNotify("black") : "#000000") : (colorManager ? colorManager.getColorNoNotify("default") : "#000000") // Change color based on state
                                }
                            }

                            Text {
                                id: expertModeToggleText
                                text: qsTr("Enable Expert Mode (Coming Soon)")
                                color: "red"
                            }
                        }
                    }
                }
            }
        }
    }
}
