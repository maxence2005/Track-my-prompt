import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: navBarRectangle
    width: parent.width
    height: parent.height
    color: "#343541"

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