import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: headerRectangle
    property double progression: 0
    anchors.top: parent.top
    anchors.horizontalCenter: parent.horizontalCenter
    width: parent.width
    height: 140
    color: (colorManager?.getColor["anthracite_gray"] ?? "FFFFFF")
    anchors.margins: 15
    radius: 20
    Rectangle {
        anchors.fill: parent
        radius: 20

        gradient: Gradient {
            GradientStop {
                position: 0.0
                color: (colorManager?.getColor["dark_bluish_gray"] ?? "FFFFFF")
            } // Couleur supérieure
            GradientStop {
                position: 1.0
                color: (colorManager?.getColor["anthracite_gray"] ?? "FFFFFF")
            } // Couleur inférieure
        }
    }
    Rectangle {
        anchors.fill: parent
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 5  // Décalage vertical
        color: Qt.rgba(0, 0, 0, 0.2)  // Ombre semi-transparente
        radius: 20
        z: -1  // Pour que l'ombre soit en dessous
    }

    Label {
        id: headerLabel
        text: "Encyclopédie"
        anchors.verticalCenter: progressBar.verticalCenter
        anchors.bottom: progressBar.top
        anchors.bottomMargin: -75
        font.pixelSize: 32
        color: (colorManager?.getColor["default"] ?? "FFFFFF")
        horizontalAlignment: Text.AlignHCenter
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.horizontalCenterOffset: 0
        Layout.alignment: Qt.AlignHCenter
    }

    ProgressBar {
        id: progressBar
        height: 24
        value: headerRectangle.progression
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.leftMargin: 50
        anchors.rightMargin: 150
        anchors.verticalCenterOffset: 0
    }

    Text {
        id: progressText
        x: 462
        width: 0
        height: 18
        text: Math.round(progressBar.value * 100) + " %"
        anchors.verticalCenter: progressBar.verticalCenter
        anchors.left: progressBar.right  // Affiche la valeur en pourcentage
        anchors.leftMargin: 16  // Positionnement sous la barre de progression
        font.pixelSize: 16
        color: (colorManager?.getColor["default"] ?? "FFFFFF")
    }

    Text {
        id: _text
        text: qsTr("Cliquez sur un élement pour le rechercher")
        anchors.top: progressBar.bottom
        anchors.topMargin: 16
        font.pixelSize: 16
        anchors.horizontalCenter: parent.horizontalCenter
        color: (colorManager?.getColor["default"] ?? "FFFFFF")
        Layout.alignment: Qt.AlignHCenter
    }
}
