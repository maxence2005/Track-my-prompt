import QtQuick 2.15
import QtQuick.Layouts 1.15

Rectangle {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [mainRectangle, "color", "anthracite_gray"]
            ])
        }
    }
    id: mainRectangle
    visible: true
    color: (colorManager?.getColorNoNotify("anthracite_gray") ?? "#000000")
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
            height: 30
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
            height: 30
            Layout.fillWidth: true
        }
    }
}
