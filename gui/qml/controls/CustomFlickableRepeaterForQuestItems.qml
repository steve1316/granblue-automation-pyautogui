import QtQuick 2.15
import QtQuick.Controls 2.15

Flickable {
    anchors.fill: parent
    contentHeight: column.height
    clip: true

    ScrollBar.vertical: ScrollBar {}

    Column {
        id: column

        spacing: 15

        // Adjust the vertical scroll bar when using the mouse wheel.
        MouseArea{
            onWheel: {
                if(wheel.angleDelta.y > 0){
                    verticalScrollBar.decrease()
                }
                else if(wheel.angleDelta.y < 0){
                    verticalScrollBar.increase()
                }
            }
        }

        // Items for Port Breeze Archipelago.
        ListModel {
            id: questItemsModel_PortBreezeArchipelago

            Component.onCompleted: {
                var listOfItems = ["Satin Feather", "Zephyr Feather", "Flying Sprout"]

                for(var i = 0; i < listOfItems.length; i++){
                    append(createListElement(listOfItems[i]))
                }
            }

            function createListElement(itemName){
                var filePath = "../../../images/items/%1.png".arg(itemName)
                return {
                    name: itemName,
                    imageSource: filePath
                }
            }
        }

        // Items for Valtz Duchy.
        ListModel {
            id: questItemsModel_ValtzDuchy
            
            Component.onCompleted: {
                var listOfItems = ["Fine Sand Bottle", "Untamed Flame", "Blistering Ore"]

                for(var i = 0; i < listOfItems.length; i++){
                    append(createListElement(listOfItems[i]))
                }
            }

            function createListElement(itemName){
                var filePath = "../../../images/items/%1.png".arg(itemName)
                return {
                    name: itemName,
                    imageSource: filePath
                }
            }
        }

        // Items for Auguste Isles
        ListModel {
            id: questItemsModel_AugusteIsles

            Component.onCompleted: {
                var listOfItems = ["Fresh Water Jug", "Soothing Splash", "Glowing Coral"]

                for(var i = 0; i < listOfItems.length; i++){
                    append(createListElement(listOfItems[i]))
                }
            }

            function createListElement(itemName){
                var filePath = "../../../images/items/%1.png".arg(itemName)
                return {
                    name: itemName,
                    imageSource: filePath
                }
            }
        }

        // Items for Lumacie Archipelago.
        ListModel {
            id: questItemsModel_LumacieArchipelago

            Component.onCompleted: {
                var listOfItems = ["Rough Stone", "Swirling Amber", "Coarse Alluvium"]

                for(var i = 0; i < listOfItems.length; i++){
                    append(createListElement(listOfItems[i]))
                }
            }

            function createListElement(itemName){
                var filePath = "../../../images/items/%1.png".arg(itemName)
                return {
                    name: itemName,
                    imageSource: filePath
                }
            }
        }

        // Items for Albion Citadel.
        ListModel {
            id: questItemsModel_AlbionCitadel

            Component.onCompleted: {
                var listOfItems = ["Falcon Feather", "Spring Water Jug", "Vermilion Stone"]

                for(var i = 0; i < listOfItems.length; i++){
                    append(createListElement(listOfItems[i]))
                }
            }

            function createListElement(itemName){
                var filePath = "../../../images/items/%1.png".arg(itemName)
                return {
                    name: itemName,
                    imageSource: filePath
                }
            }
        }

        // Items for Mist-Shrouded Isle
        ListModel {
            id: questItemsModel_MistShroudedIsle

            Component.onCompleted: {
                var listOfItems = ["Slimy Shroom", "Hollow Soul", "Lacrimosa"]

                for(var i = 0; i < listOfItems.length; i++){
                    append(createListElement(listOfItems[i]))
                }
            }

            function createListElement(itemName){
                var filePath = "../../../images/items/%1.png".arg(itemName)
                return {
                    name: itemName,
                    imageSource: filePath
                }
            }
        }

        // Items for Golonzo Island.
        ListModel {
            id: questItemsModel_GolonzoIsland

            Component.onCompleted: {
                var listOfItems = ["Wheat Stalk", "Iron Cluster", "Olea Plant"]

                for(var i = 0; i < listOfItems.length; i++){
                    append(createListElement(listOfItems[i]))
                }
            }

            function createListElement(itemName){
                var filePath = "../../../images/items/%1.png".arg(itemName)
                return {
                    name: itemName,
                    imageSource: filePath
                }
            }
        }

        // Items for Amalthea Island.
        ListModel {
            id: questItemsModel_AmaltheaIsland

            Component.onCompleted: {
                var listOfItems = ["Indigo Fruit", "Foreboding Clover", "Blood Amber"]

                for(var i = 0; i < listOfItems.length; i++){
                    append(createListElement(listOfItems[i]))
                }
            }

            function createListElement(itemName){
                var filePath = "../../../images/items/%1.png".arg(itemName)
                return {
                    name: itemName,
                    imageSource: filePath
                }
            }
        }

        // Items for Former Capital Mephorash.
        ListModel {
            id: questItemsModel_FormerCapitalMephorash

            Component.onCompleted: {
                var listOfItems = ["Sand Brick", "Native Reed", "Antique Cloth"]

                for(var i = 0; i < listOfItems.length; i++){
                    append(createListElement(listOfItems[i]))
                }
            }

            function createListElement(itemName){
                var filePath = "../../../images/items/%1.png".arg(itemName)
                return {
                    name: itemName,
                    imageSource: filePath
                }
            }
        }

        // Items for Agastia.
        ListModel {
            id: questItemsModel_Agastia

            Component.onCompleted: {
                var listOfItems = ["Prosperity Flame", "Explosive Material", "Steel Liquid"]

                for(var i = 0; i < listOfItems.length; i++){
                    append(createListElement(listOfItems[i]))
                }
            }

            function createListElement(itemName){
                var filePath = "../../../images/items/%1.png".arg(itemName)
                return {
                    name: itemName,
                    imageSource: filePath
                }
            }
        }

        // Items for Scarlet Trial.
        ListModel {
            id: specialItemsModel_ScarletTrial

            Component.onCompleted: {
                var listOfItems = ["Fire Orb", "Water Orb", "Earth Orb", "Wind Orb", "Light Orb", "Dark Orb", "Inferno Orb", "Frost Orb", 
                "Rumbling Orb", "Cyclone Orb", "Shining Orb", "Abysm Orb"]

                for(var i = 0; i < listOfItems.length; i++){
                    append(createListElement(listOfItems[i]))
                }
            }

            function createListElement(itemName){
                var filePath = "../../../images/items/%1.png".arg(itemName)
                return {
                    name: itemName,
                    imageSource: filePath
                }
            }
        }

        // Items for Cerulean Trial.
        ListModel {
            id: specialItemsModel_CeruleanTrial

            Component.onCompleted: {
                var listOfItems = ["Red Tome", "Blue Tome", "Brown Tome", "Green Tome", "White Tome", "Black Tome", "Hellfire Scroll", "Flood Scroll", 
                "Thunder Scroll", "Gale Scroll", "Skylight Scroll", "Chasm Scroll", "Infernal Whorl", "Tidal Whorl", "Seismic Whorl", "Tempest Whorl",
                "Radiant Whorl", "Umbral Whorl"]

                for(var i = 0; i < listOfItems.length; i++){
                    append(createListElement(listOfItems[i]))
                }
            }

            function createListElement(itemName){
                var filePath = "../../../images/items/%1.png".arg(itemName)
                return {
                    name: itemName,
                    imageSource: filePath
                }
            }
        }

        // Items for Violet Trial.
        ListModel {
            id: specialItemsModel_VioletTrial

            Component.onCompleted: {
                var listOfItems = ["Prism Chip", "Flawed Prism", "Flawless Prism", "Rainbow Prism"]

                for(var i = 0; i < listOfItems.length; i++){
                    append(createListElement(listOfItems[i]))
                }
            }

            function createListElement(itemName){
                var filePath = "../../../images/items/%1.png".arg(itemName)
                return {
                    name: itemName,
                    imageSource: filePath
                }
            }
        }

        // Items for Shiny Slime Search!
        ListModel {
            id: specialItemsModel_ShinySlimeSearch

            Component.onCompleted: {
                var listOfItems = ["EXP"]

                for(var i = 0; i < listOfItems.length; i++){
                    append(createListElement(listOfItems[i]))
                }
            }

            function createListElement(itemName){
                var filePath = "../../../images/items/%1.png".arg(itemName)
                return {
                    name: itemName,
                    imageSource: filePath
                }
            }
        }

        // Items for Six Dragon Trials.
        ListModel {
            id: specialItemsModel_SixDragonTrials

            Component.onCompleted: {
                var listOfItems = ["Red Dragon Scale", "Blue Dragon Scale", "Brown Dragon Scale", "Green Dragon Scale", "White Dragon Scale", "Black Dragon Scale"]

                for(var i = 0; i < listOfItems.length; i++){
                    append(createListElement(listOfItems[i]))
                }
            }

            function createListElement(itemName){
                var filePath = "../../../images/items/%1.png".arg(itemName)
                return {
                    name: itemName,
                    imageSource: filePath
                }
            }
        }

        // Items for Ifrit Showdown.
        ListModel {
            id: specialItemsModel_IfritShowdown

            Component.onCompleted: {
                var listOfItems = ["Jasper Scale", "Scorching Peak", "Infernal Garnet", "Ifrit Anima", "Ifrit Omega Anima"]

                for(var i = 0; i < listOfItems.length; i++){
                    append(createListElement(listOfItems[i]))
                }
            }

            function createListElement(itemName){
                var filePath = "../../../images/items/%1.png".arg(itemName)
                return {
                    name: itemName,
                    imageSource: filePath
                }
            }
        }

        // Items for Cocytus Showdown.
        ListModel {
            id: specialItemsModel_CocytusShowdown

            Component.onCompleted: {
                var listOfItems = ["Mourning Stone", "Crystal Spirit", "Frozen Hell Prism", "Cocytus Anima", "Cocytus Omega Anima"]

                for(var i = 0; i < listOfItems.length; i++){
                    append(createListElement(listOfItems[i]))
                }
            }

            function createListElement(itemName){
                var filePath = "../../../images/items/%1.png".arg(itemName)
                return {
                    name: itemName,
                    imageSource: filePath
                }
            }
        }

        // Items for Vohu Manah Showdown.
        ListModel {
            id: specialItemsModel_VohuManahShowdown

            Component.onCompleted: {
                var listOfItems = ["Scrutiny Stone", "Luminous Judgment", "Evil Judge Crystal", "Vohu Manah Anima", "Vohu Manah Omega Anima"]

                for(var i = 0; i < listOfItems.length; i++){
                    append(createListElement(listOfItems[i]))
                }
            }

            function createListElement(itemName){
                var filePath = "../../../images/items/%1.png".arg(itemName)
                return {
                    name: itemName,
                    imageSource: filePath
                }
            }
        }

        // Items for Sagittarius Showdown.
        ListModel {
            id: specialItemsModel_SagittariusShowdown

            Component.onCompleted: {
                var listOfItems = ["Sagittarius Arrowhead", "Sagittarius Rune", "Horseman's Plate", "Sagittarius Anima", "Sagittarius Omega Anima"]

                for(var i = 0; i < listOfItems.length; i++){
                    append(createListElement(listOfItems[i]))
                }
            }

            function createListElement(itemName){
                var filePath = "../../../images/items/%1.png".arg(itemName)
                return {
                    name: itemName,
                    imageSource: filePath
                }
            }
        }

        // Items for Corow Showdown.
        ListModel {
            id: specialItemsModel_CorowShowdown

            Component.onCompleted: {
                var listOfItems = ["Solar Ring", "Sunlight Quartz", "Halo Light Quartz", "Corow Anima", "Corow Omega Anima"]

                for(var i = 0; i < listOfItems.length; i++){
                    append(createListElement(listOfItems[i]))
                }
            }

            function createListElement(itemName){
                var filePath = "../../../images/items/%1.png".arg(itemName)
                return {
                    name: itemName,
                    imageSource: filePath
                }
            }
        }

        // Items for Diablo Showdown.
        ListModel {
            id: specialItemsModel_DiabloShowdown

            Component.onCompleted: {
                var listOfItems = ["Twilight Cloth Strip", "Shadow Silver", "Phantom Demon Jewel", "Diablo Anima", "Diablo Omega Anima"]

                for(var i = 0; i < listOfItems.length; i++){
                    append(createListElement(listOfItems[i]))
                }
            }

            function createListElement(itemName){
                var filePath = "../../../images/items/%1.png".arg(itemName)
                return {
                    name: itemName,
                    imageSource: filePath
                }
            }
        }

        // Items for Extreme Trials.
        ListModel {
            id: specialItemsModel_ExtremeTrials

            Component.onCompleted: {
                var listOfItems = ["Hellfire Fragment", "Deluge Fragment", "Wasteland Fragment", "Typhoon Fragment"]

                for(var i = 0; i < listOfItems.length; i++){
                    append(createListElement(listOfItems[i]))
                }
            }

            function createListElement(itemName){
                var filePath = "../../../images/items/%1.png".arg(itemName)
                return {
                    name: itemName,
                    imageSource: filePath
                }
            }
        }

        // Items for Angel Halo.
        ListModel {
            id: specialItemsModel_AngelHalo

            Component.onCompleted: {
                var listOfItems = ["Angel Halo Weapons"]

                for(var i = 0; i < listOfItems.length; i++){
                    append(createListElement(listOfItems[i]))
                }
            }

            function createListElement(itemName){
                var filePath = "../../../images/items/%1.png".arg(itemName)
                return {
                    name: itemName,
                    imageSource: filePath
                }
            }
        }

        ///////// Quest Items - Port Breeze Archipelago /////////
        Label {
            color: "#00ff00"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Port Breeze Archipelago"
        }

        Repeater {
            model: questItemsModel_PortBreezeArchipelago
            Image {
                id: itemImage_PortBreezeArchipelago

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        questItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#00ff00"
                    anchors.left: itemImage_PortBreezeArchipelago.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Quest Items - Port Breeze Archipelago /////////

        ///////// Quest Items - Valtz Duchy /////////
        Label {
            color: "#aa0000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Valtz Duchy"
        }

        Repeater {
            model: questItemsModel_ValtzDuchy
            Image {
                id: itemImage_ValtzDuchy

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        questItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#aa0000"
                    anchors.left: itemImage_ValtzDuchy.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Quest Items - Valtz Duchy /////////

        ///////// Quest Items - Auguste Isles /////////
        Label {
            color: "#00ffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Auguste Isles"
        }

        Repeater {
            model: questItemsModel_AugusteIsles
            Image {
                id: itemImage_AugusteIsles

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        questItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#00ffff"
                    anchors.left: itemImage_AugusteIsles.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Quest Items - Auguste Isles /////////

        ///////// Quest Items - Lumacie Archipelago /////////
        Label {
            color: "#ff8000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Lumacie Archipelago"
        }

        Repeater {
            model: questItemsModel_LumacieArchipelago
            Image {
                id: itemImage_LumacieArchipelago

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        questItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#ff8000"
                    anchors.left: itemImage_LumacieArchipelago.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Quest Items - Lumacie Archipelago /////////

        ///////// Quest Items - Albion Citadel /////////
        Label {
            color: "#ffff00"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Albion Citadel"
        }

        Repeater {
            model: questItemsModel_AlbionCitadel
            Image {
                id: itemImage_AlbionCitadel

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        questItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#ffff00"
                    anchors.left: itemImage_AlbionCitadel.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Quest Items - Albion Citadel /////////

        ///////// Quest Items - Mist-Shrouded Isle /////////
        Label {
            color: "#aa00ff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Mist-Shrouded Isle"
        }

        Repeater {
            model: questItemsModel_MistShroudedIsle
            Image {
                id: itemImage_MistShroudedIsle

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        questItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#aa00ff"
                    anchors.left: itemImage_MistShroudedIsle.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Quest Items - Mist-Shrouded Isle /////////

        ///////// Quest Items - Golonzo Island /////////
        Label {
            color: "#aa0000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Golonzo Island"
        }

        Repeater {
            model: questItemsModel_GolonzoIsland
            Image {
                id: itemImage_GolonzoIsland

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        questItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#aa0000"
                    anchors.left: itemImage_GolonzoIsland.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Quest Items - Golonzo Island /////////

        ///////// Quest Items - Amalthea Island /////////
        Label {
            color: "#00ff00"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Amalthea Island"
        }

        Repeater {
            model: questItemsModel_AmaltheaIsland
            Image {
                id: itemImage_AmaltheaIsland

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        questItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#00ff00"
                    anchors.left: itemImage_AmaltheaIsland.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Quest Items - Amalthea Island /////////

        ///////// Quest Items - Former Capital Mephorash /////////
        Label {
            color: "#ff8000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Former Capital Mephorash"
        }

        Repeater {
            model: questItemsModel_FormerCapitalMephorash
            Image {
                id: itemImage_FormerCapitalMephorash

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        questItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#ff8000"
                    anchors.left: itemImage_FormerCapitalMephorash.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Quest Items - Former Capital Mephorash /////////

        ///////// Quest Items - Agastia /////////
        Label {
            color: "#00ffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Agastia"
        }

        Repeater {
            model: questItemsModel_Agastia
            Image {
                id: itemImage_Agastia

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        questItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#00ffff"
                    anchors.left: itemImage_Agastia.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Quest Items - Agastia /////////

    }

    Connections {
        target: backend
    }
}

/*##^##
Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
##^##*/
