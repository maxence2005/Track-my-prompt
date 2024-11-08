import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Column {
    id: upperGrid
    width: parent.width
    height: 470
    anchors.fill: parent
    spacing: 10

    Column {
        id: mainColumn
        width: parent.width
        spacing: 10

        Column {
            id: buttonColumn
            spacing: 10
            anchors.horizontalCenter: parent.horizontalCenter

            ButtonWithHover {
                id: newDetectionButton
                width: 180
                height: 50
                text: qsTr("+ New detection")
                topMargin: 10
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        backend.nouvelleDetection();
                    }
                }
            }

            ButtonWithHover {
                id: encyclopediaButton
                width: 180
                height: 50
                text: qsTr("Encyclopedia")
                topMargin: 70
                iconSource: "../imgs/wizard.png"
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        backend.toggle_menu();
                    }
                }
            }
        }
        SeparatorLine {
            id: upperSeparatorLine
        }
    }
}