import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: container
    width: 150
    height: 150
    color: "transparent"
    border.color: "#AAAAAA"
    border.width: 1
    radius: 10

    // Déclarez les propriétés dynamiques
    property string name: ""
    property string iconSource: ""  // Contient l'émoticône ou le symbole Unicode
    property int count: 0

    Column {
        anchors.centerIn: parent
        spacing: 10

        // Utilisez Text au lieu de Image pour afficher l'émoticône
        Text {
            id: icon
            text: iconSource
            font.pixelSize: 50  // Taille de l'émoticône (à ajuster si nécessaire)
            color: "white"  // Couleur de l'émoticône
            anchors.horizontalCenter: parent.horizontalCenter

            // Animation lors du survol
            MouseArea {
                id: mouseAreaIcon
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor

                // Gestion des événements de survol
                onEntered: {
                    // Animer l'effet de zoom avant au survol
                    iconScaleAnim.to = 1.3; // Zoomer légèrement (ajuster selon vos besoins)
                    iconScaleAnim.start();
                }

                onExited: {
                    // Revenir à la taille initiale lorsque le survol cesse
                    iconScaleAnim.to = 1.0; // Taille normale
                    iconScaleAnim.start();
                }
            }
        }

        // Animation de la mise à l'échelle de l'icône
        PropertyAnimation {
            id: iconScaleAnim
            target: icon
            property: "scale"
            duration: 150 // Durée de l'animation (en ms)
        }

        Text {
            id: nameLabel
            text: name
            font.pixelSize: 18
            color: "white"
            horizontalAlignment: Text.AlignHCenter
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Text {
            id: countLabel
            text: "Trouvé " + count + "x"
            font.pixelSize: 14
            color: "white"
            horizontalAlignment: Text.AlignHCenter
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }
}
