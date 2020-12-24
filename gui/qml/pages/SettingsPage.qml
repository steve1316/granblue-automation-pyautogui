import QtQuick 2.15
import QtQuick.Controls 2.15

Item{
    Rectangle {
        id: settingsContainer

        color: "#323741"
        anchors.fill: parent

        ComboBox {
            id: comboBox

            x: 80
            y: 32
            width: 200

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

        Label {
            id: settingsPageLabel

            x: 305
            y: 176

            color: "#ffffff"

            text: qsTr("Settings Screen")
            font.pointSize: 16

            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }
}

/*##^##
Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
##^##*/
