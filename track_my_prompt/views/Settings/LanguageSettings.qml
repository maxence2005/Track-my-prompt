import QtQuick 2.15
import QtQuick.Controls 2.15

Column {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [languageLabel, "color", "default"],
            ])
        }
    }
    id: languageSettingsColumn
    spacing: 20

    Row {
        id: languageRow
        spacing: 10

        Text {
            id: languageLabel
            text: qsTr("Application Language")
            font.pixelSize: 20
            color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
        }

        ComboBox {
            id: languageComboBox
            model: languageManager ? languageManager.getLanguages : []
            width: 100
            onActivated : {
                languageManager.setLanguage(languageComboBox.currentText)
            }
        }
        Component.onCompleted: {
            var currentLanguage = languageManager.getCurrentLanguage;
            for (var i = 0; i < languageComboBox.count; i++) {
                if (languageComboBox.model[i] === currentLanguage) {
                    languageComboBox.currentIndex = i;
                    break;
                }
            }
        }
    }

    Button {
        id: installLanguageButton
        text: qsTr("Install a Language Pack")
        width: 200
        height: 40
        onClicked: {
            languageManager.install_new_language()
        }
    }
}