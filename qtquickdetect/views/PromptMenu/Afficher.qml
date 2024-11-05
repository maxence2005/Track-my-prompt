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

        GridView {
            id: gridView
            width: parent.width
            height: parent.height
            cellWidth: 500
            cellHeight: 400
            bottomMargin: 50
            model: mediaModel
            clip: true 

            delegate: Item {
                width: gridView.cellWidth
                height: gridView.cellHeight

                ColumnLayout {
                    anchors.fill: parent
                    spacing: 20

                    Rectangle {
                        width: parent.width
                        height: parent.height * 0.8 
                        color: "transparent"
                        anchors.horizontalCenter: parent.horizontalCenter


                        Image {
                            anchors.fill: parent
                            source: model.type === "image" ? formatFilePath(model.lien) : ""
                            visible: model.type === "image"
                            fillMode: Image.PreserveAspectFit
                        }

                        // Afficher la vidéo si le type est "video"
                        MediaPlayer {
                            id: player
                            source: model.type === "video" ? formatFilePath(model.lien) : ""
                            autoPlay: true
                            loops: MediaPlayer.Infinite
                            videoOutput: videoOutput
                        }

                        VideoOutput {
                            id: videoOutput
                            anchors.fill: parent
                            visible: model.type === "video" 
                        }
                    }

                    Text {
                        text: model.prompt ? model.prompt : ""
                        visible: model.prompt && model.prompt.length > 0
                        font.pixelSize: parent.width / 25
                        color: "black"
                        wrapMode: Text.Wrap
                        horizontalAlignment: Text.AlignHCenter
                        Layout.alignment: Qt.AlignHCenter
                        width: parent.width - 20
                    }
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

    // Fonction pour formater le chemin du fichier selon le système d'exploitation
    function formatFilePath(filePath) {
        if (Qt.platform.os === "windows") {
            return "file:///" + filePath.replace("\\", "/");
        } else {
            return "file://" + filePath;
        }
    }
}
