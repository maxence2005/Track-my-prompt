import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: navBarRectangle
    width: parent.width
    height: parent.height
    color: (colorManager?.getColor["very_dark_gray"] ?? "FFFFFF")

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