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

        // Items for H3-1 In a Dusk Dream.
        ListModel {
            id: coopItemsModel_InADuskDream

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

        // Items for EX1-1 Corridor of Puzzles / EX1-3 Lost in the Dark
        ListModel {
            id: coopItemsModel_CorridorOfPuzzlesAndLostInTheDark

            Component.onCompleted: {
                var listOfItems = ["Warrior Creed", "Mage Creed"]

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

        // Items for EX2-2 Time of Judgement
        ListModel {
            id: coopItemsModel_TimeOfJudgement

            Component.onCompleted: {
                var listOfItems = ["Evil Judge Crystal", "Pilgrim Distinction", "Mage Distinction", "Alchemist Distinction", "Monk's Distinction", "Keraunos Replica", "Faust Replica"]

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

        // Items for EX2-3 Time of Revelation
        ListModel {
            id: coopItemsModel_TimeOfRevelation

            Component.onCompleted: {
                var listOfItems = ["Infernal Garnet", "Gladiator Distinction", "Fencer Distinction", "Dual Wielder Distinction", "Forester's Distinction", "Avenger Replica", "Hellion Gauntlet Replica"]

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

        // Items for EX2-4 Time of Eminence
        ListModel {
            id: coopItemsModel_TimeOfEminence

            Component.onCompleted: {
                var listOfItems = ["Halo Light Quartz", "Bandit Distinction", "Troubadour Distinction", "Mystic Distinction", "Shredder Distinction", "Nirvana Replica", "Romulus Spear Replica", "Murakumo Replica"]

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

        // Items for EX3-2 Rule of the Tundra
        ListModel {
            id: coopItemsModel_RuleOfTheTundra

            Component.onCompleted: {
                var listOfItems = ["Frozen Hell Prism", "Guardian Distinction", "Combatant Distinction", "Sword Master Distinction", "Dragoon's Distinction", "Skofnung Replica", "Langeleik Replica", "Kapilavastu Replica"]

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

        // Items for EX3-3 Rule of the Plains
        ListModel {
            id: coopItemsModel_RuleOfThePlains

            Component.onCompleted: {
                var listOfItems = ["Horseman's Plate", "Sharpshooter Distinction", "Cavalryman Distinction", "Gunslinger Distinction", "Oliver Replica", "Rosenbogen Replica", "Misericorde Replica"]

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

        // Items for EX3-4 Rule of the Twilight
        ListModel {
            id: coopItemsModel_RuleOfTheTwilight

            Component.onCompleted: {
                var listOfItems = ["Phantom Demon Jewel", "Samurai Distinction", "Ninja Distinction", "Assassin Distinction", "Ipetam Replica", "Proximo Replica", "Nebuchad Replica", "Muramasa Replica"]

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

        // Items for EX4-2 Amidst the Waves
        ListModel {
            id: coopItemsModel_AmidstTheWaves

            Component.onCompleted: {
                var listOfItems = ["Pilgrim Distinction", "Mage Distinction", "Alchemist Distinction", "Mystic Distinction", "Monk's Distinction", "Oliver Replica", "Langeleik Replica", "Romulus Spear Replica", "Proximo Replica", "Kapilavastu Replica"]

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

        // Items for EX4-3 Amidst the Petals
        ListModel {
            id: coopItemsModel_AmidstThePetals

            Component.onCompleted: {
                var listOfItems = ["Sharpshooter Distinction", "Samurai Distinction", "Ninja Distinction", "Gunslinger Distinction", "Assassin Distinction", "Longstrider's Distinction", "Langeleik Replica", "Misericorde Replica", "Faust Replica"]

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

        // Items for EX4-4 Amidst Severe Cliffs
        ListModel {
            id: coopItemsModel_AmidstSevereCliffs

            Component.onCompleted: {
                var listOfItems = ["Gladiator Distinction", "Fencer Distinction", "Combatant Distinction", "Sword Master Distinction", "Aschallon Replica", "Hellion Gauntlet Replica", "Muramasa Replica", "Practice Drum"]

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

        // Items for EX4-5 Amidst the Flames
        ListModel {
            id: coopItemsModel_AmidstTheFlames

            Component.onCompleted: {
                var listOfItems = ["Guardian Distinction", "Bandit Distinction", "Troubadour Distinction", "Cavalryman Distinction", "Dragoon's Distinction", "Ipetam Replica", "Murakumo Replica", "Nebuchad Replica"]

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

        ///////// Coop Items - H3-1 In a Dusk Dream /////////
        Label {
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
            model: coopItemsModel_InADuskDream
            Image {
                id: itemImage_InADuskDream

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        coopItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
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
            model: coopItemsModel_CorridorOfPuzzlesAndLostInTheDark
            Image {
                id: itemImage_CorridorOfPuzzlesAndLostInTheDark

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        coopItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
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
            model: coopItemsModel_TimeOfJudgement
            Image {
                id: itemImage_TimeOfJudgement

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        coopItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
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
            model: coopItemsModel_TimeOfRevelation
            Image {
                id: itemImage_TimeOfRevelation

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        coopItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
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
            model: coopItemsModel_TimeOfEminence
            Image {
                id: itemImage_TimeOfEminence

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        coopItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
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
            model: coopItemsModel_RuleOfTheTundra
            Image {
                id: itemImage_RuleOfTheTundra

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        coopItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
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
            model: coopItemsModel_RuleOfThePlains
            Image {
                id: itemImage_RuleOfThePlains

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        coopItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
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
            model: coopItemsModel_RuleOfTheTwilight
            Image {
                id: itemImage_RuleOfTheTwilight

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        coopItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
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
            model: coopItemsModel_AmidstTheWaves
            Image {
                id: itemImage_AmidstTheWaves

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        coopItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
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
            model: coopItemsModel_AmidstThePetals
            Image {
                id: itemImage_AmidstThePetals

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        coopItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
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
            model: coopItemsModel_AmidstSevereCliffs
            Image {
                id: itemImage_AmidstSevereCliffs

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        coopItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
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
            model: coopItemsModel_AmidstTheFlames
            Image {
                id: itemImage_AmidstTheFlames

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        coopItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
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
