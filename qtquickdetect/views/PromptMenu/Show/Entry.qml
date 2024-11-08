import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import Qt5Compat.GraphicalEffects

ColumnLayout {
    property var modelEntry
    anchors.leftMargin: 50
    anchors.fill: parent

    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [iaPromptText, "color", "default"]
            ]);
        }
    }

    Rectangle {
        property bool haveLienIA: modelEntry.lienIA ? true : false
        id: imageContainer
        width: parent.width
        height: parent.height * 0.8
        color: "transparent"
        anchors.horizontalCenter: parent.horizontalCenter

        Connections {
            target: backend
            function onLoad(visible) {
                overlayImage.visible = visible
                blurEffect.visible = visible
            }
        }

        EntryImage {
            id: entryImage
            modelData: modelEntry
        }

        // Afficher la vidéo si le type est "video"
        EntryVideo {
            id: entryVideo
            modelData: modelEntry
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
                        visible: modelEntry.lienIA ? true : false
                        onClicked: {
                            imageContainer.changeContent()
                        }
                    }
                }
            }
        }

        FastBlur {
            id: blurEffect
            visible: false
            anchors.fill: parent
            source: parent
            radius: 1
        }

        Item {
            id: imageOverlay
            width: gridView.cellWidth / 100
            height: gridView.cellHeight / 100
            anchors.centerIn: parent
            AnimatedImage {
                id: overlayImage
                source: "../../imgs/loading.gif"
                anchors.centerIn: parent
                visible: false
                fillMode: Image.PreserveAspectFit
            }
        }
        
        onHaveLienIAChanged: {
            if (haveLienIA) {
                imageContainer.changeContent()
            }
        }

        function changeContent() {
            switch (modelEntry.type) {
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

    Text {
        id: iaPromptText
        text: modelEntry.prompt ? modelEntry.prompt : ""
        font.pixelSize: parent.width / 25
        color: (colorManager?.getColorNoNotify("default") ?? "#000000")
        wrapMode: Text.Wrap
        horizontalAlignment: Text.AlignHCenter
        Layout.alignment: Qt.AlignHCenter
        width: parent.width - 20
    }
}