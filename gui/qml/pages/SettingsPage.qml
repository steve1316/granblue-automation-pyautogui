import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs 1.3

import "../controls"

Item{
    Rectangle {
        id: settingsContainer

        color: "#323741"
        anchors.fill: parent
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 0

        TextField {
            id: combatScriptTextField
            anchors.left: parent.left
            anchors.top: parent.top
            horizontalAlignment: Text.AlignHCenter
            anchors.topMargin: 20
            anchors.leftMargin: 20

            readOnly: true

            placeholderText: qsTr("Combat Script: None selected")
        }

        Label {
            id: combatScriptTextFieldLabel
            x: 20
            width: 200
            height: 13
            color: "#00ff00"
            text: qsTr("Combat script loaded successfully")
            anchors.top: combatScriptTextField.bottom
            anchors.topMargin: 5

            visible: false
        }

        CustomButton{
            id: buttonOpenFile
            y: 20

            text: qsTr("Open")
            anchors.left: combatScriptTextField.right
            anchors.right: parent.right
            anchors.rightMargin: 20
            anchors.leftMargin: 20

            height: 40

            onPressed: {
                fileOpen.open()
            }

            FileDialog{
                id: fileOpen

                title: "Please choose a combat script file"

                // Dialog will default to the /scripts/ folder in the root of the bot directory.
                folder: "../../../scripts/"
                selectMultiple: false
                nameFilters: ["Text File (*.txt)"]

                onAccepted: {
                    backend.open_file(fileOpen.fileUrl)
                }
            }
        }

        // Select the item and the island that the item is farmed in.
        ComboBox {
            id: itemComboBox

            width: 200
            anchors.left: parent.left
            anchors.top: combatScriptTextField.bottom
            enabled: false
            anchors.topMargin: 25
            anchors.leftMargin: 20

            displayText: qsTr("Please select a item to farm.")

            currentIndex: 0
            textRole: "text"
            
            delegate: ItemDelegate {
                width: itemComboBox.width
                text: modelData.text

                font.weight: itemComboBox.currentIndex === index ? Font.DemiBold : Font.Normal
                highlighted: ListView.isCurrentItem

                enabled: modelData.enabled
            }

            model: [
                // Port Breeze Archipelago
                { text: "Port Breeze Archipelago", enabled: false },
                { text: "Satin Feather", map: "Port Breeze Archipelago", enabled: true },
                { text: "Zephyr Feather", map: "Port Breeze Archipelago", enabled: true },
                { text: "Flying Sprout", map: "Port Breeze Archipelago", enabled: true },

                // Valtz Duchy
                { text: "Valtz Duchy", enabled: false },
                { text: "Fine Sand Bottle", map: "Valtz Duchy", enabled: true },
                { text: "Untamed Flame", map: "Valtz Duchy", enabled: true },
                { text: "Blistering Ore", map: "Valtz Duchy", enabled: true },

                // Auguste Isles
                { text: "Auguste Isles", enabled: false },
                { text: "Fresh Water Jug", map: "Auguste Isles", enabled: true },
                { text: "Soothing Splash", map: "Auguste Isles", enabled: true },
                { text: "Glowing Coral", map: "Auguste Isles", enabled: true },

                // Lumacie Archipelago
                { text: "Lumacie Archipelago", enabled: false },
                { text: "Rough Stone", map: "Lumacie Archipelago", enabled: true },
                { text: "Coarse Alluvium", map: "Lumacie Archipelago", enabled: true },
                { text: "Swirling Amber", map: "Lumacie Archipelago", enabled: true },

                // Albion Citadel
                { text: "Albion Citadel", enabled: false },
                { text: "Falcon Feather", map: "Albion Citadel", enabled: true },
                { text: "Spring Water Jug", map: "Albion Citadel", enabled: true },
                { text: "Vermilion Stone", map: "Albion Citadel", enabled: true },

                // Mist-Shrouded Isle
                { text: "Mist-Shrouded Isle", enabled: false },
                { text: "Slimy Shroom", map: "Mist-Shrouded Isle", enabled: true },
                { text: "Hollow Soul", map: "Mist-Shrouded Isle", enabled: true },
                { text: "Lacrimosa", map: "Mist-Shrouded Isle", enabled: true },

                // Golonzo Island
                { text: "Golonzo Island", enabled: false },
                { text: "Wheat Stalk", map: "Golonzo Island", enabled: true },
                { text: "Iron Cluster", map: "Golonzo Island", enabled: true },
                { text: "Olea Plant", map: "Golonzo Island", enabled: true },

                // Amalthea Island
                { text: "Amalthea Island", enabled: false },
                { text: "Indigo Fruit", map: "Amalthea Island", enabled: true },
                { text: "Foreboding Clover", map: "Amalthea Island", enabled: true },
                { text: "Blood Amber", map: "Amalthea Island", enabled: true },

                // Former Capital Mephorash
                { text: "Former Capital Mephorash", enabled: false },
                { text: "Sand Brick", map: "Former Capital Mephorash", enabled: true },
                { text: "Native Reed", map: "Former Capital Mephorash", enabled: true },
                { text: "Antique Cloth", map: "Former Capital Mephorash", enabled: true },

                // Agastia
                { text: "Agastia", enabled: false },
                { text: "Prosperity Flame", map: "Agastia", enabled: true },
                { text: "Explosive Material", map: "Agastia", enabled: true },
                { text: "Steel Liquid", map: "Agastia", enabled: true },
            ]

            onCurrentIndexChanged: {
                itemComboBox.displayText = qsTr(itemComboBox.model[currentIndex].text)

                // Enable the mission ComboBox.
                missionComboBox.enabled = true

                // Update the contents of the mission ComboBox with the appropriate mission(s).
                missionComboBox.currentIndex = 0
                if(itemComboBox.displayText == "Satin Feather" || itemComboBox.displayText == "Zephyr Feather" || itemComboBox.displayText == "Flying Sprout"){
                    missionComboBox.model = [
                        { text: "Port Breeze Archipelago", enabled: false },
                        { text: "Scattered Cargo", enabled: true },
                    ]
                } else if(itemComboBox.displayText == "Fine Sand Bottle" || itemComboBox.displayText == "Untamed Flame" || itemComboBox.displayText == "Blistering Ore"){
                    missionComboBox.model = [
                        { text: "Valtz Duchy", enabled: false },
                        { text: "Lucky Charm Hunt", enabled: true },
                        { text: "Special Op's Request", enabled: true },
                    ]
                } else if(itemComboBox.displayText == "Fresh Water Jug" || itemComboBox.displayText == "Soothing Splash" || itemComboBox.displayText == "Glowing Coral"){
                    missionComboBox.model = [
                        { text: "Auguste Isles", enabled: false },
                        { text: "Threat to the Fisheries", enabled: true },
                    ]
                } else if(itemComboBox.displayText == "Rough Stone" || itemComboBox.displayText == "Swirling Amber" || itemComboBox.displayText == "Coarse Alluvium"){
                    missionComboBox.model = [
                        { text: "Lumacie Archipelago", enabled: false },
                        { text: "The Fruit of Lumacie", enabled: true },
                        { text: "Whiff of Danger", enabled: true },
                    ]
                } else if(itemComboBox.displayText == "Falcon Feather" || itemComboBox.displayText == "Spring Water Jug" || itemComboBox.displayText == "Vermilion Stone"){
                    missionComboBox.model = [
                        { text: "Albion Citadel", enabled: false },
                        { text: "I Challenge You!", enabled: true },
                    ]
                } else if(itemComboBox.displayText == "Slimy Shroom" || itemComboBox.displayText == "Hollow Soul" || itemComboBox.displayText == "Lacrimosa"){
                    missionComboBox.model = [
                        { text: "Mist-Shrouded Isle", enabled: false },
                        { text: "For Whom the Bell Tolls", enabled: true },
                    ]
                } else if(itemComboBox.displayText == "Wheat Stalk" || itemComboBox.displayText == "Iron Cluster" || itemComboBox.displayText == "Olea Plant"){
                    missionComboBox.model = [
                        { text: "Golonzo Island", enabled: false },
                        { text: "Golonzo's Battle of Old", enabled: true },
                    ]
                } else if(itemComboBox.displayText == "Indigo Fruit" || itemComboBox.displayText == "Foreboding Clover" || itemComboBox.displayText == "Blood Amber"){
                    missionComboBox.model = [
                        { text: "Amalthea Island", enabled: false },
                        { text: "The Dungeon Diet", enabled: true },
                    ]
                } else if(itemComboBox.displayText == "Sand Brick" || itemComboBox.displayText == "Native Reed"){
                    missionComboBox.model = [
                        { text: "Former Capital Mephorash", enabled: false },
                        { text: "Trust Busting Dustup", enabled: true },
                    ]
                } else if(itemComboBox.displayText == "Antique Cloth"){
                    missionComboBox.model = [
                        { text: "Former Capital Mephorash", enabled: false },
                        { text: "Trust Busting Dustup", enabled: true },
                        { text: "Erste Kingdom Episode 4", enabled: true },
                    ]
                } else if(itemComboBox.displayText == "Prosperity Flame" || itemComboBox.displayText == "Explosive Material" || itemComboBox.displayText == "Steel Liquid"){
                    missionComboBox.model = [
                        { text: "Agastia", enabled: false },
                        { text: "Imperial Wanderer's Soul", enabled: true },
                    ]
                }

                // Reset the mission ComboBox back to default.
                missionComboBox.currentIndex = 0
                missionComboBox.displayText = qsTr("Please select a mission.")
                
                // Now update the selected item to farm in the backend.
                backend.update_item_name(itemComboBox.model[currentIndex].text)

                // Tell the backend that its not ready to start yet.
                backend.check_bot_ready(false)

                // Finally, reveal the Item Selection success message.
                itemSelectionTextFieldLabel.visible = true
            }

            onPressedChanged: {
                itemComboBox.popup.height = 300
            }
        }

        // The Item Selection success message.
        Label {
            id: itemSelectionTextFieldLabel
            x: 20
            y: 131
            width: 200
            height: 13
            visible: false
            color: "#00ff00"
            text: qsTr("Item selected successfuly")
            anchors.top: itemComboBox.bottom
            anchors.topMargin: 5
        }

        // Select mission(s) specific to each item.
        ComboBox {
            id: missionComboBox

            width: 200
            anchors.left: parent.left
            anchors.top: itemComboBox.bottom
            enabled: false
            anchors.topMargin: 25
            anchors.leftMargin: 20

            displayText: qsTr("Please select a mission.")

            currentIndex: 0
            textRole: "text"

            delegate: ItemDelegate {
                width: missionComboBox.width
                text: modelData.text

                font.weight: missionComboBox.currentIndex === index ? Font.DemiBold : Font.Normal
                highlighted: ListView.isCurrentItem

                enabled: modelData.enabled
            }

            model: []

            onVisibleChanged: {
                if(missionComboBox.displayText === qsTr("Please select a mission.") && missionComboBox.enabled == true){
                    // Inform the user with a message instructing them to select a mission from the ComboBox above.
                    missionSelectionTextFieldLabel.visible = true
                    missionSelectionTextFieldLabel.text = qsTr("Select a mission above")
                    missionSelectionTextFieldLabel.color = "#ff0000"

                    backend.check_bot_ready(false)
                }else if(missionComboBox.displayText !== qsTr("Please select a mission.") && missionComboBox.enabled == true && partySelectionComboBox.enabled == true){
                    // Inform the user with a message stating that selecting a mission was successful and set the bot as ready to start if and only if the user already set the 
                    // other settings before. This can happen if they, after setting their settings, went back and changed their selected item and mission.
                    missionSelectionTextFieldLabel.visible = true
                    missionSelectionTextFieldLabel.text = qsTr("Mission selected successfully")
                    missionSelectionTextFieldLabel.color = "#00ff00"

                    backend.check_bot_ready(true)
                }
            }

            onDisplayTextChanged: {
                // If this Mission Selection ComboBox was reset to default, reset the instructional message back to informing them that they need to select a new mission.
                if(missionComboBox.displayText === qsTr("Please select a mission.") && missionComboBox.enabled == true){
                    missionSelectionTextFieldLabel.visible = true
                    missionSelectionTextFieldLabel.text = qsTr("Select a mission above")
                    missionSelectionTextFieldLabel.color = "#ff0000"

                    backend.check_bot_ready(false)
                }else if(missionComboBox.displayText !== qsTr("Please select a mission.") && missionComboBox.enabled == true && partySelectionComboBox.enabled == true){
                    // This occurs when the user went back after setting their settings and changed their selected item and mission.
                    missionSelectionTextFieldLabel.visible = true
                    missionSelectionTextFieldLabel.text = qsTr("Mission selected successfully")
                    missionSelectionTextFieldLabel.color = "#00ff00"

                    backend.check_bot_ready(true)
                }else if(missionComboBox.displayText !== qsTr("Please select a mission.") && missionComboBox.enabled == true && partySelectionComboBox.enabled != true){
                    // Move the user to the next step by enabling the # of Items selector.
                    missionSelectionTextFieldLabel.visible = true
                    missionSelectionTextFieldLabel.text = qsTr("Mission selected successfully")
                    missionSelectionTextFieldLabel.color = "#00ff00"

                    amountOfItemTextField.enabled = true
                }
            }

            onCurrentIndexChanged: {
                missionComboBox.displayText = qsTr(missionComboBox.model[currentIndex].text)

                // Update the selected mission in the backend.
                backend.update_mission_name(missionComboBox.model[currentIndex].text, missionComboBox.model[0].text)

                // Reveal the Mission Selection success message.
                if(botReadyLabel.text !== qsTr("Bot is ready to start")){
                    missionSelectionTextFieldLabel.visible = true
                }else if(summonSelectionLabel.text === qsTr("# of Items and Summon selected successfully") && summonSelectionLabel.visible == true){
                    // Otherwise, tell the bot that it is ready to go and to just use the settings that the user set before changing the item and mission.
                    backend.check_bot_ready(true)
                }
            }
        }

        // The Mission Selection success message.
        Label {
            id: missionSelectionTextFieldLabel

            x: 20
            y: 196
            width: 200
            height: 13
            visible: false

            color: "#00ff00"
            text: qsTr("Mission selected successfully.")
            anchors.top: missionComboBox.bottom
            anchors.topMargin: 5

            onVisibleChanged: {
                // If this message is revealed, enable the # of Item Selection ComboBox as well.
                if(missionSelectionTextFieldLabel.visible == true && missionComboBox.displayText !== qsTr("Please select a mission.")){
                    amountOfItemTextField.enabled = true
                }
            }
        }

        // Select the amount of items that the user wants the bot to acquire.
        ComboBox {
            id: amountOfItemTextField

            width: 100
            height: 40
            anchors.left: parent.left
            anchors.top: missionComboBox.bottom

            textRole: "text"
            displayText: qsTr("# of Item")
            anchors.leftMargin: 20
            anchors.topMargin: 25

            currentIndex: 0
            enabled: false

            // Have the options go from 1 to 999 inclusive.
            delegate: ItemDelegate {
                width: missionComboBox.width
                text: index + 1

                font.weight: missionComboBox.currentIndex === index ? Font.DemiBold : Font.Normal
                highlighted: ListView.isCurrentItem
            }

            model: 999

            onEnabledChanged: {
                // Reveal the instructional message below this ComboBox and change its color to orange to draw the user's eyes to it
                // while resetting this ComboBox's default text.
                if(amountOfItemTextField.enabled == true){
                    amountOfItemTextField.displayText = qsTr("# of Item")
                    summonSelectionLabel.visible = true
                    summonSelectionLabel.color = "#fc8c03"
                }
            }

            onCurrentIndexChanged: {
                // Update the backend with the # of Items selected.
                amountOfItemTextField.displayText = currentIndex + 1
                backend.update_item_amount(amountOfItemTextField.displayText)

                // Now enable the Summon Selection button and update the instructional message below.
                if(summonSelectionLabel.text === qsTr("Select item amount to farm above")){
                    summonButton.enabled = true
                    summonSelectionLabel.text = qsTr("Now select your Summon")
                }
            }
        }

        // Clicking this button will open up the overlay that will contain selectable Summons.
        Button {
            id: summonButton

            text: qsTr("Select Summon")
            anchors.left: parent.left
            anchors.top: missionComboBox.bottom
            anchors.leftMargin: 180
            anchors.topMargin: 25

            enabled: false

            // On clicked, open up the overlay containing the selectable Summons.
            onClicked: popup.open()

            Popup {
                id: popup

                x: Math.round((parent.width - width - 300) / 2)
                y: Math.round((parent.height - height) / 2)

                width: 400
                height: 400
                modal: true // The modal dims the background behind the Rectangle that will hold the list of Summons.

                // This Rectangle is where the Flickable component is drawn on.
                background: Rectangle {
                    color: "#7e7e7e"
                    border.color: "#49496b"
                    border.width: 1
                    radius: 10
                }

                // This will contain all the Summons supported by the bot.
                CustomFlickableRepeaterForSummons { }
            }
        }

        // The Summon Selection success message. Defaults to instructing the user to select # of Items.
        Label {
            id: summonSelectionLabel

            x: 20
            width: 200
            height: 13
            visible: false

            color: "#fc8c03"
            text: qsTr("Select item amount to farm above")
            anchors.top: summonButton.bottom
            anchors.topMargin: 5
        }

        // Select the Group that the desired Party is under.
        ComboBox {
            id: groupSelectionComboBox

            x: 20
            y: 289
            width: 100
            height: 40
            enabled: false

            currentIndex: 0

            delegate: ItemDelegate {
                width: groupSelectionComboBox.width
                text: modelData.text

                font.weight: groupSelectionComboBox.currentIndex === index ? Font.DemiBold : Font.Normal
                highlighted: ListView.isCurrentItem
            }

            model: [
                { text: "Group 1" },
                { text: "Group 2" },
                { text: "Group 3" },
                { text: "Group 4" },
                { text: "Group 5" },
                { text: "Group 6" },
                { text: "Group 7" },
            ]

            onEnabledChanged: {
                // Reset the index and default Group of the ComboBox and update the backend when this ComboBox gets enabled/reenabled.
                if(groupSelectionComboBox.enabled == true){
                    groupSelectionComboBox.currentIndex = 0
                    groupSelectionComboBox.displayText = qsTr(groupSelectionComboBox.model[currentIndex].text)
                    backend.update_group_number(groupSelectionComboBox.model[currentIndex].text)
                }
            }

            onCurrentIndexChanged: {
                // Update the text displayed and the backend with the selected Group.
                groupSelectionComboBox.displayText = qsTr(groupSelectionComboBox.model[currentIndex].text)
                backend.update_group_number(groupSelectionComboBox.model[currentIndex].text)
            }
        }

        // Select the desired Party.
        ComboBox {
            id: partySelectionComboBox

            x: 180
            y: 289
            width: 100
            height: 40
            enabled: false

            currentIndex: 0

            delegate: ItemDelegate {
                width: partySelectionComboBox.width
                text: modelData.text

                font.weight: partySelectionComboBox.currentIndex === index ? Font.DemiBold : Font.Normal
                highlighted: ListView.isCurrentItem
            }

            model: [
                { text: "Party 1" },
                { text: "Party 2" },
                { text: "Party 3" },
                { text: "Party 4" },
                { text: "Party 5" },
                { text: "Party 6" },
            ]

            onEnabledChanged: {
                if(partySelectionComboBox.enabled == true){
                    // Reset the index and default Party of the ComboBox and update the backend when this ComboBox gets enabled/reenabled.
                    partySelectionComboBox.currentIndex = 0
                    partySelectionComboBox.displayText = qsTr(partySelectionComboBox.model[currentIndex].text)
                    backend.update_party_number(partySelectionComboBox.model[currentIndex].text)

                    // Enable the Start Button.
                    backend.check_bot_ready(true)
                }
            }

            onCurrentIndexChanged: {
                // Update the text displayed and the backend with the selected Party.
                partySelectionComboBox.displayText = qsTr(partySelectionComboBox.model[currentIndex].text)
                backend.update_party_number(partySelectionComboBox.model[currentIndex].text)
            }
        }

        // Enable/Disable the Debug Mode on whether or not the user wants to see more informational messages in the log.
        CustomCheckBox {
            id: debugModeCheckBox

            text: "Debug Mode"
            anchors.left: parent.left
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 20
            anchors.leftMargin: 20

            onClicked: {
                if(debugModeCheckBox.checked){
                    backend.update_debug_mode(true)
                    logTextArea.append("\nDebug Mode turned ON. You will now see debugging messages in the log.")
                }else{
                    backend.update_debug_mode(false)
                    logTextArea.append("\nDebug Mode turned OFF. You will no longer see debugging messages in the log.")
                }
            }
        }

        Label {
            id: botReadyLabel

            x: 180
            y: 393
            width: 100
            height: 40
            color: "#ff0000"

            text: qsTr("Bot is not ready to start")
            font.pointSize: 10

            anchors.right: parent.right
            anchors.bottom: parent.bottom
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
            wrapMode: Text.WordWrap
            anchors.bottomMargin: 20
            anchors.rightMargin: 20
        }
    }

    Connections{
        target: backend

        // Retrieve the name of the opened script file back from backend.
        function onOpenFile(scriptName){
            combatScriptTextField.text = qsTr(scriptName)
            combatScriptTextFieldLabel.visible = true
            logTextArea.append("\nCombat script selected: " + scriptName)

            // Enable the Item Selection ComboBox.
            itemComboBox.enabled = true
        }

        // Output update messages to the log.
        function onUpdateMessage(updateMessage){
            logTextArea.append("\n***************************\n" + updateMessage + "\n***************************")
        }

        // Enable the group and party selectors after the backend receives the user-selected Summon. 
        // Update the informational message to indicate success.
        function onEnableGroupAndPartySelectors(){
            summonSelectionLabel.text = qsTr("# of Items and Summon selected successfully")
            summonSelectionLabel.color = "#00ff00"

            groupSelectionComboBox.enabled = true
            partySelectionComboBox.enabled = true     
        }

        // Update the label at the bottom right on the ready state of the bot.
        function onCheckBotReady(ready_flag){
            if(ready_flag){
                botReadyLabel.text = qsTr("Bot is ready to start")
                botReadyLabel.color = "#00ff00"
            }else{
                botReadyLabel.text = qsTr("Bot is not ready to start")
                botReadyLabel.color = "#ff0000"
            }
        }
    }
}

/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:1.66;height:453;width:300}
}
##^##*/
