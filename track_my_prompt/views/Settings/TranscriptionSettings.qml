import QtQuick 2.15
import QtQuick.Controls 2.15

Column {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [transcriptionLabel, "color", "default"],
            ])
        }
    }

    id: transcriptionSettingsColumn
    spacing: 20

    Text {
        id: transcriptionLabel
        text: qsTr("Transcription Mode")
        font.pixelSize: 20
        color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
    }

    ComboBox {
        id: modeSelector
        width: 200
        model: [
            { text: "API", value: "api" },
            { text: "Local", value: "local" }
        ]
        textRole: "text"
        valueRole: "value"
        Component.onCompleted: {
            var currentMode = backend.transcriptionMode;
            for (var i = 0; i < modeSelector.model.length; i++) {
                if (modeSelector.model[i].value === currentMode) {
                    modeSelector.currentIndex = i;
                    break;
                }
            }
        }
        onActivated: {
            var selected = modeSelector.model[modeSelector.currentIndex];
            if (backend && selected) {
                backend.setTranscriptionMode(selected.value)
            }
        }
    }
}