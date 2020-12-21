import QtQuick 2.15
import QtQuick.Controls 2.15
import "../controls"

Item{
    Rectangle {
        id: rectangle
        color: "#323741"
        anchors.fill: parent

        QtObject{
            id: internal

            property bool isBotRunning: false

            function startLogParsing(){
                timerFunction.running = true
                console.log("Parsing bot logs now...")
            }

            function stopLogParsing(){
                timerFunction.running = false
                console.log("Now stopping parsing bot logs.")
            }
        }

        Rectangle {
            id: scrollViewContainer
            y: 38
            color: "#2f2f2f"
            radius: 10
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            clip: false
            anchors.leftMargin: 290
            anchors.rightMargin: 50
            anchors.bottomMargin: 50
            anchors.topMargin: 50

            ScrollView {
                id: scrollView
                x: -10
                y: 0
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.bottom: parent.bottom

                contentHeight: console_log_text.contentHeight + 50 // Update the scrollView's content height to always have room for the console log text.
                contentWidth: 280

                clip: true
                wheelEnabled: true
                anchors.rightMargin: 10
                anchors.leftMargin: 10
                anchors.bottomMargin: 10
                anchors.topMargin: 10

                Text{
                    id: console_log_text

                    color: "#ffffff"
                    text: ""
                    elide: Text.ElideNone
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    font.pixelSize: 12
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignTop
                    wrapMode: Text.WordWrap
                    anchors.rightMargin: 10
                    anchors.leftMargin: 10
                    anchors.bottomMargin: 10
                    anchors.topMargin: 10
                    clip: false
                    maximumLineCount: 10000
                    textFormat: Text.PlainText
                }
            }
        }

        Button {
            id: startButton
            width: 40
            text: qsTr("Start")
            anchors.left: parent.left
            anchors.right: scrollViewContainer.left
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.rightMargin: 70
            anchors.leftMargin: 88
            anchors.bottomMargin: 220
            anchors.topMargin: 220

            onClicked: {
                if(internal.isBotRunning == false){
                    internal.startLogParsing()
                    internal.isBotRunning = true

                    startButton.text = qsTr("Stop")
                }else{
                    internal.stopLogParsing()
                    internal.isBotRunning = false

                    startButton.text = qsTr("Start")
                }

                // backend.start_bot()
            }
        }

        Timer{
            id: timerFunction
            interval: 1000
            running: false
            repeat: true
            onTriggered: backend.update_console_log("he123456")
        }

        Connections{
            target: backend

            function onUpdateConsoleLog(line){
                console_log_text.text += line
            }
        }
    }


}



/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:1.33;height:480;width:640}
}
##^##*/
