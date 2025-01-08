import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [container, "borderColor", "default"],
                [icon, "color", "default"],
                [nameLabel, "color", "default"],
                [countLabel, "color", "default"]
            ])
        }
    }
    property color borderColor: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")

    id: container
    width: 150
    height: 150
    color: "transparent"
    border.color: borderColor
    border.width: 1
    radius: 10

    property string name: ""
    property string iconSource: ""
    property int count: 0

    Column {
        anchors.centerIn: parent
        spacing: 10

        Text {
            id: icon
            text: iconSource
            font.pixelSize: 50  
            color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
            anchors.horizontalCenter: parent.horizontalCenter

            MouseArea {
                id: mouseAreaIcon
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor

                onEntered: {
                    iconScaleAnim.to = 1.3;
                    iconScaleAnim.start();
                }

                onExited: {
                    iconScaleAnim.to = 1.0;
                    iconScaleAnim.start();
                }
            }
        }

        PropertyAnimation {
            id: iconScaleAnim
            target: icon
            property: "scale"
            duration: 150
        }

        Text {
            id: nameLabel
            text: name
            font.pixelSize: 18
            color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
            horizontalAlignment: Text.AlignHCenter
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Text {
            id: countLabel
            text: qsTr("Found ") + count + qsTr(" times")
            font.pixelSize: 14
            color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
            horizontalAlignment: Text.AlignHCenter
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }
}
