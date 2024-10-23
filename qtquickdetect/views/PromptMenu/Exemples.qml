import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15

ColumnLayout {
    id: exemplesMainColumnLayout
    anchors.horizontalCenter: parent.horizontalCenter
    spacing: 10

    Label {
        id: exemplesTitleLabel
        text: "Exemples"
        font.pixelSize: 24
        color: "white"
        horizontalAlignment: Text.AlignHCenter
        Layout.alignment: Qt.AlignHCenter
    }

    RowLayout {
        id: examplesRowLayout
        Layout.alignment: Qt.AlignHCenter
        spacing: 30

        Rectangle {
            id: dogImagesRectangle
            width: 200
            height: 100
            color: "#44464f"
            radius: 10
            Text {
                id: dogImagesText
                anchors.centerIn: parent
                width: parent.width - 20
                text: "Trouver toutes les images de chiens parmi un ensemble d'images"
                font.pixelSize: 16
                color: "white"
                horizontalAlignment: Text.AlignHCenter
                wrapMode: Text.WordWrap
            }

            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                onEntered: {
                    dogImagesRectangle.color = "#66687d";
                }
                onExited: {
                    dogImagesRectangle.color = "#44464f";
                }
            }
        }

        Rectangle {
            id: catVideoRectangle
            width: 200
            height: 100
            color: "#44464f"
            radius: 10
            Text {
                id: catVideoText
                anchors.centerIn: parent
                width: parent.width - 20
                text: "Détecter le nombre de chats sur une vidéo en simultané"
                font.pixelSize: 16
                color: "white"
                horizontalAlignment: Text.AlignHCenter
                wrapMode: Text.WordWrap
            }

            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                onEntered: {
                    catVideoRectangle.color = "#66687d";
                }
                onExited: {
                    catVideoRectangle.color = "#44464f";
                }
            }
        }
    }
}
