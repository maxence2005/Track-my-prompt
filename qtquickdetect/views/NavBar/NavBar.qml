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
    color: (colorManager ? colorManager.getColorNoNotify("very_dark_gray") : "#000000")

    Item {
        id: navBarColumn
        width: parent.width
        height: parent.height

        UpperGrid {
            id: upperGrid
        }

        LowerGrid {
            id: lowerGrid
        }
    }
}