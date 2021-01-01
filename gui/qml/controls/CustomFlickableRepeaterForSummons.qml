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

        ListModel {
            id: fireSummonsModel

            ListElement {
                imageSource: "../../../images/summons/icons/colossus_omega_icon.png"
                name: "Colossus Omega"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/shiva_icon.png"
                name: "Shiva"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/agni_icon.png"
                name: "Agni"
            }
        }

        ListModel {
            id: waterSummonsModel

            ListElement {
                imageSource: "../../../images/summons/icons/leviathan_omega_icon.png"
                name: "Leviathan Omega"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/europa_icon.png"
                name: "Europa"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/varuna_icon.png"
                name: "Varuna"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/bonito_icon.png"
                name: "Bonito"
            }
        }

        ListModel {
            id: earthSummonsModel

            ListElement {
                imageSource: "../../../images/summons/icons/yggdrasil_omega_icon.png"
                name: "Yggdrasil Omega"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/godsworn_alexiel_icon.png"
                name: "Godsworn Alexiel"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/titan_icon.png"
                name: "Titan"
            }
        }

        ListModel {
            id: windSummonsModel

            ListElement {
                imageSource: "../../../images/summons/icons/tiamat_omega_icon.png"
                name: "Tiamat Omega"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/grimnir_icon.png"
                name: "Grimnir"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/zephyrus_icon.png"
                name: "Zephyrus"
            }
        }

        ListModel {
            id: lightSummonsModel

            ListElement {
                imageSource: "../../../images/summons/icons/luminiera_omega_icon.png"
                name: "Luminiera Omega"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/lucifer_icon.png"
                name: "Lucifer"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/zeus_icon.png"
                name: "Zeus"
            }
        }

        ListModel {
            id: darkSummonsModel

            ListElement {
                imageSource: "../../../images/summons/icons/celeste_omega_icon.png"
                name: "Celeste Omega"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/bahamut_icon.png"
                name: "Bahamut"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/hades_icon.png"
                name: "Hades"
            }
        }

        ListModel {
            id: miscSummonsModel

            ListElement {
                imageSource: "../../../images/summons/icons/huanglong_icon.png"
                name: "Huanglong"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/qilin_icon.png"
                name: "Qilin"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/kaguya_icon.png"
                name: "Kaguya"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/white_rabbit_icon.png"
                name: "White Rabbit"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/black_rabbit_icon.png"
                name: "Black Rabbit"
            }
        }

        ///////// Fire Summons /////////
        Label {
            color: "#ff0033"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 12
            font.letterSpacing: 1

            text: "Fire Summons"
        }

        Repeater {
            model: fireSummonsModel
            Image {
                id: fireSummonImage

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        console.log("Selected " + name)
                        popup.close()
                    }
                }

                source: imageSource
                Label {
                    color: "#ff0033"
                    anchors.left: fireSummonImage.right
                    anchors.leftMargin: 10
                    font.letterSpacing: 1
                    font.pointSize: 9
                    text: name
                }
            }
        }
        ///////// End of Fire Summons /////////

        ///////// Water Summons /////////
        Label {
            color: "#00eeff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 12
            font.letterSpacing: 1

            text: "Water Summons"
        }

        Repeater {
            model: waterSummonsModel
            Image {
                id: waterSummonImage

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        console.log("Selected " + name)
                        popup.close()
                    }
                }

                source: imageSource
                Label {
                    color: "#00eeff"
                    anchors.left: waterSummonImage.right
                    anchors.leftMargin: 10
                    font.letterSpacing: 1
                    font.pointSize: 9
                    text: name
                }
            }
        }
        ///////// End of Water Summons /////////

        ///////// Earth Summons /////////
        Label {
            color: "#d2691e"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 12
            font.letterSpacing: 1

            text: "Earth Summons"
        }

        Repeater {
            model: earthSummonsModel
            Image {
                id: earthSummonImage

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        console.log("Selected " + name)
                        popup.close()
                    }
                }

                source: imageSource
                Label {
                    color: "#d2691e"
                    anchors.left: earthSummonImage.right
                    anchors.leftMargin: 10
                    font.letterSpacing: 1
                    font.pointSize: 9
                    text: name
                }
            }
        }
        ///////// End of Earth Summons /////////

        ///////// Wind Summons /////////
        Label {
            color: "#0dff0d"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 12
            font.letterSpacing: 1

            text: "Wind Summons"
        }

        Repeater {
            model: windSummonsModel
            Image {
                id: windSummonImage

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        console.log("Selected " + name)
                        popup.close()
                    }
                }

                source: imageSource
                Label {
                    color: "#0dff0d"
                    anchors.left: windSummonImage.right
                    anchors.leftMargin: 10
                    font.letterSpacing: 1
                    font.pointSize: 9
                    text: name
                }
            }
        }
        ///////// End of Wind Summons /////////

        ///////// Light Summons /////////
        Label {
            color: "#fbff00"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 12
            font.letterSpacing: 1

            text: "Light Summons"
        }

        Repeater {
            model: lightSummonsModel
            Image {
                id: lightSummonImage

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        console.log("Selected " + name)
                        popup.close()
                    }
                }

                source: imageSource
                Label {
                    color: "#fbff00"
                    anchors.left: lightSummonImage.right
                    anchors.leftMargin: 10
                    font.letterSpacing: 1
                    font.pointSize: 9
                    text: name
                }
            }
        }
        ///////// End of Light Summons /////////

        ///////// Dark Summons /////////
        Label {
            color: "#6a0c8a"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 12
            font.letterSpacing: 1

            text: "Dark Summons"
        }

        Repeater {
            model: darkSummonsModel
            Image {
                id: darkSummonImage

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        console.log("Selected " + name)
                        popup.close()
                    }
                }

                source: imageSource
                Label {
                    color: "#6a0c8a"
                    anchors.left: darkSummonImage.right
                    anchors.leftMargin: 10
                    font.letterSpacing: 1
                    font.pointSize: 9
                    text: name
                }
            }
        }
        ///////// End of Dark Summons /////////

        ///////// Misc Summons /////////
        Label {
            color: "#ffffff"
            anchors.left: parent.left
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.underline: true
            font.pointSize: 12
            font.letterSpacing: 1

            text: "Misc Summons"
        }

        Repeater {
            model: miscSummonsModel
            Image {
                id: miscSummonImage

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        console.log("Selected " + name)
                        popup.close()
                    }
                }

                source: imageSource
                Label {
                    color: "#ffffff"
                    anchors.left: miscSummonImage.right
                    anchors.leftMargin: 10
                    font.letterSpacing: 1
                    font.pointSize: 9
                    text: name
                }
            }
        }
        ///////// End of Misc Summons /////////
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
