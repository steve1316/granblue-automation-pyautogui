import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

Button{
    id: toggle_button

    // Custom Properties
    property url buttonIconSource: "../../images/svg_images/menu_icon.svg"
    property color buttonColorDefault: "#242424"
    property color buttonColorMouseOver: "#323741"
    property color buttonColorClicked: "#00a1f1"

    QtObject{
        id: internal

        // This will control the color of the button when hovering over it and clicking it.
        property var dynamicColor: if(toggle_button.down){
                                       toggle_button.down ? buttonColorClicked : buttonColorDefault
                                   }else{
                                       toggle_button.hovered ? buttonColorMouseOver : buttonColorDefault
                                   }
    }

    implicitWidth: 70
    implicitHeight: 60

    background: Rectangle{
        id: button_background
        color: internal.dynamicColor

        Image{
            id: button_icon
            source: buttonIconSource

            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter

            height: 25
            width: 25

            fillMode: Image.PreserveAspectFit

            visible: false
        }

        ColorOverlay{
            anchors.fill: button_icon
            source: button_icon

            color: "#ffffff"

            antialiasing: false
        }
    }
}

/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:2;height:60;width:60}
}
##^##*/
