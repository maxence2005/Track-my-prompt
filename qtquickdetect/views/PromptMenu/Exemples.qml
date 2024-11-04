import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15

ColumnLayout {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [exemplesTitleLabel, "color", "default"]
            ]);
        }
    }
    
    id: exemplesMainColumnLayout
    anchors.horizontalCenter: parent.horizontalCenter
    spacing: 10

    Label {
        id: exemplesTitleLabel
        text: "Exemples"
        font.pixelSize: 24
        color: (colorManager?.getColorNoNotify("default") ?? "#000000")
        horizontalAlignment: Text.AlignHCenter
        Layout.alignment: Qt.AlignHCenter
    }

    RowLayout {
        id: examplesRowLayout
        Layout.alignment: Qt.AlignHCenter
        spacing: 30

        ExemplesEntry {
            id: dogImagesRectangle
            entryText: "Trouver toutes les images de chiens parmi un ensemble d'images"
        }

        ExemplesEntry {
            id: catVideoRectangle
            entryText: "Détecter le nombre de chats sur une vidéo en simultané"
        }
    }
}
