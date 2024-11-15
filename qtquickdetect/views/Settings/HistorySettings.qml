
import QtQuick 2.15
import QtQuick.Controls 2.15

Column {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [historyLabel, "color", "default"],
                [historySizeText, "color", "default"],
            ])
        }
    }

    spacing: 20
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
        text: qsTr("The history currently takes up ") + (backend ? backend.getSizeOfHistory : "0B")
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