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

            // Function that handles starting the bot by interacting with the backend and frontend.
            function startBot(){
                internal.isBotRunning = true

                // Start logging.
                logTextArea.text = "" // Reset the log when starting it up.
                updateLogTimerFunction.running = true
                checkBotStatusTimerFunction.running = true
                console.log("Parsing bot logs now...")

                // Start the backend process.
                backend.start_bot()

                // Update the GUI.
                startStopButton.text = qsTr("Stop")
                topBarLeftLabel.text = qsTr("Bot Status: Running")
                startStopButton.colorDefault = "#aa0000"
            }

            // Function that handles stopping the bot by interacting with the backend and frontend.
            function stopBot(){
                internal.isBotRunning = false

                // Stop logging.
                updateLogTimerFunction.running = false
                checkBotStatusTimerFunction.running = false
                console.log("Now stopping parsing bot logs.")

                // Stop the backend process.
                backend.stop_bot()

                // Update the GUI.
                startStopButton.text = qsTr("Start")
                topBarLeftLabel.text = qsTr("Bot Status: Not Running")
                startStopButton.colorDefault = "#4891d9"
            }
        }

        CustomButton {
            id: startStopButton
            
            x: 300
            y: 208
            width: 100
            height: 50

            text: startStopButton.enabled ? qsTr("Start") : qsTr("Start disabled")

            enabled: false

            colorDefault: startStopButton.enabled ? "#4891d9" : "#57585c"
            customRadius: 20

            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.rightMargin: 70

            // Starts or stops the bot depending on whether it was already running or not.
            onClicked: {
                if(internal.isBotRunning == false){
                    internal.startBot()
                }else{
                    internal.stopBot()
                }
            }
        }

        TextField {
            id: combatScriptTextField
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            horizontalAlignment: Text.AlignHCenter
            anchors.rightMargin: 20
            anchors.topMargin: 20
            anchors.leftMargin: 20

            readOnly: true

            placeholderText: qsTr("Combat Script: None selected")
        }

        Label {
            id: combatScriptTextFieldLabel
            x: 20
            width: 260
            height: 13
            color: "#00ff00"
            text: qsTr("Combat script loaded successfully")
            anchors.top: combatScriptTextField.bottom
            horizontalAlignment: Text.AlignHCenter
            anchors.topMargin: 2

            visible: false
        }

        Timer{
            id: updateLogTimerFunction

            interval: 1000
            running: false
            repeat: true

            onTriggered: backend.update_console_log() // Call update_console_log() in the backend.
        }

        Timer{
            id: checkBotStatusTimerFunction

            interval: 1000
            running: false
            repeat: true

            onTriggered: backend.check_bot_status()
        }

        Connections{
            target: backend

            // Retrieve the string returned from update_console_log from the backend and update the log text in the window.
            function onUpdateConsoleLog(line){
                logTextArea.append(line)
            }

            // Stop the bot when the backend signals the frontend that it has ended.
            function onCheckBotStatus(check){
                if(check){
                    internal.stopBot()
                }
            }

            // Retrieve the name of the opened script file back from backend.
            function onOpenFile(scriptName){
                combatScriptTextField.text = qsTr(scriptName)
                combatScriptTextFieldLabel.visible = true
            }

            // Enable or disable the Start/Stop button depending on whether the user completed the instructions shown on screen.
            function onCheckBotReady(flag){
                startStopButton.enabled = flag
            }
        }
    }
}





/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:1.66;height:453;width:300}
}
##^##*/
