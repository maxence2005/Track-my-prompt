import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: headerRectangle
    anchors.top: parent.top
    anchors.horizontalCenter: parent.horizontalCenter
    width: parent.width
    height: 60
    color: "transparent"
    anchors.margins: 15

    Label {
        id: headerLabel
        anchors.centerIn: parent
        text: "Track My Prompts"
        font.pixelSize: 32
        color: "white"
        horizontalAlignment: Text.AlignHCenter
        Layout.alignment: Qt.AlignHCenter
    }
}