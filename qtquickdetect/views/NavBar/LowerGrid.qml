import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Grid {
    id: lowerGrid
    width: parent.width
    height: 160
    columns: 1
    rows: 3
    anchors.bottom: parent.bottom

    SeparatorLine {
        id: lowerSeparatorLine
    }


    ColumnLayout {
        id: lightModeColumn
        anchors.horizontalCenter: parent.horizontalCenter
        spacing : 10
        LowerGridEntry {
            iconSource: "../imgs/light_mode_icon.png"
            labelText: qsTr("Light mode")
        }
    
        LowerGridEntry {
            iconSource: "../imgs/settings.png"
            labelText: qsTr("Settings")
        }
    }
}