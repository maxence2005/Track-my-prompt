/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick.Controls
import "PromptMenu" as PromptMenu
import "NavBar" as NavBar
import "Encyclopedie" as  Encyclopedie
import Qt5Compat.GraphicalEffects

Rectangle {
    anchors.fill: parent  // Remplit l'espace du parent

    ListModel {
        id: mediaModel
    }

    Connections {
        target: backend
        function onMediaAdded(filePath, mediaType) {
            mediaModel.append({ "filePath": filePath, "mediaType": mediaType });
        }
    }
    
    Component {
        id: promptMenuComponent
        PromptMenu.PromptMenu {}
    }

    Component {
        id: encyclopedie
        Encyclopedie.Encyclopedie {} // Remplacez par le vrai nom de l'autre composant
    }

    Row {
        id: appView
        width: parent.width
        height: parent.height

        NavBar.NavBar {
            id: navBar
            width: parent.width * 0.2
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            enabled: (!backend?.shared_variable["settingsMenuShowed"] ?? true) && (!backend?.shared_variable["Erreur"] ?? true)
        }

        Loader {
            id: contentLoader
            width: parent.width * 0.8
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            enabled: (!backend?.shared_variable["settingsMenuShowed"] ?? true) && (!backend?.shared_variable["Erreur"] ?? true)
            sourceComponent: (backend ? (backend.shared_variable["Menu"] ? promptMenuComponent : encyclopedie) : promptMenuComponent )
        }
    }

    // Rectangle transparent pour désactiver les interactions
    Rectangle {
        id: interactionBlocker
        color: "transparent"
        anchors.fill: parent
        visible: (backend?.shared_variable["settingsMenuShowed"] ?? false) || (backend?.shared_variable["Erreur"] ?? false)
        MouseArea {
            anchors.fill: parent
            enabled: true
            hoverEnabled: true
        }
    }

    FastBlur {
        id: blurEffect
        visible: (backend?.shared_variable["settingsMenuShowed"] ?? false ) || (backend?.shared_variable["Erreur"] ?? false)
        anchors.fill: parent
        source: appView
        radius: 50
    }

    Param {
        id: param
        visible: (backend?.shared_variable["settingsMenuShowed"] ?? false)
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        width: parent.width * 0.8
        height: parent.height * 0.8
    }

    Erreur {
        id: erreur
        visible: (backend?.shared_variable["Erreur"] ?? false)
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        width: parent.width * 0.8
        height: parent.height * 0.8
    }
}
