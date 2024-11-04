import QtQuick 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: mainRectangle
    visible: true
    color: (colorManager?.getColor["anthracite_gray"] ?? "FFFFFF")
    width: parent ? parent.width : 800
    height: parent ? parent.height : 600

    Component {
        id: aff
        Afficher {}
    }

    Component {
        id: ex
        Exemples {}
    }

    ColumnLayout {
        id: mainColumnLayout
        anchors.fill: parent
        spacing: 20

        // Ajouter une marge simulée autour du contenu
        Rectangle {
            color: "transparent"
            height: Qt.application.activeWindow.width > 600 ? 30 : 10
            Layout.fillWidth: true
        }

        // Composant Header, aligné en haut
        Header {
            id: headerComponent
            Layout.alignment: Qt.AlignTop
            Layout.fillWidth: true
        }

        Loader {
            id: exemplesComponent
            Layout.alignment: Qt.AlignVCenter
            Layout.fillWidth: true
            Layout.fillHeight: true
            sourceComponent: (backend && backend.shared_variable["Start"]) ? ex : aff
        }


        ChooseFile {
            id: chooseFileComponent
            Layout.alignment: Qt.AlignCenter
            Layout.preferredWidth: Qt.application.activeWindow.width > 600 ? 400 : 200
            Layout.minimumHeight: 50
            Layout.maximumHeight: 100
        }


        PromptInput {
            id: promptInputComponent
            Layout.alignment: Qt.AlignBottom
            Layout.fillWidth: true
            Layout.minimumHeight: 80
        }

        // Marge simulée en bas
        Rectangle {
            color: "transparent"
            height: Qt.application.activeWindow.width > 600 ? 30 : 10
            Layout.fillWidth: true
        }
    }
}