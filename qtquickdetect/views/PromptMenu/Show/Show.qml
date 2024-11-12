import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtMultimedia 6.8

Rectangle {
    id: aff
    width: parent.width
    height: parent.height
    color: "transparent"
    anchors.fill: parent

    ScrollView {
        anchors.fill: parent

        ScrollBar.vertical: ScrollBar {
            policy: ScrollBar.AlwaysOff
        }

        ListView {
            id: listView
            width: parent.width
            height: parent.height
            model: mediaModel
            orientation: ListView.Vertical
            snapMode: ListView.SnapToItem
            clip: true
            anchors.fill: parent

            // Ajout des propriétés pour un défilement plus fluide
            flickDeceleration: 1000
            maximumFlickVelocity: 2500

            delegate: Item {
                width: listView.width
                height: listView.height

                Entry {
                    id: entry
                    modelEntry: model
                    anchors.fill: parent
                }
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
