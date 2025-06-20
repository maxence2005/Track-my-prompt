import QtQuick 2.0
import QtQuick.Controls 2.0

Rectangle {
    id: root
    width: 300
    height: 300
    color: "#33343B"

    Text {
        id: animatedText
        anchors.centerIn: parent
        font.pixelSize: 80
        text: ""
        color: "white"
        font.family: "Smothy Bubble"
    }

    property var textAnim: "Track My Prompts"
    property int index: 0
    property var dots: ["", ".", "..", "..."]
    property int dotIndex: 0
    property bool textFinished: false

    Timer {
        id: textTimer
        interval: 1000 / textAnim.length
        repeat: true
        running: true
        onTriggered: {
            if (index <= textAnim.length) {
                animatedText.text = textAnim.slice(0, index)
                index += 1
            } else {
                textFinished = true
                textTimer.stop()
                dotsTimer.start()
            }
        }
    }

    Timer {
        id: dotsTimer
        interval: 500
        repeat: true
        running: false
        onTriggered: {
            if (textFinished) {
                animatedText.text = textAnim + dots[dotIndex]
                dotIndex = (dotIndex + 1) % dots.length
            }
        }
    }
}
