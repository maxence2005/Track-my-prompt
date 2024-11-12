import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    width: parent.width
    height: parent.height
    color: "transparent"

    ScrollView {
        anchors.fill: parent
        anchors.centerIn: parent

        GridView {
            id: gridView
            width: parent.width
            height: parent.height
            topMargin: 30
            cellWidth: 180
            cellHeight: 50
            clip: true
            model: historiqueModel

            delegate: CaseHistorique {
                promptText: model.prompt
            }

            ScrollBar.vertical: ScrollBar {
                policy: ScrollBar.AsNeeded
                width: 15
                background: Rectangle {
                    color: "transparent"
                }
            }
        }
    }
}
