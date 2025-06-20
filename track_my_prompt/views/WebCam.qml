import QtQuick 2.15
import QtQuick.Controls 2.15
import QtMultimedia 6.8
import QtQuick.Layouts 1.15

Rectangle {
    id: cameraRectangle
    visible: true
    width: parent.width
    height: parent.height


    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [backgroundParamRectangle, "color", "very_dark_gray"],
                [closeButtonText, "color", "default"],
                [startButton, "color", "gray"],
                [text_start_stop, "color", "default"],
                [promptInput, "color", "light_gray"],
                [promptInputBackground, "color", "dark_bluish_gray"]
            ])
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

        Row {
            id: inputAndButtonRow
            spacing: 10
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 20
            width: parent.width - 10
            height: parent.height - (parent.height - 25)

            Item {
                width: 20
                height: 1
            }
            TextField {
                id: promptInput
                placeholderText: qsTr("Enter your prompt...")
                font.pixelSize: 14
                color: (colorManager ? colorManager.getColorNoNotify("light_gray") : "#ffffff")
                background: Rectangle {
                    id: promptInputBackground
                    color: (colorManager ? colorManager.getColorNoNotify("dark_bluish_gray") : "#333333")
                    radius: 5
                }
                height: parent.height
                width: parent.width - 190
            }

            Rectangle {
                id: startButton
                width: 120
                height: parent.height
                color: (colorManager ? colorManager.getColorNoNotify("gray") : "#000000")
                radius: 10

                Text {
                    id: text_start_stop
                    text: "Start"
                    color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
                    font.pixelSize: 15
                    anchors.centerIn: parent
                }

                MouseArea {
                    hoverEnabled: true
                    anchors.fill: parent
                    onClicked: {
                        if (text_start_stop.text == "Start") {
                            text_start_stop.text = "Stop";
                            backend.start_Camera(promptInput.text);
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
}
