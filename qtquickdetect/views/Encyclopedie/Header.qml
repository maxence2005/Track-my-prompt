import QtQuick 2.15
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls 2.15

Rectangle {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [headerRectangle, "color", "anthracite_gray"],
                [headerLabel, "color", "default"],
                [progressBackground, "color", "medium_gray"],
                //[progressColor, "color", "blue_gray"],
                [progressText, "color", "default"],
                [_text, "color", "default"],
                [gradientStop0, "color", "dark_bluish_gray"],
                [gradientStop1, "color", "anthracite_gray"]
            ])
        }
    }

    id: headerRectangle
    property double progression: 0
    anchors.top: parent.top
    anchors.horizontalCenter: parent.horizontalCenter
    width: parent.width
    height: parent.height * 0.3
    color: (colorManager?.getColorNoNotify("anthracite_gray") ?? "#000000")
    anchors.margins: 15
    radius: 20
    Rectangle {
        anchors.fill: parent
        radius: 20

        gradient: Gradient {
            GradientStop {
                id : gradientStop0
                position: 0.0
                color: (colorManager?.getColorNoNotify("dark_bluish_gray") ?? "#000000")
            } // Couleur supérieure
            GradientStop {
                id : gradientStop1
                position: 1.0
                color: (colorManager?.getColorNoNotify("anthracite_gray") ?? "#000000")
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
        text: "Encyclopédie : Cliquez sur un élement pour le rechercher"
        anchors.verticalCenter: progressBar.verticalCenter
        anchors.bottom: progressBar.top
        anchors.bottomMargin: -75
        font.pixelSize: parent.width / 30
        color: (colorManager?.getColorNoNotify("default") ?? "#000000")
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

        contentItem: Item {
            width: progressBar.width
            height: progressBar.height

            Rectangle {
                id: progressBackground
                width: parent.width
                height: parent.height
                color: (colorManager?.getColorNoNotify("medium_gray") ?? "#000000") // Couleur d'arrière-plan
            }

            // Filled portion color
            Rectangle {
                id: progressColor
                width: parent.width * progressBar.value
                height: parent.height
                color: "blue" // Couleur de la barre de progression
            }
        }
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
        color: (colorManager?.getColorNoNotify("default") ?? "#000000")
    }

    TextField {
        id: searchField
        placeholderText: qsTr("Rechercher un élément")
        anchors.top: progressBar.bottom
        anchors.topMargin: 16
        anchors.horizontalCenter: parent.horizontalCenter
        width: parent.width * 0.8
        font.pixelSize: 16
        color: (colorManager?.getColorNoNotify("default") ?? "#000000")
        background: Rectangle {
            color: (colorManager?.getColorNoNotify("medium_gray") ?? "#888888")
            radius: 10
        }
        onTextChanged: databaseManager.set_search_text(searchField.text)
    }
}
