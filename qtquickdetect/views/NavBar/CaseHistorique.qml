import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: container
    width: 180
    height: 40
    color: (colorManager ? colorManager.getColorNoNotify("anthracite_gray") : "#000000")
    border.width: 1
    radius: 8
    anchors.horizontalCenter: parent.horizontalCenter
    property string promptText: ""

    Rectangle {
        id: backgroundRectangle
        anchors.fill: parent
        property bool hovered: hoverArea.containsMouse
        property color borderColor: colorManager ? colorManager.getColorNoNotify("dark_bluish_gray") : "#000000"

        color: hovered ? (colorManager ? colorManager.getColor["dark_gray"] : "#333333") : "transparent"
        border.color: borderColor
        border.width: 3
        radius: 8
    }

    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [backgroundRectangle, "borderColor", "dark_bluish_gray"],
                [nameLabel, "color", "silver_gray"]
            ]);
        }
    }

    MouseArea {
        id: hoverArea
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
        onClicked: {
            console.log("Rectangle cliqué")
        }
    }

    Row {
        anchors.fill: parent
        padding: 10

        Item {
            width: container.width * 0.6
            height: parent.height

            Row {
                anchors.fill: parent
                spacing: 10

                Image {
                    id: imageIcon
                    width: 20
                    height: 20
                    source: "../imgs/Message.png"
                }

                Text {
                    id: promptHistorique
                    text: promptText !== "" ? promptText : "pas de prompt"
                    font.pixelSize: 18
                    color: "snow"
                }
            }
        }

        Item {
            width: container.width * 0.4
            height: parent.height

            Row {
                anchors.fill: parent
                spacing: 10
                anchors.horizontalCenter: parent.horizontalCenter

                Rectangle {
                    width: 18
                    height: 18
                    color: "transparent"
                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        onClicked: {
                            console.log("Bouton 1 cliqué")
                        }
                    }
                    Image {
                        width: parent.width
                        height: parent.height
                        source: "../imgs/modify.svg"
                    }
                }

                Rectangle {
                    width: 18
                    height: 18
                    color: "transparent"
                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        onClicked: {
                            console.log("Bouton 2 cliqué")
                        }
                    }
                    Image {
                        width: parent.width
                        height: parent.height
                        source: "../imgs/poubelle.svg"
                    }
                }
            }
        }
    }
}
