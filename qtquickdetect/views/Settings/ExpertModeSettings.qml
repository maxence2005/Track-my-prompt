
import QtQuick 2.15
import QtQuick.Controls 2.15


Column {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [expertModeLabel, "color", "default"],
                [expertModeCheckBoxIndicator, "color", "default"],
            ])
        }
    }
    Rectangle {
        id: expertModeContainer
        width: 200
        height: 100
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
                        id: expertModeCheckBoxIndicator
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