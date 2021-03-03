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
                element: "Fire"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/shiva_icon.png"
                name: "Shiva"
                element: "Fire"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/agni_icon.png"
                name: "Agni"
                element: "Fire"
            }
        }

        ListModel {
            id: waterSummonsModel

            ListElement {
                imageSource: "../../../images/summons/icons/leviathan_omega_icon.png"
                name: "Leviathan Omega"
                element: "Water"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/europa_icon.png"
                name: "Europa"
                element: "Water"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/varuna_icon.png"
                name: "Varuna"
                element: "Water"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/bonito_icon.png"
                name: "Bonito"
                element: "Water"
            }
        }

        ListModel {
            id: earthSummonsModel

            ListElement {
                imageSource: "../../../images/summons/icons/yggdrasil_omega_icon.png"
                name: "Yggdrasil Omega"
                element: "Earth"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/godsworn_alexiel_icon.png"
                name: "Godsworn Alexiel"
                element: "Earth"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/titan_icon.png"
                name: "Titan"
                element: "Earth"
            }
        }

        ListModel {
            id: windSummonsModel

            ListElement {
                imageSource: "../../../images/summons/icons/tiamat_omega_icon.png"
                name: "Tiamat Omega"
                element: "Wind"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/grimnir_icon.png"
                name: "Grimnir"
                element: "Wind"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/zephyrus_icon.png"
                name: "Zephyrus"
                element: "Wind"
            }
        }

        ListModel {
            id: lightSummonsModel

            ListElement {
                imageSource: "../../../images/summons/icons/luminiera_omega_icon.png"
                name: "Luminiera Omega"
                element: "Light"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/lucifer_icon.png"
                name: "Lucifer"
                element: "Light"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/zeus_icon.png"
                name: "Zeus"
                element: "Light"
            }
        }

        ListModel {
            id: darkSummonsModel

            ListElement {
                imageSource: "../../../images/summons/icons/celeste_omega_icon.png"
                name: "Celeste Omega"
                element: "Dark"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/bahamut_icon.png"
                name: "Bahamut"
                element: "Dark"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/hades_icon.png"
                name: "Hades"
                element: "Dark"
            }
        }

        ListModel {
            id: miscSummonsModel

            ListElement {
                imageSource: "../../../images/summons/icons/huanglong_icon.png"
                name: "Huanglong"
                element: "Misc"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/qilin_icon.png"
                name: "Qilin"
                element: "Misc"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/kaguya_icon.png"
                name: "Kaguya"
                element: "Misc"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/white_rabbit_icon.png"
                name: "White Rabbit"
                element: "Misc"
            }

            ListElement {
                imageSource: "../../../images/summons/icons/black_rabbit_icon.png"
                name: "Black Rabbit"
                element: "Misc"
            }
        }

        ///////// Fire Summons /////////
        Label {
            color: "#aa0000"
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
                        backend.update_summon_list(name, element)
                    }
                }

                source: imageSource
                Label {
                    color: "#aa0000"
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
            color: "#00ffff"
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
                        backend.update_summon_list(name, element)
                    }
                }

                source: imageSource
                Label {
                    color: "#00ffff"
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
            color: "#ff8000"
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
                        backend.update_summon_list(name, element)
                    }
                }

                source: imageSource
                Label {
                    color: "#ff8000"
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
            color: "#00ff00"
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
                        backend.update_summon_list(name, element)
                    }
                }

                source: imageSource
                Label {
                    color: "#00ff00"
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
            color: "#ffff00"
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
                        backend.update_summon_list(name, element)
                    }
                }

                source: imageSource
                Label {
                    color: "#ffff00"
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
            color: "#aa00ff"
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
                        backend.update_summon_list(name, element)
                    }
                }

                source: imageSource
                Label {
                    color: "#aa00ff"
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
                        backend.update_summon_list(name, element)
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
