import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [backgroundParamRectangle, "color", "very_dark_gray"],
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

        CloseButton { }
        TitleText { }
        Column {
            property int separatorHeight: 20

            id: allSettingsColumn
            anchors.centerIn: parent
            spacing: 20

            Row {
                id: settingsRow
                spacing: 50

                Column {
                    spacing: 20
                    LanguageSettings { }
                    
                    Rectangle {
                        height: allSettingsColumn.separatorHeight
                        width: 1
                        color: "transparent"
                    }
                    
                    HistorySettings { }
                }
                Column {
                    ExpertModeSettings { }

                    Rectangle {
                        height: allSettingsColumn.separatorHeight
                        width: 1
                        color: "transparent"
                    }

                    PromptInterpreterSettings { }
                }
            }
        }
    }
}
