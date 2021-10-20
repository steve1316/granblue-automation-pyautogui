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

        // TextField that will inform the user what combat script they have selected.
        TextField {
            id: combatScriptTextField

            height: 30

            placeholderText: qsTr("Combat Script: None selected")
            horizontalAlignment: Text.AlignHCenter
            readOnly: true

            anchors.left: parent.left
            anchors.top: parent.top
            anchors.topMargin: 20
            anchors.leftMargin: 20
        }

        // Status message for the selection of the combat script.
        Label {
            id: combatScriptStatusMessage

            x: 20
            width: 200
            height: 13

            visible: true
            color: "#fc8c03"
            text: qsTr("Please select a combat script")

            anchors.top: combatScriptTextField.bottom
            anchors.topMargin: 5
        }

        // Select what combat script to use for Combat Mode.
        CustomButton{
            id: buttonOpenFile
            y: 20

            text: qsTr("Open")
            anchors.left: combatScriptTextField.right
            anchors.right: parent.right
            font.pointSize: 10
            anchors.rightMargin: 20
            anchors.leftMargin: 10

            height: 30

            FileDialog{
                id: fileOpen

                title: "Please choose a combat script file"

                // Dialog will default to the /scripts/ folder in the root of the bot directory.
                folder: "../../../scripts/"
                selectMultiple: false
                nameFilters: ["Text File (*.txt)"]

                onAccepted: {
                    // Send the file path to the selected combat script to the backend.
                    backend.open_file(fileOpen.fileUrl)

                    // Now update the combat script status message to indicate success.
                    combatScriptStatusMessage.color = "#00ff00"
                    combatScriptStatusMessage.text = qsTr("Combat script loaded successfully")
                }
            }

            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor

                onPressed: {
                    fileOpen.open()
                }
            }
        }

        // Select the farming mode (Quest, Special, Coop, Raid, etc).
        ComboBox {
            id: farmingModeComboBox

            width: 200
            height: 30
            anchors.left: parent.left
            anchors.top: combatScriptTextField.bottom
            anchors.topMargin: 25
            anchors.leftMargin: 20

            delegate: ItemDelegate {
                width: farmingModeComboBox.width
                text: modelData.text
                enabled: modelData.enabled
                highlighted: ListView.isCurrentItem
                font.weight: farmingModeComboBox.currentIndex === index ? Font.DemiBold : Font.Normal
            }

            enabled: false // Gets enabled when you select your combat script.
            currentIndex: 0
            textRole: "text"

            displayText: qsTr("Please select farming mode")

            model: [
                { text: "Farming Modes", enabled: false },
                { text: "Quest", enabled: true },
                { text: "Special", enabled: true },
                { text: "Coop", enabled: true },
                { text: "Raid", enabled: true },
                { text: "Event", enabled: true },
                { text: "Event (Token Drawboxes)", enabled: true },
                { text: "Rise of the Beasts", enabled: true },
                { text: "Guild Wars", enabled: true },
                { text: "Dread Barrage", enabled: true },
                { text: "Proving Grounds", enabled: true },
                { text: "Xeno Clash", enabled: true },
                { text: "Arcarum", enabled: true },
            ]

            onCurrentIndexChanged: {
                // Update the display text to show the Farming Mode that the user selected. Then reveal the relevant status message.
                farmingModeComboBox.displayText = qsTr(farmingModeComboBox.model[currentIndex].text)
                farmingModeStatusMessage.visible = true

                // Display either the Item Selection button or ComboBox depending on the Farming Mode selected.
                if(farmingModeComboBox.displayText === "Event" || farmingModeComboBox.displayText === "Event (Token Drawboxes)" || farmingModeComboBox.displayText === "Dread Barrage" || 
                farmingModeComboBox.displayText === "Rise of the Beasts" || farmingModeComboBox.displayText === "Guild Wars" || farmingModeComboBox.displayText === "Proving Grounds" ||
                farmingModeComboBox.displayText === "Xeno Clash" || farmingModeComboBox.displayText === "Arcarum") {
                    // Set the contents of the Item Selection ComboBox.
                    if(farmingModeComboBox.displayText === "Dread Barrage") {
                        itemSelectionComboBox.model = [
                            { text: "Dread Barrage", enabled: false},
                            { text: "Repeated Runs", enabled: true },
                        ]
                    } else {
                        itemSelectionComboBox.model = [
                            { text: "Event", enabled: false},
                            { text: "Repeated Runs", enabled: true },
                        ]
                    }

                    // Hide and disable the Item Selection button.
                    itemSelectionButton.visible = false
                    itemSelectionButton.enabled = false
                    itemSelectionButton.text = qsTr("Please select item to farm")

                    // Reveal and enable the Item Selection ComboBox and reset it to default.
                    itemSelectionComboBox.visible = true
                    itemSelectionComboBox.enabled = true
                    itemSelectionComboBox.currentIndex = 0
                    itemSelectionComboBox.displayText = qsTr("Please select item to farm")
                } else{
                    // Hide and disable the Item Selection ComboBox.
                    itemSelectionComboBox.visible = false
                    itemSelectionComboBox.enabled = false
                    itemSelectionComboBox.currentIndex = 0
                    itemSelectionComboBox.displayText = qsTr("Please select item to farm")

                    // Reveal and enable the Item Selection Button and reset it to default.
                    itemSelectionButton.visible = true
                    itemSelectionButton.enabled = true
                    itemSelectionButton.text = qsTr("Please select item to farm")
                }

                // Reset the Item Selection status message.
                itemSelectionStatusMessage.visible = true
                itemSelectionStatusMessage.color = "#fc8c03"
                itemSelectionStatusMessage.text = qsTr("Now select the item to farm")

                // Enable the Mission Selection ComboBox. Then reset its displayText and its currentIndex.
                missionSelectionComboBox.enabled = false
                missionSelectionComboBox.displayText = qsTr("Please select a mission")
                missionSelectionComboBox.currentIndex = 0

                // Since the user changed their selected item, reveal and reset the Mission Selection status message.
                missionSelectionStatusMessage.visible = false
                missionSelectionStatusMessage.color = "#fc8c03"
                missionSelectionStatusMessage.text = qsTr("Now select the mission to farm from")

                // Reset the Amount Selection ComboBox and its relevant status message.
                amountSelectionComboBox.enabled = false
                amountSelectionComboBox.displayText = qsTr("# of Item")
                amountSelectionComboBox.currentIndex = -1

                amountSelectionStatusMessage.visible = false
                amountSelectionStatusMessage.color = "#fc8c03"
                amountSelectionStatusMessage.text = qsTr("Now select the amount of items to farm")

                // Reset the Summon Selection button and its relevant status message.
                summonSelectionButton.enabled = false
                summonSelectionButton.text = qsTr("Select Summon")

                summonSelectionStatusMessage.visible = false
                summonSelectionStatusMessage.color = "#fc8c03"
                summonSelectionStatusMessage.text = qsTr("Now select your Summon")

                // Reset the Group and Party Selection ComboBoxes.
                groupSelectionComboBox.enabled = false
                groupSelectionComboBox.displayText = qsTr("Group #")
                groupSelectionComboBox.currentIndex = 0

                partySelectionComboBox.enabled = false
                partySelectionComboBox.displayText = qsTr("Party #")
                partySelectionComboBox.currentIndex = 0

                // Update the relevant status message to indicate success.
                farmingModeStatusMessage.text = qsTr("Farming Mode selected successfully")
                farmingModeStatusMessage.color = "#00ff00"

                // Reset the values in the backend back to default.
                backend.reset_values()

                // Now update the backend with the selected Farming Mode.
                backend.update_farming_mode(farmingModeComboBox.model[currentIndex].text)

                // Finally, set the bot ready status to false.
                backend.check_bot_ready(false)
            }
        }

        // Status message for the selection of the Farming Mode.
        Label {
            id: farmingModeStatusMessage

            x: 20
            width: 200
            height: 13

            visible: false
            color: "#fc8c03"
            text: qsTr("Now select the Farming Mode")

            anchors.top: farmingModeComboBox.bottom
            anchors.topMargin: 5
        }

        // Select the item to farm.
        Button {
            id: itemSelectionButton

            width: 200
            height: 30
            anchors.left: parent.left
            anchors.top: farmingModeComboBox.bottom
            anchors.topMargin: 25
            enabled: false
            anchors.leftMargin: 20

            visible: true

            text: qsTr("Please select the item to farm")

            // This gets fired when the relevant CustomFlickerableRepeater components updates the text on this button.
            onTextChanged: {
                if(farmingModeComboBox.displayText === "Quest") {
                    if(itemSelectionButton.text === "Satin Feather" || itemSelectionButton.text === "Zephyr Feather" || itemSelectionButton.text === "Flying Sprout") {
                        missionSelectionComboBox.model = [
                            { text: "Port Breeze Archipelago", enabled: false },
                            { text: "Scattered Cargo", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Fine Sand Bottle" || itemSelectionButton.text === "Untamed Flame" || itemSelectionButton.text === "Blistering Ore") {
                        missionSelectionComboBox.model = [
                            { text: "Valtz Duchy", enabled: false },
                            { text: "Lucky Charm Hunt", enabled: true },
                            { text: "Special Op's Request", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Fresh Water Jug" || itemSelectionButton.text === "Soothing Splash" || itemSelectionButton.text === "Glowing Coral") {
                        missionSelectionComboBox.model = [
                            { text: "Auguste Isles", enabled: false },
                            { text: "Threat to the Fisheries", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Rough Stone" || itemSelectionButton.text === "Swirling Amber" || itemSelectionButton.text === "Coarse Alluvium") {
                        missionSelectionComboBox.model = [
                            { text: "Lumacie Archipelago", enabled: false },
                            { text: "The Fruit of Lumacie", enabled: true },
                            { text: "Whiff of Danger", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Falcon Feather" || itemSelectionButton.text === "Spring Water Jug" || itemSelectionButton.text === "Vermilion Stone") {
                        missionSelectionComboBox.model = [
                            { text: "Albion Citadel", enabled: false },
                            { text: "I Challenge You!", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Slimy Shroom" || itemSelectionButton.text === "Hollow Soul" || itemSelectionButton.text === "Lacrimosa") {
                        missionSelectionComboBox.model = [
                            { text: "Mist-Shrouded Isle", enabled: false },
                            { text: "For Whom the Bell Tolls", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Wheat Stalk" || itemSelectionButton.text === "Iron Cluster" || itemSelectionButton.text === "Olea Plant") {
                        missionSelectionComboBox.model = [
                            { text: "Golonzo Island", enabled: false },
                            { text: "Golonzo's Battles of Old", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Indigo Fruit" || itemSelectionButton.text === "Foreboding Clover" || itemSelectionButton.text === "Blood Amber") {
                        missionSelectionComboBox.model = [
                            { text: "Amalthea Island", enabled: false },
                            { text: "The Dungeon Diet", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Sand Brick" || itemSelectionButton.text === "Native Reed") {
                        missionSelectionComboBox.model = [
                            { text: "Former Capital Mephorash", enabled: false },
                            { text: "Trust Busting Dustup", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Antique Cloth") {
                        missionSelectionComboBox.model = [
                            { text: "Former Capital Mephorash", enabled: false },
                            { text: "Trust Busting Dustup", enabled: true },
                            { text: "Erste Kingdom Episode 4", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Prosperity Flame" || itemSelectionButton.text === "Explosive Material" || itemSelectionButton.text === "Steel Liquid") {
                        missionSelectionComboBox.model = [
                            { text: "Agastia", enabled: false },
                            { text: "Imperial Wanderer's Soul", enabled: true },
                        ]
                    }
                } else if(farmingModeComboBox.displayText === "Special") {
                    if(itemSelectionButton.text === "Fire Orb" || itemSelectionButton.text === "Inferno Orb") {
                        missionSelectionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "H Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "VH Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Hellfire Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    }else if(itemSelectionButton.text === "Water Orb" || itemSelectionButton.text === "Frost Orb") {
                        missionSelectionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "H Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "VH Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Deluge Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Earth Orb" || itemSelectionButton.text === "Rumbling Orb") {
                        missionSelectionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "H Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "VH Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Wasteland Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Wind Orb" || itemSelectionButton.text === "Cyclone Orb") {
                        missionSelectionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "H Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "VH Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Typhoon Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Light Orb" || itemSelectionButton.text === "Shining Orb") {
                        missionSelectionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "H Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "VH Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Aurora Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Dark Orb" || itemSelectionButton.text === "Abysm Orb") {
                        missionSelectionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "H Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "VH Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Oblivion Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    }

                    // Tomes, Scrolls, and Whorls.
                    else if(itemSelectionButton.text === "Red Tome") {
                        missionSelectionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Hellfire Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    }
                    else if(itemSelectionButton.text === "Hellfire Scroll" || itemSelectionButton.text === "Infernal Whorl") {
                        missionSelectionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "H Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "VH Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Hellfire Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Blue Tome") {
                        missionSelectionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Deluge Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Flood Scroll" || itemSelectionButton.text === "Tidal Whorl") {
                        missionSelectionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "H Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "VH Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Deluge Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Brown Tome") {
                        missionSelectionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Wasteland Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Thunder Scroll" || itemSelectionButton.text === "Seismic Whorl") {
                        missionSelectionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "H Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "VH Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Wasteland Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Green Tome") {
                        missionSelectionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Typhoon Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Gale Scroll" || itemSelectionButton.text === "Tempest Whorl") {
                        missionSelectionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "H Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "VH Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Typhoon Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "White Tome") {
                        missionSelectionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Aurora Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Skylight Scroll" || itemSelectionButton.text === "Radiant Whorl") {
                        missionSelectionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "H Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "VH Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Aurora Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Black Tome") {
                        missionSelectionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Oblivion Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Chasm Scroll" || itemSelectionButton.text === "Umbral Whorl") {
                        missionSelectionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "H Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "VH Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Oblivion Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    }

                    // Chips and Prisms.
                    else if(itemSelectionButton.text === "Prism Chip") {
                        missionSelectionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Violet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "H Violet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Hellfire Trial", map: "Elemental Treasure Quests", enabled: true },
                            { text: "The Deluge Trial", map: "Elemental Treasure Quests", enabled: true },
                            { text: "The Wasteland Trial", map: "Elemental Treasure Quests", enabled: true },
                            { text: "The Typhoon Trial", map: "Elemental Treasure Quests", enabled: true },
                            { text: "The Aurora Trial", map: "Elemental Treasure Quests", enabled: true },
                            { text: "The Oblivion Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Flawed Prism") {
                        missionSelectionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Violet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "H Violet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "VH Violet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Hellfire Trial", map: "Elemental Treasure Quests", enabled: true },
                            { text: "The Deluge Trial", map: "Elemental Treasure Quests", enabled: true },
                            { text: "The Wasteland Trial", map: "Elemental Treasure Quests", enabled: true },
                            { text: "The Typhoon Trial", map: "Elemental Treasure Quests", enabled: true },
                            { text: "The Aurora Trial", map: "Elemental Treasure Quests", enabled: true },
                            { text: "The Oblivion Trial", map: "Elemental Treasure Quests", enabled: true },
                            { text: "Angel Halo", enabled: false },
                            { text: "H Angel Halo", map: "Angel Halo", enabled: true },
                            { text: "VH Angel Halo", map: "Angel Halo", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Flawless Prism" || itemSelectionButton.text === "Rainbow Prism") {
                        missionSelectionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "VH Violet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Hellfire Trial", map: "Elemental Treasure Quests", enabled: true },
                            { text: "The Deluge Trial", map: "Elemental Treasure Quests", enabled: true },
                            { text: "The Wasteland Trial", map: "Elemental Treasure Quests", enabled: true },
                            { text: "The Typhoon Trial", map: "Elemental Treasure Quests", enabled: true },
                            { text: "The Aurora Trial", map: "Elemental Treasure Quests", enabled: true },
                            { text: "The Oblivion Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    }

                    // Farm EXP for characters.
                    else if(itemSelectionButton.text === "EXP") {
                        missionSelectionComboBox.model = [
                            { text: "Shiny Slime Search!", enabled: false },
                            { text: "N Shiny Slime Search!", map: "Shiny Slime Search!", enabled: true },
                            { text: "H Shiny Slime Search!", map: "Shiny Slime Search!", enabled: true },
                            { text: "VH Shiny Slime Search!", map: "Shiny Slime Search!", enabled: true },
                            { text: "Angel Halo", enabled: false },
                            { text: "N Angel Halo", map: "Angel Halo", enabled: true },
                            { text: "H Angel Halo", map: "Angel Halo", enabled: true },
                            { text: "VH Angel Halo", map: "Angel Halo", enabled: true },
                            { text: "Campaign-Exclusive Quest", enabled: false },
                            { text: "Campaign-Exclusive Quest", map: "Campaign-Exclusive Quest", enabled: true },
                        ]
                    }

                    // Showdown materials.
                    else if(itemSelectionButton.text === "Jasper Scale" || itemSelectionButton.text === "Scorching Peak" || itemSelectionButton.text === "Infernal Garnet"
                            || itemSelectionButton.text === "Ifrit Anima" || itemSelectionButton.text === "Ifrit Omega Anima") {
                        missionSelectionComboBox.model = [
                            { text: "Showdowns", enabled: false },
                            { text: "H Ifrit Showdown", map: "Showdowns", enabled: true },
                            { text: "VH Ifrit Showdown", map: "Showdowns", enabled: true },
                            { text: "EX Ifrit Showdown", map: "Showdowns", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Mourning Stone" || itemSelectionButton.text === "Crystal Spirit" || itemSelectionButton.text === "Frozen Hell Prism"
                            || itemSelectionButton.text === "Cocytus Anima" || itemSelectionButton.text === "Cocytus Omega Anima") {
                        missionSelectionComboBox.model = [
                            { text: "Showdowns", enabled: false },
                            { text: "H Cocytus Showdown", map: "Showdowns", enabled: true },
                            { text: "VH Cocytus Showdown", map: "Showdowns", enabled: true },
                            { text: "EX Cocytus Showdown", map: "Showdowns", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Scrutiny Stone" || itemSelectionButton.text === "Luminous Judgment" || itemSelectionButton.text === "Evil Judge Crystal"
                            || itemSelectionButton.text === "Vohu Manah Anima" || itemSelectionButton.text === "Vohu Manah Omega Anima") {
                        missionSelectionComboBox.model = [
                            { text: "Showdowns", enabled: false },
                            { text: "H Vohu Manah Showdown", map: "Showdowns", enabled: true },
                            { text: "VH Vohu Manah Showdown", map: "Showdowns", enabled: true },
                            { text: "EX Vohu Manah Showdown", map: "Showdowns", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Sagittarius Arrowhead" || itemSelectionButton.text === "Sagittarius Rune" || itemSelectionButton.text === "Horseman's Plate"
                            || itemSelectionButton.text === "Sagittarius Anima" || itemSelectionButton.text === "Sagittarius Omega Anima") {
                        missionSelectionComboBox.model = [
                            { text: "Showdowns", enabled: false },
                            { text: "H Sagittarius Showdown", map: "Showdowns", enabled: true },
                            { text: "VH Sagittarius Showdown", map: "Showdowns", enabled: true },
                            { text: "EX Sagittarius Showdown", map: "Showdowns", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Solar Ring" || itemSelectionButton.text === "Sunlight Quartz" || itemSelectionButton.text === "Halo Light Quartz"
                            || itemSelectionButton.text === "Corow Anima" || itemSelectionButton.text === "Corow Omega Anima") {
                        missionSelectionComboBox.model = [
                            { text: "Showdowns", enabled: false },
                            { text: "H Corow Showdown", map: "Showdowns", enabled: true },
                            { text: "VH Corow Showdown", map: "Showdowns", enabled: true },
                            { text: "EX Corow Showdown", map: "Showdowns", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Twilight Cloth Strip" || itemSelectionButton.text === "Shadow Silver" || itemSelectionButton.text === "Phantom Demon Jewel"
                            || itemSelectionButton.text === "Diablo Anima" || itemSelectionButton.text === "Diablo Omega Anima") {
                        missionSelectionComboBox.model = [
                            { text: "Showdowns", enabled: false },
                            { text: "H Diablo Showdown", map: "Showdowns", enabled: true },
                            { text: "VH Diablo Showdown", map: "Showdowns", enabled: true },
                            { text: "EX Diablo Showdown", map: "Showdowns", enabled: true },
                        ]
                    }

                    // Dragon Scales.
                    else if(itemSelectionButton.text === "Red Dragon Scale") {
                        missionSelectionComboBox.model = [
                            { text: "Six Dragon Trial", enabled: false },
                            { text: "N Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "H Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "VH Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Hellfire Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Blue Dragon Scale") {
                        missionSelectionComboBox.model = [
                            { text: "Six Dragon Trial", enabled: false },
                            { text: "N Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "H Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "VH Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Deluge Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Brown Dragon Scale") {
                        missionSelectionComboBox.model = [
                            { text: "Six Dragon Trial", enabled: false },
                            { text: "N Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "H Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "VH Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Wasteland Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Green Dragon Scale") {
                        missionSelectionComboBox.model = [
                            { text: "Six Dragon Trial", enabled: false },
                            { text: "N Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "H Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "VH Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Typhoon Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "White Dragon Scale") {
                        missionSelectionComboBox.model = [
                            { text: "Six Dragon Trial", enabled: false },
                            { text: "N Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "H Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "VH Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Aurora Trial", map: "Elemental Treasure Quests", enabled: true },
                            { text: "Angel Halo", enabled: false },
                            { text: "H Angel Halo", map: "Angel Halo", enabled: true },
                            { text: "VH Angel Halo", map: "Angel Halo", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Black Dragon Scale") {
                        missionSelectionComboBox.model = [
                            { text: "Six Dragon Trial", enabled: false },
                            { text: "N Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "H Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "VH Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Oblivion Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    }

                    // Fragments
                    else if(itemSelectionButton.text === "Hellfire Fragment") {
                        missionSelectionComboBox.model = [
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Hellfire Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Deluge Fragment") {
                        missionSelectionComboBox.model = [
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Deluge Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Wasteland Fragment") {
                        missionSelectionComboBox.model = [
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Wasteland Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Typhoon Fragment") {
                        missionSelectionComboBox.model = [
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Typhoon Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    }

                    // Angel Halo
                    else if(itemSelectionButton.text === "Angel Halo Weapons") {
                        missionSelectionComboBox.model = [
                            { text: "Angel Halo", enabled: false },
                            { text: "N Angel Halo", map: "Angel Halo", enabled: true },
                            { text: "H Angel Halo", map: "Angel Halo", enabled: true },
                            { text: "VH Angel Halo", map: "Angel Halo", enabled: true },
                        ]
                    }
                } else if(farmingModeComboBox.displayText === "Coop") {
                    // EXP
                    if(itemSelectionButton.text === "EXP") {
                        missionSelectionComboBox.model = [
                            { text: "H3", enabled: false },
                            { text: "In a Dusk Dream", map: "", enabled: true },
                        ]
                    }

                    // Creeds
                    else if(itemSelectionButton.text === "Warrior Creed" || itemSelectionButton.text === "Mage Creed") {
                        missionSelectionComboBox.model = [
                            { text: "EX1", enabled: false },
                            { text: "Corridor of Puzzles", map: "", enabled: true },
                            { text: "Lost in the Dark", map: "", enabled: true },
                        ]
                    }

                    // Materials
                    else if(itemSelectionButton.text === "Infernal Garnet") {
                        missionSelectionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Revelation", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Frozen Hell Prism") {
                        missionSelectionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Tundra", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Evil Judge Crystal") {
                        missionSelectionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Judgement", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Horseman's Plate") {
                        missionSelectionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Plains", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Halo Light Quartz") {
                        missionSelectionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Eminence", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Phantom Demon Jewel") {
                        missionSelectionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Twilight", map: "", enabled: true },
                        ]
                    }

                    // Distinctions
                    else if(itemSelectionButton.text === "Gladiator Distinction") {
                        missionSelectionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Revelation", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst Severe Cliffs", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Guardian Distinction") {
                        missionSelectionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Tundra", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Flames", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Pilgrim Distinction") {
                        missionSelectionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Judgement", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Waves", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Mage Distinction") {
                        missionSelectionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Judgement", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Waves", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Bandit Distinction") {
                        missionSelectionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Eminence", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Flames", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Fencer Distinction") {
                        missionSelectionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Revelation", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst Severe Cliffs", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Combatant Distinction") {
                        missionSelectionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Tundra", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst Severe Cliffs", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Sharpshooter Distinction") {
                        missionSelectionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Plains", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Petals", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Troubadour Distinction") {
                        missionSelectionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Eminence", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Flames", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Cavalryman Distinction") {
                        missionSelectionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Plains", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Flames", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Alchemist Distinction") {
                        missionSelectionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Judgement", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Waves", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Samurai Distinction") {
                        missionSelectionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Twilight", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Petals", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Ninja Distinction") {
                        missionSelectionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Twilight", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Petals", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Sword Master Distinction") {
                        missionSelectionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Tundra", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst Severe Cliffs", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Gunslinger Distinction") {
                        missionSelectionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Plains", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Petals", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Mystic Distinction") {
                        missionSelectionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Eminence", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Waves", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Assassin Distinction") {
                        missionSelectionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Twilight", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Petals", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Dual Wielder Distinction") {
                        missionSelectionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Revelation", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Shredder Distinction") {
                        missionSelectionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Eminence", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Forester's Distinction") {
                        missionSelectionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Revelation", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Dragoon's Distinction") {
                        missionSelectionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Rule of the Tundra", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Flames", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Monk's Distinction") {
                        missionSelectionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Judgement", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Waves", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Longstrider's Distinction") {
                        missionSelectionComboBox.model = [
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Petals", map: "", enabled: true },
                        ]
                    }

                    // Replicas
                    else if(itemSelectionButton.text === "Avenger Replica") {
                        missionSelectionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Revelation", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Skofnung Replica") {
                        missionSelectionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Tundra", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Oliver Replica") {
                        missionSelectionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Plains", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Waves", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Aschallon Replica") {
                        missionSelectionComboBox.model = [
                            { text: "EX4", enabled: false },
                            { text: "Amidst Severe Cliffs", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Nirvana Replica") {
                        missionSelectionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Eminence", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Keraunos Replica") {
                        missionSelectionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Judgement", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Hellion Gauntlet Replica") {
                        missionSelectionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Revelation", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst Severe Cliffs", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Ipetam Replica") {
                        missionSelectionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Twilight", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Flames", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Rosenbogen Replica") {
                        missionSelectionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Plains", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Langeleik Replica") {
                        missionSelectionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Tundra", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Waves", map: "", enabled: true },
                            { text: "Amidst the Petals", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Romulus Spear Replica") {
                        missionSelectionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Eminence", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Waves", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Proximo Replica") {
                        missionSelectionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Twilight", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Waves", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Murakumo Replica") {
                        missionSelectionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Eminence", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Flames", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Nebuchad Replica") {
                        missionSelectionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Twilight", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Flames", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Misericorde Replica") {
                        missionSelectionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Plains", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Petals", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Faust Replica") {
                        missionSelectionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Judgement", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Petals", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Muramasa Replica") {
                        missionSelectionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Twilight", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst Severe Cliffs", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Kapilavastu Replica") {
                        missionSelectionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Tundra", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Waves", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Practice Drum") {
                        missionSelectionComboBox.model = [
                            { text: "EX4", enabled: false },
                            { text: "Amidst Severe Cliffs", map: "", enabled: true },
                        ]
                    }
                } else if(farmingModeComboBox.displayText === "Raid") {
                    // Omega Weapons
                    if(itemSelectionButton.text === "Tiamat Omega" || itemSelectionButton.text === "Tiamat Anima" || itemSelectionButton.text === "Tiamat Omega Anima" || itemSelectionButton.text === "Tiamat Amood Omega" || itemSelectionButton.text === "Tiamat Bolt Omega"
                    || itemSelectionButton.text === "Tiamat Gauntlet Omega" || itemSelectionButton.text === "Tiamat Glaive Omega") {
                        missionSelectionComboBox.model = [
                            { text: "Tiamat Omega", enabled: false },
                            { text: "Lvl 50 Tiamat Omega", map: "", enabled: true },
                            { text: "Lvl 100 Tiamat Omega Ayr", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Colossus Omega" || itemSelectionButton.text === "Colossus Anima" || itemSelectionButton.text === "Colossus Omega Anima" || itemSelectionButton.text === "Colossus Blade Omega" || itemSelectionButton.text === "Colossus Cane Omega"
                    || itemSelectionButton.text === "Colossus Carbine Omega" || itemSelectionButton.text === "Colossus Fist Omega") {
                        missionSelectionComboBox.model = [
                            { text: "Colossus Omega", enabled: false },
                            { text: "Lvl 70 Colossus Omega", map: "", enabled: true },
                            { text: "Lvl 100 Colossus Omega", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Leviathan Omega" || itemSelectionButton.text === "Leviathan Anima" || itemSelectionButton.text === "Leviathan Omega Anima" || itemSelectionButton.text === "Leviathan Bow Omega" || itemSelectionButton.text === "Leviathan Gaze Omega"
                    || itemSelectionButton.text === "Leviathan Scepter Omega" || itemSelectionButton.text === "Leviathan Spear Omega") {
                        missionSelectionComboBox.model = [
                            { text: "Leviathan Omega", enabled: false },
                            { text: "Lvl 60 Leviathan Omega", map: "", enabled: true },
                            { text: "Lvl 100 Leviathan Omega", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Yggdrasil Omega" || itemSelectionButton.text === "Yggdrasil Anima" || itemSelectionButton.text === "Yggdrasil Omega Anima" || itemSelectionButton.text === "Yggdrasil Bow Omega" || itemSelectionButton.text === "Yggdrasil Crystal Blade Omega"
                    || itemSelectionButton.text === "Yggdrasil Dagger Omega" || itemSelectionButton.text === "Yggdrasil Dewbranch Omega") {
                        missionSelectionComboBox.model = [
                            { text: "Yggdrasil Omega", enabled: false },
                            { text: "Lvl 60 Yggdrasil Omega", map: "", enabled: true },
                            { text: "Lvl 100 Yggdrasil Omega", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Luminiera Omega" || itemSelectionButton.text === "Luminiera Anima" || itemSelectionButton.text === "Luminiera Omega Anima" || itemSelectionButton.text === "Luminiera Bhuj Omega" || itemSelectionButton.text === "Luminiera Bolt Omega"
                    || itemSelectionButton.text === "Luminiera Harp Omega" || itemSelectionButton.text === "Luminiera Sword Omega") {
                        missionSelectionComboBox.model = [
                            { text: "Luminiera Omega", enabled: false },
                            { text: "Lvl 75 Luminiera Omega", map: "", enabled: true },
                            { text: "Lvl 100 Luminiera Omega", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Celeste Omega" || itemSelectionButton.text === "Celeste Anima" || itemSelectionButton.text === "Celeste Omega Anima" || itemSelectionButton.text === "Celeste Harp Omega" || itemSelectionButton.text === "Celeste Claw Omega"
                    || itemSelectionButton.text === "Celeste Horn Omega" || itemSelectionButton.text === "Celeste Zaghnal Omega") {
                        missionSelectionComboBox.model = [
                            { text: "Celeste", enabled: false },
                            { text: "Lvl 75 Celeste Omega", map: "", enabled: true },
                            { text: "Lvl 100 Celeste Omega", map: "", enabled: true },
                        ]
                    }

                    // Regalia Weapons
                    else if(itemSelectionButton.text === "Shiva Anima" || itemSelectionButton.text === "Shiva Omega Anima" || itemSelectionButton.text === "Hand of Brahman" || itemSelectionButton.text === "Scimitar of Brahman"
                    || itemSelectionButton.text === "Trident of Brahman" || itemSelectionButton.text === "Nilakantha") {
                        missionSelectionComboBox.model = [
                            { text: "Shiva", enabled: false },
                            { text: "Lvl 120 Shiva", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Europa Anima" || itemSelectionButton.text === "Europa Omega Anima" || itemSelectionButton.text === "Tyros Bow" || itemSelectionButton.text === "Tyros Scepter"
                    || itemSelectionButton.text === "Tyros Zither" || itemSelectionButton.text === "Spirit of Mana") {
                        missionSelectionComboBox.model = [
                            { text: "Europa", enabled: false },
                            { text: "Lvl 120 Europa", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Alexiel Anima" || itemSelectionButton.text === "Alexiel Omega Anima" || itemSelectionButton.text === "Nibelung Horn" || itemSelectionButton.text === "Nibelung Klinge"
                    || itemSelectionButton.text === "Nibelung Messer" || itemSelectionButton.text === "Godsworn Edge") {
                        missionSelectionComboBox.model = [
                            { text: "Godsworn Alexiel", enabled: false },
                            { text: "Lvl 120 Godsworn Alexiel", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Grimnir Anima" || itemSelectionButton.text === "Grimnir Omega Anima" || itemSelectionButton.text === "Last Storm Blade" || itemSelectionButton.text === "Last Storm Harp"
                    || itemSelectionButton.text === "Last Storm Lance" || itemSelectionButton.text === "Coruscant Crozier") {
                        missionSelectionComboBox.model = [
                            { text: "Grimnir", enabled: false },
                            { text: "Lvl 120 Grimnir", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Metatron Anima" || itemSelectionButton.text === "Metatron Omega Anima" || itemSelectionButton.text === "Mittron's Treasured Blade" || itemSelectionButton.text === "Mittron's Gauntlet"
                    || itemSelectionButton.text === "Mittron's Bow" || itemSelectionButton.text === "Pillar of Flame") {
                        missionSelectionComboBox.model = [
                            { text: "Metatron", enabled: false },
                            { text: "Lvl 120 Metatron", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Avatar Anima" || itemSelectionButton.text === "Avatar Omega Anima" || itemSelectionButton.text === "Abyss Striker" || itemSelectionButton.text === "Abyss Spine"
                    || itemSelectionButton.text === "Abyss Gaze" || itemSelectionButton.text === "Zechariah") {
                        missionSelectionComboBox.model = [
                            { text: "Avatar", enabled: false },
                            { text: "Lvl 120 Avatar", map: "", enabled: true },
                        ]
                    }

                    // Olden Primal and Primal Weapons
                    else if(itemSelectionButton.text === "Twin Elements Anima" || itemSelectionButton.text === "Twin Elements Omega Anima" || itemSelectionButton.text === "Ancient Ecke Sachs" || itemSelectionButton.text === "Ecke Sachs") {
                        missionSelectionComboBox.model = [
                            { text: "Twin Elements", enabled: false },
                            { text: "Lvl 100 Twin Elements", map: "", enabled: true },
                            { text: "Lvl 120 Twin Elements", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Macula Marius Anima" || itemSelectionButton.text === "Macula Marius Omega Anima" || itemSelectionButton.text === "Ancient Auberon" || itemSelectionButton.text === "Auberon") {
                        missionSelectionComboBox.model = [
                            { text: "Macula Marius", enabled: false },
                            { text: "Lvl 100 Macula Marius", map: "", enabled: true },
                            { text: "Lvl 120 Macula Marius", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Medusa Anima" || itemSelectionButton.text === "Medusa Omega Anima" || itemSelectionButton.text === "Ancient Perseus" || itemSelectionButton.text === "Perseus") {
                        missionSelectionComboBox.model = [
                            { text: "Medusa", enabled: false },
                            { text: "Lvl 100 Medusa", map: "", enabled: true },
                            { text: "Lvl 120 Medusa", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Nezha Anima" || itemSelectionButton.text === "Nezha Omega Anima" || itemSelectionButton.text === "Ancient Nalakuvara" || itemSelectionButton.text === "Nalakuvara") {
                        missionSelectionComboBox.model = [
                            { text: "Nezha", enabled: false },
                            { text: "Lvl 100 Nezha", map: "", enabled: true },
                            { text: "Lvl 120 Nezha", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Apollo Anima" || itemSelectionButton.text === "Apollo Omega Anima" || itemSelectionButton.text === "Ancient Bow of Artemis" || itemSelectionButton.text === "Bow of Artemis") {
                        missionSelectionComboBox.model = [
                            { text: "Apollo", enabled: false },
                            { text: "Lvl 100 Apollo", map: "", enabled: true },
                            { text: "Lvl 120 Apollo", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Dark Angel Olivia Anima" || itemSelectionButton.text === "Dark Angel Olivia Omega Anima" || itemSelectionButton.text === "Ancient Cortana" || itemSelectionButton.text === "Cortana") {
                        missionSelectionComboBox.model = [
                            { text: "Dark Angel Olivia", enabled: false },
                            { text: "Lvl 100 Dark Angel Olivia", map: "", enabled: true },
                            { text: "Lvl 120 Dark Angel Olivia", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Athena Anima" || itemSelectionButton.text === "Athena Omega Anima") {
                        missionSelectionComboBox.model = [
                            { text: "Athena", enabled: false },
                            { text: "Lvl 100 Athena", map: "", enabled: true },
                            { text: "Ultimate Bahamut", enabled: false },
                            { text: "Lvl 150 Ultimate Bahamut", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Erichthonius" || itemSelectionButton.text === "Sword of Pallas") {
                        missionSelectionComboBox.model = [
                            { text: "Athena", enabled: false },
                            { text: "Lvl 100 Athena", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Grani Anima" || itemSelectionButton.text === "Grani Omega Anima") {
                        missionSelectionComboBox.model = [
                            { text: "Grani", enabled: false },
                            { text: "Lvl 100 Grani", map: "", enabled: true },
                            { text: "Ultimate Bahamut", enabled: false },
                            { text: "Lvl 150 Ultimate Bahamut", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Bow of Sigurd" || itemSelectionButton.text === "Wilhelm") {
                        missionSelectionComboBox.model = [
                            { text: "Grani", enabled: false },
                            { text: "Lvl 100 Grani", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Baal Anima" || itemSelectionButton.text === "Baal Omega Anima") {
                        missionSelectionComboBox.model = [
                            { text: "Baal", enabled: false },
                            { text: "Lvl 100 Baal", map: "", enabled: true },
                            { text: "Ultimate Bahamut", enabled: false },
                            { text: "Lvl 150 Ultimate Bahamut", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Solomon's Axe" || itemSelectionButton.text === "Spymur's Vision") {
                        missionSelectionComboBox.model = [
                            { text: "Baal", enabled: false },
                            { text: "Lvl 100 Baal", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Garuda Anima" || itemSelectionButton.text === "Garuda Omega Anima") {
                        missionSelectionComboBox.model = [
                            { text: "Garuda", enabled: false },
                            { text: "Lvl 100 Garuda", map: "", enabled: true },
                            { text: "Ultimate Bahamut", enabled: false },
                            { text: "Lvl 150 Ultimate Bahamut", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Plume of Suparna" || itemSelectionButton.text === "Indra's Edge") {
                        missionSelectionComboBox.model = [
                            { text: "Garuda", enabled: false },
                            { text: "Lvl 100 Garuda", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Odin Anima" || itemSelectionButton.text === "Odin Omega Anima") {
                        missionSelectionComboBox.model = [
                            { text: "Odin", enabled: false },
                            { text: "Lvl 100 Odin", map: "", enabled: true },
                            { text: "Ultimate Bahamut", enabled: false },
                            { text: "Lvl 150 Ultimate Bahamut", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Gungnir" || itemSelectionButton.text === "Sleipnir Shoe") {
                        missionSelectionComboBox.model = [
                            { text: "Odin", enabled: false },
                            { text: "Lvl 100 Odin", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Lich Anima" || itemSelectionButton.text === "Lich Omega Anima") {
                        missionSelectionComboBox.model = [
                            { text: "Lich", enabled: false },
                            { text: "Lvl 100 Lich", map: "", enabled: true },
                            { text: "Ultimate Bahamut", enabled: false },
                            { text: "Lvl 150 Ultimate Bahamut", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Obscuritas" || itemSelectionButton.text === "Phantasmas") {
                        missionSelectionComboBox.model = [
                            { text: "Lich", enabled: false },
                            { text: "Lvl 100 Lich", map: "", enabled: true },
                        ]
                    }

                    // Epic Weapons
                    else if(itemSelectionButton.text === "Prometheus Anima" || itemSelectionButton.text === "Fire of Prometheus" || itemSelectionButton.text === "Chains of Caucasus") {
                        missionSelectionComboBox.model = [
                            { text: "Prometheus", enabled: false },
                            { text: "Lvl 120 Prometheus", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Ca Ong Anima" || itemSelectionButton.text === "Keeper of Hallowed Ground" || itemSelectionButton.text === "Savior of Hallowed Ground") {
                        missionSelectionComboBox.model = [
                            { text: "Ca Ong", enabled: false },
                            { text: "Lvl 120 Ca Ong", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Gilgamesh Anima" || itemSelectionButton.text === "All-Might Spear" || itemSelectionButton.text === "All-Might Battle-Axe") {
                        missionSelectionComboBox.model = [
                            { text: "Gilgamesh", enabled: false },
                            { text: "Lvl 120 Gilgamesh", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Morrigna Anima" || itemSelectionButton.text === "Le Fay" || itemSelectionButton.text === "Unius") {
                        missionSelectionComboBox.model = [
                            { text: "Morrigna", enabled: false },
                            { text: "Lvl 120 Morrigna", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Hector Anima" || itemSelectionButton.text === "Bow of Iliad" || itemSelectionButton.text === "Adamantine Gauntlet") {
                        missionSelectionComboBox.model = [
                            { text: "Hector", enabled: false },
                            { text: "Lvl 120 Hector", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Anubis Anima" || itemSelectionButton.text === "Hermanubis" || itemSelectionButton.text === "Scales of Dominion") {
                        missionSelectionComboBox.model = [
                            { text: "Anubis", enabled: false },
                            { text: "Lvl 120 Anubis", map: "", enabled: true },
                        ]
                    }

                    // Six Dragon Weapons
                    else if(itemSelectionButton.text === "Wilnas's Finger") {
                        missionSelectionComboBox.model = [
                            { text: "Wilnas", enabled: false },
                            { text: "Lvl 200 Wilnas", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Wamdus's Cnidocyte") {
                        missionSelectionComboBox.model = [
                            { text: "Wamdus", enabled: false },
                            { text: "Lvl 200 Wamdus", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Galleon's Jaw") {
                        missionSelectionComboBox.model = [
                            { text: "Galleon", enabled: false },
                            { text: "Lvl 200 Galleon", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Ewiyar's Beak") {
                        missionSelectionComboBox.model = [
                            { text: "Ewiyar", enabled: false },
                            { text: "Lvl 200 Ewiyar", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Lu Woh's Horn") {
                        missionSelectionComboBox.model = [
                            { text: "Lu Woh", enabled: false },
                            { text: "Lvl 200 Lu Woh", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Fediel's Spine") {
                        missionSelectionComboBox.model = [
                            { text: "Fediel", enabled: false },
                            { text: "Lvl 200 Fediel", map: "", enabled: true },
                        ]
                    }

                    // Malice Weapons
                    else if(itemSelectionButton.text === "Tiamat Malice Anima" || itemSelectionButton.text === "Hatsoiiłhał" || itemSelectionButton.text === "Majestas") {
                        missionSelectionComboBox.model = [
                            { text: "Tiamat Malice", enabled: false },
                            { text: "Lvl 150 Tiamat Malice", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Leviathan Malice Anima" || itemSelectionButton.text === "Kaladanda" || itemSelectionButton.text === "Kris of Hypnos") {
                        missionSelectionComboBox.model = [
                            { text: "Leviathan Malice", enabled: false },
                            { text: "Lvl 150 Leviathan Malice", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Phronesis Anima" || itemSelectionButton.text === "Dark Thrasher" || itemSelectionButton.text === "Master Bamboo Sword") {
                        missionSelectionComboBox.model = [
                            { text: "Phronesis", enabled: false },
                            { text: "Lvl 150 Phronesis", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Luminiera Malice Anima" || itemSelectionButton.text === "Colomba" || itemSelectionButton.text === "Seyfert") {
                        missionSelectionComboBox.model = [
                            { text: "Luminiera Malice", enabled: false },
                            { text: "Lvl 150 Luminiera Malice", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Hive God Anima" || itemSelectionButton.text === "Agonize" || itemSelectionButton.text === "Faceless") {
                        missionSelectionComboBox.model = [
                            { text: "Anima-Animus Core", enabled: false },
                            { text: "Lvl 150 Anima-Animus Core", map: "", enabled: true },
                        ]
                    }

                    // Xeno Items
                    else if(itemSelectionButton.text === "True Xeno Ifrit Anima" || itemSelectionButton.text === "Infernal Vajra") {
                        missionSelectionComboBox.model = [
                            { text: "Xeno Ifrit", enabled: false },
                            { text: "Lvl 100 Xeno Ifrit", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "True Xeno Cocytus Anima" || itemSelectionButton.text === "Frozen Hellplume") {
                        missionSelectionComboBox.model = [
                            { text: "Xeno Cocytus", enabled: false },
                            { text: "Lvl 100 Xeno Cocytus", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "True Xeno Vohu Manah Anima" || itemSelectionButton.text === "Sacrosanct Sutra") {
                        missionSelectionComboBox.model = [
                            { text: "Xeno Vohu Manah", enabled: false },
                            { text: "Lvl 100 Xeno Vohu Manah", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "True Xeno Sagittarius Anima" || itemSelectionButton.text === "Zodiac Arc") {
                        missionSelectionComboBox.model = [
                            { text: "Xeno Sagittarius", enabled: false },
                            { text: "Lvl 100 Xeno Sagittarius", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "True Xeno Corow Anima" || itemSelectionButton.text === "Flame Fanner") {
                        missionSelectionComboBox.model = [
                            { text: "Xeno Corow", enabled: false },
                            { text: "Lvl 100 Xeno Corow", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "True Xeno Diablo Anima" || itemSelectionButton.text === "Wraithbind Fetter") {
                        missionSelectionComboBox.model = [
                            { text: "Xeno Diablo", enabled: false },
                            { text: "Lvl 100 Xeno Diablo", enabled: true },
                        ]
                    }

                    // Misc Items
                    else if(itemSelectionButton.text === "Azure Feather" || itemSelectionButton.text === "Heavenly Horn") {
                        missionSelectionComboBox.model = [
                            { text: "Grand Order", enabled: false },
                            { text: "Lvl 100 Grand Order", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Verdant Azurite") {
                        missionSelectionComboBox.model = [
                            { text: "Grand Order", enabled: false },
                            { text: "Lvl 200 Grand Order", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Horn of Bahamut" || itemSelectionButton.text === "Champion Merit") {
                        missionSelectionComboBox.model = [
                            { text: "Proto Bahamut", enabled: false },
                            { text: "Lvl 100 Proto Bahamut", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Primeval Horn") {
                        missionSelectionComboBox.model = [
                            { text: "Proto Bahamut", enabled: false },
                            { text: "Lvl 150 Proto Bahamut", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Meteorite Fragment" || itemSelectionButton.text === "Meteorite") {
                        missionSelectionComboBox.model = [
                            { text: "Ultimate Bahamut", enabled: false },
                            { text: "Lvl 150 Ultimate Bahamut", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Silver Centrum") {
                        missionSelectionComboBox.model = [
                            { text: "Ultimate Bahamut", enabled: false },
                            { text: "Lvl 150 Ultimate Bahamut", map: "", enabled: true },
                            { text: "Lvl 200 Ultimate Bahamut", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Ultima Unit") {
                        missionSelectionComboBox.model = [
                            { text: "Ultimate Bahamut", enabled: false },
                            { text: "Lvl 200 Ultimate Bahamut", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Rose Petal") {
                        missionSelectionComboBox.model = [
                            { text: "Rose Queen", enabled: false },
                            { text: "Lvl 110 Rose Queen", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Hollow Key") {
                        missionSelectionComboBox.model = [
                            { text: "Akasha", enabled: false },
                            { text: "Lvl 200 Akasha", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Dark Residue" || itemSelectionButton.text === "Shadow Substance") {
                        missionSelectionComboBox.model = [
                            { text: "Lucilius", enabled: false },
                            { text: "Lvl 150 Lucilius", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Golden Scale" || itemSelectionButton.text === "Lineage Fragment") {
                        missionSelectionComboBox.model = [
                            { text: "Lindwurm", enabled: false },
                            { text: "Lvl 200 Lindwurm", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Michael Anima") {
                        missionSelectionComboBox.model = [
                            { text: "Michael", enabled: false },
                            { text: "Lvl 100 Michael", map: "", enabled: true },
                            { text: "Ultimate Bahamut", enabled: false },
                            { text: "Lvl 150 Ultimate Bahamut", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Gabriel Anima") {
                        missionSelectionComboBox.model = [
                            { text: "Gabriel", enabled: false },
                            { text: "Lvl 100 Gabriel", map: "", enabled: true },
                            { text: "Ultimate Bahamut", enabled: false },
                            { text: "Lvl 150 Ultimate Bahamut", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Uriel Anima") {
                        missionSelectionComboBox.model = [
                            { text: "Uriel", enabled: false },
                            { text: "Lvl 100 Uriel", map: "", enabled: true },
                            { text: "Ultimate Bahamut", enabled: false },
                            { text: "Lvl 150 Ultimate Bahamut", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Raphael Anima") {
                        missionSelectionComboBox.model = [
                            { text: "Raphael", enabled: false },
                            { text: "Lvl 100 Raphael", map: "", enabled: true },
                            { text: "Ultimate Bahamut", enabled: false },
                            { text: "Lvl 150 Ultimate Bahamut", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Fire Halo" || itemSelectionButton.text === "Water Halo" || itemSelectionButton.text === "Earth Halo" || itemSelectionButton.text === "Wind Halo") {
                        missionSelectionComboBox.model = [
                            { text: "Four Primarchs", enabled: false },
                            { text: "The Four Primarchs", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Huanglong Anima" || itemSelectionButton.text === "Qilin Anima" || itemSelectionButton.text === "Golden Talisman" || itemSelectionButton.text === "Obsidian Talisman") {
                        missionSelectionComboBox.model = [
                            { text: "Huanglong and Qilin", enabled: false },
                            { text: "Huanglong & Qilin (Impossible)", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Shenxian Badge") {
                        missionSelectionComboBox.model = [
                            { text: "Shenxian", enabled: false },
                            { text: "Lvl 100 Shenxian", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Zhuque Badge") {
                        missionSelectionComboBox.model = [
                            { text: "Agni", enabled: false },
                            { text: "Lvl 90 Agni", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Xuanwu Badge") {
                        missionSelectionComboBox.model = [
                            { text: "Neptune", enabled: false },
                            { text: "Lvl 90 Neptune", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Baihu Badge") {
                        missionSelectionComboBox.model = [
                            { text: "Titan", enabled: false },
                            { text: "Lvl 90 Titan", map: "", enabled: true },
                        ]
                    } else if(itemSelectionButton.text === "Qinglong Badge") {
                        missionSelectionComboBox.model = [
                            { text: "Zephyrus", enabled: false },
                            { text: "Lvl 90 Zephyrus", map: "", enabled: true },
                        ]
                    }
                }

                if(itemSelectionButton.text !== qsTr("Please select the item to farm") && itemSelectionButton.text !== "") {
                    // Update the Item Selection status message to indicate success.
                    itemSelectionStatusMessage.visible = true
                    itemSelectionStatusMessage.color = "#00ff00"
                    itemSelectionStatusMessage.text = qsTr("Item selected successfully")

                    // Enable the Mission Selection ComboBox. Then reset its displayText and its currentIndex.
                    missionSelectionComboBox.enabled = true
                    missionSelectionComboBox.displayText = qsTr("Please select a mission")
                    missionSelectionComboBox.currentIndex = 0

                    // Since the user changed their selected item, reveal and reset the Mission Selection status message.
                    missionSelectionStatusMessage.visible = true
                    missionSelectionStatusMessage.color = "#fc8c03"
                    missionSelectionStatusMessage.text = qsTr("Now select the mission to farm from")

                    // Reset the Amount Selection ComboBox and its relevant status message.
                    amountSelectionComboBox.enabled = false
                    amountSelectionComboBox.displayText = qsTr("# of Item")
                    amountSelectionComboBox.currentIndex = -1

                    amountSelectionStatusMessage.visible = false
                    amountSelectionStatusMessage.color = "#fc8c03"
                    amountSelectionStatusMessage.text = qsTr("Now select the amount of items to farm")

                    // Reset the Summon Selection button and its relevant status message.
                    summonSelectionButton.enabled = false
                    summonSelectionButton.text = qsTr("Select Summon")

                    summonSelectionStatusMessage.visible = false
                    summonSelectionStatusMessage.color = "#fc8c03"
                    summonSelectionStatusMessage.text = qsTr("Now select your Summon")

                    // Reset the Group and Party Selection ComboBoxes.
                    groupSelectionComboBox.enabled = false
                    groupSelectionComboBox.displayText = qsTr("Group #")
                    groupSelectionComboBox.currentIndex = 0

                    partySelectionComboBox.enabled = false
                    partySelectionComboBox.displayText = qsTr("Party #")
                    partySelectionComboBox.currentIndex = 0

                    // Finally, reset the mission and location names in the backend to default and set the bot ready status to false.
                    backend.update_mission_name("", "")
                    backend.check_bot_ready(false)
                }
            }

            // On clicked, open up the overlay containing the selectable items.
            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor

                onClicked: {
                    if(farmingModeComboBox.displayText == "Quest") {
                        questItemsPopup.open()
                    } else if(farmingModeComboBox.displayText == "Special") {
                        specialItemsPopup.open()
                    } else if(farmingModeComboBox.displayText == "Coop") {
                        coopItemsPopup.open()
                    } else if(farmingModeComboBox.displayText == "Raid") {
                        raidItemsPopup.open()
                    }
                }
            }

            Popup {
                id: questItemsPopup

                x: Math.round((parent.width - width - 300) / 2)
                y: Math.round((parent.height - height) / 2)

                width: 400
                height: 400
                modal: true

                // This Rectangle is where the Flickable component is drawn on.
                background: Rectangle {
                    color: "#7e7e7e"
                    border.color: "#49496b"
                    border.width: 1
                    radius: 10
                }

                // This will contain all the Quest Items supported by the bot.
                RepeaterForQuestItems { }
            }

            Popup {
                id: specialItemsPopup

                x: Math.round((parent.width - width - 300) / 2)
                y: Math.round((parent.height - height) / 2)

                width: 400
                height: 400
                modal: true

                // This Rectangle is where the Flickable component is drawn on.
                background: Rectangle {
                    color: "#7e7e7e"
                    border.color: "#49496b"
                    border.width: 1
                    radius: 10
                }

                // This will contain all the Special Items supported by the bot.
                RepeaterForSpecialItems { }
            }

            Popup {
                id: coopItemsPopup

                x: Math.round((parent.width - width - 300) / 2)
                y: Math.round((parent.height - height) / 2)

                width: 400
                height: 400
                modal: true

                // This Rectangle is where the Flickable component is drawn on.
                background: Rectangle {
                    color: "#7e7e7e"
                    border.color: "#49496b"
                    border.width: 1
                    radius: 10
                }

                // This will contain all the Coop Items supported by the bot.
                RepeaterForCoopItems { }
            }

            Popup {
                id: raidItemsPopup

                x: Math.round((parent.width - width - 300) / 2)
                y: Math.round((parent.height - height) / 2)

                width: 400
                height: 400
                modal: true

                // This Rectangle is where the Flickable component is drawn on.
                background: Rectangle {
                    color: "#7e7e7e"
                    border.color: "#49496b"
                    border.width: 1
                    radius: 10
                }

                // This will contain all the Raid Items supported by the bot.
                RepeaterForRaidItems { }
            }
        }

        // This ComboBox is for Events and Dread Barrage whose available missions to farm in are pretty similar to each other.
        ComboBox {
            id: itemSelectionComboBox

            width: 200
            height: 30
            anchors.left: parent.left
            anchors.top: farmingModeComboBox.bottom
            anchors.topMargin: 25
            enabled: false
            anchors.leftMargin: 20

            visible: false

            displayText: qsTr("Please select the item to farm")
            currentIndex: 0
            textRole: "text"

            model: [
                { text: "Event", enabled: false},
                { text: "Repeated Runs", enabled: true },
            ]

            delegate: ItemDelegate {
                width: itemSelectionComboBox.width
                text: modelData.text

                property var map: modelData.map // Holds the map in which the mission takes place in. For some missions, it is intentionally blank.

                font.weight: itemSelectionComboBox.currentIndex === index ? Font.DemiBold : Font.Normal
                highlighted: ListView.isCurrentItem

                enabled: modelData.enabled
            }

            onCurrentIndexChanged: {
                // Update the displayText on this ComboBox with the selected item.
                itemSelectionComboBox.displayText = itemSelectionComboBox.model[currentIndex].text

                if(itemSelectionComboBox.displayText !== qsTr("Please select the item to farm")) {
                    // If the selected Farming Mode is either Event or Dread Barrage, update the contents of the Mission Selection ComboBox with the following.
                    if(farmingModeComboBox.displayText === "Event (Token Drawboxes)" && itemSelectionComboBox.displayText === "Repeated Runs") {
                        missionSelectionComboBox.model = [
                            { text: "Event Raid", enabled: false },
                            { text: "VH Event Raid", map: "", enabled: true },
                            { text: "EX Event Raid", map: "", enabled: true },
                            { text: "IM Event Raid", map: "", enabled: true },
                            { text: "Event Quest", enabled: false },
                            { text: "EX Event Quest", map: "", enabled: true },
                        ]
                    } else if(farmingModeComboBox.displayText === "Event" && itemSelectionComboBox.displayText === "Repeated Runs") {
                        missionSelectionComboBox.model = [
                            { text: "Event Raid", enabled: false },
                            { text: "VH Event Raid", map: "", enabled: true },
                            { text: "EX Event Raid", map: "", enabled: true },
                            { text: "EX+ Event Raid", map: "", enabled: true },
                            { text: "Event Quest", enabled: false },
                            { text: "EX Event Quest", map: "", enabled: true },
                            { text: "EX+ Event Quest", map: "", enabled: true },
                        ]
                    } else if(farmingModeComboBox.displayText === "Dread Barrage" && itemSelectionComboBox.displayText === "Repeated Runs") {
                        missionSelectionComboBox.model = [
                            { text: "Dread Barrage Raids", enabled: false },
                            { text: "1 Star", map: "", enabled: true },
                            { text: "2 Star", map: "", enabled: true },
                            { text: "3 Star", map: "", enabled: true },
                            { text: "4 Star", map: "", enabled: true },
                            { text: "5 Star", map: "", enabled: true },
                        ]
                    } else if(farmingModeComboBox.displayText === "Rise of the Beasts" && itemSelectionComboBox.displayText === "Repeated Runs") {
                        missionSelectionComboBox.model = [
                            { text: "Event Raid", enabled: false },
                            { text: "EX Zhuque", map: "", enabled: true },
                            { text: "EX Xuanwu", map: "", enabled: true },
                            { text: "EX Baihu", map: "", enabled: true },
                            { text: "EX Qinglong", map: "", enabled: true },
                            { text: "Lvl 100 Shenxian", map: "", enabled: true },
                            { text: "Event Quest", enabled: false },
                            { text: "VH Zhuque", map: "", enabled: true },
                            { text: "VH Xuanwu", map: "", enabled: true },
                            { text: "VH Baihu", map: "", enabled: true },
                            { text: "VH Qinglong", map: "", enabled: true },
                        ]
                    } else if(farmingModeComboBox.displayText === "Guild Wars" && itemSelectionComboBox.displayText === "Repeated Runs") {
                        missionSelectionComboBox.model = [
                            { text: "Meat", enabled: false },
                            { text: "Very Hard", enabled: true },
                            { text: "Extreme", enabled: true },
                            { text: "Extreme+", enabled: true },
                            { text: "Nightmare", enabled: false },
                            { text: "NM90", enabled: true },
                            { text: "NM95", enabled: true },
                            { text: "NM100", enabled: true },
                            { text: "NM150", enabled: true },
                        ]
                    } else if(farmingModeComboBox.displayText === "Proving Grounds" && itemSelectionComboBox.displayText === "Repeated Runs") {
                        missionSelectionComboBox.model = [
                            { text: "Proving Ground Missions", enabled: false },
                            { text: "Extreme", enabled: true },
                            { text: "Extreme+", enabled: true },
                        ]
                    } else if(farmingModeComboBox.displayText === "Xeno Clash" && itemSelectionComboBox.displayText === "Repeated Runs") {
                        missionSelectionComboBox.model = [
                            { text: "Xeno Clash", enabled: false },
                            { text: "Xeno Clash Extreme", enabled: true },
                            { text: "Xeno Clash Raid", enabled: true },
                        ]
                    } else if(farmingModeComboBox.displayText === "Arcarum" && itemSelectionComboBox.displayText === "Repeated Runs") {
                        missionSelectionComboBox.model = [
                            { text: "Arcarum", enabled: false },
                            { text: "Point Aquila", enabled: true },
                            { text: "Point Bellator", enabled: true },
                            { text: "Point Celsus", enabled: true },
                        ]
                    }

                    // Update the status message for this ComboBox to indicate success.
                    itemSelectionStatusMessage.visible = true
                    itemSelectionStatusMessage.text = qsTr("Item selected successfully")
                    itemSelectionStatusMessage.color = "#00ff00"

                    // Reset the Mission Selection ComboBox and its relevant status message.
                    missionSelectionComboBox.enabled = true
                    missionSelectionComboBox.displayText = qsTr("Please select a mission")
                    missionSelectionComboBox.currentIndex = 0

                    missionSelectionStatusMessage.visible = true
                    missionSelectionStatusMessage.color = "#fc8c03"
                    missionSelectionStatusMessage.text = qsTr("Now select the mission to farm from")
                    
                    // Reset the Amount Selection ComboBox and its relevant status message.
                    amountSelectionComboBox.enabled = false
                    amountSelectionComboBox.displayText = qsTr("# of Item")
                    amountSelectionComboBox.currentIndex = -1
                    
                    amountSelectionStatusMessage.visible = false
                    amountSelectionStatusMessage.color = "#fc8c03"
                    amountSelectionStatusMessage.text = qsTr("Now select the amount of items to farm")

                    // Reset the Summon Selection button and its relevant status message.
                    summonSelectionButton.enabled = false
                    summonSelectionButton.text = qsTr("Select Summon")

                    summonSelectionStatusMessage.visible = false
                    summonSelectionStatusMessage.color = "#fc8c03"
                    summonSelectionStatusMessage.text = qsTr("Now select your Summon")

                    // Reset the Group and Party Selection ComboBoxes.
                    groupSelectionComboBox.enabled = false
                    groupSelectionComboBox.displayText = qsTr("Group #")
                    groupSelectionComboBox.currentIndex = 0

                    partySelectionComboBox.enabled = false
                    partySelectionComboBox.displayText = qsTr("Party #")
                    partySelectionComboBox.currentIndex = 0

                    // Now reset the following to default in the backend.
                    backend.update_mission_name("", "")
                    backend.update_item_amount("0")
                    backend.update_summon_list("", "")
                    
                    // Finally, update the item name in the backend and set the bot ready status to false.
                    backend.update_item_name(itemSelectionComboBox.model[currentIndex].text)
                    backend.check_bot_ready(false)
                }
            }
        }

        // Status message for the selection of the item.
        Label {
            id: itemSelectionStatusMessage

            x: 20
            y: 131
            width: 200
            height: 13

            visible: false
            color: "#fc8c03"
            text: qsTr("Now select the item to farm")

            anchors.top: itemSelectionButton.bottom
            anchors.topMargin: 5
        }

        // Select a mission that is specific to each item.
        ComboBox {
            id: missionSelectionComboBox

            width: 200
            height: 30
            anchors.left: parent.left
            anchors.top: itemSelectionButton.bottom
            anchors.topMargin: 25
            enabled: false
            anchors.leftMargin: 20

            displayText: qsTr("Please select a mission")

            currentIndex: 0
            textRole: "text"

            model: []

            delegate: ItemDelegate {
                width: missionSelectionComboBox.width
                text: modelData.text

                property var map: modelData.map // Holds the map in which the mission will take place in. For some missions, it is intentionally blank.

                font.weight: missionSelectionComboBox.currentIndex === index ? Font.DemiBold : Font.Normal
                highlighted: ListView.isCurrentItem

                enabled: modelData.enabled
            }

            onCurrentIndexChanged: {
                // Update the displayText for this ComboBox with the selected mission.
                missionSelectionComboBox.displayText = qsTr(missionSelectionComboBox.model[currentIndex].text)

                // Update the mission and location names in the backend.
                if(farmingModeComboBox.displayText === "Quest" && itemSelectionButton.text !== qsTr("Please select item to farm")) {
                    backend.update_mission_name(missionSelectionComboBox.model[currentIndex].text, missionSelectionComboBox.model[0].text)
                } else if(farmingModeComboBox.displayText !== "Quest" && (itemSelectionButton.text !== qsTr("Please select item to farm") || itemSelectionComboBox.displayText !== qsTr("Please select item to farm"))) {
                    backend.update_mission_name(missionSelectionComboBox.model[currentIndex].text, missionSelectionComboBox.model[currentIndex].map)
                }

                // Update the Mission Selection status message to indicate success.
                missionSelectionStatusMessage.color = "#00ff00"
                missionSelectionStatusMessage.text = qsTr("Mission selected successfully")
                
                // If the selected mission was changed but it still belongs to the same item, don't reset the following and keep the previously selected settings.
                if(botReadyLabel.text !== qsTr("Bot is ready to start")) {
                    // Reset the Amount Selection ComboBox and its relevant status message.
                    amountSelectionComboBox.enabled = true
                    amountSelectionComboBox.displayText = qsTr("# of Item")
                    amountSelectionComboBox.currentIndex = -1
                    
                    amountSelectionStatusMessage.visible = true
                    amountSelectionStatusMessage.color = "#fc8c03"
                    amountSelectionStatusMessage.text = qsTr("Now select the amount of items to farm")

                    // Reset the Summon Selection button and its relevant status message.
                    summonSelectionButton.enabled = false
                    summonSelectionButton.text = qsTr("Select Summon")

                    summonSelectionStatusMessage.visible = false
                    summonSelectionStatusMessage.color = "#fc8c03"
                    summonSelectionStatusMessage.text = qsTr("Now select your Summon")

                    // Reset the Group and Party Selection ComboBoxes.
                    groupSelectionComboBox.enabled = false
                    groupSelectionComboBox.displayText = qsTr("Group #")
                    groupSelectionComboBox.currentIndex = 0

                    partySelectionComboBox.enabled = false
                    partySelectionComboBox.displayText = qsTr("Party #")
                    partySelectionComboBox.currentIndex = 0

                    // Reset the following to default in the backend.
                    backend.update_item_amount("0")
                    backend.update_summon_list("", "")

                    // Finally, set the bot ready status to false.
                    backend.check_bot_ready(false)
                }
            }
        }

        // The Mission Selection status message.
        Label {
            id: missionSelectionStatusMessage

            x: 20
            y: 196
            width: 200
            height: 13
            visible: false

            color: "#fc8c03"
            text: qsTr("Now select the mission to farm from")
            anchors.top: missionSelectionComboBox.bottom
            anchors.topMargin: 5
        }

        // Select the amount of items that the user wants the bot to acquire.
        ComboBox {
            id: amountSelectionComboBox

            width: 100
            height: 30
            anchors.left: parent.left
            anchors.top: missionSelectionComboBox.bottom
            anchors.topMargin: 25
            anchors.leftMargin: 20

            textRole: "text"
            displayText: qsTr("# of Item")

            currentIndex: -1
            enabled: false

            // Have the options go from 1 to 999 inclusive.
            delegate: ItemDelegate {
                width: missionSelectionComboBox.width
                text: index + 1

                font.weight: missionSelectionComboBox.currentIndex === index ? Font.DemiBold : Font.Normal
                highlighted: ListView.isCurrentItem
            }

            model: 999

            onCurrentIndexChanged: {
                // Update the Amount Selection status message to indicate success.
                amountSelectionStatusMessage.color = "#00ff00"
                amountSelectionStatusMessage.text = qsTr("Amount of Items saved successfully")

                if(farmingModeComboBox.displayText === qsTr("Coop") || farmingModeComboBox.displayText === qsTr("Arcarum")) {
                    // Reset the Summon Selection button and its relevant status message.
                    summonSelectionButton.enabled = false
                    summonSelectionButton.text = qsTr("Select Summon")

                    summonSelectionStatusMessage.visible = false
                    summonSelectionStatusMessage.color = "#fc8c03"
                    summonSelectionStatusMessage.text = qsTr("Now select your Summon")

                    // Send blank Summon and element names to bypass enabling the Select Summon button as hosting Coop solo does not have any selectable Summons.
                    backend.update_summon_list("", "")

                    // Now enable the Group and Party Selectors.
                    groupSelectionComboBox.enabled = true
                    partySelectionComboBox.enabled = true

                    // Finally, set the bot ready status to true.
                    backend.check_bot_ready(true)
                } else if(summonSelectionButton.text === qsTr("Select Summon")) {
                    // Reset the Summon Selection button and its relevant status message.
                    summonSelectionButton.enabled = true
                    summonSelectionButton.text = qsTr("Select Summon")

                    summonSelectionStatusMessage.visible = true
                    summonSelectionStatusMessage.color = "#fc8c03"
                    summonSelectionStatusMessage.text = qsTr("Now select your Summon")

                    // Finally, set the bot ready status to false.
                    backend.check_bot_ready(false)
                }

                // Update the backend with the # of Items selected.
                if(amountSelectionComboBox.currentIndex !== -1) {
                    amountSelectionComboBox.displayText = currentIndex + 1
                    backend.update_item_amount(amountSelectionComboBox.displayText)
                }
            }
        }

        // The Amount Selection status message.
        Label {
            id: amountSelectionStatusMessage

            x: 20
            width: 200
            height: 13
            visible: false

            color: "#fc8c03"
            text: qsTr("Now select the amount of items to farm")

            anchors.top: amountSelectionComboBox.bottom
            anchors.topMargin: 5
        }

        // Selects the Summon for Combat Mode.
        Button {
            id: summonSelectionButton
            width: 200
            height: 30

            text: qsTr("Select Summon")
            anchors.left: parent.left
            anchors.top: amountSelectionComboBox.bottom
            anchors.topMargin: 25
            anchors.leftMargin: 20

            enabled: false

            onTextChanged: {
                if(farmingModeComboBox.enabled === true && farmingModeComboBox.displayText !== qsTr("Coop") && summonSelectionButton.text !== qsTr("Select Summon")) {
                    // Update the Summon Selection status message to indicate success.
                    summonSelectionStatusMessage.visible = true
                    summonSelectionStatusMessage.color = "#00ff00"
                    summonSelectionStatusMessage.text = qsTr("Summon selected successfully")
                } else if(farmingModeComboBox.enabled === true && farmingModeComboBox.displayText !== qsTr("Coop") && summonSelectionButton.text === qsTr("Select Summon")) {
                    summonSelectionStatusMessage.visible = true
                    summonSelectionStatusMessage.color = "#fc8c03"
                    summonSelectionStatusMessage.text = qsTr("Now select your Summon")
                }

                if(summonSelectionButton.text !== qsTr("Select Summon")) {
                    if(farmingModeComboBox.displayText !== "Proving Grounds") {
                        // Now enable the Group and Party ComboBoxes.
                        groupSelectionComboBox.enabled = true
                        partySelectionComboBox.enabled = true
                    }

                    // Finally, enable the Start Button on the Home page.
                    backend.check_bot_ready(true)
                } else {
                    // If the user got back to 0 Summons selected, disable the Group and Party ComboBoxes and disable the Start Button.
                    groupSelectionComboBox.enabled = false
                    partySelectionComboBox.enabled = false
                    backend.check_bot_ready(false)
                    backend.clear_summon_list()
                }
            }

            // On clicked, open up the overlay containing the selectable Summons.
            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor

                onClicked: summonPopup.open()
            }

            Popup {
                id: summonPopup

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

                // This will contain all the Summons supported by the bot. It will update the Summon and element names in the backend and then update the text on this button as well.
                RepeaterForSummons { }
            }
        }

        // The Summon Selection status message.
        Label {
            id: summonSelectionStatusMessage

            x: 20
            width: 200
            height: 13
            visible: false

            color: "#fc8c03"
            text: qsTr("Now select your Summon")

            anchors.top: summonSelectionButton.bottom
            anchors.topMargin: 5
        }

        // Select the Group that the desired Party is under.
        ComboBox {
            id: groupSelectionComboBox

            y: 289
            width: 100
            height: 30
            anchors.left: parent.left
            anchors.bottom: debugModeCheckBox.top
            anchors.bottomMargin: 20
            anchors.leftMargin: 20
            enabled: false

            currentIndex: 0
            displayText: qsTr("Group #")

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
                if(groupSelectionComboBox.enabled === true) {
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
            height: 30
            anchors.right: parent.right
            anchors.bottom: botReadyLabel.top
            anchors.rightMargin: 20
            anchors.bottomMargin: 20
            enabled: false

            currentIndex: 0
            displayText: qsTr("Party #")

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
                if(partySelectionComboBox.enabled === true) {
                    // Reset the index and default Party of the ComboBox and update the backend when this ComboBox gets enabled/reenabled.
                    partySelectionComboBox.currentIndex = 0
                    partySelectionComboBox.displayText = qsTr(partySelectionComboBox.model[currentIndex].text)
                    backend.update_party_number(partySelectionComboBox.model[currentIndex].text)
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
            y: 365
            width: 100
            height: 30

            text: "Debug Mode"
            anchors.left: parent.left
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 20
            anchors.leftMargin: 20

            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor

                onClicked: {
                    debugModeCheckBox.checked = !debugModeCheckBox.checked

                    if(debugModeCheckBox.checked) {
                        backend.update_debug_mode(true)
                        logTextArea.append("\nDebug Mode turned ON. You will now see debugging messages in the log.")
                    }else{
                        backend.update_debug_mode(false)
                        logTextArea.append("\nDebug Mode turned OFF. You will no longer see debugging messages in the log.")
                    }
                }
            }
        }

        Label {
            id: botReadyLabel

            x: 180
            y: 393
            width: 100
            height: 30
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

            MouseArea {
                id: botReadyLabelMouseArea

                width: 20
                height: 20
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter

                onClicked: {
                    testModeCheckBox.visible = !testModeCheckBox.visible
                }

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor

                    onClicked: {
                        testModeCheckBox.visible = !testModeCheckBox.visible
                    }
                }
            }
        }

        CustomCheckBox {
            id: testModeCheckBox

            x: 180
            y: 240
            width: 100
            height: 30
            visible: false

            text: "Test Mode"
            anchors.right: parent.right
            anchors.rightMargin: 20

            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor

                onClicked: {
                    testModeCheckBox.checked = !testModeCheckBox.checked
                    backend.check_bot_ready(testModeCheckBox.checked)
                    backend.update_test_mode(testModeCheckBox.checked)
                }
            }
        }
    }

    Connections{
        target: backend

        // Retrieve the name of the opened script file back from backend.
        function onOpenFile(scriptName) {
            combatScriptTextField.text = qsTr(scriptName)
            combatScriptStatusMessage.visible = true
            logTextArea.append("\nCombat script selected: " + scriptName)

            // Enable the Farming Mode ComboBox and make its instruction message visible.
            farmingModeComboBox.enabled = true
            farmingModeStatusMessage.visible = true
        }

        // Output update messages to the log.
        function onUpdateMessage(updateMessage) {
            logTextArea.text = `Welcome to Granblue Automation! 
                                \n*************************** 
                                \nInstructions\n----------------
                                \nNote: The START button is disabled until the following steps are followed through.
                                \n1. Please have your game window fully visible.
                                \n2. Go into the Settings Page and follow the on-screen messages to guide you through setting up the bot.
                                \n3. You can head back to the Home Page and click START.
                                \n\n***************************`
            logTextArea.append("\n***************************\n" + updateMessage + "\n***************************")
        }

        // Update the label at the bottom right on the ready state of the bot.
        function onCheckBotReady(ready_flag) {
            if(ready_flag) {
                botReadyLabel.text = qsTr("Bot is ready to start")
                botReadyLabel.color = "#00ff00"
            }else{
                botReadyLabel.text = qsTr("Bot is not ready to start")
                botReadyLabel.color = "#ff0000"
            }
        }

        // Gets the current length of the Summon list and updates the Summon Selection button with the number of Summons currently selected.
        function onGetSummonListLength(listLength) {
            if(listLength !== 0) {
                summonSelectionButton.text = listLength + qsTr(" Summon(s) selected")
            } else {
                summonSelectionButton.text = qsTr("Select Summon")
            }
        }
    }
}

/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:1.66;height:453;width:300}
}
##^##*/
