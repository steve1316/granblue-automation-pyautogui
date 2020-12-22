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
                //console_log_text.text = "" // Reset the log when starting it up.
                timerFunction.running = true
                console.log("Parsing bot logs now...")
            }

            function stopLogParsing(){
                timerFunction.running = false
                console.log("Now stopping parsing bot logs.")
            }

            function startBot(){
                backend.start_bot()
            }

            function stopBot(){
                backend.stop_bot()
            }
        }

        Button {
            id: startButton
            x: 300
            y: 208
            width: 40
            text: qsTr("Start")
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.rightMargin: 70

            onClicked: {
                if(internal.isBotRunning == false){
                    internal.startLogParsing()
                    internal.isBotRunning = true

                    startButton.text = qsTr("Stop")

                    internal.startBot()
                }else{
                    internal.stopLogParsing()
                    internal.isBotRunning = false

                    startButton.text = qsTr("Start")

                    internal.stopBot()
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
