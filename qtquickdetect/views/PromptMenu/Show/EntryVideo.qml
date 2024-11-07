import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtMultimedia 6.8

Item {
    property var modelData
    property bool isIAimage: false
    property string pathImg: isIAimage ? modelData.lienIA : modelData.lien
    property var videoPlayer: player
    width: parent.width
    height: parent.height
    visible: modelData.type === "video"
    anchors.horizontalCenter: parent.horizontalCenter

    MediaPlayer {
        id: player
        source: formatFilePath(pathImg)
        autoPlay: true
        loops: MediaPlayer.Infinite
        videoOutput: videoOutput
    }

    VideoOutput {
        id: videoOutput
        anchors.fill: parent
        visible: modelData.type === "video"
    }

    function formatFilePath(filePath) {
        if (Qt.platform.os === "windows") {
            return "file:///" + filePath.replace("\\", "/");
        } else {
            return "file://" + filePath;
        }
    }
}
