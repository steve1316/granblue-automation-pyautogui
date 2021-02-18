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

        // List model that holds all the Quest items that are supported.
        ListModel {
            id: itemsModel

            property var listOfItems: {
                "Port Breeze Archipelago": ["Satin Feather", "Zephyr Feather", "Flying Sprout"],
                "Valtz Duchy": ["Fine Sand Bottle", "Untamed Flame", "Blistering Ore"],
                "Auguste Isles": ["Fresh Water Jug", "Soothing Splash", "Glowing Coral"],
                "Lumacie Archipelago": ["Rough Stone", "Swirling Amber", "Coarse Alluvium"],
                "Albion Citadel": ["Falcon Feather", "Spring Water Jug", "Vermilion Stone"],
                "Mist-Shrouded Isle": ["Slimy Shroom", "Hollow Soul", "Lacrimosa"],
                "Golonzo Island": ["Wheat Stalk", "Iron Cluster", "Olea Plant"],
                "Amalthea Island": ["Indigo Fruit", "Foreboding Clover", "Blood Amber"],
                "Former Capital Mephorash": ["Sand Brick", "Native Reed", "Antique Cloth"],
                "Agastia": ["Prosperity Flame", "Explosive Material", "Steel Liquid"],
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
            id: label_PortBreezeArchipelago

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
            id: repeater_PortBreezeArchipelago
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_PortBreezeArchipelago.visible === true){
                    repeater_PortBreezeArchipelago.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_PortBreezeArchipelago.text].length; i++){
                        repeater_PortBreezeArchipelago.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_PortBreezeArchipelago.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_PortBreezeArchipelago
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        questItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_ValtzDuchy

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
            id: repeater_ValtzDuchy
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_ValtzDuchy.visible === true){
                    repeater_ValtzDuchy.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_ValtzDuchy.text].length; i++){
                        repeater_ValtzDuchy.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_ValtzDuchy.text][i]))
                    }
                }
            }
            
            Image {
                id: itemImage_ValtzDuchy
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        questItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_AugusteIsles

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
            id: repeater_AugusteIsles
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_AugusteIsles.visible === true){
                    repeater_AugusteIsles.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_AugusteIsles.text].length; i++){
                        repeater_AugusteIsles.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_AugusteIsles.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_AugusteIsles
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        questItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_LumacieArchipelago

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
            id: repeater_LumacieArchipelago
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_LumacieArchipelago.visible === true){
                    repeater_LumacieArchipelago.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_LumacieArchipelago.text].length; i++){
                        repeater_LumacieArchipelago.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_LumacieArchipelago.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_LumacieArchipelago
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        questItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_AlbionCitadel

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
            id: repeater_AlbionCitadel
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_AlbionCitadel.visible === true){
                    repeater_AlbionCitadel.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_AlbionCitadel.text].length; i++){
                        repeater_AlbionCitadel.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_AlbionCitadel.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_AlbionCitadel
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        questItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_MistShroudedIsle

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
            id: repeater_MistShroudedIsle
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_MistShroudedIsle.visible === true){
                    repeater_MistShroudedIsle.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_MistShroudedIsle.text].length; i++){
                        repeater_MistShroudedIsle.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_MistShroudedIsle.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_MistShroudedIsle
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        questItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_GolonzoIsland

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
            id: repeater_GolonzoIsland
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_GolonzoIsland.visible === true){
                    repeater_GolonzoIsland.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_GolonzoIsland.text].length; i++){
                        repeater_GolonzoIsland.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_GolonzoIsland.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_GolonzoIsland
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        questItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_AmaltheaIsland

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
            id: repeater_AmaltheaIsland
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_AmaltheaIsland.visible === true){
                    repeater_AmaltheaIsland.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_AmaltheaIsland.text].length; i++){
                        repeater_AmaltheaIsland.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_AmaltheaIsland.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_AmaltheaIsland
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        questItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_FormerCapitalMephorash

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
            id: repeater_FormerCapitalMephorash
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_FormerCapitalMephorash.visible === true){
                    repeater_FormerCapitalMephorash.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_FormerCapitalMephorash.text].length; i++){
                        repeater_FormerCapitalMephorash.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_FormerCapitalMephorash.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_FormerCapitalMephorash
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        questItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
            id: label_Agastia

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
            id: repeater_Agastia
            model: ListModel { }

            onVisibleChanged: {
                if(repeater_Agastia.visible === true){
                    repeater_Agastia.model.clear()
                    for(var i = 0; i < itemsModel.listOfItems[label_Agastia.text].length; i++){
                        repeater_Agastia.model.append(itemsModel.createListElement(itemsModel.listOfItems[label_Agastia.text][i]))
                    }
                }
            }

            Image {
                id: itemImage_Agastia
                source: imageSource
                width: 35
                height: 40

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        backend.update_item_name(name)
                        questItemsPopup.close()
                        itemSelectionButton.text = name
                    }
                }

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
