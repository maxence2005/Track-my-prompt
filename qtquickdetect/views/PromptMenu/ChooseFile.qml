import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15

Rectangle {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [chooseFileMainRectangle, "backgroundColor", "dark_bluish_gray"],
                [dragDropText, "color", "very_light_gray"],
                [orText, "color", "light_gray"]
            ])
        }
    }

    id: chooseFileMainRectangle
    property bool hovered: false
    property color backgroundColor: (colorManager ? colorManager.getColorNoNotify("dark_bluish_gray") : "#000000")
    property color backgroundColorHover: (colorManager ? colorManager.getColor["steel_gray"] : "#000000")

    width: 600
    height: 100
    color: hovered ? backgroundColorHover : backgroundColor
    radius: 10

    property bool isFileOver: false

    DropArea {
        id: dropArea
        anchors.fill: parent
        onEntered: function(drag) {
            if (drag.hasUrls) {
                drag.accept(Qt.CopyAction);  
                chooseFileMainRectangle.hovered = true; 
            }
        }

        onExited: {
            chooseFileMainRectangle.hovered = false; 
        }

        onDropped: function(drag) {
            if (drag.hasUrls) {
                for (var i = 0; i < drag.urls.length; i++) {
                    var fileUrl = drag.urls[i];
                    backend.receiveFile(fileUrl);
                }
                chooseFileMainRectangle.hovered = false;
            }
        }
    }

    RowLayout {
        id: mainRowLayout
        anchors.centerIn: parent
        spacing: 50

        RowLayout {
            id: chooseFileMainRowLayout
            spacing: 10
            Image {
                id: uploadIcon
                source: "../imgs/upload.svg"
                width: 40
                height: 40
            }

            Text {
                id: dragDropText
                text: qsTr("Drag\nand Drop ")
                font.pixelSize: 18
                color: (colorManager ? colorManager.getColorNoNotify("very_light_gray") : "#000000")
            }
        }

        Text {
            id: orText
            text: qsTr("or")
            font.pixelSize: 36
            color: (colorManager ? colorManager.getColorNoNotify("light_gray") : "#000000")
        }

        RowLayout {
            id: iconRowLayout
            spacing: 15

            IconRectangle {
                id: camIcon
                imageSource: "../imgs/cam.svg"
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        backend.toggle_camera();
                    }
                }
            }

            IconRectangle {
                id: fileIcon
                imageSource: "../imgs/file.svg"
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        backend.openFileExplorer();
                    }
                }
            }

            IconRectangle {
                id: linkIcon
                imageSource: "../imgs/link.svg"
                MouseArea {
                    anchors.fill: parent
                    onClicked: linkDialog.open()
                }
            }
        }
    }

    Dialog {
        id: linkDialog
        title: qsTr("Enter the link")
        standardButtons: Dialog.Ok | Dialog.Cancel
        modal: true

        ColumnLayout {
            spacing: 10
            TextField {
                id: linkInput
                placeholderText: qsTr("Enter the link here")
                Layout.preferredWidth: 500
                Layout.fillWidth: true
            }
        }

        onAccepted: {
            backend.receiveFile(linkInput.text);
        }
    }
}