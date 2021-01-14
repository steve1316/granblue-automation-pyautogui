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
            height: 30
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
                    backend.open_file(fileOpen.fileUrl)
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
                { text: "Special", enabled: true }
            ]

            onCurrentIndexChanged: {
                farmingModeComboBox.displayText = qsTr(farmingModeComboBox.model[currentIndex].text)
                farmingModeTextFieldLabel.visible = true

                backend.update_farming_mode(farmingModeComboBox.model[currentIndex].text)

                // Once done updating the backend with the selected farming mode, update the item selection ComboBox below with the appropriate items.
                if(farmingModeComboBox.model[currentIndex].text === "Quest"){
                    itemComboBox.model = [
                        // Port Breeze Archipelago
                        { text: "Port Breeze Archipelago", enabled: false },
                        { text: "Satin Feather", enabled: true },
                        { text: "Zephyr Feather", enabled: true },
                        { text: "Flying Sprout", enabled: true },

                        // Valtz Duchy
                        { text: "Valtz Duchy", enabled: false },
                        { text: "Fine Sand Bottle", enabled: true },
                        { text: "Untamed Flame", enabled: true },
                        { text: "Blistering Ore", enabled: true },

                        // Auguste Isles
                        { text: "Auguste Isles", enabled: false },
                        { text: "Fresh Water Jug", enabled: true },
                        { text: "Soothing Splash", enabled: true },
                        { text: "Glowing Coral", enabled: true },

                        // Lumacie Archipelago
                        { text: "Lumacie Archipelago", enabled: false },
                        { text: "Rough Stone", enabled: true },
                        { text: "Coarse Alluvium", enabled: true },
                        { text: "Swirling Amber", enabled: true },

                        // Albion Citadel
                        { text: "Albion Citadel", enabled: false },
                        { text: "Falcon Feather", enabled: true },
                        { text: "Spring Water Jug", enabled: true },
                        { text: "Vermilion Stone", enabled: true },

                        // Mist-Shrouded Isle
                        { text: "Mist-Shrouded Isle", enabled: false },
                        { text: "Slimy Shroom", enabled: true },
                        { text: "Hollow Soul", enabled: true },
                        { text: "Lacrimosa", enabled: true },

                        // Golonzo Island
                        { text: "Golonzo Island", enabled: false },
                        { text: "Wheat Stalk", enabled: true },
                        { text: "Iron Cluster", enabled: true },
                        { text: "Olea Plant", enabled: true },

                        // Amalthea Island
                        { text: "Amalthea Island", enabled: false },
                        { text: "Indigo Fruit", enabled: true },
                        { text: "Foreboding Clover", enabled: true },
                        { text: "Blood Amber", enabled: true },

                        // Former Capital Mephorash
                        { text: "Former Capital Mephorash", enabled: false },
                        { text: "Sand Brick", enabled: true },
                        { text: "Native Reed", enabled: true },
                        { text: "Antique Cloth", enabled: true },

                        // Agastia
                        { text: "Agastia", enabled: false },
                        { text: "Prosperity Flame", enabled: true },
                        { text: "Explosive Material", enabled: true },
                        { text: "Steel Liquid", enabled: true },
                    ]
                } else if(farmingModeComboBox.model[currentIndex].text === "Special"){
                    itemComboBox.model = [
                        // Scarlet Trial
                        { text: "--------------------", enabled: false },
                        { text: "Fire Orb", map: "Scarlet Trial", enabled: true },
                        { text: "Water Orb", map: "Scarlet Trial", enabled: true },
                        { text: "Earth Orb", map: "Scarlet Trial", enabled: true },
                        { text: "Wind Orb", map: "Scarlet Trial", enabled: true },
                        { text: "Light Orb", map: "Scarlet Trial", enabled: true },
                        { text: "Dark Orb", map: "Scarlet Trial", enabled: true },
                        { text: "Inferno Orb", map: "Scarlet Trial", enabled: true },
                        { text: "Frost Orb", map: "Scarlet Trial", enabled: true },
                        { text: "Rumbling Orb", map: "Scarlet Trial", enabled: true },
                        { text: "Cyclone Orb", map: "Scarlet Trial", enabled: true },
                        { text: "Shining Orb", map: "Scarlet Trial", enabled: true },
                        { text: "Abysm Orb", map: "Scarlet Trial", enabled: true },

                        // Cerulean Trial
                        { text: "--------------------", enabled: false },
                        { text: "Red Tome", enabled: true },
                        { text: "Blue Tome", enabled: true },
                        { text: "Brown Tome", enabled: true },
                        { text: "Green Tome", enabled: true },
                        { text: "White Tome", enabled: true },
                        { text: "Black Tome", enabled: true },
                        { text: "Hellfire Scroll", enabled: true },
                        { text: "Flood Scroll", enabled: true },
                        { text: "Thunder Scroll", enabled: true },
                        { text: "Gale Scroll", enabled: true },
                        { text: "Skylight Scroll", enabled: true },
                        { text: "Chasm Scroll", enabled: true },
                        { text: "Infernal Whorl", enabled: true },
                        { text: "Tidal Whorl", enabled: true },
                        { text: "Seismic Whorl", enabled: true },
                        { text: "Tempest Whorl", enabled: true },
                        { text: "Radiant Whorl", enabled: true },
                        { text: "Umbral Whorl", enabled: true },

                        // Violet Trial
                        { text: "--------------------", enabled: false },
                        { text: "Prism Chip", enabled: true },
                        { text: "Flawed Prism", enabled: true },
                        { text: "Flawless Prism", enabled: true },
                        { text: "Rainbow Prism", enabled: true },

                        // Shiny Slime Search!
                        { text: "--------------------", enabled: false },
                        { text: "EXP", enabled: true },

                        // Elemental Treasure Quests
                        { text: "--------------------", enabled: false },
                        { text: "Hellfire Fragment", enabled: true },
                        { text: "Deluge Fragment", enabled: true },
                        { text: "Wasteland Fragment", enabled: true },
                        { text: "Typhoon Fragment", enabled: true },

                        // Showdowns
                        { text: "--------------------", enabled: false },
                        { text: "Jasper Scale", enabled: true },
                        { text: "Scorching Peak", enabled: true },
                        { text: "Infernal Garnet", enabled: true },
                        { text: "Ifrit Anima", enabled: true },
                        { text: "Ifrit Omega Anima", enabled: true },
                        { text: "Mourning Stone", enabled: true },
                        { text: "Crystal Spirit", enabled: true },
                        { text: "Frozen Hell Prism", enabled: true },
                        { text: "Cocytus Anima", enabled: true },
                        { text: "Cocytus Omega Anima", enabled: true },
                        { text: "Scrutiny Stone", enabled: true },
                        { text: "Luminous Judgment", enabled: true },
                        { text: "Evil Judge Crystal", enabled: true },
                        { text: "Vohu Manah Anima", enabled: true },
                        { text: "Vohu Manah Omega Anima", enabled: true },
                        { text: "Sagittarius Arrowhead", enabled: true },
                        { text: "Sagittarius Rune", enabled: true },
                        { text: "Horseman's Plate", enabled: true },
                        { text: "Sagittarius Anima", enabled: true },
                        { text: "Sagittarius Omega Anima", enabled: true },
                        { text: "Solar Ring", enabled: true },
                        { text: "Sunlight Quartz", enabled: true },
                        { text: "Halo Light Quartz", enabled: true },
                        { text: "Corow Anima", enabled: true },
                        { text: "Corow Omega Anima", enabled: true },
                        { text: "Twilight Cloth Strip", enabled: true },
                        { text: "Shadow Silver", enabled: true },
                        { text: "Phantom Demon Jewel", enabled: true },
                        { text: "Diablo Anima", enabled: true },
                        { text: "Diablo Omega Anima", enabled: true },

                        // Six Dragon Trial
                        { text: "--------------------", enabled: false },
                        { text: "Red Dragon Scale", enabled: true },
                        { text: "Blue Dragon Scale", enabled: true },
                        { text: "Brown Dragon Scale", enabled: true },
                        { text: "Green Dragon Scale", enabled: true },
                        { text: "White Dragon Scale", enabled: true },
                        { text: "Black Dragon Scale", enabled: true },
                    ]
                }

                // After setting the contents of the Item Selection ComboBox, enable it for the user.
                itemComboBox.enabled = true
                itemComboBox.currentIndex = 1
            }

        }

        Label {
            id: farmingModeTextFieldLabel

            x: 20
            width: 200
            height: 13

            visible: false
            color: "#00ff00"
            text: qsTr("Farming Mode selected successfully")

            anchors.top: farmingModeComboBox.bottom
            anchors.topMargin: 5
        }

        // Select the item and the island that the item is farmed in.
        ComboBox {
            id: itemComboBox

            width: 200
            height: 30
            anchors.left: parent.left
            anchors.top: farmingModeComboBox.bottom
            anchors.topMargin: 25
            enabled: false
            anchors.leftMargin: 20

            displayText: qsTr("Please select item to farm")

            currentIndex: 0
            textRole: "text"
            
            delegate: ItemDelegate {
                width: itemComboBox.width
                text: modelData.text

                font.weight: itemComboBox.currentIndex === index ? Font.DemiBold : Font.Normal
                highlighted: ListView.isCurrentItem

                enabled: modelData.enabled
            }

            model: []

            onCurrentIndexChanged: {
                itemComboBox.displayText = qsTr(itemComboBox.model[currentIndex].text)

                // Enable the mission ComboBox.
                missionComboBox.enabled = true

                missionComboBox.currentIndex = 0

                if(farmingModeComboBox.displayText === "Quest"){
                    // Update the contents of the mission ComboBox with the appropriate Quest mission(s).
                    if(itemComboBox.displayText === "Satin Feather" || itemComboBox.displayText === "Zephyr Feather" || itemComboBox.displayText === "Flying Sprout"){
                        missionComboBox.model = [
                            { text: "Port Breeze Archipelago", enabled: false },
                            { text: "Scattered Cargo", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Fine Sand Bottle" || itemComboBox.displayText === "Untamed Flame" || itemComboBox.displayText === "Blistering Ore"){
                        missionComboBox.model = [
                            { text: "Valtz Duchy", enabled: false },
                            { text: "Lucky Charm Hunt", enabled: true },
                            { text: "Special Op's Request", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Fresh Water Jug" || itemComboBox.displayText === "Soothing Splash" || itemComboBox.displayText === "Glowing Coral"){
                        missionComboBox.model = [
                            { text: "Auguste Isles", enabled: false },
                            { text: "Threat to the Fisheries", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Rough Stone" || itemComboBox.displayText === "Swirling Amber" || itemComboBox.displayText === "Coarse Alluvium"){
                        missionComboBox.model = [
                            { text: "Lumacie Archipelago", enabled: false },
                            { text: "The Fruit of Lumacie", enabled: true },
                            { text: "Whiff of Danger", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Falcon Feather" || itemComboBox.displayText === "Spring Water Jug" || itemComboBox.displayText === "Vermilion Stone"){
                        missionComboBox.model = [
                            { text: "Albion Citadel", enabled: false },
                            { text: "I Challenge You!", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Slimy Shroom" || itemComboBox.displayText === "Hollow Soul" || itemComboBox.displayText === "Lacrimosa"){
                        missionComboBox.model = [
                            { text: "Mist-Shrouded Isle", enabled: false },
                            { text: "For Whom the Bell Tolls", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Wheat Stalk" || itemComboBox.displayText === "Iron Cluster" || itemComboBox.displayText === "Olea Plant"){
                        missionComboBox.model = [
                            { text: "Golonzo Island", enabled: false },
                            { text: "Golonzo's Battle of Old", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Indigo Fruit" || itemComboBox.displayText === "Foreboding Clover" || itemComboBox.displayText === "Blood Amber"){
                        missionComboBox.model = [
                            { text: "Amalthea Island", enabled: false },
                            { text: "The Dungeon Diet", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Sand Brick" || itemComboBox.displayText === "Native Reed"){
                        missionComboBox.model = [
                            { text: "Former Capital Mephorash", enabled: false },
                            { text: "Trust Busting Dustup", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Antique Cloth"){
                        missionComboBox.model = [
                            { text: "Former Capital Mephorash", enabled: false },
                            { text: "Trust Busting Dustup", enabled: true },
                            { text: "Erste Kingdom Episode 4", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Prosperity Flame" || itemComboBox.displayText === "Explosive Material" || itemComboBox.displayText === "Steel Liquid"){
                        missionComboBox.model = [
                            { text: "Agastia", enabled: false },
                            { text: "Imperial Wanderer's Soul", enabled: true },
                        ]
                    }
                }else if(farmingModeComboBox.displayText === "Special"){
                    // Update the contents of the mission ComboBox with the appropriate Special mission(s).
                    // Low and High Orbs.
                    if(itemComboBox.displayText === "Fire Orb" || itemComboBox.displayText === "Inferno Orb"){
                        missionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "H Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "VH Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Hellfire Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    }else if(itemComboBox.displayText === "Water Orb" || itemComboBox.displayText === "Frost Orb"){
                        missionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "H Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "VH Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Deluge Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Earth Orb" || itemComboBox.displayText === "Rumbling Orb"){
                        missionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "H Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "VH Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Wasteland Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Wind Orb" || itemComboBox.displayText === "Cyclone Orb"){
                        missionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "H Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "VH Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Typhoon Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Light Orb" || itemComboBox.displayText === "Shining Orb"){
                        missionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "H Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "VH Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Aurora Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Dark Orb" || itemComboBox.displayText === "Abysm Orb"){
                        missionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "H Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "VH Scarlet Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Oblivion Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    }
                    
                    // Tomes, Scrolls, and Whorls.
                    else if(itemComboBox.displayText === "Red Tome"){
                        missionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Hellfire Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    }
                    else if(itemComboBox.displayText === "Hellfire Scroll" || itemComboBox.displayText === "Infernal Whorl"){
                        missionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "H Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "VH Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Hellfire Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Blue Tome"){
                        missionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Deluge Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Flood Scroll" || itemComboBox.displayText === "Tidal Whorl"){
                        missionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "H Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "VH Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Deluge Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Brown Tome"){
                        missionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Wasteland Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Thunder Scroll" || itemComboBox.displayText === "Seismic Whorl"){
                        missionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "H Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "VH Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Wasteland Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Green Tome"){
                        missionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Typhoon Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Gale Scroll" || itemComboBox.displayText === "Tempest Whorl"){
                        missionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "H Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "VH Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Typhoon Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "White Tome"){
                        missionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Aurora Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Skylight Scroll" || itemComboBox.displayText === "Radiant Whorl"){
                        missionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "H Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "VH Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Aurora Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Black Tome"){
                        missionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Oblivion Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Chasm Scroll" || itemComboBox.displayText === "Umbral Whorl"){
                        missionComboBox.model = [
                            { text: "Basic Treasure Quests", enabled: false },
                            { text: "N Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "H Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "VH Cerulean Trial", map: "Basic Treasure Quests", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Oblivion Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    }

                    // Chips and Prisms.
                    else if(itemComboBox.displayText === "Prism Chip"){
                        missionComboBox.model = [
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
                    } else if(itemComboBox.displayText === "Flawed Prism"){
                        missionComboBox.model = [
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
                    } else if(itemComboBox.displayText === "Flawless Prism" || itemComboBox.displayText === "Rainbow Prism"){
                        missionComboBox.model = [
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
                    else if(itemComboBox.displayText === "EXP"){
                        missionComboBox.model = [
                            { text: "Shiny Slime Search!", enabled: false },
                            { text: "N Shiny Slime Search!", map: "Shiny Slime Search!", enabled: true },
                            { text: "H Shiny Slime Search!", map: "Shiny Slime Search!", enabled: true },
                            { text: "VH Shiny Slime Search!", map: "Shiny Slime Search!", enabled: true },
                        ]
                    }

                    // Showdown materials.
                    else if(itemComboBox.displayText === "Jasper Scale" || itemComboBox.displayText === "Scorching Peak" || itemComboBox.displayText === "Infernal Garnet"
                            || itemComboBox.displayText === "Ifrit Anima" || itemComboBox.displayText === "Ifrit Omega Anima"){
                        missionComboBox.model = [
                            { text: "Showdowns", enabled: false },
                            { text: "H Ifrit Showdown", map: "Showdowns", enabled: true },
                            { text: "VH Ifrit Showdown", map: "Showdowns", enabled: true },
                            { text: "EX Ifrit Showdown", map: "Showdowns", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Mourning Stone" || itemComboBox.displayText === "Crystal Spirit" || itemComboBox.displayText === "Frozen Hell Prism"
                            || itemComboBox.displayText === "Cocytus Anima" || itemComboBox.displayText === "Cocytus Omega Anima"){
                        missionComboBox.model = [
                            { text: "Showdowns", enabled: false },
                            { text: "H Cocytus Showdown", map: "Showdowns", enabled: true },
                            { text: "VH Cocytus Showdown", map: "Showdowns", enabled: true },
                            { text: "EX Cocytus Showdown", map: "Showdowns", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Scrutiny Stone" || itemComboBox.displayText === "Luminous Judgment" || itemComboBox.displayText === "Evil Judge Crystal"
                            || itemComboBox.displayText === "Vohu Manah Anima" || itemComboBox.displayText === "Vohu Manah Omega Anima"){
                        missionComboBox.model = [
                            { text: "Showdowns", enabled: false },
                            { text: "H Vohu Manah Showdown", map: "Showdowns", enabled: true },
                            { text: "VH Vohu Manah Showdown", map: "Showdowns", enabled: true },
                            { text: "EX Vohu Manah Showdown", map: "Showdowns", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Sagittarius Arrowhead" || itemComboBox.displayText === "Sagittarius Rune" || itemComboBox.displayText === "Horseman's Plate"
                            || itemComboBox.displayText === "Sagittarius Anima" || itemComboBox.displayText === "Sagittarius Omega Anima"){
                        missionComboBox.model = [
                            { text: "Showdowns", enabled: false },
                            { text: "H Sagittarius Showdown", map: "Showdowns", enabled: true },
                            { text: "VH Sagittarius Showdown", map: "Showdowns", enabled: true },
                            { text: "EX Sagittarius Showdown", map: "Showdowns", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Solar Ring" || itemComboBox.displayText === "Sunlight Quartz" || itemComboBox.displayText === "Halo Light Quartz"
                            || itemComboBox.displayText === "Corow Anima" || itemComboBox.displayText === "Corow Omega Anima"){
                        missionComboBox.model = [
                            { text: "Showdowns", enabled: false },
                            { text: "H Corow Showdown", map: "Showdowns", enabled: true },
                            { text: "VH Corow Showdown", map: "Showdowns", enabled: true },
                            { text: "EX Corow Showdown", map: "Showdowns", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Twilight Cloth Strip" || itemComboBox.displayText === "Shadow Silver" || itemComboBox.displayText === "Phantom Demon Jewel"
                            || itemComboBox.displayText === "Diablo Anima" || itemComboBox.displayText === "Diablo Omega Anima"){
                        missionComboBox.model = [
                            { text: "Showdowns", enabled: false },
                            { text: "H Diablo Showdown", map: "Showdowns", enabled: true },
                            { text: "VH Diablo Showdown", map: "Showdowns", enabled: true },
                            { text: "EX Diablo Showdown", map: "Showdowns", enabled: true },
                        ]
                    }

                    // Dragon Scales.
                    else if(itemComboBox.displayText === "Red Dragon Scale"){
                        missionComboBox.model = [
                            { text: "Six Dragon Trial", enabled: false },
                            { text: "N Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "H Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "VH Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Hellfire Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Blue Dragon Scale"){
                        missionComboBox.model = [
                            { text: "Six Dragon Trial", enabled: false },
                            { text: "N Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "H Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "VH Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Deluge Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Brown Dragon Scale"){
                        missionComboBox.model = [
                            { text: "Six Dragon Trial", enabled: false },
                            { text: "N Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "H Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "VH Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Wasteland Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Green Dragon Scale"){
                        missionComboBox.model = [
                            { text: "Six Dragon Trial", enabled: false },
                            { text: "N Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "H Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "VH Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Typhoon Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "White Dragon Scale"){
                        missionComboBox.model = [
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
                    } else if(itemComboBox.displayText === "Black Dragon Scale"){
                        missionComboBox.model = [
                            { text: "Six Dragon Trial", enabled: false },
                            { text: "N Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "H Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "VH Six Dragon Trial", map: "Six Dragon Trial", enabled: true },
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Oblivion Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    }

                    // Fragments
                    else if(itemComboBox.displayText === "Hellfire Fragment"){
                        missionComboBox.model = [
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Hellfire Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Deluge Fragment"){
                        missionComboBox.model = [
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Deluge Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Wasteland Fragment"){
                        missionComboBox.model = [
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Wasteland Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Typhoon Fragment"){
                        missionComboBox.model = [
                            { text: "Elemental Treasure Quests", enabled: false },
                            { text: "The Typhoon Trial", map: "Elemental Treasure Quests", enabled: true },
                        ]
                    }
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
            height: 30
            anchors.left: parent.left
            anchors.top: itemComboBox.bottom
            anchors.topMargin: 25
            enabled: false
            anchors.leftMargin: 20

            displayText: qsTr("Please select mission")

            currentIndex: 0
            textRole: "text"

            model: []

            delegate: ItemDelegate {
                width: missionComboBox.width
                text: modelData.text

                property var map: modelData.map // Holds the map in which the mission will take place in.

                font.weight: missionComboBox.currentIndex === index ? Font.DemiBold : Font.Normal
                highlighted: ListView.isCurrentItem

                enabled: modelData.enabled
            }

            onVisibleChanged: {
                if(missionComboBox.displayText === qsTr("Please select a mission.") && missionComboBox.enabled === true){
                    // Inform the user with a message instructing them to select a mission from the ComboBox above.
                    missionSelectionTextFieldLabel.visible = true
                    missionSelectionTextFieldLabel.text = qsTr("Select a mission above")
                    missionSelectionTextFieldLabel.color = "#ff0000"

                    backend.check_bot_ready(false)
                }else if(missionComboBox.displayText !== qsTr("Please select a mission.") && missionComboBox.enabled === true && partySelectionComboBox.enabled === true){
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
                if(missionComboBox.displayText === qsTr("Please select a mission.") && missionComboBox.enabled === true){
                    missionSelectionTextFieldLabel.visible = true
                    missionSelectionTextFieldLabel.text = qsTr("Select a mission above")
                    missionSelectionTextFieldLabel.color = "#ff0000"

                    backend.check_bot_ready(false)
                }else if(missionComboBox.displayText !== qsTr("Please select a mission.") && missionComboBox.enabled === true && partySelectionComboBox.enabled === true){
                    // This occurs when the user went back after setting their settings and changed their selected item and mission.
                    missionSelectionTextFieldLabel.visible = true
                    missionSelectionTextFieldLabel.text = qsTr("Mission selected successfully")
                    missionSelectionTextFieldLabel.color = "#00ff00"

                    backend.check_bot_ready(true)
                }else if(missionComboBox.displayText !== qsTr("Please select a mission.") && missionComboBox.enabled === true && partySelectionComboBox.enabled != true){
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
                if(farmingModeComboBox.displayText === "Quest"){
                    backend.update_mission_name(missionComboBox.model[currentIndex].text, missionComboBox.model[0].text)
                }else if(farmingModeComboBox.displayText === "Special"){
                    backend.update_mission_name(missionComboBox.model[currentIndex].text, missionComboBox.model[currentIndex].map)
                }
                

                // Reveal the Mission Selection success message.
                if(botReadyLabel.text !== qsTr("Bot is ready to start")){
                    missionSelectionTextFieldLabel.visible = true
                }else if(summonSelectionLabel.text === qsTr("Summon selected successfully") && summonSelectionLabel.visible === true){
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
                if(missionSelectionTextFieldLabel.visible === true && missionComboBox.displayText !== qsTr("Please select a mission.")){
                    amountOfItemTextField.enabled = true
                }
            }
        }

        // Select the amount of items that the user wants the bot to acquire.
        ComboBox {
            id: amountOfItemTextField

            width: 100
            height: 30
            anchors.left: parent.left
            anchors.top: missionComboBox.bottom
            anchors.topMargin: 25
            anchors.leftMargin: 20

            textRole: "text"
            displayText: qsTr("# of Item")

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
                if(amountOfItemTextField.enabled === true){
                    amountOfItemTextField.displayText = qsTr("# of Item")
                    //summonSelectionLabel.visible = true
                    //summonSelectionLabel.color = "#fc8c03"
                }
            }

            onCurrentIndexChanged: {
                // Update the backend with the # of Items selected.
                amountOfItemTextField.displayText = currentIndex + 1
                backend.update_item_amount(amountOfItemTextField.displayText)

                amountOfItemTextFieldLabel.visible = true

                summonButton.enabled = true
            }
        }

        Label {
            id: amountOfItemTextFieldLabel

            x: 20
            width: 200
            height: 13
            visible: false

            color: "#00ff00"
            text: qsTr("Amount of items selected successfully")

            anchors.top: amountOfItemTextField.bottom
            anchors.topMargin: 5

            onVisibleChanged: {
                if(amountOfItemTextFieldLabel.visible === true){
                    summonButton.enabled = true
                    summonSelectionLabel.visible = true
                }
            }
        }

        // Clicking this button will open up the overlay that will contain selectable Summons.
        Button {
            id: summonButton
            height: 30

            text: qsTr("Select Summon")
            anchors.left: parent.left
            anchors.top: amountOfItemTextField.bottom
            anchors.topMargin: 25
            anchors.leftMargin: 20

            enabled: false

            // On clicked, open up the overlay containing the selectable Summons.
            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor

                onClicked: popup.open()
            }

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
            text: qsTr("Now select your Summon")
            anchors.top: summonButton.bottom
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
                if(groupSelectionComboBox.enabled === true){
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
                if(partySelectionComboBox.enabled === true){
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

                    if(debugModeCheckBox.checked){
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
            y: 295
            width: 100
            height: 30
            visible: false

            text: "Test Mode"

            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor

                onClicked: {
                    testModeCheckBox.checked = !testModeCheckBox.checked

                    if(testModeCheckBox.checked){
                        backend.check_bot_ready(true)
                    }else{
                        backend.check_bot_ready(false)
                    }
                }
            }
        }
    }

    Connections{
        target: backend

        // Retrieve the name of the opened script file back from backend.
        function onOpenFile(scriptName){
            combatScriptTextField.text = qsTr(scriptName)
            combatScriptTextFieldLabel.visible = true
            logTextArea.append("\nCombat script selected: " + scriptName)

            // Enable the Farming Mode ComboBox.
            farmingModeComboBox.enabled = true
        }

        // Output update messages to the log.
        function onUpdateMessage(updateMessage){
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

        // Enable the group and party selectors after the backend receives the user-selected Summon. 
        // Update the informational message to indicate success.
        function onEnableGroupAndPartySelectors(){
            summonSelectionLabel.text = qsTr("Summon selected successfully")
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
    D{i:0;autoSize:true;formeditorZoom:1.66;height:453;width:300}D{i:29}D{i:34}
}
##^##*/
