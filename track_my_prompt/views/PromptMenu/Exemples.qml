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
        text: qsTr("Examples")
        font.pixelSize: parent.width / 20
        color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
        horizontalAlignment: Text.AlignHCenter
        Layout.alignment: Qt.AlignHCenter
    }

    RowLayout {
        id: examplesRowLayout
        Layout.alignment: Qt.AlignHCenter
        spacing: 30

        ExemplesEntry {
            id: dogImagesRectangle
            entryText: qsTr("Find all dog images among a set of images")
        }

        ExemplesEntry {
            id: catVideoRectangle
            entryText: qsTr("Detect the number of cats in a video simultaneously")
        }
    }
}
