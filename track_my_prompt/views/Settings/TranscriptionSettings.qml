import QtQuick 2.15
import QtQuick.Controls 2.15

Column {
    id: transcriptionSettingsColumn
    spacing: 20

    Text {
        id: transcriptionLabel
        text: qsTr("Mode de transcription")
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
        onActivated: {
            var selected = modeSelector.model[modeSelector.currentIndex];
            if (backend && selected) {
                backend.setTranscriptionMode(selected.value)
            }
        }
    }
}