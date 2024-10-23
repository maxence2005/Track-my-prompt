

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

Rectangle {
    anchors.fill: parent  // Remplit l'espace du parent

    NavBar.NavBar {
        id: navBar
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        width: parent.width * 0.2
    }

    PromptMenu.PromptMenu {
        id: promptMenu
        anchors.left: navBar.right
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.bottom: parent.bottom
    }
}