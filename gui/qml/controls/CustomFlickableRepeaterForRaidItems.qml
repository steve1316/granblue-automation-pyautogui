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

        // Items for Lvl 50 Tiamat Omega / Lvl 100 Tiamat Omega Ayr
        ListModel {
            id: raidItemsModel_TiamatOmega

            Component.onCompleted: {
                var listOfItems = ["Tiamat Omega", "Tiamat Anima", "Tiamat Omega Anima", "Tiamat Amood Omega", "Tiamat Bolt Omega", "Tiamat Gauntlet Omega", "Tiamat Glaive Omega"]

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

        // Items for Lvl 70 Colossus Omega / Lvl 100 Colossus Omega
        ListModel {
            id: raidItemsModel_ColossusOmega

            Component.onCompleted: {
                var listOfItems = ["Colossus Omega", "Colossus Anima", "Colossus Omega Anima", "Colossus Blade Omega", "Colossus Cane Omega", "Colossus Carbine Omega", "Colossus Fist Omega"]

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

        // Items for Lvl 60 Leviathan Omega / Lvl 100 Leviathan Omega
        ListModel {
            id: raidItemsModel_LeviathanOmega

            Component.onCompleted: {
                var listOfItems = ["Leviathan Omega", "Leviathan Anima", "Leviathan Omega Anima", "Leviathan Bow Omega", "Leviathan Gaze Omega", "Leviathan Scepter Omega", "Leviathan Spear Omega"]

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

        // Items for Lvl 60 Yggdrasil Omega / Lvl 100 Yggdrasil Omega
        ListModel {
            id: raidItemsModel_YggdrasilOmega

            Component.onCompleted: {
                var listOfItems = ["Yggdrasil Omega", "Yggdrasil Anima", "Yggdrasil Omega Anima", "Yggdrasil Bow Omega", "Yggdrasil Crystal Blade Omega", "Yggdrasil Dagger Omega", "Yggdrasil Dewbranch Omega"]

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

        // Items for Lvl 75 Luminiera Omega / Lvl 100 Luminiera Omega
        ListModel {
            id: raidItemsModel_LuminieraOmega

            Component.onCompleted: {
                var listOfItems = ["Luminiera Omega", "Luminiera Anima", "Luminiera Omega Anima", "Luminiera Bhuj Omega", "Luminiera Bolt Omega", "Luminiera Harp Omega", "Luminiera Sword Omega"]

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

        // Items for Lvl 75 Celeste Omega / Lvl 100 Celeste Omega
        ListModel {
            id: raidItemsModel_CelesteOmega

            Component.onCompleted: {
                var listOfItems = ["Celeste Omega", "Celeste Anima", "Celeste Omega Anima", "Celeste Harp Omega", "Celeste Claw Omega", "Celeste Horn Omega", "Celeste Zaghnal Omega"]

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

        // Items for Lvl 120 Shiva
        ListModel {
            id: raidItemsModel_Shiva

            Component.onCompleted: {
                var listOfItems = ["Shiva Anima", "Shiva Omega Anima", "Hand of Brahman", "Scimitar of Brahman", "Trident of Brahman", "Nilakantha"]

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

        // Items for Lvl 120 Europa
        ListModel {
            id: raidItemsModel_Europa

            Component.onCompleted: {
                var listOfItems = ["Europa Anima", "Europa Omega Anima", "Tyros Bow", "Tyros Scepter", "Tyros Zither", "Spirit of Mana"]

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

        // Items for Lvl 120 Godsworn Alexiel
        ListModel {
            id: raidItemsModel_Alexiel

            Component.onCompleted: {
                var listOfItems = ["Alexiel Anima", "Alexiel Omega Anima", "Nibelung Horn", "Nibelung Klinge", "Nibelung Messer", "Godsworn Edge"]

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

        // Items for Lvl 120 Grimnir
        ListModel {
            id: raidItemsModel_Grimnir

            Component.onCompleted: {
                var listOfItems = ["Grimnir Anima", "Grimnir Omega Anima", "Last Storm Blade", "Last Storm Harp", "Last Storm Lance", "Coruscant Crozier"]

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

        // Items for Lvl 120 Metatron
        ListModel {
            id: raidItemsModel_Metatron

            Component.onCompleted: {
                var listOfItems = ["Metatron Anima", "Metatron Omega Anima", "Mittron's Treasured Blade", "Mittron's Gauntlet", "Mittron's Bow", "Pillar of Flame"]

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

        // Items for Lvl 120 Avatar
        ListModel {
            id: raidItemsModel_Avatar

            Component.onCompleted: {
                var listOfItems = ["Avatar Anima", "Avatar Omega Anima", "Abyss Striker", "Abyss Spine", "Abyss Gaze", "Zechariah"]

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

        // Items for Lvl 100 Twin Elements / Lvl 120 Twin Elements
        ListModel {
            id: raidItemsModel_TwinElements

            Component.onCompleted: {
                var listOfItems = ["Twin Elements Anima", "Twin Elements Omega Anima", "Ancient Ecke Sachs", "Ecke Sachs"]

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

        // Items for Lvl 100 Macula Marius / Lvl 120 Macula Marius
        ListModel {
            id: raidItemsModel_MaculaMarius

            Component.onCompleted: {
                var listOfItems = ["Macula Marius Anima", "Macula Marius Omega Anima", "Ancient Auberon", "Auberon"]

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

        // Items for Lvl 100 Medusa / Lvl 120 Medusa
        ListModel {
            id: raidItemsModel_Medusa

            Component.onCompleted: {
                var listOfItems = ["Medusa Anima", "Medusa Omega Anima", "Ancient Perseus", "Perseus"]

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

        // Items for Lvl 100 Nezha / Lvl 120 Nezha
        ListModel {
            id: raidItemsModel_Nezha

            Component.onCompleted: {
                var listOfItems = ["Nezha Anima", "Nezha Omega Anima", "Ancient Nalakuvara", "Nalakuvara"]

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

        // Items for Lvl 100 Apollo / Lvl 120 Apollo
        ListModel {
            id: raidItemsModel_Apollo

            Component.onCompleted: {
                var listOfItems = ["Apollo Anima", "Apollo Omega Anima", "Ancient Bow of Artemis", "Bow of Artemis"]

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

        // Items for Lvl 100 Dark Angel Olivia / Lvl 120 Dark Angel Olivia
        ListModel {
            id: raidItemsModel_DarkAngelOlivia

            Component.onCompleted: {
                var listOfItems = ["Dark Angel Olivia Anima", "Dark Angel Olivia Omega Anima", "Ancient Cortana", "Cortana"]

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

        // Items for Lvl 100 Athena
        ListModel {
            id: raidItemsModel_Athena

            Component.onCompleted: {
                var listOfItems = ["Athena Anima", "Athena Omega Anima", "Erichthonius", "Sword of Pallas"]

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
        
        // Items for Lvl 100 Grani
        ListModel {
            id: raidItemsModel_Grani

            Component.onCompleted: {
                var listOfItems = ["Grani Anima", "Grani Omega Anima", "Bow of Sigurd", "Wilhelm"]

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

        // Items for Lvl 100 Baal
        ListModel {
            id: raidItemsModel_Baal

            Component.onCompleted: {
                var listOfItems = ["Baal Anima", "Baal Omega Anima", "Solomon's Axe", "Spymur's Vision"]

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

        // Items for Lvl 100 Garuda
        ListModel {
            id: raidItemsModel_Garuda

            Component.onCompleted: {
                var listOfItems = ["Garuda Anima", "Garuda Omega Anima", "Plume of Suparna", "Indra's Edge"]

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
        
        // Items for Lvl 100 Odin
        ListModel {
            id: raidItemsModel_Odin

            Component.onCompleted: {
                var listOfItems = ["Odin Anima", "Odin Omega Anima", "Gungnir", "Sleipnir Shoe"]

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

        // Items for Lvl 100 Lich
        ListModel {
            id: raidItemsModel_Lich

            Component.onCompleted: {
                var listOfItems = ["Lich Anima", "Lich Omega Anima", "Obscuritas", "Phantasmas"]

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

        // Items for Lvl 120 Prometheus
        ListModel {
            id: raidItemsModel_Prometheus

            Component.onCompleted: {
                var listOfItems = ["Prometheus Anima", "Fire of Prometheus", "Chains of Caucasus"]

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

        // Items for Lvl 120 Ca Ong
        ListModel {
            id: raidItemsModel_CaOng

            Component.onCompleted: {
                var listOfItems = ["Ca Ong Anima", "Keeper of Hallowed Ground", "Savior of Hallowed Ground"]

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

        // Items for Lvl 120 Gilgamesh
        ListModel {
            id: raidItemsModel_Gilgamesh

            Component.onCompleted: {
                var listOfItems = ["Gilgamesh Anima", "All-Might Spear", "All-Might Battle-Axe"]

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

        // Items for Lvl 120 Morrigna
        ListModel {
            id: raidItemsModel_Morrigna

            Component.onCompleted: {
                var listOfItems = ["Morrigna Anima", "Le Fay", "Unius"]

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

        // Items for Lvl 120 Hector
        ListModel {
            id: raidItemsModel_Hector

            Component.onCompleted: {
                var listOfItems = ["Hector Anima", "Bow of Iliad", "Adamantine Gauntlet"]

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

        // Items for Lvl 120 Anubis
        ListModel {
            id: raidItemsModel_Anubis

            Component.onCompleted: {
                var listOfItems = ["Anubis Anima", "Hermanubis", "Scales of Dominion"]

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

        // Items for Lvl 150 Tiamat Malice
        ListModel {
            id: raidItemsModel_TiamatMalice

            Component.onCompleted: {
                var listOfItems = ["Tiamat Malice Anima", "Hatsoiiłhał", "Majestas"]

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

        // Items for Lvl 150 Leviathan Malice
        ListModel {
            id: raidItemsModel_LeviathanMalice

            Component.onCompleted: {
                var listOfItems = ["Leviathan Malice Anima", "Kaladanda", "Kris of Hypnos"]

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

        // Items for Lvl 150 Phronesis
        ListModel {
            id: raidItemsModel_Phronesis

            Component.onCompleted: {
                var listOfItems = ["Phronesis Anima", "Dark Thrasher", "Master Bamboo Sword"]

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

        ///////// Raid Items - Tiamat Omega /////////
        Label {
            color: "#00ff00"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Tiamat Omega"
        }

        Repeater {
            model: raidItemsModel_TiamatOmega
            Image {
                id: itemImage_TiamatOmega

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#00ff00"
                    anchors.left: itemImage_TiamatOmega.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Tiamat Omega /////////

        ///////// Raid Items - Colossus Omega /////////
        Label {
            color: "#aa0000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Colossus Omega"
        }

        Repeater {
            model: raidItemsModel_ColossusOmega
            Image {
                id: itemImage_ColossusOmega

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#aa0000"
                    anchors.left: itemImage_ColossusOmega.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Colossus Omega /////////

        ///////// Raid Items - Leviathan Omega /////////
        Label {
            color: "#00ffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Leviathan Omega"
        }

        Repeater {
            model: raidItemsModel_LeviathanOmega
            Image {
                id: itemImage_LeviathanOmega

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#00ffff"
                    anchors.left: itemImage_LeviathanOmega.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Leviathan Omega /////////

        ///////// Raid Items - Yggdrasil Omega /////////
        Label {
            color: "#ff8000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Yggdrasil Omega"
        }

        Repeater {
            model: raidItemsModel_YggdrasilOmega
            Image {
                id: itemImage_YggdrasilOmega

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#ff8000"
                    anchors.left: itemImage_YggdrasilOmega.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Yggdrasil Omega /////////

        ///////// Raid Items - Luminiera Omega /////////
        Label {
            color: "#ffff00"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Luminiera Omega"
        }

        Repeater {
            model: raidItemsModel_LuminieraOmega
            Image {
                id: itemImage_LuminieraOmega

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#ffff00"
                    anchors.left: itemImage_LuminieraOmega.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Luminiera Omega /////////

        ///////// Raid Items - Celeste Omega /////////
        Label {
            color: "#aa00ff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Celeste Omega"
        }

        Repeater {
            model: raidItemsModel_CelesteOmega
            Image {
                id: itemImage_CelesteOmega

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#aa00ff"
                    anchors.left: itemImage_CelesteOmega.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Celeste Omega /////////

        ///////// Raid Items - Shiva /////////
        Label {
            color: "#aa0000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Shiva"
        }

        Repeater {
            model: raidItemsModel_Shiva
            Image {
                id: itemImage_Shiva

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#aa0000"
                    anchors.left: itemImage_Shiva.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Shiva /////////

        ///////// Raid Items - Europa /////////
        Label {
            color: "#00ffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Europa"
        }

        Repeater {
            model: raidItemsModel_Europa
            Image {
                id: itemImage_Europa

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#00ffff"
                    anchors.left: itemImage_Europa.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Europa /////////

        ///////// Raid Items - Godsworn Alexiel /////////
        Label {
            color: "#ff8000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Godsworn Alexiel"
        }

        Repeater {
            model: raidItemsModel_Alexiel
            Image {
                id: itemImage_Alexiel

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#ff8000"
                    anchors.left: itemImage_Alexiel.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Godsworn Alexiel /////////

        ///////// Raid Items - Grimnir /////////
        Label {
            color: "#00ff00"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Grimnir"
        }

        Repeater {
            model: raidItemsModel_Grimnir
            Image {
                id: itemImage_Grimnir

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#00ff00"
                    anchors.left: itemImage_Grimnir.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Grimnir /////////

        ///////// Raid Items - Metatron /////////
        Label {
            color: "#ffff00"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Metatron"
        }

        Repeater {
            model: raidItemsModel_Metatron
            Image {
                id: itemImage_Metatron

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#ffff00"
                    anchors.left: itemImage_Metatron.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Metatron /////////

        ///////// Raid Items - Avatar /////////
        Label {
            color: "#aa00ff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Avatar"
        }

        Repeater {
            model: raidItemsModel_Avatar
            Image {
                id: itemImage_Avatar

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#aa00ff"
                    anchors.left: itemImage_Avatar.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Avatar /////////

        ///////// Raid Items - Twin Elements /////////
        Label {
            color: "#aa0000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Twin Elements"
        }

        Repeater {
            model: raidItemsModel_TwinElements
            Image {
                id: itemImage_TwinElements

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#aa0000"
                    anchors.left: itemImage_TwinElements.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Twin Elements /////////

        ///////// Raid Items - Macula Marius /////////
        Label {
            color: "#00ffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Macula Marius"
        }

        Repeater {
            model: raidItemsModel_MaculaMarius
            Image {
                id: itemImage_MaculaMarius

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#00ffff"
                    anchors.left: itemImage_MaculaMarius.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Macula Marius /////////

        ///////// Raid Items - Medusa /////////
        Label {
            color: "#ff8000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Medusa"
        }

        Repeater {
            model: raidItemsModel_Medusa
            Image {
                id: itemImage_Medusa

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#ff8000"
                    anchors.left: itemImage_Medusa.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Medusa /////////

        ///////// Raid Items - Nezha /////////
        Label {
            color: "#00ff00"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Nezha"
        }

        Repeater {
            model: raidItemsModel_Nezha
            Image {
                id: itemImage_Nezha

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#00ff00"
                    anchors.left: itemImage_Nezha.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Nezha /////////

        ///////// Raid Items - Apollo /////////
        Label {
            color: "#ffff00"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Apollo"
        }

        Repeater {
            model: raidItemsModel_Apollo
            Image {
                id: itemImage_Apollo

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#ffff00"
                    anchors.left: itemImage_Apollo.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Apollo /////////

        ///////// Raid Items - Dark Angel Olivia /////////
        Label {
            color: "#aa00ff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Dark Angel Olivia"
        }

        Repeater {
            model: raidItemsModel_DarkAngelOlivia
            Image {
                id: itemImage_DarkAngelOlivia

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#aa00ff"
                    anchors.left: itemImage_DarkAngelOlivia.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Dark Angel Olivia /////////

        ///////// Raid Items - Athena /////////
        Label {
            color: "#aa0000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Athena"
        }

        Repeater {
            model: raidItemsModel_Athena
            Image {
                id: itemImage_Athena

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#aa0000"
                    anchors.left: itemImage_Athena.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Athena /////////

        ///////// Raid Items - Grani /////////
        Label {
            color: "#00ffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Grani"
        }

        Repeater {
            model: raidItemsModel_Grani
            Image {
                id: itemImage_Grani

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#00ffff"
                    anchors.left: itemImage_Grani.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Grani /////////

        ///////// Raid Items - Baal /////////
        Label {
            color: "#ff8000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Baal"
        }

        Repeater {
            model: raidItemsModel_Baal
            Image {
                id: itemImage_Baal

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#ff8000"
                    anchors.left: itemImage_Baal.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Baal /////////

        ///////// Raid Items - Garuda /////////
        Label {
            color: "#00ff00"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Garuda"
        }

        Repeater {
            model: raidItemsModel_Garuda
            Image {
                id: itemImage_Garuda

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#00ff00"
                    anchors.left: itemImage_Garuda.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Garuda /////////

        ///////// Raid Items - Odin /////////
        Label {
            color: "#ffff00"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Odin"
        }

        Repeater {
            model: raidItemsModel_Odin
            Image {
                id: itemImage_Odin

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#ffff00"
                    anchors.left: itemImage_Odin.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Odin /////////

        ///////// Raid Items - Lich /////////
        Label {
            color: "#aa00ff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Lich"
        }

        Repeater {
            model: raidItemsModel_Lich
            Image {
                id: itemImage_Lich

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#aa00ff"
                    anchors.left: itemImage_Lich.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Lich /////////

        ///////// Raid Items - Prometheus /////////
        Label {
            color: "#aa0000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Prometheus"
        }

        Repeater {
            model: raidItemsModel_Prometheus
            Image {
                id: itemImage_Prometheus

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#aa0000"
                    anchors.left: itemImage_Prometheus.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Prometheus /////////

        ///////// Raid Items - Ca Ong /////////
        Label {
            color: "#00ffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Ca Ong"
        }

        Repeater {
            model: raidItemsModel_CaOng
            Image {
                id: itemImage_CaOng

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#00ffff"
                    anchors.left: itemImage_CaOng.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Ca Ong /////////

        ///////// Raid Items - Gilgamesh /////////
        Label {
            color: "#ff8000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Gilgamesh"
        }

        Repeater {
            model: raidItemsModel_Gilgamesh
            Image {
                id: itemImage_Gilgamesh

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#ff8000"
                    anchors.left: itemImage_Gilgamesh.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Gilgamesh /////////

        ///////// Raid Items - Morrigna /////////
        Label {
            color: "#00ff00"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Morrigna"
        }

        Repeater {
            model: raidItemsModel_Morrigna
            Image {
                id: itemImage_Morrigna

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#00ff00"
                    anchors.left: itemImage_Morrigna.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Morrigna /////////

        ///////// Raid Items - Hector /////////
        Label {
            color: "#ffff00"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Hector"
        }

        Repeater {
            model: raidItemsModel_Hector
            Image {
                id: itemImage_Hector

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#ffff00"
                    anchors.left: itemImage_Hector.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Hector /////////

        ///////// Raid Items - Anubis /////////
        Label {
            color: "#aa00ff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Anubis"
        }

        Repeater {
            model: raidItemsModel_Anubis
            Image {
                id: itemImage_Anubis

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#aa00ff"
                    anchors.left: itemImage_Anubis.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Anubis /////////

        ///////// Raid Items - Tiamat Malice /////////
        Label {
            color: "#00ff00"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Tiamat Malice"
        }

        Repeater {
            model: raidItemsModel_TiamatMalice
            Image {
                id: itemImage_TiamatMalice

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#00ff00"
                    anchors.left: itemImage_TiamatMalice.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Tiamat Malice /////////

        ///////// Raid Items - Leviathan Malice /////////
        Label {
            color: "#00ffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Leviathan Malice"
        }

        Repeater {
            model: raidItemsModel_LeviathanMalice
            Image {
                id: itemImage_LeviathanMalice

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#00ffff"
                    anchors.left: itemImage_LeviathanMalice.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Leviathan Malice /////////

        ///////// Raid Items - Phronesis /////////
        Label {
            color: "#ff8000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Phronesis"
        }

        Repeater {
            model: raidItemsModel_Phronesis
            Image {
                id: itemImage_Phronesis

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
                Label {
                    color: "#ff8000"
                    anchors.left: itemImage_Phronesis.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Phronesis /////////

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
