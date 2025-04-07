import QtQuick
import QtQuick.Controls

Rectangle {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [navBar, "color", "very_dark_gray"]
            ]);
        }
    }

    id: navBar
    width: parent.width
    height: parent.height
    color: (colorManager ? colorManager.getColorNoNotify("very_dark_gray") : "#000000")

    // UpperGrid
    UpperGrid {
        id: upperGrid
        width: parent.width
        height: 115
        anchors.bottom: historique.top
    }

    // Historique
    Historique {
        id: historique
        width: parent.width
        height: 200
        anchors.top: upperGrid.bottom
        anchors.bottom: lowerGrid.top
        anchors.topMargin: 150
        anchors.bottomMargin: 185
    }

    // LowerGrid
    LowerGrid {
        id: lowerGrid
        width: parent.width
        height: 185 
        anchors.bottom: parent.bottom
    }
}
