import QtQuick 2.15
import QtQuick.Controls 2.15
import "../controls"

Item{
    Rectangle {
        id: pageContainer

        color: "#323741"
        anchors.fill: parent

        QtObject{
            id: internal

            property bool isBotRunning: false

            function startLogParsing(){
                logTextArea.text = "" // Reset the log when starting it up.
                timerFunction.running = true
                console.log("Parsing bot logs now...")
            }

            function stopLogParsing(){
                timerFunction.running = false
                console.log("Now stopping parsing bot logs.")
            }

            function startBot(){
                backend.start_bot()

                topBarLeftLabel.text = qsTr("Bot Status: Running")
            }

            function stopBot(){
                backend.stop_bot()

                topBarLeftLabel.text = qsTr("Bot Status: Not Running")
            }
        }

        CustomButton {
            id: startStopButton
            
            x: 300
            y: 208
            width: 100
            height: 50

            text: qsTr("Start")

            colorDefault: "#4891d9"
            customRadius: 20

            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.rightMargin: 70

            // Starts or stops the bot depending on whether it was already running or not.
            onClicked: {
                if(internal.isBotRunning == false){
                    internal.startLogParsing()
                    internal.isBotRunning = true

                    startStopButton.text = qsTr("Stop")

                    internal.startBot()

                    startStopButton.colorDefault = "#aa0000"
                }else{
                    internal.stopLogParsing()
                    internal.isBotRunning = false

                    startStopButton.text = qsTr("Start")

                    internal.stopBot()

                    startStopButton.colorDefault = "#4891d9"
                }
            }
        }

        Timer{
            id: timerFunction

            interval: 1000
            running: false
            repeat: true

            onTriggered: backend.update_console_log("") // Call update_console_log() in the backend.
        }

        Connections{
            target: backend

            // Retrieve the string returned from update_console_log from the backend and update the log text in the window.
            function onUpdateConsoleLog(line){
                logTextArea.append(line)
            }
        }
    }
}





/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:1.1;height:480;width:640}
}
##^##*/
