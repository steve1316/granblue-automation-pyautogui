import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

Button{
    id: toggleButton

    // Custom Properties
    property url buttonIconSource: "../../images/svg_images/menu_icon.svg"
    property color buttonColorDefault: "#242424"
    property color buttonColorMouseOver: "#323741"
    property color buttonColorClicked: "#00a1f1"

    QtObject{
        id: internal

        // This will control the color of the button when hovering over it and clicking it.
        property var dynamicColor: if(toggleButton.down){
                                       toggleButton.down ? buttonColorClicked : buttonColorDefault
                                   }else{
                                       toggleButton.hovered ? buttonColorMouseOver : buttonColorDefault
                                   }
    }

    implicitWidth: 70
    implicitHeight: 60

    background: Rectangle{
        id: buttonBackground
        
        color: internal.dynamicColor

        Image{
            id: buttonIcon

            source: buttonIconSource

            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter

            height: 25
            width: 25

            fillMode: Image.PreserveAspectFit

            visible: false
        }

        ColorOverlay{
            anchors.fill: buttonIcon
            source: buttonIcon

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
