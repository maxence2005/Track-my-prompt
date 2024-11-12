import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    width: parent.width
    height: parent.height
    color: "transparent"  // La couleur peut être ajustée ou laissée transparente

    ScrollView {
        anchors.fill: parent

        ScrollBar.vertical: ScrollBar {
            policy: ScrollBar.AlwaysOff
        }        

        GridView {
            id: gridView
            width: parent.width
            height: parent.height
            cellWidth: 200  // Largeur de chaque cellule
            cellHeight: 200 // Hauteur de chaque cellule
            bottomMargin: 100
            clip: true      // Assurez-vous que le contenu qui déborde soit masqué

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
