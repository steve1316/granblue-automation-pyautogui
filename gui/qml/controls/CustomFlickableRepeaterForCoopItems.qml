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

        // List model that holds all the Coop items that are supported.
        ListModel {
            id: itemsModel

            // The order of these items is defined in-game by heading to their "Get from Quests" section when you click on the item to find out where to farm it. Additional locations are provided by the item's page at gbf.wiki
            property var listOfItems: {
                "H3-1 In a Dusk Dream": ["EXP"],
                "EX1-1 Corridor of Puzzles / EX1-3 Lost in the Dark": ["Warrior Creed", "Mage Creed"],
                "EX2-2 Time of Judgement": ["Keraunos Replica", "Faust Replica", "Mage Distinction", "Pilgrim Distinction", "Alchemist Distinction", "Monk's Distinction", "Evil Judge Crystal"],
                "EX2-3 Time of Revelation": ["Avenger Replica", "Hellion Gauntlet Replica", "Gladiator Distinction", "Fencer Distinction", "Dual Wielder Distinction", "Forester's Distinction", "Infernal Garnet"],
                "EX2-4 Time of Eminence": ["Nirvana Replica", "Romulus Spear Replica", "Murakumo Replica", "Bandit Distinction", "Troubadour Distinction", "Mystic Distinction", "Shredder Distinction", "Contractor Distinction", "Halo Light Quartz"],
                "EX3-2 Rule of the Tundra": ["Skofnung Replica", "Langeleik Replica", "Combatant Distinction", "Guardian Distinction", "Sword Master Distinction", "Dragoon's Distinction", "Frozen Hell Prism"],
                "EX3-3 Rule of the Plains": ["Oliver Replica", "Rosenbogen Replica",  "Sharpshooter Distinction", "Gunslinger Distinction", "Cavalryman Distinction", "Longstrider's Distinction", "Horseman's Plate"],
                "EX3-4 Rule of the Twilight": ["Ipetam Replica", "Muramasa Replica", "Proximo Replica", "Samurai Distinction", "Assassin Distinction", "Ninja Distinction", "Dancer Distinction", "Phantom Demon Jewel"],
                "EX4-2 Amidst the Waves": ["Oliver Replica", "Romulus Spear Replica", "Kapilavastu Replica", "Mystic Distinction", "Pilgrim Distinction", "Alchemist Distinction", "Mage Distinction", "Monk's Distinction"],
                "EX4-3 Amidst the Petals": ["Langeleik Replica", "Faust Replica", "Misericorde Replica", "Arabesque Replica", "Ninja Distinction", "Samurai Distinction", "Sharpshooter Distinction", "Gunslinger Distinction", "Longstrider's Distinction", "Dancer Distinction"],
                "EX4-4 Amidst Severe Cliffs": ["Hellion Gauntlet Replica", "Muramasa Replica", "Aschallon Replica", "Practice Drum", "Combatant Distinction", "Gladiator Distinction", "Sword Master Distinction", "Fencer Distinction"],
                "EX4-5 Amidst the Flames": ["Ipetam Replica", "Murakumo Replica", "Nebuchad Replica", "Proximo Replica", "Guardian Distinction", "Cavalryman Distinction", "Bandit Distinction", "Troubadour Distinction", "Dragoon's Distinction", "Contractor Distinction"],
            }

            function createListElement(itemName){
                var filePath = "../../../images/items/%1.png".arg(itemName)
                return {
                    name: itemName,
                    imageSource: filePath
                }
            }
        }

        ///////// Coop Items - H3-1 In a Dusk Dream /////////
        Label {
            id: label_InADuskDream

            color: "#ffffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "H3-1 In a Dusk Dream"
        }

        Repeater {
            id: repeater_InADuskDream
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_InADuskDream.visible === true){
                    repeater_InADuskDream.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_InADuskDream.text].length; i++){
                        repeater_InADuskDream.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_InADuskDream.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_InADuskDream
                source: imageSource
                width: 35
                height: 40
                
                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        coopItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ffffff"
                    anchors.left: itemImage_InADuskDream.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Coop Items - H3-1 In a Dusk Dream /////////

        ///////// Coop Items - EX1-1 Corridor of Puzzles / EX1-3 Lost in the Dark /////////
        Label {
            id: label_CorridorOfPuzzlesAndLostInTheDark

            color: "#ffffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 9
            font.letterSpacing: 1

            text: "EX1-1 Corridor of Puzzles / EX1-3 Lost in the Dark"
        }

        Repeater {
            id: repeater_CorridorOfPuzzlesAndLostInTheDark
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_CorridorOfPuzzlesAndLostInTheDark.visible === true){
                    repeater_CorridorOfPuzzlesAndLostInTheDark.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_CorridorOfPuzzlesAndLostInTheDark.text].length; i++){
                        repeater_CorridorOfPuzzlesAndLostInTheDark.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_CorridorOfPuzzlesAndLostInTheDark.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_CorridorOfPuzzlesAndLostInTheDark
                source: imageSource
                width: 35
                height: 40
                
                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        coopItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ffffff"
                    anchors.left: itemImage_CorridorOfPuzzlesAndLostInTheDark.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Coop Items - EX1-1 Corridor of Puzzles / EX1-3 Lost in the Dark /////////

        ///////// Coop Items - EX2-2 Time of Judgement /////////
        Label {
            id: label_TimeOfJudgement

            color: "#ff8000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "EX2-2 Time of Judgement"
        }

        Repeater {
            id: repeater_TimeOfJudgement
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_TimeOfJudgement.visible === true){
                    repeater_TimeOfJudgement.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_TimeOfJudgement.text].length; i++){
                        repeater_TimeOfJudgement.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_TimeOfJudgement.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_TimeOfJudgement
                source: imageSource
                width: 35
                height: 40
                
                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        coopItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ff8000"
                    anchors.left: itemImage_TimeOfJudgement.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Coop Items - EX2-2 Time of Judgement /////////

        ///////// Coop Items - EX2-3 Time of Revelation /////////
        Label {
            id: label_TimeOfRevelation

            color: "#aa0000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "EX2-3 Time of Revelation"
        }

        Repeater {
            id: repeater_TimeOfRevelation
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_TimeOfRevelation.visible === true){
                    repeater_TimeOfRevelation.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_TimeOfRevelation.text].length; i++){
                        repeater_TimeOfRevelation.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_TimeOfRevelation.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_TimeOfRevelation
                source: imageSource
                width: 35
                height: 40
                
                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        coopItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#aa0000"
                    anchors.left: itemImage_TimeOfRevelation.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Coop Items - EX2-3 Time of Revelation /////////

        ///////// Coop Items - EX2-4 Time of Eminence /////////
        Label {
            id: label_TimeOfEminence

            color: "#ffff00"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "EX2-4 Time of Eminence"
        }

        Repeater {
            id: repeater_TimeOfEminence
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_TimeOfEminence.visible === true){
                    repeater_TimeOfEminence.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_TimeOfEminence.text].length; i++){
                        repeater_TimeOfEminence.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_TimeOfEminence.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_TimeOfEminence
                source: imageSource
                width: 35
                height: 40
                
                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        coopItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ffff00"
                    anchors.left: itemImage_TimeOfEminence.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Coop Items - EX2-4 Time of Eminence /////////

        ///////// Coop Items - EX3-2 Rule of the Tundra /////////
        Label {
            id: label_RuleOfTheTundra

            color: "#00ffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "EX3-2 Rule of the Tundra"
        }

        Repeater {
            id: repeater_RuleOfTheTundra
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_RuleOfTheTundra.visible === true){
                    repeater_RuleOfTheTundra.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_RuleOfTheTundra.text].length; i++){
                        repeater_RuleOfTheTundra.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_RuleOfTheTundra.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_RuleOfTheTundra
                source: imageSource
                width: 35
                height: 40
                
                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        coopItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#00ffff"
                    anchors.left: itemImage_RuleOfTheTundra.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Coop Items - EX3-2 Rule of the Tundra /////////

        ///////// Coop Items - EX3-3 Rule of the Plains /////////
        Label {
            id: label_RuleOfThePlains

            color: "#00ff00"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "EX3-3 Rule of the Plains"
        }

        Repeater {
            id: repeater_RuleOfThePlains
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_RuleOfThePlains.visible === true){
                    repeater_RuleOfThePlains.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_RuleOfThePlains.text].length; i++){
                        repeater_RuleOfThePlains.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_RuleOfThePlains.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_RuleOfThePlains
                source: imageSource
                width: 35
                height: 40
                
                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        coopItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#00ff00"
                    anchors.left: itemImage_RuleOfThePlains.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Coop Items - EX3-3 Rule of the Plains /////////

        ///////// Coop Items - EX3-4 Rule of the Twilight /////////
        Label {
            id: label_RuleOfTheTwilight

            color: "#aa00ff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "EX3-4 Rule of the Twilight"
        }

        Repeater {
            id: repeater_RuleOfTheTwilight
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_RuleOfTheTwilight.visible === true){
                    repeater_RuleOfTheTwilight.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_RuleOfTheTwilight.text].length; i++){
                        repeater_RuleOfTheTwilight.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_RuleOfTheTwilight.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_RuleOfTheTwilight
                source: imageSource
                width: 35
                height: 40
                
                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        coopItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#aa00ff"
                    anchors.left: itemImage_RuleOfTheTwilight.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Coop Items - EX3-4 Rule of the Twilight /////////

        ///////// Coop Items - EX4-2 Amidst the Waves /////////
        Label {
            id: label_AmidstTheWaves

            color: "#00ffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "EX4-2 Amidst the Waves"
        }

        Repeater {
            id: repeater_AmidstTheWaves
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_AmidstTheWaves.visible === true){
                    repeater_AmidstTheWaves.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_AmidstTheWaves.text].length; i++){
                        repeater_AmidstTheWaves.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_AmidstTheWaves.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_AmidstTheWaves
                source: imageSource
                width: 35
                height: 40
                
                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        coopItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#00ffff"
                    anchors.left: itemImage_AmidstTheWaves.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Coop Items - EX4-2 Amidst the Waves /////////

        ///////// Coop Items - EX4-3 Amidst the Petals /////////
        Label {
            id: label_AmidstThePetals

            color: "#00ff00"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "EX4-3 Amidst the Petals"
        }

        Repeater {
            id: repeater_AmidstThePetals
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_AmidstThePetals.visible === true){
                    repeater_AmidstThePetals.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_AmidstThePetals.text].length; i++){
                        repeater_AmidstThePetals.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_AmidstThePetals.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_AmidstThePetals
                source: imageSource
                width: 35
                height: 40
                
                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        coopItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#00ff00"
                    anchors.left: itemImage_AmidstThePetals.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Coop Items - EX4-3 Amidst the Petals /////////

        ///////// Coop Items - EX4-4 Amidst Severe Cliffs /////////
        Label {
            id: label_AmidstSevereCliffs

            color: "#ff8000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "EX4-4 Amidst Severe Cliffs"
        }

        Repeater {
            id: repeater_AmidstSevereCliffs
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_AmidstSevereCliffs.visible === true){
                    repeater_AmidstSevereCliffs.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_AmidstSevereCliffs.text].length; i++){
                        repeater_AmidstSevereCliffs.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_AmidstSevereCliffs.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_AmidstSevereCliffs
                source: imageSource
                width: 35
                height: 40
                
                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        coopItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ff8000"
                    anchors.left: itemImage_AmidstSevereCliffs.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Coop Items - EX4-4 Amidst Severe Cliffs /////////

        ///////// Coop Items - EX4-5 Amidst the Flames /////////
        Label {
            id: label_AmidstTheFlames

            color: "#aa0000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "EX4-5 Amidst the Flames"
        }

        Repeater {
            id: repeater_AmidstTheFlames
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_AmidstTheFlames.visible === true){
                    repeater_AmidstTheFlames.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_AmidstTheFlames.text].length; i++){
                        repeater_AmidstTheFlames.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_AmidstTheFlames.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_AmidstTheFlames
                source: imageSource
                width: 35
                height: 40
                
                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        coopItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#aa0000"
                    anchors.left: itemImage_AmidstTheFlames.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Coop Items - EX4-5 Amidst the Flames /////////
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
