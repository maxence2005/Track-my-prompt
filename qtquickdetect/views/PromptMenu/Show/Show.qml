import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtMultimedia 6.8

Rectangle {
    id: aff
    width: parent.width
    height: parent.height
    color: "transparent"
    anchors.fill: parent

    ScrollView {
        anchors.fill: parent

        ScrollBar.vertical: ScrollBar {
            policy: ScrollBar.AlwaysOff
        }

        GridView {
            id: gridView
            width: parent.width
            height: parent.height
            cellWidth: 500
            cellHeight: 400
            bottomMargin: 50
            model: mediaModel
            clip: true

            delegate: Item {
                width: gridView.cellWidth
                height: gridView.cellHeight

                Entry {
                    id: entry
                    modelEntry: model
                }
            }

            ScrollBar.vertical: ScrollBar {
                policy: ScrollBar.AlwaysOn
                width: 15
                background: Rectangle {
                    color: "transparent"
                }
            }
        }
    }
}
