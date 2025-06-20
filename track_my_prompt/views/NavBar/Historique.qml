import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    width: parent.width
    height: parent.height
    color: "transparent"
    anchors.fill: parent

    // Modèle par défaut en cas d'absence de historiqueModel
    ListModel {
        id: fallbackModel
        ListElement { prompt: "Aucun historique disponible" }
    }

    ScrollView {
        width: parent.width
        height: parent.height  // Laisser ScrollView occuper toute la hauteur disponible

        // GridView
        GridView {
            id: gridView
            width: parent.width
            height: parent.height
            topMargin: 10
            cellWidth: parent.width
            cellHeight: 50
            clip: true

            // Vérifier si histaoriqueModel existe, sinon utiliser fallbackModel
            model: historiqueModel

            // Delegate avec CaseHistorique
            delegate: CaseHistorique {
                promptText: model.titre_case
                caseID: model.pageID
            }

            // ScrollBar vertical
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
