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

        ///////// Special Items - Scarlet Trial /////////
        Label {
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
            model: specialItemsModel_ScarletTrial
            Image {
                id: itemImage_ScarletTrial

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        specialItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
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
            model: specialItemsModel_CeruleanTrial
            Image {
                id: itemImage_CeruleanTrial

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        specialItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
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
            model: specialItemsModel_VioletTrial
            Image {
                id: itemImage_VioletTrial

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        specialItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
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
            model: specialItemsModel_ShinySlimeSearch
            Image {
                id: itemImage_ShinySlimeSearch

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        specialItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
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
            model: specialItemsModel_SixDragonTrials
            Image {
                id: itemImage_SixDragonTrials

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        specialItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
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
            model: specialItemsModel_IfritShowdown
            Image {
                id: itemImage_IfritShowdown

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        specialItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
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
            model: specialItemsModel_CocytusShowdown
            Image {
                id: itemImage_CocytusShowdown

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        specialItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
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
            model: specialItemsModel_VohuManahShowdown
            Image {
                id: itemImage_VohuManahShowdown

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        specialItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
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
            model: specialItemsModel_SagittariusShowdown
            Image {
                id: itemImage_SagittariusShowdown

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        specialItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
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
            model: specialItemsModel_CorowShowdown
            Image {
                id: itemImage_CorowShowdown

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        specialItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
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
            model: specialItemsModel_DiabloShowdown
            Image {
                id: itemImage_DiabloShowdown

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        specialItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
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
            model: specialItemsModel_ExtremeTrials
            Image {
                id: itemImage_ExtremeTrials

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        specialItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
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
            model: specialItemsModel_AngelHalo
            Image {
                id: itemImage_AngelHalo

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        specialItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

                source: imageSource
                width: 35
                height: 40
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
