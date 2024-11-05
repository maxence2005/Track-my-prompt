import QtQuick 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: mainRectangle
    visible: true
    color: (colorManager?.getColor["anthracite_gray"] ?? "FFFFFF")
    width: parent ? parent.width : 1536
    height: parent ? parent.height : 864

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
        spacing: 10

        Rectangle {
            color: "transparent"
            height: parent.width
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
            Layout.alignment: Qt.AlignHCenter // Alignement horizontal centré
            Layout.preferredWidth: 600
            Layout.minimumHeight: 50
            Layout.maximumHeight: 100
        }

        PromptInput {
            id: promptInputComponent
            Layout.alignment: Qt.AlignBottom
            Layout.preferredWidth: parent.width - 150
            Layout.minimumHeight: 80
            Layout.maximumHeight: 100
        }

        // Marge simulée en bas
        Rectangle {
            color: "transparent"
            height: parent.width
            Layout.fillWidth: true
        }
    }
}
