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
    property string promptMessage: "" 

    ScrollView {
        anchors.fill: parent

        ScrollBar.vertical: ScrollBar {
            policy: ScrollBar.AlwaysOff
        }

        GridView {
            id: gridView
            width: parent.width
            height: parent.height
            cellWidth: parent.width - 20
            cellHeight: parent.height - 20
            bottomMargin: 100
            model: mediaModel
            clip: true 

            delegate: Item {
                width: gridView.cellWidth
                height: gridView.cellHeight

                Rectangle {
                    anchors.fill: parent
                    color: "transparent"
                    anchors.margins: 10

                    Image {
                        anchors.fill: parent
                        source: model.mediaType === "image" ? formatFilePath(model.filePath) : ""
                        visible: model.mediaType === "image"
                        fillMode: Image.PreserveAspectFit
                    }
                    
                    MediaPlayer {
                        id: player
                        source: model.mediaType === "video" ? formatFilePath(model.filePath) : ""
                        autoPlay: true
                        loops: MediaPlayer.Infinite
                        videoOutput: videoOutput
                    }

                    VideoOutput {
                        id: videoOutput
                        anchors.fill: parent
                        visible: model.mediaType === "video" 
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


    function formatFilePath(filePath) {
        if (Qt.platform.os === "windows") {
            return "file:///" + filePath.replace("\\", "/");
        } else {
            return "file://" + filePath;
        }
    }

}
