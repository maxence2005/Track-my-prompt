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
                Connections {
                    target: colorManager
                    function onThemeChanged() {
                        colorManager.animateColorChange([
                            [iaPromptText, "color", "default"]
                        ]);
                    }
                }
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

                        EntryImage {
                            id: entryImage
                            modelData: model
                        }

                        // Afficher la vidéo si le type est "video"
                        EntryVideo {
                            id: entryVideo
                            modelData: model
                        }
                        
                        MouseArea {
                            id: mouseArea
                            anchors.fill: parent
                            hoverEnabled: true
                            onEntered: overlay.visible = true
                            onExited: overlay.visible = false
                            Item {
                                anchors.fill: parent
                                id: overlay
                                visible: false

                                Row {
                                    spacing: 5

                                    Button {
                                        text: qsTr("Change content")
                                        visible: model.lienIA ? true : false
                                        onClicked: {
                                            switch (model.type) {
                                                case "image":
                                                    entryImage.isIAimage = !entryImage.isIAimage
                                                    break
                                                case "video":
                                                    entryVideo.isIAimage = !entryVideo.isIAimage
                                                    entryVideo.videoPlayer.play()
                                                    break
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }

                    Text {
                        id: iaPromptText
                        text: model.prompt ? model.prompt : ""
                        visible: model.prompt && model.prompt.length > 0
                        font.pixelSize: parent.width / 25
                        color: (colorManager?.getColorNoNotify("default") ?? "#000000")
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
}
