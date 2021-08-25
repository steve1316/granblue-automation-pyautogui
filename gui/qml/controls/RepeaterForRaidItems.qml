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

        // List model that holds all the Raid items that are supported.
        ListModel {
            id: itemsModel

            property var listOfItems: {
                "Tiamat Omega": ["Tiamat Omega", "Tiamat Anima", "Tiamat Omega Anima", "Tiamat Amood Omega", "Tiamat Bolt Omega", "Tiamat Gauntlet Omega", "Tiamat Glaive Omega"],
                "Colossus Omega": ["Colossus Omega", "Colossus Anima", "Colossus Omega Anima", "Colossus Blade Omega", "Colossus Cane Omega", "Colossus Carbine Omega", "Colossus Fist Omega"],
                "Leviathan Omega": ["Leviathan Omega", "Leviathan Anima", "Leviathan Omega Anima", "Leviathan Bow Omega", "Leviathan Gaze Omega", "Leviathan Scepter Omega", "Leviathan Spear Omega"],
                "Yggdrasil Omega": ["Yggdrasil Omega", "Yggdrasil Anima", "Yggdrasil Omega Anima", "Yggdrasil Bow Omega", "Yggdrasil Crystal Blade Omega", "Yggdrasil Dagger Omega", "Yggdrasil Dewbranch Omega"],
                "Luminiera Omega": ["Luminiera Omega", "Luminiera Anima", "Luminiera Omega Anima", "Luminiera Bhuj Omega", "Luminiera Bolt Omega", "Luminiera Harp Omega", "Luminiera Sword Omega"],
                "Celeste Omega": ["Celeste Omega", "Celeste Anima", "Celeste Omega Anima", "Celeste Harp Omega", "Celeste Claw Omega", "Celeste Horn Omega", "Celeste Zaghnal Omega"],
                "Shiva": ["Shiva Anima", "Shiva Omega Anima", "Hand of Brahman", "Scimitar of Brahman", "Trident of Brahman", "Nilakantha"],
                "Europa": ["Europa Anima", "Europa Omega Anima", "Tyros Bow", "Tyros Scepter", "Tyros Zither", "Spirit of Mana"],
                "Godsworn Alexiel": ["Alexiel Anima", "Alexiel Omega Anima", "Nibelung Horn", "Nibelung Klinge", "Nibelung Messer", "Godsworn Edge"],
                "Grimnir": ["Grimnir Anima", "Grimnir Omega Anima", "Last Storm Blade", "Last Storm Harp", "Last Storm Lance", "Coruscant Crozier"],
                "Metatron": ["Metatron Anima", "Metatron Omega Anima", "Mittron's Treasured Blade", "Mittron's Gauntlet", "Mittron's Bow", "Pillar of Flame"],
                "Avatar": ["Avatar Anima", "Avatar Omega Anima", "Abyss Striker", "Abyss Spine", "Abyss Gaze", "Zechariah"],
                "Twin Elements": ["Twin Elements Anima", "Twin Elements Omega Anima", "Ancient Ecke Sachs", "Ecke Sachs"],
                "Macula Marius": ["Macula Marius Anima", "Macula Marius Omega Anima", "Ancient Auberon", "Auberon"],
                "Medusa": ["Medusa Anima", "Medusa Omega Anima", "Ancient Perseus", "Perseus"],
                "Nezha": ["Nezha Anima", "Nezha Omega Anima", "Ancient Nalakuvara", "Nalakuvara"],
                "Apollo": ["Apollo Anima", "Apollo Omega Anima", "Ancient Bow of Artemis", "Bow of Artemis"],
                "Dark Angel Olivia": ["Dark Angel Olivia Anima", "Dark Angel Olivia Omega Anima", "Ancient Cortana", "Cortana"],
                "Athena": ["Athena Anima", "Athena Omega Anima", "Erichthonius", "Sword of Pallas"],
                "Grani": ["Grani Anima", "Grani Omega Anima", "Bow of Sigurd", "Wilhelm"],
                "Baal": ["Baal Anima", "Baal Omega Anima", "Solomon's Axe", "Spymur's Vision"],
                "Garuda": ["Garuda Anima", "Garuda Omega Anima", "Plume of Suparna", "Indra's Edge"],
                "Odin": ["Odin Anima", "Odin Omega Anima", "Gungnir", "Sleipnir Shoe"],
                "Lich": ["Lich Anima", "Lich Omega Anima", "Obscuritas", "Phantasmas"],
                "Prometheus": ["Prometheus Anima", "Fire of Prometheus", "Chains of Caucasus"],
                "Ca Ong": ["Ca Ong Anima", "Keeper of Hallowed Ground", "Savior of Hallowed Ground"],
                "Gilgamesh": ["Gilgamesh Anima", "All-Might Spear", "All-Might Battle-Axe"],
                "Morrigna": ["Morrigna Anima", "Le Fay", "Unius"],
                "Hector": ["Hector Anima", "Bow of Iliad", "Adamantine Gauntlet"],
                "Anubis": ["Anubis Anima", "Hermanubis", "Scales of Dominion"],
                "Tiamat Malice": ["Tiamat Malice Anima", "Hatsoiiłhał", "Majestas"],
                "Leviathan Malice": ["Leviathan Malice Anima", "Kaladanda", "Kris of Hypnos"],
                "Phronesis": ["Phronesis Anima", "Dark Thrasher", "Master Bamboo Sword"],
                "Luminiera Malice": ["Luminiera Malice Anima", "Colomba", "Seyfert"],
                "Anima-Animus Core": ["Hive God Anima", "Agonize", "Faceless"],
                "Grand Order": ["Azure Feather", "Heavenly Horn", "Verdant Azurite"],
                "Proto Bahamut": ["Horn of Bahamut", "Champion Merit", "Primeval Horn"],
                "Rose Queen": ["Rose Petal"],
                "Michael": ["Michael Anima"],
                "Gabriel": ["Gabriel Anima"],
                "Uriel": ["Uriel Anima"],
                "Raphael": ["Raphael Anima"],
                "Four Primarchs": ["Fire Halo", "Water Halo", "Earth Halo", "Wind Halo"],
                "Wilnas": ["Wilnas's Finger"],
                "Wamdus": ["Wamdus's Cnidocyte"],
                "Galleon": ["Galleon's Jaw"],
                "Ewiyar": ["Ewiyar's Beak"],
                "Lu Woh": ["Lu Woh's Horn"],
                "Fediel": ["Fediel's Spine"],
                "Xeno Ifrit": ["True Xeno Ifrit Anima", "Infernal Vajra"],
                "Xeno Cocytus": ["True Xeno Cocytus Anima", "Frozen Hellplume"],
                "Xeno Vohu Manah": ["True Xeno Vohu Manah Anima", "Sacrosanct Sutra"],
                "Xeno Sagittarius": ["True Xeno Sagittarius Anima", "Zodiac Arc"],
                "Xeno Corow": ["True Xeno Corow Anima", "Flame Fanner"],
                "Xeno Diablo": ["True Xeno Diablo Anima", "Wraithbind Fetter"],
                "Akasha": ["Hollow Key"],
                "Lucilius": ["Dark Residue", "Shadow Substance"],
                "Ultimate Bahamut": ["Michael Anima", "Gabriel Anima", "Uriel Anima", "Raphael Anima", "Meteorite Fragment", "Meteorite", "Silver Centrum", "Ultima Unit", "Athena Anima", "Athena Omega Anima", "Grani Anima", "Grani Omega Anima", "Baal Anima", "Baal Omega Anima", "Garuda Anima", "Garuda Omega Anima", "Odin Anima", "Odin Omega Anima", "Lich Anima", "Lich Omega Anima"],
                "Lindwurm": ["Golden Scale", "Lineage Fragment"],
                "Huanglong and Qilin": ["Huanglong Anima", "Qilin Anima", "Golden Talisman", "Obsidian Talisman"],
                "Shenxian": ["Shenxian Badge"],
                "Agni": ["Zhuque Badge"],
                "Neptune": ["Xuanwu Badge"],
                "Titan": ["Baihu Badge"],
                "Zephyrus": ["Qinglong Badge"]
            }

            function createListElement(itemName){
                var filePath = "../../../images/items/%1.png".arg(itemName)
                return {
                    name: itemName,
                    imageSource: filePath
                }
            }
        }

        Rectangle {
            width: parent.width
            height: 3
            color: "black"
        }
        Label {
            color: "black"
            font.bold: true
            font.pointSize: 18
            text: "Omega I Raids"
        }
        Rectangle {
            width: parent.width
            height: 3
            color: "black"
        }

        ///////// Raid Items - Tiamat Omega /////////
        Label {
            id: label_TiamatOmega

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
            id: repeater_TiamatOmega
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_TiamatOmega.visible === true){
                    repeater_TiamatOmega.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_TiamatOmega.text].length; i++){
                        repeater_TiamatOmega.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_TiamatOmega.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_TiamatOmega
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_ColossusOmega

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
            id: repeater_ColossusOmega
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_ColossusOmega.visible === true){
                    repeater_ColossusOmega.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_ColossusOmega.text].length; i++){
                        repeater_ColossusOmega.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_ColossusOmega.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_ColossusOmega
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_LeviathanOmega

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
            id: repeater_LeviathanOmega
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_LeviathanOmega.visible === true){
                    repeater_LeviathanOmega.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_LeviathanOmega.text].length; i++){
                        repeater_LeviathanOmega.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_LeviathanOmega.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_LeviathanOmega
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_YggdrasilOmega

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
            id: repeater_YggdrasilOmega
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_YggdrasilOmega.visible === true){
                    repeater_YggdrasilOmega.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_YggdrasilOmega.text].length; i++){
                        repeater_YggdrasilOmega.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_YggdrasilOmega.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_YggdrasilOmega
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_LuminieraOmega

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
            id: repeater_LuminieraOmega
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_LuminieraOmega.visible === true){
                    repeater_LuminieraOmega.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_LuminieraOmega.text].length; i++){
                        repeater_LuminieraOmega.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_LuminieraOmega.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_LuminieraOmega
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_CelesteOmega

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
            id: repeater_CelesteOmega
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_CelesteOmega.visible === true){
                    repeater_CelesteOmega.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_CelesteOmega.text].length; i++){
                        repeater_CelesteOmega.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_CelesteOmega.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_CelesteOmega
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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

        Rectangle {
            width: parent.width
            height: 3
            color: "black"
        }
        Label {
            color: "black"
            font.bold: true
            font.pointSize: 18
            text: "Omega II Raids"
        }
        Rectangle {
            width: parent.width
            height: 3
            color: "black"
        }

        ///////// Raid Items - Shiva /////////
        Label {
            id: label_Shiva

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
            id: repeater_Shiva
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_Shiva.visible === true){
                    repeater_Shiva.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Shiva.text].length; i++){
                        repeater_Shiva.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Shiva.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_Shiva
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_Europa

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
            id: repeater_Europa
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_Europa.visible === true){
                    repeater_Europa.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Europa.text].length; i++){
                        repeater_Europa.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Europa.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_Europa
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_Alexiel

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
            id: repeater_Alexiel
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_Alexiel.visible === true){
                    repeater_Alexiel.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Alexiel.text].length; i++){
                        repeater_Alexiel.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Alexiel.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_Alexiel
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }
            
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
            id: label_Grimnir

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
            id: repeater_Grimnir
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_Grimnir.visible === true){
                    repeater_Grimnir.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Grimnir.text].length; i++){
                        repeater_Grimnir.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Grimnir.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_Grimnir
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_Metatron

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
            id: repeater_Metatron
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_Metatron.visible === true){
                    repeater_Metatron.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Metatron.text].length; i++){
                        repeater_Metatron.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Metatron.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_Metatron
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_Avatar

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
            id: repeater_Avatar
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_Avatar.visible === true){
                    repeater_Avatar.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Avatar.text].length; i++){
                        repeater_Avatar.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Avatar.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_Avatar
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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

        Rectangle {
            width: parent.width
            height: 3
            color: "black"
        }
        Label {
            color: "black"
            font.bold: true
            font.pointSize: 18
            text: "Primarch Raids"
        }
        Rectangle {
            width: parent.width
            height: 3
            color: "black"
        }

        ///////// Raid Items - Michael /////////
        Label {
            id: label_Michael

            color: "#aa0000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Michael"
        }

        Repeater {
            id: repeater_Michael
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_Michael.visible === true){
                    repeater_Michael.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Michael.text].length; i++){
                        repeater_Michael.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Michael.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_Michael
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#aa0000"
                    anchors.left: itemImage_Michael.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Michael /////////

        ///////// Raid Items - Gabriel /////////
        Label {
            id: label_Gabriel

            color: "#00ffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Gabriel"
        }

        Repeater {
            id: repeater_Gabriel
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_Gabriel.visible === true){
                    repeater_Gabriel.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Gabriel.text].length; i++){
                        repeater_Gabriel.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Gabriel.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_Gabriel
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#00ffff"
                    anchors.left: itemImage_Gabriel.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Gabriel /////////

        ///////// Raid Items - Uriel /////////
        Label {
            id: label_Uriel

            color: "#ff8000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Uriel"
        }

        Repeater {
            id: repeater_Uriel
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_Uriel.visible === true){
                    repeater_Uriel.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Uriel.text].length; i++){
                        repeater_Uriel.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Uriel.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_Uriel
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ff8000"
                    anchors.left: itemImage_Uriel.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Uriel /////////

        ///////// Raid Items - Raphael /////////
        Label {
            id: label_Raphael

            color: "#00ff00"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Raphael"
        }

        Repeater {
            id: repeater_Raphael
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_Raphael.visible === true){
                    repeater_Raphael.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Raphael.text].length; i++){
                        repeater_Raphael.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Raphael.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_Raphael
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#00ff00"
                    anchors.left: itemImage_Raphael.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Raphael /////////

        ///////// Raid Items - Four Primarchs /////////
        Label {
            id: label_FourPrimarchs

            color: "#ffffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Four Primarchs"
        }

        Repeater {
            id: repeater_FourPrimarchs
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_FourPrimarchs.visible === true){
                    repeater_FourPrimarchs.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_FourPrimarchs.text].length; i++){
                        repeater_FourPrimarchs.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_FourPrimarchs.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_FourPrimarchs
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ffffff"
                    anchors.left: itemImage_FourPrimarchs.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Four Primarchs /////////

        Rectangle {
            width: parent.width
            height: 3
            color: "black"
        }
        Label {
            color: "black"
            font.bold: true
            font.pointSize: 18
            text: "Nightmare/Impossible Raids"
        }
        Rectangle {
            width: parent.width
            height: 3
            color: "black"
        }

        ///////// Raid Items - Rose Queen /////////
        Label {
            id: label_RoseQueen

            color: "#ff8000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Rose Queen"
        }

        Repeater {
            id: repeater_RoseQueen
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_RoseQueen.visible === true){
                    repeater_RoseQueen.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_RoseQueen.text].length; i++){
                        repeater_RoseQueen.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_RoseQueen.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_RoseQueen
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ff8000"
                    anchors.left: itemImage_RoseQueen.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Rose Queen /////////

        ///////// Raid Items - Grand Order /////////
        Label {
            id: label_GrandOrder

            color: "#ffff00"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Grand Order"
        }

        Repeater {
            id: repeater_GrandOrder
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_GrandOrder.visible === true){
                    repeater_GrandOrder.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_GrandOrder.text].length; i++){
                        repeater_GrandOrder.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_GrandOrder.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_GrandOrder
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ffff00"
                    anchors.left: itemImage_GrandOrder.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Grand Order /////////

        ///////// Raid Items - Akasha /////////
        Label {
            id: label_Akasha

            color: "#ffffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Akasha"
        }

        Repeater {
            id: repeater_Akasha
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_Akasha.visible === true){
                    repeater_Akasha.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Akasha.text].length; i++){
                        repeater_Akasha.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Akasha.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_Akasha
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ffffff"
                    anchors.left: itemImage_Akasha.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Akasha /////////

        ///////// Raid Items - Lucilius /////////
        Label {
            id: label_Lucilius

            color: "#ffffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Lucilius"
        }

        Repeater {
            id: repeater_Lucilius
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_Lucilius.visible === true){
                    repeater_Lucilius.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Lucilius.text].length; i++){
                        repeater_Lucilius.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Lucilius.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_Lucilius
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ffffff"
                    anchors.left: itemImage_Lucilius.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Lucilius /////////

        ///////// Raid Items - Lindwurm /////////
        Label {
            id: label_Lindwurm

            color: "#ffffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Lindwurm"
        }

        Repeater {
            id: repeater_Lindwurm
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_Lindwurm.visible === true){
                    repeater_Lindwurm.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Lindwurm.text].length; i++){
                        repeater_Lindwurm.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Lindwurm.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_Lindwurm
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ffffff"
                    anchors.left: itemImage_Lindwurm.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Lindwurm /////////

        ///////// Raid Items - Huanglong and Qilin /////////
        Label {
            id: label_HuanglongAndQilin

            color: "#ffffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Huanglong and Qilin"
        }

        Repeater {
            id: repeater_HuanglongAndQilin
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_HuanglongAndQilin.visible === true){
                    repeater_HuanglongAndQilin.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_HuanglongAndQilin.text].length; i++){
                        repeater_HuanglongAndQilin.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_HuanglongAndQilin.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_HuanglongAndQilin
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ffffff"
                    anchors.left: itemImage_HuanglongAndQilin.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Huanglong and Qilin /////////

        ///////// Raid Items - Proto Bahamut /////////
        Label {
            id: label_ProtoBahamut

            color: "#aa00ff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Proto Bahamut"
        }

        Repeater {
            id: repeater_ProtoBahamut
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_ProtoBahamut.visible === true){
                    repeater_ProtoBahamut.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_ProtoBahamut.text].length; i++){
                        repeater_ProtoBahamut.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_ProtoBahamut.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_ProtoBahamut
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#aa00ff"
                    anchors.left: itemImage_ProtoBahamut.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Proto Bahamut /////////

        ///////// Raid Items - Ultimate Bahamut /////////
        Label {
            id: label_UltimateBahamut

            color: "#ffffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Ultimate Bahamut"
        }

        Repeater {
            id: repeater_UltimateBahamut
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_UltimateBahamut.visible === true){
                    repeater_UltimateBahamut.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_UltimateBahamut.text].length; i++){
                        repeater_UltimateBahamut.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_UltimateBahamut.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_UltimateBahamut
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ffffff"
                    anchors.left: itemImage_UltimateBahamut.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Ultimate Bahamut /////////

        Rectangle {
            width: parent.width
            height: 3
            color: "black"
        }
        Label {
            color: "black"
            font.bold: true
            font.pointSize: 18
            text: "Tier 1 Summon Raids"
        }
        Rectangle {
            width: parent.width
            height: 3
            color: "black"
        }

        ///////// Raid Items - Twin Elements /////////
        Label {
            id: label_TwinElements

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
            id: repeater_TwinElements
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_TwinElements.visible === true){
                    repeater_TwinElements.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_TwinElements.text].length; i++){
                        repeater_TwinElements.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_TwinElements.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_TwinElements
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_MaculaMarius
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
            id: repeater_MaculaMarius
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_MaculaMarius.visible === true){
                    repeater_MaculaMarius.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_MaculaMarius.text].length; i++){
                        repeater_MaculaMarius.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_MaculaMarius.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_MaculaMarius
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_Medusa

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
            id: repeater_Medusa
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_Medusa.visible === true){
                    repeater_Medusa.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Medusa.text].length; i++){
                        repeater_Medusa.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Medusa.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_Medusa
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_Nezha

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
            id: repeater_Nezha
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_Nezha.visible === true){
                    repeater_Nezha.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Nezha.text].length; i++){
                        repeater_Nezha.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Nezha.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_Nezha
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_Apollo

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
            id: repeater_Apollo
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_Apollo.visible === true){
                    repeater_Apollo.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Apollo.text].length; i++){
                        repeater_Apollo.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Apollo.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_Apollo
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_DarkAngelOlivia

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
            id: repeater_DarkAngelOlivia
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_DarkAngelOlivia.visible === true){
                    repeater_DarkAngelOlivia.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_DarkAngelOlivia.text].length; i++){
                        repeater_DarkAngelOlivia.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_DarkAngelOlivia.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_DarkAngelOlivia
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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

        Rectangle {
            width: parent.width
            height: 3
            color: "black"
        }
        Label {
            color: "black"
            font.bold: true
            font.pointSize: 18
            text: "Tier 2 Summon Raids"
        }
        Rectangle {
            width: parent.width
            height: 3
            color: "black"
        }

        ///////// Raid Items - Athena /////////
        Label {
            id: label_Athena

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
            id: repeater_Athena
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_Athena.visible === true){
                    repeater_Athena.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Athena.text].length; i++){
                        repeater_Athena.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Athena.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_Athena
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_Grani

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
            id: repeater_Grani
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_Grani.visible === true){
                    repeater_Grani.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Grani.text].length; i++){
                        repeater_Grani.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Grani.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_Grani
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_Baal

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
            id: repeater_Baal
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_Baal.visible === true){
                    repeater_Baal.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Baal.text].length; i++){
                        repeater_Baal.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Baal.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_Baal
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_Garuda

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
            id: repeater_Garuda
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_Garuda.visible === true){
                    repeater_Garuda.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Garuda.text].length; i++){
                        repeater_Garuda.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Garuda.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_Garuda
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_Odin

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
            id: repeater_Odin
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_Odin.visible === true){
                    repeater_Odin.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Odin.text].length; i++){
                        repeater_Odin.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Odin.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_Odin
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_Lich

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
            id: repeater_Lich
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_Lich.visible === true){
                    repeater_Lich.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Lich.text].length; i++){
                        repeater_Lich.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Lich.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_Lich
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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

        Rectangle {
            width: parent.width
            height: 3
            color: "black"
        }
        Label {
            color: "black"
            font.bold: true
            font.pointSize: 18
            text: "Tier 3 Summon Raids"
        }
        Rectangle {
            width: parent.width
            height: 3
            color: "black"
        }

        ///////// Raid Items - Prometheus /////////
        Label {
            id: label_Prometheus

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
            id: repeater_Prometheus
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_Prometheus.visible === true){
                    repeater_Prometheus.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Prometheus.text].length; i++){
                        repeater_Prometheus.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Prometheus.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_Prometheus
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_CaOng

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
            id: repeater_CaOng
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_CaOng.visible === true){
                    repeater_CaOng.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_CaOng.text].length; i++){
                        repeater_CaOng.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_CaOng.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_CaOng
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_Gilgamesh

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
            id: repeater_Gilgamesh
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_Gilgamesh.visible === true){
                    repeater_Gilgamesh.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Gilgamesh.text].length; i++){
                        repeater_Gilgamesh.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Gilgamesh.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_Gilgamesh
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_Morrigna

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
            id: repeater_Morrigna
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_Morrigna.visible === true){
                    repeater_Morrigna.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Morrigna.text].length; i++){
                        repeater_Morrigna.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Morrigna.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_Morrigna
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_Hector

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
            id: repeater_Hector
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_Hector.visible === true){
                    repeater_Hector.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Hector.text].length; i++){
                        repeater_Hector.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Hector.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_Hector
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_Anubis

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
            id: repeater_Anubis
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_Anubis.visible === true){
                    repeater_Anubis.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Anubis.text].length; i++){
                        repeater_Anubis.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Anubis.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_Anubis
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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

        Rectangle {
            width: parent.width
            height: 3
            color: "black"
        }
        Label {
            color: "black"
            font.bold: true
            font.pointSize: 18
            text: "Six Dragon Raids"
        }
        Rectangle {
            width: parent.width
            height: 3
            color: "black"
        }

        ///////// Raid Items - Wilnas /////////
        Label {
            id: label_Wilnas

            color: "#aa0000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Wilnas"
        }

        Repeater {
            id: repeater_Wilnas
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_Wilnas.visible === true){
                    repeater_Wilnas.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Wilnas.text].length; i++){
                        repeater_Wilnas.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Wilnas.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_Wilnas
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#aa0000"
                    anchors.left: itemImage_Wilnas.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Wilnas /////////

        ///////// Raid Items - Wamdus /////////
        Label {
            id: label_Wamdus

            color: "#00ffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Wamdus"
        }

        Repeater {
            id: repeater_Wamdus
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_Wamdus.visible === true){
                    repeater_Wamdus.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Wamdus.text].length; i++){
                        repeater_Wamdus.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Wamdus.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_Wamdus
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#00ffff"
                    anchors.left: itemImage_Wamdus.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Wamdus /////////

        ///////// Raid Items - Galleon /////////
        Label {
            id: label_Galleon

            color: "#ff8000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Galleon"
        }

        Repeater {
            id: repeater_Galleon
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_Galleon.visible === true){
                    repeater_Galleon.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Galleon.text].length; i++){
                        repeater_Galleon.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Galleon.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_Galleon
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ff8000"
                    anchors.left: itemImage_Galleon.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Galleon /////////

        ///////// Raid Items - Ewiyar /////////
        Label {
            id: label_Ewiyar

            color: "#00ff00"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Ewiyar"
        }

        Repeater {
            id: repeater_Ewiyar
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_Ewiyar.visible === true){
                    repeater_Ewiyar.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Ewiyar.text].length; i++){
                        repeater_Ewiyar.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Ewiyar.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_Ewiyar
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#00ff00"
                    anchors.left: itemImage_Ewiyar.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Ewiyar /////////

        ///////// Raid Items - Lu Woh /////////
        Label {
            id: label_LuWoh

            color: "#ffff00"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Lu Woh"
        }

        Repeater {
            id: repeater_LuWoh
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_LuWoh.visible === true){
                    repeater_LuWoh.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_LuWoh.text].length; i++){
                        repeater_LuWoh.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_LuWoh.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_LuWoh
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ffff00"
                    anchors.left: itemImage_LuWoh.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Lu Woh /////////

        ///////// Raid Items - Fediel /////////
        Label {
            id: label_Fediel

            color: "#aa00ff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Fediel"
        }

        Repeater {
            id: repeater_Fediel
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_Fediel.visible === true){
                    repeater_Fediel.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Fediel.text].length; i++){
                        repeater_Fediel.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Fediel.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_Fediel
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#aa00ff"
                    anchors.left: itemImage_Fediel.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Fediel /////////

        Rectangle {
            width: parent.width
            height: 3
            color: "black"
        }
        Label {
            color: "black"
            font.bold: true
            font.pointSize: 18
            text: "Malice Raids"
        }
        Rectangle {
            width: parent.width
            height: 3
            color: "black"
        }

        ///////// Raid Items - Tiamat Malice /////////
        Label {
            id: label_TiamatMalice

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
            id: repeater_TiamatMalice
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_TiamatMalice.visible === true){
                    repeater_TiamatMalice.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_TiamatMalice.text].length; i++){
                        repeater_TiamatMalice.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_TiamatMalice.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_TiamatMalice
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_LeviathanMalice

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
            id: repeater_LeviathanMalice
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_LeviathanMalice.visible === true){
                    repeater_LeviathanMalice.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_LeviathanMalice.text].length; i++){
                        repeater_LeviathanMalice.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_LeviathanMalice.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_LeviathanMalice
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_Phronesis

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
            id: repeater_Phronesis
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_Phronesis.visible === true){
                    repeater_Phronesis.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Phronesis.text].length; i++){
                        repeater_Phronesis.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Phronesis.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_Phronesis
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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

        ///////// Raid Items - Luminiera Malice /////////
        Label {
            id: label_LuminieraMalice

            color: "#ffff00"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Luminiera Malice"
        }

        Repeater {
            id: repeater_LuminieraMalice
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_LuminieraMalice.visible === true){
                    repeater_LuminieraMalice.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_LuminieraMalice.text].length; i++){
                        repeater_LuminieraMalice.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_LuminieraMalice.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_LuminieraMalice
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ffff00"
                    anchors.left: itemImage_LuminieraMalice.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Luminiera Malice /////////

        ///////// Raid Items - Anima-Animus Core /////////
        Label {
            id: label_AnimaAnimusCore

            color: "#aa00ff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Anima-Animus Core"
        }

        Repeater {
            id: repeater_AnimaAnimusCore
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_AnimaAnimusCore.visible === true){
                    repeater_AnimaAnimusCore.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_AnimaAnimusCore.text].length; i++){
                        repeater_AnimaAnimusCore.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_AnimaAnimusCore.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_AnimaAnimusCore
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#aa00ff"
                    anchors.left: itemImage_AnimaAnimusCore.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Anima-Animus Core /////////

        Rectangle {
            width: parent.width
            height: 3
            color: "black"
        }
        Label {
            color: "black"
            font.bold: true
            font.pointSize: 18
            text: "Xeno Clash Raids"
        }
        Rectangle {
            width: parent.width
            height: 3
            color: "black"
        }

        ///////// Raid Items - Xeno Ifrit /////////
        Label {
            id: label_XenoIfrit

            color: "#aa0000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Xeno Ifrit"
        }

        Repeater {
            id: repeater_XenoIfrit
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_XenoIfrit.visible === true){
                    repeater_XenoIfrit.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_XenoIfrit.text].length; i++){
                        repeater_XenoIfrit.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_XenoIfrit.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_XenoIfrit
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#aa0000"
                    anchors.left: itemImage_XenoIfrit.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Xeno Ifrit /////////

        ///////// Raid Items - Xeno Cocytus /////////
        Label {
            id: label_XenoCocytus

            color: "#00ffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Xeno Cocytus"
        }

        Repeater {
            id: repeater_XenoCocytus
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_XenoCocytus.visible === true){
                    repeater_XenoCocytus.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_XenoCocytus.text].length; i++){
                        repeater_XenoCocytus.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_XenoCocytus.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_XenoCocytus
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#00ffff"
                    anchors.left: itemImage_XenoCocytus.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Xeno Cocytus /////////

        ///////// Raid Items - Xeno Vohu Manah /////////
        Label {
            id: label_XenoVohuManah

            color: "#ff8000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Xeno Vohu Manah"
        }

        Repeater {
            id: repeater_XenoVohuManah
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_XenoVohuManah.visible === true){
                    repeater_XenoVohuManah.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_XenoVohuManah.text].length; i++){
                        repeater_XenoVohuManah.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_XenoVohuManah.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_XenoVohuManah
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ff8000"
                    anchors.left: itemImage_XenoVohuManah.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Xeno Vohu Manah /////////

        ///////// Raid Items - Xeno Sagittarius /////////
        Label {
            id: label_XenoSagittarius

            color: "#00ff00"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Xeno Sagittarius"
        }

        Repeater {
            id: repeater_XenoSagittarius
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_XenoSagittarius.visible === true){
                    repeater_XenoSagittarius.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_XenoSagittarius.text].length; i++){
                        repeater_XenoSagittarius.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_XenoSagittarius.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_XenoSagittarius
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#00ff00"
                    anchors.left: itemImage_XenoSagittarius.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Xeno Sagittarius /////////

        ///////// Raid Items - Xeno Corow /////////
        Label {
            id: label_XenoCorow

            color: "#ffff00"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Xeno Corow"
        }

        Repeater {
            id: repeater_XenoCorow
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_XenoCorow.visible === true){
                    repeater_XenoCorow.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_XenoCorow.text].length; i++){
                        repeater_XenoCorow.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_XenoCorow.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_XenoCorow
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ffff00"
                    anchors.left: itemImage_XenoCorow.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Xeno Corow /////////

        ///////// Raid Items - Xeno Diablo /////////
        Label {
            id: label_XenoDiablo

            color: "#aa00ff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Xeno Diablo"
        }

        Repeater {
            id: repeater_XenoDiablo
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_XenoDiablo.visible === true){
                    repeater_XenoDiablo.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_XenoDiablo.text].length; i++){
                        repeater_XenoDiablo.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_XenoDiablo.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_XenoDiablo
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#aa00ff"
                    anchors.left: itemImage_XenoDiablo.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Xeno Diablo /////////

        Rectangle {
            width: parent.width
            height: 3
            color: "black"
        }
        Label {
            color: "black"
            font.bold: true
            font.pointSize: 18
            text: "Rise of the Beasts Raids"
        }
        Rectangle {
            width: parent.width
            height: 3
            color: "black"
        }

        ///////// Raid Items - Shenxian /////////
        Label {
            id: label_Shenxian

            color: "#ffffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Shenxian"
        }

        Repeater {
            id: repeater_Shenxian
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_Shenxian.visible === true){
                    repeater_Shenxian.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Shenxian.text].length; i++){
                        repeater_Shenxian.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Shenxian.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_Shenxian
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ffffff"
                    anchors.left: itemImage_Shenxian.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Shenxian /////////

        ///////// Raid Items - Agni /////////
        Label {
            id: label_Agni

            color: "#aa0000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Agni"
        }

        Repeater {
            id: repeater_Agni
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_Agni.visible === true){
                    repeater_Agni.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Agni.text].length; i++){
                        repeater_Agni.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Agni.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_Agni
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#aa0000"
                    anchors.left: itemImage_Agni.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Agni /////////

        ///////// Raid Items - Neptune /////////
        Label {
            id: label_Neptune

            color: "#00ffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Neptune"
        }

        Repeater {
            id: repeater_Neptune
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_Neptune.visible === true){
                    repeater_Neptune.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Neptune.text].length; i++){
                        repeater_Neptune.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Neptune.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_Neptune
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#00ffff"
                    anchors.left: itemImage_Neptune.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Neptune /////////

        ///////// Raid Items - Titan /////////
        Label {
            id: label_Titan

            color: "#ff8000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Titan"
        }

        Repeater {
            id: repeater_Titan
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_Titan.visible === true){
                    repeater_Titan.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Titan.text].length; i++){
                        repeater_Titan.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Titan.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_Titan
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ff8000"
                    anchors.left: itemImage_Titan.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Titan /////////

        ///////// Raid Items - Zephyrus /////////
        Label {
            id: label_Zephyrus

            color: "#00ff00"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Zephyrus"
        }

        Repeater {
            id: repeater_Zephyrus
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_Zephyrus.visible === true){
                    repeater_Zephyrus.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Zephyrus.text].length; i++){
                        repeater_Zephyrus.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Zephyrus.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_Zephyrus
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        raidItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#00ff00"
                    anchors.left: itemImage_Zephyrus.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Raid Items - Zephyrus /////////
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
