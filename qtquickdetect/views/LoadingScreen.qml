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

    Timer {
        interval: 1000 / textAnim.length
        repeat: true
        running: true
        onTriggered: {
			let textAnimArray = textAnim.split("")

            if (index <= textAnim.length) {
				let point = (index == textAnim.length ? "" : ".")
                animatedText.text = textAnimArray.slice(0, index).join("") + point ;
            } else {
                stop()
            }
			root.index += 1
        }
    }
}