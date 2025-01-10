import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Column {
    id: lowerColumn
    width: parent.width
    height: parent.height
    anchors.bottom: parent.bottom

    SeparatorLine {
        id: lowerSeparatorLine
    }

    ColumnLayout {
        id: lightModeColumn
        property string iconLight: "../imgs/light_mode_icon.png"
        property string textLight: qsTr("Light mode")

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