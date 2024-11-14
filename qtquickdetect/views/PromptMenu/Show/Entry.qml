import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import Qt5Compat.GraphicalEffects

ColumnLayout {
    property var modelEntry
    height: parent.height
    width: parent.width
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
        Layout.fillWidth: true
        Layout.fillHeight: true
        color: "transparent"
        Layout.alignment: Qt.AlignHCenter

        EntryImage {
            id: entryImage
            modelData: modelEntry
        }

        // Afficher la vidéo si le type est "video"
        EntryVideo {
            id: entryVideo
            modelData: modelEntry
        }
        
        Item {
            anchors.fill: parent
            id: overlay
            visible: true

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

        FastBlur {
            id: blurEffect
            visible: (backend ? backend.shared_variable["Chargement"] : false) && (modelEntry.id == backend.idChargement)
            anchors.fill: parent
            source: parent
            radius: 1
        }

        Item {
            id: imageOverlay
            anchors.centerIn: parent
            width: parent.width
            height: parent.height
            clip: true
            AnimatedImage {
                id: overlayImage
                source: "../../imgs/loading.gif"
                anchors.centerIn: parent
                visible: (backend ? backend.shared_variable["Chargement"] : false) && (modelEntry.id == backend.idChargement)
                fillMode: Image.PreserveAspectFit
                width: parent.width
                height: parent.height
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
        color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
        wrapMode: Text.Wrap
        Layout.alignment: Qt.AlignHCenter
        width: parent.width - 20
    }
}