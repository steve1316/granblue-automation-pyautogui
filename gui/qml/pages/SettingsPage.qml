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
                { text: "Special", enabled: true },
                { text: "Coop", enabled: true},
                { text: "Raid", enabled: true}
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
                        { text: "Fire Orb", enabled: true },
                        { text: "Water Orb", enabled: true },
                        { text: "Earth Orb",  enabled: true },
                        { text: "Light Orb", enabled: true },
                        { text: "Dark Orb", enabled: true },
                        { text: "Inferno Orb", enabled: true },
                        { text: "Frost Orb", enabled: true },
                        { text: "Rumbling Orb", enabled: true },
                        { text: "Cyclone Orb", enabled: true },
                        { text: "Shining Orb", enabled: true },
                        { text: "Abysm Orb", enabled: true },

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
                } else if(farmingModeComboBox.model[currentIndex].text === "Coop"){
                    itemComboBox.model = [
                        // Creeds
                        { text: "--------------------", enabled: false },
                        { text: "Warrior Creed", enabled: true },
                        { text: "Mage Creed", enabled: true },

                        // Materials
                        { text: "--------------------", enabled: false },
                        { text: "Infernal Garnet", enabled: true },
                        { text: "Frozen Hell Prism", enabled: true },
                        { text: "Evil Judge Crystal", enabled: true },
                        { text: "Horseman's Plate", enabled: true },
                        { text: "Halo Light Quartz", enabled: true },
                        { text: "Phantom Demon Jewel", enabled: true },

                        // Distinctions
                        { text: "--------------------", enabled: false },
                        { text: "Gladiator Distinction", enabled: true },
                        { text: "Guardian Distinction", enabled: true },
                        { text: "Pilgrim Distinction", enabled: true },
                        { text: "Mage Distinction", enabled: true },
                        { text: "Bandit Distinction", enabled: true },
                        { text: "Fencer Distinction", enabled: true },
                        { text: "Combatant Distinction", enabled: true },
                        { text: "Sharpshooter Distinction", enabled: true },
                        { text: "Troubadour Distinction", enabled: true },
                        { text: "Cavalryman Distinction", enabled: true },
                        { text: "Alchemist Distinction", enabled: true },
                        { text: "Samurai Distinction", enabled: true },
                        { text: "Ninja Distinction", enabled: true },
                        { text: "Sword Master Distinction", enabled: true },
                        { text: "Gunslinger Distinction", enabled: true },
                        { text: "Mystic Distinction", enabled: true },
                        { text: "Assassin Distinction", enabled: true },
                        { text: "Dual Wielder Distinction", enabled: true },
                        { text: "Shredder Distinction", enabled: true },
                        { text: "Forester's Distinction", enabled: true },
                        { text: "Dragoon's Distinction", enabled: true },
                        { text: "Monk's Distinction", enabled: true },
                        { text: "Longstrider's Distinction", enabled: true },

                        // Replicas
                        { text: "--------------------", enabled: false },
                        { text: "Avenger Replica", enabled: true },
                        { text: "Skofnung Replica", enabled: true },
                        { text: "Oliver Replica", enabled: true },
                        { text: "Aschallon Replica", enabled: true },
                        { text: "Nirvana Replica", enabled: true },
                        { text: "Keraunos Replica", enabled: true },
                        { text: "Hellion Gauntlet Replica", enabled: true },
                        { text: "Ipetam Replica", enabled: true },
                        { text: "Rosenbogen Replica", enabled: true },
                        { text: "Langeleik Replica", enabled: true },
                        { text: "Romulus Spear Replica", enabled: true },
                        { text: "Proximo Replica", enabled: true },
                        { text: "Murakumo Replica", enabled: true },
                        { text: "Nebuchad Replica", enabled: true },
                        { text: "Misericorde Replica", enabled: true },
                        { text: "Faust Replica", enabled: true },
                        { text: "Muramasa Replica", enabled: true },
                        { text: "Kapilavastu Replica", enabled: true },
                        { text: "Practice Drum", enabled: true },
                    ]
                } else if(farmingModeComboBox.model[currentIndex].text === "Raid"){
                    itemComboBox.model = [
                        // Tiamat Omega
                        { text: "--------------------", enabled: false },
                        { text: "Tiamat Omega", enabled: true },
                        { text: "Tiamat Anima", enabled: true },
                        { text: "Tiamat Omega Anima", enabled: true },
                        { text: "Tiamat Amood Omega",  enabled: true },
                        { text: "Tiamat Bolt Omega", enabled: true },
                        { text: "Tiamat Gauntlet Omega", enabled: true },
                        { text: "Tiamat Glaive Omega", enabled: true },

                        // Colossus Omega
                        { text: "--------------------", enabled: false },
                        { text: "Colossus Omega", enabled: true },
                        { text: "Colossus Anima", enabled: true },
                        { text: "Colossus Omega Anima", enabled: true },
                        { text: "Colossus Blade Omega",  enabled: true },
                        { text: "Colossus Cane Omega", enabled: true },
                        { text: "Colossus Carbine Omega", enabled: true },
                        { text: "Colossus Fist Omega", enabled: true },

                        // Leviathan Omega
                        { text: "--------------------", enabled: false },
                        { text: "Leviathan Omega", enabled: true },
                        { text: "Leviathan Anima", enabled: true },
                        { text: "Leviathan Omega Anima", enabled: true },
                        { text: "Leviathan Gaze Omega",  enabled: true },
                        { text: "Leviathan Spear Omega", enabled: true },
                        { text: "Leviathan Scepter Omega", enabled: true },
                        { text: "Leviathan Bow Omega", enabled: true },

                        // Yggdrasil Omega
                        { text: "--------------------", enabled: false },
                        { text: "Yggdrasil Omega", enabled: true },
                        { text: "Yggdrasil Anima", enabled: true },
                        { text: "Yggdrasil Omega Anima", enabled: true },
                        { text: "Yggdrasil Crystal Blade Omega",  enabled: true },
                        { text: "Yggdrasil Bow Omega", enabled: true },
                        { text: "Yggdrasil Dagger Omega", enabled: true },
                        { text: "Yggdrasil Dewbranch Omega", enabled: true },

                        // Luminiera Omega
                        { text: "--------------------", enabled: false },
                        { text: "Luminiera Omega", enabled: true },
                        { text: "Luminiera Anima", enabled: true },
                        { text: "Luminiera Omega Anima", enabled: true },
                        { text: "Luminiera Sword Omega",  enabled: true },
                        { text: "Luminiera Bhuj Omega", enabled: true },
                        { text: "Luminiera Bolt Omega", enabled: true },
                        { text: "Luminiera Harp Omega", enabled: true },

                        // Celeste Omega
                        { text: "--------------------", enabled: false },
                        { text: "Celeste Omega", enabled: true },
                        { text: "Celeste Anima", enabled: true },
                        { text: "Celeste Omega Anima", enabled: true },
                        { text: "Celeste Harp Omega",  enabled: true },
                        { text: "Celeste Zaghnal Omega", enabled: true },
                        { text: "Celeste Horn Omega", enabled: true },
                        { text: "Celeste Claw Omega", enabled: true },

                        // Twin Elements
                        { text: "--------------------", enabled: false },
                        { text: "Twin Elements Anima", enabled: true },
                        { text: "Twin Elements Omega Anima", enabled: true },
                        { text: "Ecke Sachs",  enabled: true },
                        { text: "Ancient Ecke Sachs", enabled: true },

                        // Macula Marius
                        { text: "--------------------", enabled: false },
                        { text: "Macula Marius Anima", enabled: true },
                        { text: "Macula Marius Omega Anima", enabled: true },
                        { text: "Auberon",  enabled: true },
                        { text: "Ancient Auberon", enabled: true },

                        // Medusa
                        { text: "--------------------", enabled: false },
                        { text: "Medusa Anima", enabled: true },
                        { text: "Medusa Omega Anima", enabled: true },
                        { text: "Perseus",  enabled: true },
                        { text: "Ancient Perseus", enabled: true },

                        // Nezha
                        { text: "--------------------", enabled: false },
                        { text: "Nezha Anima", enabled: true },
                        { text: "Nezha Omega Anima", enabled: true },
                        { text: "Nalakuvara",  enabled: true },
                        { text: "Ancient Nalakuvara", enabled: true },

                        // Apollo
                        { text: "--------------------", enabled: false },
                        { text: "Apollo Anima", enabled: true },
                        { text: "Apollo Omega Anima", enabled: true },
                        { text: "Bow of Artemis",  enabled: true },
                        { text: "Ancient Bow of Artemis", enabled: true },

                        // Dark Angel Olivia
                        { text: "--------------------", enabled: false },
                        { text: "Dark Angel Olivia Anima", enabled: true },
                        { text: "Dark Angel Olivia Omega Anima", enabled: true },
                        { text: "Cortana",  enabled: true },
                        { text: "Ancient Cortana", enabled: true },

                        // Athena
                        { text: "--------------------", enabled: false },
                        { text: "Athena Anima", enabled: true },
                        { text: "Athena Omega Anima", enabled: true },
                        { text: "Erichthonius",  enabled: true },
                        { text: "Sword of Pallas", enabled: true },

                        // Grani
                        { text: "--------------------", enabled: false },
                        { text: "Grani Anima", enabled: true },
                        { text: "Grani Omega Anima", enabled: true },
                        { text: "Bow of Sigurd",  enabled: true },
                        { text: "Wilhelm", enabled: true },

                        // Baal
                        { text: "--------------------", enabled: false },
                        { text: "Baal Anima", enabled: true },
                        { text: "Baal Omega Anima", enabled: true },
                        { text: "Solomon's Axe",  enabled: true },
                        { text: "Spymur's Vision", enabled: true },

                        // Garuda
                        { text: "--------------------", enabled: false },
                        { text: "Garuda Anima", enabled: true },
                        { text: "Garuda Omega Anima", enabled: true },
                        { text: "Plume of Suparna",  enabled: true },
                        { text: "Indra's Edge", enabled: true },

                        // Odin
                        { text: "--------------------", enabled: false },
                        { text: "Odin Anima", enabled: true },
                        { text: "Odin Omega Anima", enabled: true },
                        { text: "Gungnir",  enabled: true },
                        { text: "Sleipnir Shoe", enabled: true },

                        // Lich
                        { text: "--------------------", enabled: false },
                        { text: "Lich Anima", enabled: true },
                        { text: "Lich Omega Anima", enabled: true },
                        { text: "Obscuritas",  enabled: true },
                        { text: "Phantasmas", enabled: true },

                        // Michael
                        // { text: "--------------------", enabled: false },
                        // { text: "Michael Anima", enabled: true },

                        // Gabriel
                        // { text: "--------------------", enabled: false },
                        // { text: "Gabriel Anima", enabled: true },

                        // Uriel
                        // { text: "--------------------", enabled: false },
                        // { text: "Uriel Anima", enabled: true },

                        // Raphael
                        // { text: "--------------------", enabled: false },
                        // { text: "Raphael Anima", enabled: true },

                        // Huanglong and Qilin
                        { text: "--------------------", enabled: false },
                        { text: "Huanglong Anima", enabled: true },
                        { text: "Qilin Anima", enabled: true },

                        // Shiva
                        { text: "--------------------", enabled: false },
                        { text: "Shiva Anima", enabled: true },
                        { text: "Shiva Omega Anima", enabled: true },
                        { text: "Scimitar of Brahman",  enabled: true },
                        { text: "Trident of Brahman", enabled: true },
                        { text: "Hand of Brahman", enabled: true },
                        { text: "Nilakantha", enabled: true },

                        // Europa
                        { text: "--------------------", enabled: false },
                        { text: "Europa Anima", enabled: true },
                        { text: "Europa Omega Anima", enabled: true },
                        { text: "Tyros Bow",  enabled: true },
                        { text: "Tyros Scepter", enabled: true },
                        { text: "Tyros Zither", enabled: true },
                        { text: "Spirit of Mana", enabled: true },

                        // Godsworn Alexiel
                        { text: "--------------------", enabled: false },
                        { text: "Godsworn Alexiel Anima", enabled: true },
                        { text: "Godsworn Alexiel Omega Anima", enabled: true },
                        { text: "Nibelung Horn",  enabled: true },
                        { text: "Nibelung Klinge", enabled: true },
                        { text: "Nibelung Messer", enabled: true },
                        { text: "Godsworn Edge", enabled: true },

                        // Grimnir
                        { text: "--------------------", enabled: false },
                        { text: "Grimnir Anima", enabled: true },
                        { text: "Grimnir Omega Anima", enabled: true },
                        { text: "Last Storm Blade",  enabled: true },
                        { text: "Last Storm Harp", enabled: true },
                        { text: "Last Storm Lance", enabled: true },
                        { text: "Coruscant Crozier", enabled: true },

                        // Metatron
                        { text: "--------------------", enabled: false },
                        { text: "Metatron Anima", enabled: true },
                        { text: "Metatron Omega Anima", enabled: true },
                        { text: "Mittron's Treasured Blade",  enabled: true },
                        { text: "Mittron's Gauntlet", enabled: true },
                        { text: "Mittron's Bow", enabled: true },
                        { text: "Pillar of Flame", enabled: true },

                        // Avatar
                        { text: "--------------------", enabled: false },
                        { text: "Avatar Anima", enabled: true },
                        { text: "Avatar Omega Anima", enabled: true },
                        { text: "Abyss Striker",  enabled: true },
                        { text: "Abyss Spine", enabled: true },
                        { text: "Abyss Gaze", enabled: true },
                        { text: "Zechariah", enabled: true },

                        // Prometheus
                        { text: "--------------------", enabled: false },
                        { text: "Prometheus Anima", enabled: true },
                        { text: "Fire of Prometheus",  enabled: true },
                        { text: "Chains of Caucasus", enabled: true },

                        // Ca Ong
                        { text: "--------------------", enabled: false },
                        { text: "Ca Ong Anima", enabled: true },
                        { text: "Keeper of Hallowed Ground",  enabled: true },
                        { text: "Savior of Hallowed Ground", enabled: true },

                        // Gilgamesh
                        { text: "--------------------", enabled: false },
                        { text: "Gilgamesh Anima", enabled: true },
                        { text: "All-Might Spear",  enabled: true },
                        { text: "All-Might Battle-Axe", enabled: true },

                        // Morrigna
                        { text: "--------------------", enabled: false },
                        { text: "Morrigna Anima", enabled: true },
                        { text: "Le Fay",  enabled: true },
                        { text: "Unius", enabled: true },

                        // Hector
                        { text: "--------------------", enabled: false },
                        { text: "Hector Anima", enabled: true },
                        { text: "Bow of Iliad",  enabled: true },
                        { text: "Adamantine Gauntlet", enabled: true },

                        // Anubis
                        { text: "--------------------", enabled: false },
                        { text: "Anubis Anima", enabled: true },
                        { text: "Hermanubis",  enabled: true },
                        { text: "Scales of Dominion", enabled: true },

                        // Tiamat Malice
                        { text: "--------------------", enabled: false },
                        { text: "Tiamat Malice Anima", enabled: true },
                        { text: "Hatsoiiłhał",  enabled: true },
                        { text: "Majestas", enabled: true },

                        // Leviathan Malice
                        { text: "--------------------", enabled: false },
                        { text: "Leviathan Malice Anima", enabled: true },
                        { text: "Kaladanda",  enabled: true },
                        { text: "Kris of Hypnos", enabled: true },

                        // Leviathan Malice
                        { text: "--------------------", enabled: false },
                        { text: "Leviathan Malice Anima", enabled: true },
                        { text: "Kaladanda",  enabled: true },
                        { text: "Kris of Hypnos", enabled: true },

                        // Phronesis
                        { text: "--------------------", enabled: false },
                        { text: "Phronesis Anima", enabled: true },
                        { text: "Dark Thrasher",  enabled: true },
                        { text: "Master Bamboo Sword", enabled: true },
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
                            { text: "Golonzo's Battles of Old", enabled: true },
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
                            { text: "Angel Halo", enabled: false },
                            { text: "N Angel Halo", map: "Angel Halo", enabled: true },
                            { text: "H Angel Halo", map: "Angel Halo", enabled: true },
                            { text: "VH Angel Halo", map: "Angel Halo", enabled: true },
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
                } else if(farmingModeComboBox.displayText === "Coop"){
                    // Creeds
                    if(itemComboBox.displayText === "Warrior Creed" || itemComboBox.displayText === "Mage Creed"){
                        missionComboBox.model = [
                            { text: "EX1", enabled: false },
                            { text: "Corridor of Puzzles", map: "", enabled: true },
                            { text: "Lost in the Dark", map: "", enabled: true },
                        ]
                    } 
                    
                    // Materials
                    else if(itemComboBox.displayText === "Infernal Garnet"){
                        missionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Revelation", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Frozen Hell Prism"){
                        missionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Tundra", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Evil Judge Crystal"){
                        missionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Judgement", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Horseman's Plate"){
                        missionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Plains", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Halo Light Quartz"){
                        missionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Eminence", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Phantom Demon Jewel"){
                        missionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Twilight", map: "", enabled: true },
                        ]
                    }

                    // Distinctions
                    else if(itemComboBox.displayText === "Gladiator Distinction"){
                        missionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Revelation", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst Severe Cliffs", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Guardian Distinction"){
                        missionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Tundra", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Flames", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Pilgrim Distinction"){
                        missionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Judgement", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Waves", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Mage Distinction"){
                        missionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Judgement", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Waves", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Bandit Distinction"){
                        missionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Eminence", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Flames", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Fencer Distinction"){
                        missionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Revelation", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst Severe Cliffs", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Combatant Distinction"){
                        missionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Tundra", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst Severe Cliffs", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Sharpshooter Distinction"){
                        missionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Plains", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Petals", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Troubadour Distinction"){
                        missionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Eminence", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Flames", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Cavalryman Distinction"){
                        missionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Plains", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Flames", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Alchemist Distinction"){
                        missionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Judgement", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Waves", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Samurai Distinction"){
                        missionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Twilight", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Petals", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Ninja Distinction"){
                        missionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Twilight", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Petals", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Sword Master Distinction"){
                        missionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Tundra", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst Severe Cliffs", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Gunslinger Distinction"){
                        missionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Plains", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Petals", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Mystic Distinction"){
                        missionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Eminence", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Waves", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Assassin Distinction"){
                        missionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Twilight", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Petals", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Dual Wielder Distinction"){
                        missionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Revelation", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Shredder Distinction"){
                        missionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Eminence", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Forester's Distinction"){
                        missionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Revelation", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Dragoon's Distinction"){
                        missionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Rule of the Tundra", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Flames", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Monk's Distinction"){
                        missionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Judgement", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Waves", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Longstrider's Distinction"){
                        missionComboBox.model = [
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Petals", map: "", enabled: true },
                        ]
                    }

                    // Replicas
                    else if(itemComboBox.displayText === "Avenger Replica"){
                        missionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Revelation", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Skofnung Replica"){
                        missionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Tundra", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Oliver Replica"){
                        missionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Plains", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Waves", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Aschallon Replica"){
                        missionComboBox.model = [
                            { text: "EX4", enabled: false },
                            { text: "Amidst Severe Cliffs", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Nirvana Replica"){
                        missionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Eminence", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Keraunos Replica"){
                        missionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Judgement", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Hellion Gauntlet Replica"){
                        missionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Revelation", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst Severe Cliffs", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Ipetam Replica"){
                        missionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Twilight", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Flames", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Rosenbogen Replica"){
                        missionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Plains", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Langeleik Replica"){
                        missionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Tundra", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Waves", map: "", enabled: true },
                            { text: "Amidst the Petals", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Romulus Spear Replica"){
                        missionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Eminence", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Waves", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Proximo Replica"){
                        missionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Twilight", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Waves", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Murakumo Replica"){
                        missionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Eminence", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Flames", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Nebuchad Replica"){
                        missionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Twilight", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Flames", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Misericorde Replica"){
                        missionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Plains", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Petals", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Faust Replica"){
                        missionComboBox.model = [
                            { text: "EX2", enabled: false },
                            { text: "Time of Judgement", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Petals", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Muramasa Replica"){
                        missionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Twilight", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst Severe Cliffs", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Kapilavastu Replica"){
                        missionComboBox.model = [
                            { text: "EX3", enabled: false },
                            { text: "Rule of the Tundra", map: "", enabled: true },
                            { text: "EX4", enabled: false },
                            { text: "Amidst the Waves", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Practice Drum"){
                        missionComboBox.model = [
                            { text: "EX4", enabled: false },
                            { text: "Amidst Severe Cliffs", map: "", enabled: true },
                        ]
                    }
                } else if(farmingModeComboBox.displayText === "Raid"){
                    // Omega Weapons
                    if(itemComboBox.displayText === "Tiamat Omega" || itemComboBox.displayText === "Tiamat Anima" || itemComboBox.displayText === "Tiamat Omega Anima" || itemComboBox.displayText === "Tiamat Amood Omega" || itemComboBox.displayText === "Tiamat Bolt Omega"
                    || itemComboBox.displayText === "Tiamat Gauntlet Omega" || itemComboBox.displayText === "Tiamat Glaive Omega"){
                        missionComboBox.model = [
                            { text: "Tiamat Omega", enabled: false },
                            { text: "Lvl 50 Tiamat Omega", map: "", enabled: true },
                            { text: "Lvl 100 Tiamat Omega Ayr", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Colossus Omega" || itemComboBox.displayText === "Colossus Anima" || itemComboBox.displayText === "Colossus Omega Anima" || itemComboBox.displayText === "Colossus Blade Omega" || itemComboBox.displayText === "Colossus Cane Omega"
                    || itemComboBox.displayText === "Colossus Carbine Omega" || itemComboBox.displayText === "Colossus Fist Omega"){
                        missionComboBox.model = [
                            { text: "Colossus Omega", enabled: false },
                            { text: "Lvl 70 Colossus Omega", map: "", enabled: true },
                            { text: "Lvl 100 Colossus Omega", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Leviathan Omega" || itemComboBox.displayText === "Leviathan Anima" || itemComboBox.displayText === "Leviathan Omega Anima" || itemComboBox.displayText === "Leviathan Bow Omega" || itemComboBox.displayText === "Leviathan Gaze Omega"
                    || itemComboBox.displayText === "Leviathan Scepter Omega" || itemComboBox.displayText === "Leviathan Spear Omega"){
                        missionComboBox.model = [
                            { text: "Leviathan Omega", enabled: false },
                            { text: "Lvl 60 Leviathan Omega", map: "", enabled: true },
                            { text: "Lvl 100 Leviathan Omega", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Yggdrasil Omega" || itemComboBox.displayText === "Yggdrasil Anima" || itemComboBox.displayText === "Yggdrasil Omega Anima" || itemComboBox.displayText === "Yggdrasil Bow Omega" || itemComboBox.displayText === "Yggdrasil Crystal Blade Omega"
                    || itemComboBox.displayText === "Yggdrasil Dagger Omega" || itemComboBox.displayText === "Yggdrasil Dewbranch Omega"){
                        missionComboBox.model = [
                            { text: "Yggdrasil Omega", enabled: false },
                            { text: "Lvl 60 Yggdrasil Omega", map: "", enabled: true },
                            { text: "Lvl 100 Yggdrasil Omega", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Luminiera Omega" || itemComboBox.displayText === "Luminiera Anima" || itemComboBox.displayText === "Luminiera Omega Anima" || itemComboBox.displayText === "Luminiera Bhuj Omega" || itemComboBox.displayText === "Luminiera Bolt Omega"
                    || itemComboBox.displayText === "Luminiera Harp Omega" || itemComboBox.displayText === "Luminiera Sword Omega"){
                        missionComboBox.model = [
                            { text: "Luminiera Omega", enabled: false },
                            { text: "Lvl 75 Luminiera Omega", map: "", enabled: true },
                            { text: "Lvl 100 Luminiera Omega", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Celeste Omega" || itemComboBox.displayText === "Celeste Anima" || itemComboBox.displayText === "Celeste Omega Anima" || itemComboBox.displayText === "Celeste Harp Omega" || itemComboBox.displayText === "Celeste Claw Omega"
                    || itemComboBox.displayText === "Celeste Horn Omega" || itemComboBox.displayText === "Celeste Zaghnal Omega"){
                        missionComboBox.model = [
                            { text: "Celeste", enabled: false },
                            { text: "Lvl 75 Celeste Omega", map: "", enabled: true },
                            { text: "Lvl 100 Celeste Omega", map: "", enabled: true },
                        ]
                    } 
                    
                    // Regalia Weapons
                    else if(itemComboBox.displayText === "Shiva Anima" || itemComboBox.displayText === "Shiva Omega Anima" || itemComboBox.displayText === "Hand of Brahman" || itemComboBox.displayText === "Scimitar of Brahman"
                    || itemComboBox.displayText === "Trident of Brahman" || itemComboBox.displayText === "Nilakantha"){
                        missionComboBox.model = [
                            { text: "Shiva", enabled: false },
                            { text: "Lvl 120 Shiva", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Europa Anima" || itemComboBox.displayText === "Europa Omega Anima" || itemComboBox.displayText === "Tyros Bow" || itemComboBox.displayText === "Tyros Scepter"
                    || itemComboBox.displayText === "Tyros Zither" || itemComboBox.displayText === "Spirit of Mana"){
                        missionComboBox.model = [
                            { text: "Europa", enabled: false },
                            { text: "Lvl 120 Europa", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Alexiel Anima" || itemComboBox.displayText === "Alexiel Omega Anima" || itemComboBox.displayText === "Nibelung Horn" || itemComboBox.displayText === "Nibelung Klinge"
                    || itemComboBox.displayText === "Nibelung Messer" || itemComboBox.displayText === "Godsworn Edge"){
                        missionComboBox.model = [
                            { text: "Godsworn Alexiel", enabled: false },
                            { text: "Lvl 120 Godsworn Alexiel", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Grimnir Anima" || itemComboBox.displayText === "Grimnir Omega Anima" || itemComboBox.displayText === "Last Storm Blade" || itemComboBox.displayText === "Last Storm Harp"
                    || itemComboBox.displayText === "Last Storm Lance" || itemComboBox.displayText === "Coruscant Crozier"){
                        missionComboBox.model = [
                            { text: "Grimnir", enabled: false },
                            { text: "Lvl 120 Grimnir", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Metatron Anima" || itemComboBox.displayText === "Metatron Omega Anima" || itemComboBox.displayText === "Mittron's Treasured Blade" || itemComboBox.displayText === "Mittron's Gauntlet"
                    || itemComboBox.displayText === "Mittron's Bow" || itemComboBox.displayText === "Pillar of Flame"){
                        missionComboBox.model = [
                            { text: "Metatron", enabled: false },
                            { text: "Lvl 120 Metatron", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Avatar Anima" || itemComboBox.displayText === "Avatar Omega Anima" || itemComboBox.displayText === "Abyss Striker" || itemComboBox.displayText === "Abyss Spine"
                    || itemComboBox.displayText === "Abyss Gaze" || itemComboBox.displayText === "Zechariah"){
                        missionComboBox.model = [
                            { text: "Avatar", enabled: false },
                            { text: "Lvl 120 Avatar", map: "", enabled: true },
                        ]
                    }

                    // Olden Primal and Primal Weapons
                    else if(itemComboBox.displayText === "Twin Elements Anima" || itemComboBox.displayText === "Twin Elements Omega Anima" || itemComboBox.displayText === "Ancient Ecke Sachs" || itemComboBox.displayText === "Ecke Sachs"){
                        missionComboBox.model = [
                            { text: "Twin Elements", enabled: false },
                            { text: "Lvl 100 Twin Elements", map: "", enabled: true },
                            { text: "Lvl 120 Twin Elements", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Macula Marius Anima" || itemComboBox.displayText === "Macula Marius Omega Anima" || itemComboBox.displayText === "Ancient Auberon" || itemComboBox.displayText === "Auberon"){
                        missionComboBox.model = [
                            { text: "Macula Marius", enabled: false },
                            { text: "Lvl 100 Macula Marius", map: "", enabled: true },
                            { text: "Lvl 120 Macula Marius", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Medusa Anima" || itemComboBox.displayText === "Medusa Omega Anima" || itemComboBox.displayText === "Ancient Perseus" || itemComboBox.displayText === "Perseus"){
                        missionComboBox.model = [
                            { text: "Medusa", enabled: false },
                            { text: "Lvl 100 Medusa", map: "", enabled: true },
                            { text: "Lvl 120 Medusa", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Nezha Anima" || itemComboBox.displayText === "Nezha Omega Anima" || itemComboBox.displayText === "Ancient Nalakuvara" || itemComboBox.displayText === "Nalakuvara"){
                        missionComboBox.model = [
                            { text: "Nezha", enabled: false },
                            { text: "Lvl 100 Nezha", map: "", enabled: true },
                            { text: "Lvl 120 Nezha", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Apollo Anima" || itemComboBox.displayText === "Apollo Omega Anima" || itemComboBox.displayText === "Ancient Bow of Artemis" || itemComboBox.displayText === "Bow of Artemis"){
                        missionComboBox.model = [
                            { text: "Apollo", enabled: false },
                            { text: "Lvl 100 Apollo", map: "", enabled: true },
                            { text: "Lvl 120 Apollo", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Dark Angel Olivia Anima" || itemComboBox.displayText === "Dark Angel Olivia Omega Anima" || itemComboBox.displayText === "Ancient Cortana" || itemComboBox.displayText === "Cortana"){
                        missionComboBox.model = [
                            { text: "Dark Angel Olivia", enabled: false },
                            { text: "Lvl 100 Dark Angel Olivia", map: "", enabled: true },
                            { text: "Lvl 120 Dark Angel Olivia", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Athena Anima" || itemComboBox.displayText === "Athena Omega Anima" || itemComboBox.displayText === "Erichthonius" || itemComboBox.displayText === "Sword of Pallas"){
                        missionComboBox.model = [
                            { text: "Athena", enabled: false },
                            { text: "Lvl 100 Athena", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Grani Anima" || itemComboBox.displayText === "Grani Omega Anima" || itemComboBox.displayText === "Bow of Sigurd" || itemComboBox.displayText === "Wilhelm"){
                        missionComboBox.model = [
                            { text: "Grani", enabled: false },
                            { text: "Lvl 100 Grani", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Baal Anima" || itemComboBox.displayText === "Baal Omega Anima" || itemComboBox.displayText === "Solomon's Axe" || itemComboBox.displayText === "Spymur's Vision"){
                        missionComboBox.model = [
                            { text: "Baal", enabled: false },
                            { text: "Lvl 100 Baal", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Garuda Anima" || itemComboBox.displayText === "Garuda Omega Anima" || itemComboBox.displayText === "Plume of Suparna" || itemComboBox.displayText === "Indra's Edge"){
                        missionComboBox.model = [
                            { text: "Garuda", enabled: false },
                            { text: "Lvl 100 Garuda", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Odin Anima" || itemComboBox.displayText === "Odin Omega Anima" || itemComboBox.displayText === "Gungnir" || itemComboBox.displayText === "Sleipnir Shoe"){
                        missionComboBox.model = [
                            { text: "Odin", enabled: false },
                            { text: "Lvl 100 Odin", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Lich Anima" || itemComboBox.displayText === "Lich Omega Anima" || itemComboBox.displayText === "Obscuritas" || itemComboBox.displayText === "Phantasmas"){
                        missionComboBox.model = [
                            { text: "Lich", enabled: false },
                            { text: "Lvl 100 Lich", map: "", enabled: true },
                        ]
                    } 
                    
                    // Epic Weapons
                    else if(itemComboBox.displayText === "Prometheus Anima" || itemComboBox.displayText === "Fire of Prometheus" || itemComboBox.displayText === "Chains of Caucasus"){
                        missionComboBox.model = [
                            { text: "Prometheus", enabled: false },
                            { text: "Lvl 120 Prometheus", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Ca Ong Anima" || itemComboBox.displayText === "Keeper of Hallowed Ground" || itemComboBox.displayText === "Savior of Hallowed Ground"){
                        missionComboBox.model = [
                            { text: "Ca Ong", enabled: false },
                            { text: "Lvl 120 Ca Ong", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Gilgamesh Anima" || itemComboBox.displayText === "All-Might Spear" || itemComboBox.displayText === "All-Might Battle-Axe"){
                        missionComboBox.model = [
                            { text: "Gilgamesh", enabled: false },
                            { text: "Lvl 120 Gilgamesh", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Morrigna Anima" || itemComboBox.displayText === "Le Fay" || itemComboBox.displayText === "Unius"){
                        missionComboBox.model = [
                            { text: "Morrigna", enabled: false },
                            { text: "Lvl 120 Morrigna", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Hector Anima" || itemComboBox.displayText === "Bow of Iliad" || itemComboBox.displayText === "Adamantine Gauntlet"){
                        missionComboBox.model = [
                            { text: "Hector", enabled: false },
                            { text: "Lvl 120 Hector", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Anubis Anima" || itemComboBox.displayText === "Hermanubis" || itemComboBox.displayText === "Scales of Dominion"){
                        missionComboBox.model = [
                            { text: "Anubis", enabled: false },
                            { text: "Lvl 120 Anubis", map: "", enabled: true },
                        ]
                    }

                    // Malice Weapons
                    else if(itemComboBox.displayText === "Tiamat Malice Anima" || itemComboBox.displayText === "Hatsoiiłhał" || itemComboBox.displayText === "Majestas"){
                        missionComboBox.model = [
                            { text: "Tiamat Malice", enabled: false },
                            { text: "Lvl 150 Tiamat Malice", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Leviathan Malice Anima" || itemComboBox.displayText === "Kaladanda" || itemComboBox.displayText === "Kris of Hypnos"){
                        missionComboBox.model = [
                            { text: "Leviathan Malice", enabled: false },
                            { text: "Lvl 150 Leviathan Malice", map: "", enabled: true },
                        ]
                    } else if(itemComboBox.displayText === "Phronesis Anima" || itemComboBox.displayText === "Dark Thrasher" || itemComboBox.displayText === "Master Bamboo Sword"){
                        missionComboBox.model = [
                            { text: "Phronesis", enabled: false },
                            { text: "Lvl 150 Phronesis", map: "", enabled: true },
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
                } else if(farmingModeComboBox.displayText === "Coop"){
                    backend.update_mission_name(missionComboBox.model[currentIndex].text, missionComboBox.model[currentIndex].map)
                } else if(farmingModeComboBox.displayText === "Raid"){
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

            currentIndex: -1
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

                if(farmingModeComboBox.displayText === qsTr("Coop")){
                    // Send a blank Summon name to bypass enabling the Select Summon button as hosting Coop solo does not have any selectable Summons.
                    backend.update_summon_name("", "")
                } else {
                    summonButton.enabled = true
                }
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
                    if(farmingModeComboBox.displayText !== qsTr("Coop")){
                        // Only enable the Summon Button if the current farming mode is not Coop.
                        summonButton.enabled = true
                        summonSelectionLabel.visible = true
                    }
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
            if(farmingModeComboBox.displayText !== qsTr("Coop")){
                summonSelectionLabel.text = qsTr("Summon selected successfully")
                summonSelectionLabel.color = "#00ff00"
            }
            
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
