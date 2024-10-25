import QtQuick 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: mainRectangle
    visible: true
    width: parent.width - 50
    height: parent.height
    color: (colorManager?.getColor["anthracite_gray"] ?? "FFFFFF")

    ColumnLayout {
        id: mainColumnLayout
        anchors.fill: parent
        spacing: 0

        Header {
            progression: 0.5
            id: headerComponent
            Layout.alignment: Qt.AlignTop
        }

        Affiche {
            id: exemplesComponent
            Layout.leftMargin: 20
            Layout.alignment: Qt.AlignCenter
        }
    }
}
