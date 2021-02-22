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
                "Grand Order": ["Azure Feather", "Heavenly Horn"],
                "Proto Bahamut": ["Horn of Bahamut", "Champion Merit", "Primeval Horn"],
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
