import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtMultimedia 6.8

Item {
    property string sourceMedia: ""
    width: parent.width
    height: parent.height
    visible: model.type === "video"
    anchors.horizontalCenter: parent.horizontalCenter

    MediaPlayer {
        id: player
        source: sourceMedia
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