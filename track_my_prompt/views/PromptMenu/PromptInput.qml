import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import Qt5Compat.GraphicalEffects 1.0

RowLayout {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [wizardIconRectangle, "backgroundColor", "dark_gray"],
                [wizardColorOverlay, "color", "default"],
                [microphoneIconRectangle, "backgroundColor", "dark_gray"],
                [microphoneColorOverlay, "color", "default"],
                [promptInputRectangle, "color", "dark_bluish_gray"],
                [promptInputField, "color", "light_gray"],
                [promptInputField, "placeholderTextColor", "blue_gray"],
                [sendColorOverlay, "color", "light_bluish_gray"]
            ])
        }
    }

    id: promptRowLayout
    width: parent.width
    height: 50

    Rectangle {
        id: wizardIconRectangle
        property bool hovered: false
        property color backgroundColor: (colorManager ? colorManager.getColorNoNotify("dark_gray") : "#000000")
        property color backgroundColorHover: (colorManager ? colorManager.getColor["blue_gray"] : "#000000")
        width: 50
        height: 50
        radius: 50
        Layout.leftMargin: 10
        color: hovered ? backgroundColorHover : backgroundColor

        Image {
            id: wizardIconImage
            source: "../imgs/wizard.png"
            fillMode: Image.PreserveAspectFit
            anchors.centerIn: parent
            width: 30
            height: 30
        }

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            onEntered: {
                wizardIconRectangle.hovered = true;
            }
            onExited: {
                wizardIconRectangle.hovered = false;
            }
            onClicked: {
                backend.toggle_menu();
            }
        }

        ColorOverlay {
            id: wizardColorOverlay
            anchors.fill: wizardIconImage
            source: wizardIconImage
            color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
        }
    }

    Rectangle {
        id: microphoneIconRectangle
        property bool hovered: false
        property bool isRecording: false
        property bool isTranscribing: false
        property color backgroundColor: (colorManager ? colorManager.getColorNoNotify("dark_gray") : "#000000")
        property color backgroundColorHover: (colorManager ? colorManager.getColor["blue_gray"] : "#000000")
        width: 50
        height: 50
        radius: 50
        color: hovered ? backgroundColorHover : backgroundColor

        Image {
            id: microphoneIconImage
            source: "../imgs/microphone.png"
            fillMode: Image.PreserveAspectFit
            anchors.centerIn: parent
            width: 30
            height: 30
        }

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            enabled: !microphoneIconRectangle.isTranscribing
            onEntered: microphoneIconRectangle.hovered = true
            onExited: microphoneIconRectangle.hovered = false

            onClicked: {
                if (!microphoneIconRectangle.isRecording) {
                    backend.startRecording();
                    microphoneIconRectangle.isRecording = true;
                } else {
                    backend.stopRecording();
                    microphoneIconRectangle.isRecording = false;
                }
            }
        }

        ColorOverlay {
            id: microphoneColorOverlay
            anchors.fill: microphoneIconImage
            source: microphoneIconImage
            color: microphoneIconRectangle.isTranscribing ? "#2196F3" : (microphoneIconRectangle.isRecording ? "red" : (colorManager ? colorManager.getColorNoNotify("default") : "#000000"))
        }

        Connections {
            target: backend
            function onTranscriptionReady(result) {
                promptInputField.text = result;
                microphoneIconRectangle.isTranscribing = false;
                microphoneIconRectangle.isRecording = false;
            }
            function onTranscriptionStarted() {
                microphoneIconRectangle.isTranscribing = true;
            }
            function onTranscriptionError(error) {
                microphoneIconRectangle.isTranscribing = false;
                microphoneIconRectangle.isRecording = false;
            }
        }
    }

    Rectangle {
        id: promptInputRectangle
        Layout.fillWidth: true
        Layout.minimumWidth: 60
        Layout.maximumWidth: parent.width - 170
        height: 50
        color: (colorManager ? colorManager.getColorNoNotify("dark_bluish_gray") : "#000000")
        radius: 10

        TextField {
            id: promptInputField
            placeholderText: qsTr("Enter your prompt...")
            font.pixelSize: 18
            width: parent.width - 80
            height: parent.height
            color: (colorManager ? colorManager.getColorNoNotify("light_gray") : "#000000")
            placeholderTextColor: (colorManager ? colorManager.getColorNoNotify("blue_gray") : "#000000")
            background: Rectangle {
                color: "transparent"
            }
            onAccepted: sendPrompt();
        }

        Image {
            id: sendIconImage
            source: "../imgs/send.svg"
            width: 20
            height: 20
            anchors.verticalCenter: parent.verticalCenter
            anchors.right: parent.right
            anchors.rightMargin: 10

            MouseArea {
                id: sendMouseArea
                anchors.fill: parent
                onClicked: sendPrompt();
            }
        }

        ColorOverlay {
            id: sendColorOverlay
            anchors.fill: sendIconImage
            source: sendIconImage
            color: (colorManager ? colorManager.getColorNoNotify("light_bluish_gray") : "#000000")
        }
    }

    function sendPrompt() {
        if (backend.shared_variable["Chargement"] == false) {
            backend.receivePrompt(promptInputField.text);
            promptInputField.text = "";
        }
    }
}
