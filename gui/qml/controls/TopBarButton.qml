import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

Button{
    id: topBarButton

    // Custom Properties
    property url buttonIconSource: "../../images/svg_images/minimize_icon.svg"
    property color buttonColorDefault: "#242424"
    property color buttonColorMouseOver: "#323741"
    property color buttonColorClicked: "#00a1f1"

    QtObject{
        id: internal

        // This will control the color of the button when hovering over it and clicking it.
        property var dynamicColor: if(topBarButton.down){
                                       topBarButton.down ? buttonColorClicked : buttonColorDefault
                                   }else{
                                       topBarButton.hovered ? buttonColorMouseOver : buttonColorDefault
                                   }
    }

    width: 35
    height: 35

    background: Rectangle{
        id: buttonBackground

        color: internal.dynamicColor

        Image{
            id: buttonIcon
            source: buttonIconSource

            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter

            height: 16
            width: 16

            fillMode: Image.PreserveAspectFit

            visible: false

            antialiasing: false
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
    D{i:0;formeditorZoom:8;height:35;width:35}
}
##^##*/
