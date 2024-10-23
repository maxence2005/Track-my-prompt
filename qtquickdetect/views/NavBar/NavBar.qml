import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: navBarRectangle
    width: parent.width
    height: parent.height
    color: "#1e1e2d"

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