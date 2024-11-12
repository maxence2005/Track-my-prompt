import QtQuick
import QtQuick.Controls

Rectangle {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [navBarRectangle, "color", "very_dark_gray"]
            ])
        }
    }

    id: navBarRectangle
    width: parent.width
    height: parent.height
    color: (colorManager?.getColorNoNotify("very_dark_gray") ?? "#000000")

    UpperGrid {
        id: upperGrid
        width: parent.width
        height: parent.height * 0.2  // 20% de la hauteur totale
        anchors.top: parent.top
    }

    Historique {
        id: historique
        width: parent.width
        height: parent.height * 0.5  // 50% de la hauteur totale
        anchors.top: upperGrid.bottom
        anchors.topMargin: 0  // Assurez-vous qu'il n'y a pas de marge inutile
    }

    LowerGrid {
        id: lowerGrid
        width: parent.width
        height: parent.height * 0.3  // 30% de la hauteur totale
        anchors.top: historique.bottom
        anchors.topMargin: 0  // Assurez-vous qu'il n'y a pas de marge inutile
    }
}
