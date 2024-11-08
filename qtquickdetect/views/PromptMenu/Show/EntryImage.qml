import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Image {
    property var modelData
    property bool isIAimage: false
    property string pathImg: isIAimage ? modelData.lienIA : modelData.lien
    anchors.fill: parent
    visible: modelData.type === "image"
    fillMode: Image.PreserveAspectFit
    source: modelData.type === "image" ? formatFilePath(pathImg) : ""
    
    function formatFilePath(filePath) {
        if (Qt.platform.os === "windows") {
            return "file:///" + filePath.replace("\\", "/");
        } else {
            return "file://" + filePath;
        }
    }
}