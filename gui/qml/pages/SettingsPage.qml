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

        ComboBox {
            id: comboBox

            x: 80
            y: 89
            width: 200
            anchors.horizontalCenterOffset: 0

            anchors.horizontalCenter: parent.horizontalCenter
            displayText: qsTr("Please select a item to farm.")

            currentIndex: 0

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

            textRole: "text"

            onCurrentIndexChanged: {
                comboBox.displayText = qsTr(comboBox.model[currentIndex].text)
                console.log("Map selected", comboBox.model[currentIndex].map)
            }

            delegate: ItemDelegate {
                width: comboBox.width
                text: modelData.text

                font.weight: comboBox.currentIndex === index ? Font.DemiBold : Font.Normal
                highlighted: ListView.isCurrentItem

                enabled: modelData.enabled
            }

            onPressedChanged: {
                comboBox.popup.height = 300
            }
        }

        CustomButton{
            id: buttonOpenFile

            text: qsTr("Open Script")
            anchors.left: textField.right
            anchors.leftMargin: 16

            y: 29
            width: 95
            height: 28

            onPressed: {
                fileOpen.open()
            }

            FileDialog{
                id: fileOpen

                title: "Please choose a combat script file"

                folder: shortcuts.home
                selectMultiple: false
                nameFilters: ["Text File (*.txt)"]

                onAccepted: {
                    backend.openFile(fileOpen.fileUrl)
                }
            }

        }

        CheckBox {
            id: checkBox

            text: qsTr("Check Box")

            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.rightMargin: 273
            anchors.leftMargin: 273
            anchors.bottomMargin: 284
            anchors.topMargin: 156
        }

        TextField {
            id: textField
            y: 23
            anchors.left: parent.left
            anchors.leftMargin: 121

            readOnly: true

            placeholderText: qsTr("No combat script selected.")
        }
    }

    Connections{
        target: backend
    }
}

/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:1.25;height:480;width:640}D{i:4}D{i:6}D{i:7}
}
##^##*/
