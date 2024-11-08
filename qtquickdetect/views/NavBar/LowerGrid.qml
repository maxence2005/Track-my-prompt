import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Column {
    id: lowerColumn
    width: parent.width
    height: 160
    anchors.bottom: parent.bottom
    anchors.margins: 20

    SeparatorLine {
        id: lowerSeparatorLine
    }

    ColumnLayout {
        id: lightModeColumn
        // Icon quand on est en dark mode
        property string iconLight: "../imgs/light_mode_icon.png"
        property string textLight: qsTr("Light mode")

        // Icon quand on est en light mode
        property string iconDark: "../imgs/dark_mode_icon.svg"
        property string textDark: qsTr("Dark mode")

        anchors.horizontalCenter: parent.horizontalCenter
        spacing: 10
        LowerGridEntry {
            iconSource: colorManager ? (colorManager.isDarkMode ? lightModeColumn.iconLight : lightModeColumn.iconDark) : ""
            labelText: colorManager ? (colorManager.isDarkMode ? lightModeColumn.textLight : lightModeColumn.textDark) : ""
            
            onClicked: {
                colorManager.switchTheme();
            }
        }

        LowerGridEntry {
            iconSource: "../imgs/settings.png"
            labelText: qsTr("Settings")

            onClicked: {
                backend.toggle_param();
            }
        }
    }
}