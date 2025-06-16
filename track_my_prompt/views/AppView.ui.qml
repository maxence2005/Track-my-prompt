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
import "Encyclopedie" as Encyclopedie
import "Settings" as Settings
import Qt5Compat.GraphicalEffects

Rectangle {
    property var mediaModel: (appContext ? appContext.mediaModel : null)
    property var databaseManager: (appContext ? appContext.databaseManager : null)
    property var databaseManagerHistorique: (appContext ? appContext.databaseManagerHistorique : null)
    property var encyclopediaModel: (appContext ? appContext.encyclopediaModel : null)
    property var historiqueModel: (appContext ? appContext.historiqueModel : null)
    property var backend: (appContext ? appContext.backend : null)
    property var colorManager: (appContext ? appContext.colorManager : null)
    property var languageManager: (appContext ? appContext.languageManager : null)

    anchors.fill: parent 
    
    Component {
        id: promptMenuComponent
        PromptMenu.PromptMenu {}
    }

    Component {
        id: encyclopedie
        Encyclopedie.Encyclopedie {} 
    }

    Row {
        id: appView
        width: parent.width
        height: parent.height

        NavBar.NavBar {
            id: navBar
            width: 240
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            enabled: (backend ? !backend.shared_variable["settingsMenuShowed"] : true) && (backend ? !backend.shared_variable["Erreur"] : true) && (backend ? !backend.shared_variable["Camera"] : true)
        }

        Loader {
            id: contentLoader
            width: parent.width - 240

            anchors.top: parent.top
            anchors.bottom: parent.bottom
            enabled: (backend ? !backend.shared_variable["settingsMenuShowed"] : true) && (backend ? !backend.shared_variable["Erreur"] : true) && (backend ? !backend.shared_variable["Camera"] : true)
            sourceComponent: (backend ? (backend.shared_variable["Menu"] ? promptMenuComponent : encyclopedie) : promptMenuComponent )
        }
    }

    Rectangle {
        id: interactionBlocker
        color: "transparent"
        anchors.fill: parent
        visible: (backend ? backend.shared_variable["settingsMenuShowed"] : false) || (backend ? backend.shared_variable["Erreur"] : false) || (backend ? backend.shared_variable["Camera"] : false)
        MouseArea {
            anchors.fill: parent
            enabled: true
            hoverEnabled: true
        }
    }

    FastBlur {
        id: blurEffect
        visible: (backend ? backend.shared_variable["settingsMenuShowed"] : false ) || (backend ? backend.shared_variable["Erreur"] : false) || (backend ? backend.shared_variable["Camera"] : false)
        anchors.fill: parent
        source: appView
        radius: 50
    }

    Settings.Param {
        id: param
        visible: (backend ? backend.shared_variable["settingsMenuShowed"] : false)
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        width: parent.width * 0.8
        height: parent.height * 0.8
    }

    Erreur {
        id: erreur
        visible: (backend ? backend.shared_variable["Erreur"] : false)
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        width: parent.width * 0.8
        height: parent.height * 0.8
    }

    WebCam {
        id: webcam
        visible: (backend ? backend.shared_variable["Camera"] : false)
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        width: parent.width * 0.8
        height: parent.height * 0.8
    }

    function showCelebration() {
        celebrationOverlay.visible = true;
        hideCelebrationTimer.start();
    }

    Rectangle {
        id: celebrationOverlay
        anchors.fill: parent
        z: 999
        visible: false
        color: "transparent"

        ShaderEffectSource {
            id: celebrationBlurSource
            anchors.fill: parent
            sourceItem: appView
            hideSource: false
            live: true
        }

        FastBlur {
            anchors.fill: parent
            source: celebrationBlurSource
            radius: 90
        }

        Fireworks {
            anchors.fill: parent
            running_p: celebrationOverlay.visible
        }

        Column {
            anchors.centerIn: parent
            spacing: 16 

            Text {
                id: mainText
                text: "🎉 Bravo, vous avez 100% ! 🎉"
                font.pixelSize: 46
                color: "white"
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
            }

            Text {
                text: "Une surprise vous attend dans les paramètres !"
                font.pixelSize: 23
                color: "white"
                font.bold: true
                anchors.horizontalCenter: mainText.horizontalCenter
            }
        }

        Timer {
            id: hideCelebrationTimer
            interval: 10000
            repeat: false
            onTriggered: celebrationOverlay.visible = false
        }
    }
}
