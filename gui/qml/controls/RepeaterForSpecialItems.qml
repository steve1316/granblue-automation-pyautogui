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

        // List model that holds all the Special items that are supported.
        ListModel {
            id: itemsModel

            property var listOfItems: {
                "Scarlet Trial": ["Fire Orb", "Water Orb", "Earth Orb", "Wind Orb", "Light Orb", "Dark Orb", "Inferno Orb", "Frost Orb", "Rumbling Orb", "Cyclone Orb", "Shining Orb", "Abysm Orb"],
                "Cerulean Trial": ["Red Tome", "Blue Tome", "Brown Tome", "Green Tome", "White Tome", "Black Tome", "Hellfire Scroll", "Flood Scroll", "Thunder Scroll", "Gale Scroll", "Skylight Scroll", "Chasm Scroll", "Infernal Whorl", 
                "Tidal Whorl", "Seismic Whorl", "Tempest Whorl", "Radiant Whorl", "Umbral Whorl"],
                "Violet Trial": ["Prism Chip", "Flawed Prism", "Flawless Prism", "Rainbow Prism"],
                "Shiny Slime Search!": ["EXP"],
                "Six Dragon Trials": ["Red Dragon Scale", "Blue Dragon Scale", "Brown Dragon Scale", "Green Dragon Scale", "White Dragon Scale", "Black Dragon Scale"],
                "Ifrit Showdown": ["Jasper Scale", "Scorching Peak", "Infernal Garnet", "Ifrit Anima", "Ifrit Omega Anima"],
                "Cocytus Showdown": ["Mourning Stone", "Crystal Spirit", "Frozen Hell Prism", "Cocytus Anima", "Cocytus Omega Anima"],
                "Vohu Manah Showdown": ["Scrutiny Stone", "Luminous Judgment", "Evil Judge Crystal", "Vohu Manah Anima", "Vohu Manah Omega Anima"],
                "Sagittarius Showdown": ["Sagittarius Arrowhead", "Sagittarius Rune", "Horseman's Plate", "Sagittarius Anima", "Sagittarius Omega Anima"],
                "Corow Showdown": ["Solar Ring", "Sunlight Quartz", "Halo Light Quartz", "Corow Anima", "Corow Omega Anima"],
                "Diablo Showdown": ["Twilight Cloth Strip", "Shadow Silver", "Phantom Demon Jewel", "Diablo Anima", "Diablo Omega Anima"],
                "Extreme Trials": ["Hellfire Fragment", "Deluge Fragment", "Wasteland Fragment", "Typhoon Fragment"],
                "Angel Halo": ["Angel Halo Weapons"],
            }

            function createListElement(itemName){
                var filePath = "../../../images/items/%1.png".arg(itemName)
                return {
                    name: itemName,
                    imageSource: filePath
                }
            }
        }

        ///////// Special Items - Scarlet Trial /////////
        Label {
            id: label_ScarletTrial

            color: "#ffffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Scarlet Trial"
        }

        Repeater {
            id: repeater_ScarletTrial
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_ScarletTrial.visible === true){
                    repeater_ScarletTrial.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_ScarletTrial.text].length; i++){
                        repeater_ScarletTrial.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_ScarletTrial.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_ScarletTrial
                source: imageSource
                width: 35
                height: 40
                
                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        specialItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ffffff"
                    anchors.left: itemImage_ScarletTrial.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Special Items - Scarlet Trial /////////

        ///////// Special Items - Cerulean Trial /////////
        Label {
            id: label_CeruleanTrial

            color: "#ffffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Cerulean Trial"
        }

        Repeater {
            id: repeater_CeruleanTrial
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_CeruleanTrial.visible === true){
                    repeater_CeruleanTrial.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_CeruleanTrial.text].length; i++){
                        repeater_CeruleanTrial.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_CeruleanTrial.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_CeruleanTrial
                source: imageSource
                width: 35
                height: 40
                
                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        specialItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ffffff"
                    anchors.left: itemImage_CeruleanTrial.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Special Items - Cerulean Trial /////////

        ///////// Special Items - Violet Trial /////////
        Label {
            id: label_VioletTrial

            color: "#ffffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Violet Trial"
        }

        Repeater {
            id: repeater_VioletTrial
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_VioletTrial.visible === true){
                    repeater_VioletTrial.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_VioletTrial.text].length; i++){
                        repeater_VioletTrial.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_VioletTrial.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_VioletTrial
                source: imageSource
                width: 35
                height: 40
                
                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        specialItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ffffff"
                    anchors.left: itemImage_VioletTrial.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Special Items - Violet Trial /////////

        ///////// Special Items - Shiny Slime Search! /////////
        Label {
            id: label_ShinySlimeSearch

            color: "#ffffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Shiny Slime Search!"
        }

        Repeater {
            id: repeater_ShinySlimeSearch
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_ShinySlimeSearch.visible === true){
                    repeater_ShinySlimeSearch.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_ShinySlimeSearch.text].length; i++){
                        repeater_ShinySlimeSearch.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_ShinySlimeSearch.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_ShinySlimeSearch
                source: imageSource
                width: 35
                height: 40
                
                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        specialItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ffffff"
                    anchors.left: itemImage_ShinySlimeSearch.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Special Items - Shiny Slime Search! /////////

        ///////// Special Items - Six Dragon Trials /////////
        Label {
            id: label_SixDragonTrials

            color: "#ffffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Six Dragon Trials"
        }

        Repeater {
            id: repeater_SixDragonTrials
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_SixDragonTrials.visible === true){
                    repeater_SixDragonTrials.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_SixDragonTrials.text].length; i++){
                        repeater_SixDragonTrials.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_SixDragonTrials.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_SixDragonTrials
                source: imageSource
                width: 35
                height: 40
                
                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        specialItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ffffff"
                    anchors.left: itemImage_SixDragonTrials.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Special Items - Six Dragon Trials /////////

        ///////// Special Items - Ifrit Showdown /////////
        Label {
            id: label_IfritShowdown

            color: "#aa0000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Ifrit Showdown"
        }

        Repeater {
            id: repeater_IfritShowdown
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_IfritShowdown.visible === true){
                    repeater_IfritShowdown.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_IfritShowdown.text].length; i++){
                        repeater_IfritShowdown.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_IfritShowdown.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_IfritShowdown
                source: imageSource
                width: 35
                height: 40
                
                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        specialItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#aa0000"
                    anchors.left: itemImage_IfritShowdown.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Special Items - Ifrit Showdown /////////

        ///////// Special Items - Cocytus Showdown /////////
        Label {
            id: label_CocytusShowdown

            color: "#00ffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Cocytus Showdown"
        }

        Repeater {
            id: repeater_CocytusShowdown
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_CocytusShowdown.visible === true){
                    repeater_CocytusShowdown.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_CocytusShowdown.text].length; i++){
                        repeater_CocytusShowdown.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_CocytusShowdown.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_CocytusShowdown
                source: imageSource
                width: 35
                height: 40
                
                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        specialItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#00ffff"
                    anchors.left: itemImage_CocytusShowdown.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Special Items - Cocytus Showdown /////////

        ///////// Special Items - Vohu Manah Showdown /////////
        Label {
            id: label_VohuManahShowdown

            color: "#ff8000"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Vohu Manah Showdown"
        }

        Repeater {
            id: repeater_VohuManahShowdown
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_VohuManahShowdown.visible === true){
                    repeater_VohuManahShowdown.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_VohuManahShowdown.text].length; i++){
                        repeater_VohuManahShowdown.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_VohuManahShowdown.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_VohuManahShowdown
                source: imageSource
                width: 35
                height: 40
                
                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        specialItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ff8000"
                    anchors.left: itemImage_VohuManahShowdown.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Special Items - Sagittarius Showdown /////////

        ///////// Special Items - Sagittarius Showdown /////////
        Label {
            id: label_SagittariusShowdown

            color: "#00ff00"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Sagittarius Showdown"
        }

        Repeater {
            id: repeater_SagittariusShowdown
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_SagittariusShowdown.visible === true){
                    repeater_SagittariusShowdown.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_SagittariusShowdown.text].length; i++){
                        repeater_SagittariusShowdown.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_SagittariusShowdown.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_SagittariusShowdown
                source: imageSource
                width: 35
                height: 40
                
                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        specialItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#00ff00"
                    anchors.left: itemImage_SagittariusShowdown.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Special Items - Sagittarius Showdown /////////

        ///////// Special Items - Corow Showdown /////////
        Label {
            id: label_CorowShowdown

            color: "#ffff00"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Corow Showdown"
        }

        Repeater {
            id: repeater_CorowShowdown
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_CorowShowdown.visible === true){
                    repeater_CorowShowdown.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_CorowShowdown.text].length; i++){
                        repeater_CorowShowdown.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_CorowShowdown.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_CorowShowdown
                source: imageSource
                width: 35
                height: 40
                
                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        specialItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ffff00"
                    anchors.left: itemImage_CorowShowdown.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Special Items - Corow Showdown /////////

        ///////// Special Items - Diablo Showdown /////////
        Label {
            id: label_DiabloShowdown

            color: "#aa00ff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Diablo Showdown"
        }

        Repeater {
            id: repeater_DiabloShowdown
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_DiabloShowdown.visible === true){
                    repeater_DiabloShowdown.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_DiabloShowdown.text].length; i++){
                        repeater_DiabloShowdown.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_DiabloShowdown.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_DiabloShowdown
                source: imageSource
                width: 35
                height: 40
                
                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        specialItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#aa00ff"
                    anchors.left: itemImage_DiabloShowdown.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Special Items - Diablo Showdown /////////

        ///////// Special Items - Extreme Trials /////////
        Label {
            id: label_ExtremeTrials

            color: "#ffffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Extreme Trials"
        }

        Repeater {
            id: repeater_ExtremeTrials
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_ExtremeTrials.visible === true){
                    repeater_ExtremeTrials.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_ExtremeTrials.text].length; i++){
                        repeater_ExtremeTrials.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_ExtremeTrials.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_ExtremeTrials
                source: imageSource
                width: 35
                height: 40
                
                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        specialItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ffffff"
                    anchors.left: itemImage_ExtremeTrials.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Special Items - Extreme Trials /////////

        ///////// Special Items - Angel Halo /////////
        Label {
            id: label_AngelHalo

            color: "#ffffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 15
            font.letterSpacing: 1

            text: "Angel Halo"
        }

        Repeater {
            id: repeater_AngelHalo
            model: ListModel { }
            
            onVisibleChanged: {
                if(repeater_AngelHalo.visible === true){
                    repeater_AngelHalo.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_AngelHalo.text].length; i++){
                        repeater_AngelHalo.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_AngelHalo.text][i]))
                    }
                }
            }
        
            Image {
                id: itemImage_AngelHalo
                source: imageSource
                width: 35
                height: 40
                
                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        specialItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                Label {
                    color: "#ffffff"
                    anchors.left: itemImage_AngelHalo.right
                    anchors.leftMargin: 12
                    font.letterSpacing: 1
                    font.pointSize: 10
                    text: name
                }
            }
        }
        ///////// End of Special Items - Angel Halo /////////
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
