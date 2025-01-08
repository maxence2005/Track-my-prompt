import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    width: parent.width
    height: parent.height
    color: "transparent"  

    ScrollView {
        anchors.fill: parent

        ScrollBar.vertical: ScrollBar {
            policy: ScrollBar.AlwaysOff
        }        

        GridView {
            id: gridView
            width: parent.width
            height: parent.height
            cellWidth: 200 
            cellHeight: 200
            bottomMargin: 100
            clip: true    

            model: encyclopediaModel

            delegate: CaseEncyclopedie {
                name: model.englishName
                iconSource: model.emoticon
                count: model.timeFound
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
