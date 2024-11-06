import QtQuick 2.15
import QtQuick.Layouts 1.15

Rectangle {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [mainRectangle, "color", "anthracite_gray"]
            ])
        }
    }

    id: mainRectangle
    visible: true
    width: parent.width - 50
    height: parent.height
    color: (colorManager ? colorManager.getColorNoNotify("anthracite_gray") : "#000000")

    ColumnLayout {
        id: mainColumnLayout
        anchors.fill: parent
        spacing: 0

        Header {
            progression: 0.5
            id: headerComponent
            Layout.alignment: Qt.AlignTop
        }

        Affiche {
            id: exemplesComponent
            Layout.leftMargin: 20
            Layout.alignment: Qt.AlignCenter
        }
    }
}
