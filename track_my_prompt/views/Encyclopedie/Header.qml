import QtQuick 2.15
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls 2.15

Rectangle {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [headerRectangle, "color", "anthracite_gray"],
                [headerLabel, "color", "default"],
                [progressBackground, "color", "medium_gray"],
                //[progressColor, "color", "blue_gray"],
                [progressText, "color", "default"],
                [gradientStop0, "color", "dark_bluish_gray"],
                [gradientStop1, "color", "anthracite_gray"],
                [searchField, "color", "default"],
                [searchFieldBackground, "color", "medium_gray"]
            ])
        }
    }

    Connections {
        target: languageManager
        function onLanguageChanged() {
            searchField.text = ""
        }
    }

    Connections {
        target: backend
        function onCelebrationUnlocked() {
            showCelebration()
        }
    }

    id: headerRectangle
    property double progression: 0
    width: parent.width
    height: parent.height * 0.3
    color: (colorManager ? colorManager.getColorNoNotify("anthracite_gray") : "#000000")
    anchors.margins: 15
    radius: 20
    Rectangle {
        anchors.fill: parent
        radius: 20

        gradient: Gradient {
            GradientStop {
                id : gradientStop0
                position: 0.0
                color: (colorManager ? colorManager.getColorNoNotify("dark_bluish_gray") : "#000000")
            } 
            GradientStop {
                id : gradientStop1
                position: 1.0
                color: (colorManager ? colorManager.getColorNoNotify("anthracite_gray") : "#000000")
            }
        }
    }
    Rectangle {
        anchors.fill: parent
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 5 
        color: Qt.rgba(0, 0, 0, 0.2)  
        radius: 20
        z: -1 
    }

    RowLayout {
        id: headerRow
        anchors.top: headerRectangle.top
        anchors.topMargin: 10
        width: parent.width * 0.8
        spacing: 0

        Button {
            id: giftButton
            text: "🎁"
            visible: !backend.hasUnlocked100() && progressBar.value >= 1.0
            onClicked: {
                backend.checkAndUnlock100(Math.round(progressBar.value * 100))
            }
            font.pixelSize: parent.width/15
            
            background: Rectangle {
                radius: 10
                color: "transparent"
            }
        }

        Label {
            id: headerLabel
            text: qsTr("Encyclopedia")
            font.pixelSize: parent.width/15
            horizontalAlignment: Text.AlignHCenter
            Layout.alignment: Qt.AlignHCenter
            color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
        }
    }


    ProgressBar {
        id: progressBar
        height: parent.height * 0.06
        anchors.leftMargin: parent.width * 0.1
        anchors.rightMargin: parent.width * 0.1
        value: headerRectangle.progression
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.verticalCenterOffset: 0

        contentItem: Item {
            width: progressBar.width
            height: progressBar.height

            Rectangle {
                id: progressBackground
                width: parent.width
                height: parent.height
                color: (colorManager ? colorManager.getColorNoNotify("medium_gray") : "#000000")
            }

            Rectangle {
                id: progressColor
                width: parent.width * progressBar.value
                height: parent.height
                color: "blue"
            }
        }
    }


    Text {
        id: progressText
        text: Math.round(progressBar.value * 100) + " %"
        font.pixelSize: parent.width / 50
        anchors.verticalCenter: progressBar.verticalCenter
        anchors.left: progressBar.right
        anchors.leftMargin: parent.width * 0.01
        color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
    }

    TextField {
        id: searchField
        placeholderText: qsTr("Search for an item")
        anchors.top: progressBar.bottom
        anchors.topMargin: 16
        anchors.horizontalCenter: parent.horizontalCenter
        width: parent.width * 0.8
        font.pixelSize: 16
        color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
        background: Rectangle {
            id: searchFieldBackground
            color: (colorManager ? colorManager.getColorNoNotify("medium_gray") : "#888888")
            radius: 10
        }
        onTextChanged: databaseManager.set_search_text(searchField.text)
    }
}
