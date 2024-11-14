
import QtQuick 2.15
import QtQuick.Controls 2.15

Column {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [promptInterpreterLabel, "color", "default"],
            ])
        }
    }

    id: promptInterpreterColumn
    spacing: 20

    Text {
        id: promptInterpreterLabel
        text: qsTr("Change the prompt interpreter")
        font.pixelSize: 20
        color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
    }

    ComboBox {
        id: promptInterpreterComboBox
        model: ListModel {
            ListElement { elementId: "dumb"; name: qsTr("Dumb") }
            ListElement { elementId: "mistral"; name: "Mistral" }
        }
        width: 100
        textRole: "name"
        onActivated: {
            var selectedItem = promptInterpreterComboBox.model.get(promptInterpreterComboBox.currentIndex);
            var selectedId = selectedItem.elementId;
            backend.change_prompt_recognition(selectedId, "");
            verifyMistralField(selectedId);
        }
    }

    TextField {
        id: promptInterpreterApiKeyField
        placeholderText: qsTr("Mistral API Key")
        text: backend ? backend.shared_variable["api_key_mistral"] : ""
        visible: false
        width: 200
        echoMode: TextInput.PasswordEchoOnEdit

        onEditingFinished: {
            var selectedItem = promptInterpreterComboBox.model.get(promptInterpreterComboBox.currentIndex);
            var selectedId = selectedItem.elementId;
            backend.change_prompt_recognition(selectedId, text)
        }
    }

    Component.onCompleted: {
        var currentPromptInterpreter = backend.shared_variable["prompt_ia"];
        for (var i = 0; i < promptInterpreterComboBox.count; i++) {
            var item = promptInterpreterComboBox.model.get(i);
            if (item.elementId === currentPromptInterpreter) {
                promptInterpreterComboBox.currentIndex = i;
                break;
            }
        }
        verifyMistralField(item.elementId);
    }

    function verifyMistralField(id) {
        if (id === "mistral") {
            promptInterpreterApiKeyField.visible = true;
        } else {
            promptInterpreterApiKeyField.visible = false;
        }
    }
}
