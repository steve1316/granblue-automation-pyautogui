import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

Button {
    id: button

    // Custom Properties
    property int customRadius: 10
    property color colorDefault: "#4891d9"
    property color colorMouseOver: "#55AAFF"
    property color colorPressed: "#3F7EBD"

    QtObject{
        id: internal

        property var dynamicColor: if(button.down){
                                       button.down ? colorPressed : colorDefault
                                   }else{
                                       button.hovered ? colorMouseOver : colorDefault
                                   }
    }

    text: qsTr("Placeholder")

    contentItem: Item{
        Text {
            id: buttonText
            text: button.text
            font: button.font
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
