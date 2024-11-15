import QtQuick 2.15
import QtQuick.Controls 2.15
import QtMultimedia 6.8

Rectangle {
    id: cameraRectangle
    visible: true
    width: parent.width
    height: parent.height


    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([[backgroundParamRectangle, "color", "very_dark_gray"], [closeButton, "color", "gray"], [closeButtonText, "color", "default"]])
        }
    }

    Rectangle {
        id: backgroundParamRectangle
        width: parent.width
        height: parent.height
        color: (colorManager ? colorManager.getColorNoNotify("very_dark_gray") : "#000000")


        Rectangle {
            id: closeButtonContainer
            width: 30
            height: 30
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.margins: 10
            color: "transparent"

            Text {
                id: closeButtonText
                text: "✖"
                color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
                font.pixelSize: 24
                anchors.centerIn: parent
            }

            MouseArea {
                id: closeButtonMouseArea
                anchors.fill: parent
                onClicked: {
                    if (text_start_stop.text == "Stop"){
                        text_start_stop.text = "Start";
                        refreshTimer.running = false
                        backend.stop_Camera();
                        backend.toggle_camera();
                    }
                    else{
                        text_start_stop.text = "Start";
                        backend.toggle_camera();
                    }
                }
            }
        }


        Rectangle {
            id: cameraContainer
            anchors.centerIn: parent
            width: parent.width - 50
            height: parent.height - 100
            color: "black"

            Timer {
                id: refreshTimer
                interval: 50
                running: false
                repeat: true
                onTriggered: {
                    imageItem.source = "image://frameprovider/frame?" + Date.now()
                }
            }

            Image {
                id: imageItem
                anchors.centerIn: parent
                width: parent.width
                height: parent.height
                fillMode: Image.PreserveAspectFit
            }
        }



        Rectangle {
            id: startButton
            width: 120
            height: 25
            color: (colorManager ? colorManager.getColorNoNotify("gray") : "#000000")
            radius: 10
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 20

            Text {
                id: text_start_stop
                text: "Start"
                color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
                font.pixelSize: 15
                anchors.centerIn: parent
            }

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    if (text_start_stop.text == "Start") {
                        text_start_stop.text = "Stop";
                        backend.start_Camera();
                        refreshTimer.running = true;
                    } else {
                        text_start_stop.text = "Start";
                        refreshTimer.running = false;
                        backend.stop_Camera();
                        backend.toggle_camera();
                    }
                }

                onEntered: {
                    startButton.color = (colorManager ? colorManager.getColorNoNotify("medium_gray") : "#000000");
                }

                onExited: {
                    startButton.color = (colorManager ? colorManager.getColorNoNotify("gray") : "#000000");
                }
            }
        }
    }
}
