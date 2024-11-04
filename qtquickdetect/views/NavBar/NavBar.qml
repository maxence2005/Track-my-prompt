import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

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

    Grid {
        id: navBarGrid
        width: parent.width
        height: parent.height
        columns: 1
        rows: 2

        UpperGrid {
            id: upperGrid
        }

        LowerGrid {
            id: lowerGrid
        }
    }
}