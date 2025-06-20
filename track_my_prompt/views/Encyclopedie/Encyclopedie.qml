import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15

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
    focus: true
    width: parent.width - 50
    height: parent.height
    color: (colorManager ? colorManager.getColorNoNotify("anthracite_gray") : "#000000")

    Component.onCompleted: mainRectangle.forceActiveFocus()

    Keys.onReleased: (event) => {
        if (event.key === Qt.Key_Escape) {
            backend.toggle_menu()
            event.accepted = true
        }
    }

    ColumnLayout {
        id: mainColumnLayout
        anchors.fill: parent
        spacing: 0

        Header {
            progression: 1.0 //databaseManager ? databaseManager.pourcentFound() : 0.0
            id: headerComponent
            Layout.alignment: Qt.AlignTop | Qt.AlignHCenter
        }

        Affiche {
            id: exemplesComponent
            Layout.leftMargin: 20
            Layout.alignment: Qt.AlignCenter
        }
    }
}
