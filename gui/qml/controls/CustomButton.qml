import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

Button {
    id: customButton

    // Custom Properties
    property int customRadius: 10
    property color colorDefault: "#4891d9"
    property color colorMouseOver: "#55AAFF"
    property color colorPressed: "#3F7EBD"

    QtObject{
        id: internal

        property var dynamicColor: if(customButton.down){
                                       customButton.down ? colorPressed : colorDefault
                                   }else{
                                       customButton.hovered ? colorMouseOver : colorDefault
                                   }
    }

    text: qsTr("Placeholder text")

    contentItem: Item{
        Text {
            id: customButtonText
            text: customButton.text
            font: customButton.font
            color: "#ffffff"
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }

    background: Rectangle{
        color: internal.dynamicColor
        radius: customRadius
    }
}
