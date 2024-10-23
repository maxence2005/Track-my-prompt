import QtQuick 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: mainRectangle
    visible: true
    width: 800
    height: 600
    color: "#33343b" // Couleur de fond similaire à celle de l'image

    ColumnLayout {
        id: mainColumnLayout
        anchors.centerIn: parent
        spacing: 50

        // Inclure le composant Header avec Layout.alignment
        Header {
            id: headerComponent
            Layout.alignment: Qt.AlignTop
        }

        // Inclure le composant Exemples avec Layout.alignment
        Exemples {
            id: exemplesComponent
            Layout.alignment: Qt.AlignCenter
        }

        // Inclure le composant DragDrop
        ChooseFile {
            id: chooseFileComponent
        }

        // Inclure le composant PromptInput avec Layout.alignment
        PromptInput {
            id: promptInputComponent
            Layout.alignment: Qt.AlignBottom
        }
    }
}