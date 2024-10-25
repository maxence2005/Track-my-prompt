import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Grid {
    id: upperGrid
    width: parent.width
    height: 470
    columns: 1
    rows: 2

    Column {
        id: mainColumn
        anchors.fill: parent
        spacing: 10

        Column {
            id: buttonColumn
            spacing: 10
            anchors.horizontalCenter: parent.horizontalCenter

            ButtonWithHover {
                id: newDetectionButton
                width: 180
                height: 50
                text: "+ New detection"
                topMargin: 10
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        backend.selectFile(); // Appeler la méthode pour ouvrir l'explorateur de fichiers
                    }
                }
            }

            ButtonWithHover {
                id: encyclopediaButton
                width: 180
                height: 50
                text: "Encyclopédie"
                topMargin: 70
                iconSource: "../imgs/wizard.png"
            }
        }
        SeparatorLine {
            id: upperSeparatorLine
        }
    }
}
