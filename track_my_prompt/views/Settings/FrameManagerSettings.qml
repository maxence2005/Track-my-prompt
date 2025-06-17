import QtQuick 2.15
import QtQuick.Controls 2.15

Column {
    Connections {
        target: colorManager
        function onThemeChanged() {
            colorManager.animateColorChange([
                [frameManagerLabel, "color", "default"],
                [frameColorPreview, "border.color", "default"]
            ])
        }
    }

    Rectangle {
        id: frameManagerContainer
        width: 200
        height: 130
        color: "transparent"

        Column {
            id: frameManagerColumn
            spacing: 12

            Row {
                id: frameManagerLabelRow
                Text {
                    id: frameManagerLabel
                    text: qsTr("Choose a color")
                    font.pixelSize: 20
                    color: (colorManager ? colorManager.getColorNoNotify("default") : "#000000")
                }
            }

            Row {
                id: frameManagerToggleRow
                spacing: 20
                anchors.horizontalCenter: parent.horizontalCenter

                Rectangle {
                    id: frameColorPreview
                    width: 24
                    height: 24
                    radius: 4
                    border.color: colorManager ? colorManager.getColorNoNotify("default") : "#000"
                    border.width: 1
                    visible: !(appContext && appContext.backend && appContext.backend.shared_variable.frame_color === "rainbow")
                    color: appContext && appContext.backend ? appContext.backend.shared_variable.frame_color === "rainbow" ? "#db1f1f" : appContext.backend.shared_variable.frame_color : "#787878"

                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        onClicked: backend.openColorDialog()
                    }
                }

                Row {
                    spacing: 6
                    anchors.verticalCenter: parent.verticalCenter

                    Item {
                        width: rainbowText.implicitWidth
                        height: rainbowText.implicitHeight

                        Rectangle {
                            anchors.fill: parent
                            radius: 4
                            color: "#787878"
                            visible: !(appContext && appContext.backend && appContext.backend.shared_variable.frame_color === "rainbow") && (appContext && appContext.backend && appContext.backend.hasUnlocked100())

                            MouseArea {
                                anchors.fill: parent
                                cursorShape: Qt.PointingHandCursor
                                onClicked: {
                                    if (!appContext || !appContext.backend) return;
                                    backend.toggle_rainbow()
                                }
                            }
                        }

                        Rectangle {
                            anchors.fill: parent
                            radius: 4
                            clip: true
                            visible: (appContext && appContext.backend && appContext.backend.shared_variable.frame_color === "rainbow" && appContext.backend.hasUnlocked100())

                            gradient: Gradient {
                                GradientStop { position: 0.0; color: "red" }
                                GradientStop { position: 0.2; color: "orange" }
                                GradientStop { position: 0.4; color: "yellow" }
                                GradientStop { position: 0.6; color: "green" }
                                GradientStop { position: 0.8; color: "blue" }
                                GradientStop { position: 1.0; color: "purple" }
                            }

                            MouseArea {
                                anchors.fill: parent
                                cursorShape: Qt.PointingHandCursor
                                onClicked: {
                                    if (!appContext || !appContext.backend) return;
                                    backend.disable_rainbow()
                                }
                            }
                        }

                        Text {
                            id: rainbowText
                            text: qsTr("Multicolor")
                            visible: (appContext && appContext.backend && appContext.backend.shared_variable.frame_color && appContext.backend.hasUnlocked100())
                            font.pixelSize: 18
                            color: "#1f1c1c"
                            anchors.centerIn: parent
                        }
                    }
                }
            }
        }
    }
}
