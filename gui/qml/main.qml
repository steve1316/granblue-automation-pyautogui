import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15
import "controls"

Window {
    id: mainWindow

    width: 1250
    height: 600

    minimumWidth: 1000
    minimumHeight: 600

    visible: true

    color: "#00000000"
    title: qsTr("Granblue Automation")

    // Removes the default window title bar.
    flags: Qt.Window | Qt.FramelessWindowHint

    // Custom Properties
    property int windowStatus: 0
    property int windowMargin: 10

    // Internal functions
    QtObject{
        id: internal

        // Removes or adds back in the window margins when maximizing or restoring. Also change the visibility of all the resizes to false.
        function maximizeRestore(){
            if(windowStatus == 0){
                mainWindow.showMaximized()
                windowStatus = 1
                windowMargin = 0

                internal.hideResizeArea()

                buttonMaximize.buttonIconSource = "../images/svg_images/restore_icon.svg"
            }else{
                mainWindow.showNormal()
                windowStatus = 0
                windowMargin = 10

                internal.showResizeArea()

                buttonMaximize.buttonIconSource = "../images/svg_images/maximize_icon.svg"
            }
        }

        // Reset the window back to normal when dragging the title bar around.
        function restoreWindowStatus(){
            if(windowStatus == 1){
                mainWindow.showNormal()
                windowStatus = 0
                windowMargin = 10

                internal.showResizeArea()

                buttonMaximize.buttonIconSource = "../images/svg_images/maximize_icon.svg"
            }
        }

        // Restore the window status and margins to default when restoring the window to normal.
        function restoreWindowMargin(){
            windowStatus = 0
            windowMargin = 10

            internal.showResizeArea()

            buttonMaximize.buttonIconSource = "../images/svg_images/maximize_icon.svg"
        }

        // Hides the resizing arrows when the window is maximized.
        function hideResizeArea(){
            resizeWindowBottomRight.visible = false
            resizeWindowLeft.visible = false
            resizeWindowRight.visible = false
            resizeWindowBottom.visible = false
        }

        // Restores the resizing arrows when the window is normal.
        function showResizeArea(){
            resizeWindowBottomRight.visible = true
            resizeWindowLeft.visible = true
            resizeWindowRight.visible = true
            resizeWindowBottom.visible = true
        }
    }

    Rectangle {
        id: background

        color: "#40405f"
        border.color: "#49496b"
        border.width: 1

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.rightMargin: windowMargin
        anchors.leftMargin: windowMargin
        anchors.bottomMargin: windowMargin
        anchors.topMargin: windowMargin

        z: 1

        Rectangle {
            id: container

            color: "#00000000"

            anchors.fill: parent
            anchors.rightMargin: 1
            anchors.leftMargin: 1
            anchors.bottomMargin: 1
            anchors.topMargin: 1

            Rectangle {
                id: topBar

                height: 60
                color: "#242424"

                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.rightMargin: 0
                anchors.leftMargin: 0
                anchors.topMargin: 0

                ToggleButton {
                    // When clicking the button, run LeftMenu's PropertyAnimation function.
                    onClicked: animationMenu.running = true
                }

                Rectangle {
                    id: topBarDescriptionContainer

                    y: 32
                    height: 25
                    color: "#272741"

                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.bottom: parent.bottom
                    anchors.rightMargin: 0
                    anchors.leftMargin: 70
                    anchors.bottomMargin: 0

                    Label {
                        id: topBarLeftLabel

                        color: "#d9d9d9"
                        text: qsTr("Bot Status: Not Running")

                        verticalAlignment: Text.AlignVCenter

                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        anchors.rightMargin: 300
                        anchors.leftMargin: 10
                        anchors.bottomMargin: 0
                        anchors.topMargin: 0
                    }

                    Label {
                        id: topBarRightLabel

                        color: "#d9d9d9"
                        text: qsTr("| HOME")

                        horizontalAlignment: Text.AlignRight
                        verticalAlignment: Text.AlignVCenter

                        anchors.left: topBarLeftLabel.right
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        anchors.rightMargin: 10
                        anchors.leftMargin: 0
                        anchors.bottomMargin: 0
                        anchors.topMargin: 0
                    }
                }

                Rectangle {
                    id: titleBar

                    height: 35
                    color: "#00000000"

                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.rightMargin: 105
                    anchors.leftMargin: 70
                    anchors.topMargin: 0

                    // This DragHandler will handle moving the window around as removing the default title bar disabled it.
                    DragHandler{
                        onActiveChanged: if(active){
                                             mainWindow.startSystemMove()

                                             internal.restoreWindowStatus()
                                         }
                    }

                    Image {
                        id: appIcon

                        width: 22
                        height: 22

                        anchors.left: parent.left
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        anchors.leftMargin: 5
                        anchors.bottomMargin: 0
                        anchors.topMargin: 0

                        source: "../images/svg_images/icon_app_top.svg"
                        fillMode: Image.PreserveAspectFit
                    }

                    Label {
                        id: appNameLabel

                        color: "#ffffff"
                        text: qsTr("Granblue Automation")
                        font.pointSize: 10

                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        
                        anchors.left: appIcon.right
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        anchors.leftMargin: 5
                    }
                }

                Row {
                    id: windowButtonsRow

                    x: 764
                    width: 105
                    height: 35

                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.rightMargin: 0
                    anchors.topMargin: 0

                    // This button minimizes the window.
                    TopBarButton{
                        id: buttonMinimize

                        onClicked: {
                            mainWindow.showMinimized()
                            internal.restoreWindowMargin()
                        }
                    }

                    // This button maximizes or restores the window.
                    TopBarButton {
                        id: buttonMaximize
                        
                        buttonIconSource: "../images/svg_images/maximize_icon.svg"

                        onClicked: internal.maximizeRestore()
                    }

                    // This button exits the application.
                    TopBarButton {
                        id: buttonClose
                        
                        buttonColorClicked: "#cc0000"
                        buttonIconSource: "../images/svg_images/close_icon.svg"

                        onClicked: mainWindow.close()
                    }
                }

                MouseArea {
                    id: topBarMouseAreaForMaximizeRestore

                    x: 75
                    y: 0

                    anchors.left: parent.left
                    anchors.right: windowButtonsRow.left
                    anchors.top: parent.top
                    anchors.bottom: topBarDescriptionContainer.top
                    anchors.rightMargin: 0
                    anchors.leftMargin: 70
                    anchors.bottomMargin: 0
                    anchors.topMargin: 0

                    // Double clicking this area will maximize or restore the window.
                    onDoubleClicked: internal.maximizeRestore()
                }

                MouseArea {
                    id: resizeWindowTopRight

                    x: 963
                    y: -10
                    width: 10
                    height: 10

                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.rightMargin: -5
                    anchors.topMargin: -5

                    cursorShape: Qt.SizeBDiagCursor

                    // Resize the window by dragging the top right corner.
                    DragHandler {
                        target: null
                        onActiveChanged: if(active){
                                             mainWindow.startSystemResize(Qt.RightEdge | Qt.TopEdge)
                                         }
                    }
                }
            }

            Rectangle {
                id: contentContainer

                color: "#00000000"

                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: topBar.bottom
                anchors.bottom: parent.bottom
                anchors.topMargin: 0

                Rectangle {
                    id: leftMenu

                    width: 70
                    color: "#242424"

                    clip: true

                    anchors.left: parent.left
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    anchors.topMargin: 0
                    anchors.bottomMargin: 0
                    anchors.leftMargin: 0

                    // PropertyAnimation will handle the LeftMenu's width when expanding and retracting.
                    PropertyAnimation{
                        id: animationMenu
                        target: leftMenu

                        property: "width"
                        to: if(leftMenu.width == 70){
                                return 200;
                            }else{
                                return 70;
                            }

                        duration: 500
                        easing.type: Easing.InOutBack
                    }

                    Column {
                        id: leftMenuColumn

                        width: 70

                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        anchors.rightMargin: 0
                        anchors.leftMargin: 0
                        anchors.bottomMargin: 90
                        anchors.topMargin: 0

                        LeftMenu {
                            id: homeButton

                            width: leftMenu.width

                            text: qsTr("Home")

                            buttonColorMouseOver: "#323741"
                            isActiveMenu: true

                            // Clicking this will set the Home Page as visible and hides the Settings Page.
                            onClicked: {
                                if(homeButton.isActiveMenu == false){
                                    homeButton.isActiveMenu = true
                                    settingsButton.isActiveMenu = false

                                    //stackView.push(Qt.resolvedUrl("pages/HomePage.qml"))
                                    pageHomeLoader.visible = true
                                    pageSettingsLoader.visible = false

                                    topBarRightLabel.text = qsTr("| HOME")
                                }
                            }
                        }

                        LeftMenu {
                            id: settingsButton

                            width: leftMenu.width

                            text: qsTr("Settings")

                            buttonColorMouseOver: "#323741"
                            buttonIconSource: "../images/svg_images/settings_icon.svg"

                            // Clicking this will set the Settings Page as visible and hides the Home Page.
                            onClicked: {
                                if(settingsButton.isActiveMenu == false){
                                    homeButton.isActiveMenu = false
                                    settingsButton.isActiveMenu = true

                                    //stackView.push(Qt.resolvedUrl("pages/SettingsPage.qml"))
                                    pageHomeLoader.visible = false
                                    pageSettingsLoader.visible = true

                                    topBarRightLabel.text = qsTr("| SETTINGS")
                                }
                            }
                        }
                    }

                    MouseArea {
                        id: resizeWindowBottomLeft

                        x: 65
                        y: 493
                        width: 10
                        height: 10

                        anchors.left: parent.left
                        anchors.bottom: parent.bottom
                        anchors.bottomMargin: -5
                        anchors.leftMargin: -5

                        cursorShape: Qt.SizeBDiagCursor

                        // Resize the window by dragging the bottom left corner.
                        DragHandler {
                            target: null
                            onActiveChanged: if(active){
                                                 mainWindow.startSystemResize(Qt.LeftEdge | Qt.BottomEdge)
                                             }
                        }
                    }

                    MouseArea {
                        id: resizeWindowTopLeft

                        x: 62
                        width: 15
                        height: 15

                        anchors.left: parent.left
                        anchors.top: parent.top
                        anchors.topMargin: -68
                        anchors.leftMargin: -7

                        cursorShape: Qt.SizeFDiagCursor

                        // Resize the window by dragging the top left corner.
                        DragHandler {
                            target: null
                            onActiveChanged: if(active){
                                                 mainWindow.startSystemResize(Qt.LeftEdge | Qt.TopEdge)
                                             }
                        }
                    }
                }

                Rectangle {
                    id: contentAreaContainer

                    color: "#2e2e4d"

                    clip: true

                    anchors.left: leftMenu.right
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    anchors.rightMargin: 0
                    anchors.leftMargin: 0
                    anchors.bottomMargin: 25
                    anchors.topMargin: 0

                    Rectangle {
                        id: scrollingViewContainer

                        y: 38
                        color: "#2f2f2f"
                        radius: 10

                        clip: false

                        anchors.left: parent.left
                        anchors.right: pageHomeLoader.left
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        anchors.rightMargin: 20
                        anchors.leftMargin: 20
                        anchors.bottomMargin: 20
                        anchors.topMargin: 20

                        Flickable {
                            id: scrollingView

                            x: -10
                            y: 0

                            clip: true

                            anchors.left: parent.left
                            anchors.right: parent.right
                            anchors.top: parent.top
                            anchors.bottom: parent.bottom
                            anchors.rightMargin: 10
                            anchors.leftMargin: 10
                            anchors.bottomMargin: 10
                            anchors.topMargin: 10

                            contentHeight: logTextArea.contentHeight + 50 // Update the scrollingView's content height to always have room for the console log text.
                            //contentWidth: 280

                            // Create a vertical ScrollBar for this Flickable component.
                            ScrollBar.vertical: ScrollBar {
                                id: verticalScrollBar
                                policy: ScrollBar.AlwaysOn // Always display the vertical scrollbar.
                            }

                            // Create a horizontal ScrollBar for this Flickable component.
//                            ScrollBar.horizontal: ScrollBar {
//                                id: horizontalScrollBar
//                                 policy: ScrollBar.AsNeeded // Only display the horizontal scrollbar when needed.
//                            }

                            // Adjust the scroll bars depending on arrow keys pressed.
                            Keys.onUpPressed: verticalScrollBar.decrease()
                            Keys.onDownPressed: verticalScrollBar.increase()

                            // Keys.onLeftPressed: horizontalScrollBar.decrease()
                            // Keys.onRightPressed: horizontalScrollBar.increase()

                            // Adjust the vertical scroll bar when using the mouse wheel.
                            MouseArea{
                                anchors.fill: parent

                                onWheel: {
                                    if(wheel.angleDelta.y > 0){
                                        verticalScrollBar.decrease()
                                    }
                                    else if(wheel.angleDelta.y < 0){
                                        verticalScrollBar.increase()
                                    }
                                }
                            }
                            

                            TextArea.flickable: TextArea {
                                id: logTextArea

                                color: "#ffffff"

                                text: `Welcome to Granblue Automation! 
                                \n*************************** 
                                \nInstructions\n----------------
                                \nNote: The START button is disabled until the following steps are followed through.
                                \n1. Please have your game window fully visible.
                                \n2. Go into the Settings Page and select your combat script and select the item and amount that you want to farm for.
                                \n3. You can head back to the Home Page and click START.
                                \n\n***************************`
                                font.pixelSize: 12
                                textMargin: 5
                                textFormat: Text.AutoText

                                horizontalAlignment: Text.AlignLeft
                                verticalAlignment: Text.AlignTop
                                wrapMode: Text.NoWrap

                                clip: false
                                
                                readOnly: true
                                selectByMouse: true
                                selectedTextColor: "#ffffffff"
                                selectionColor: "#ff007f"

                                bottomPadding: 10 // This is necessary to prevent any newly appended messages from getting partially cut off at the bottom.
                        
                                anchors.left: parent.left
                                anchors.right: parent.right
                                anchors.top: parent.top
                                anchors.bottom: parent.bottom
                                anchors.rightMargin: 10
                                anchors.leftMargin: 10
                                anchors.bottomMargin: 10
                                anchors.topMargin: 10
                            }
                        }
                    }

//                    StackView {
//                        id: stackView
//                        anchors.left: parent.left
//                        anchors.right: parent.right
//                        anchors.top: parent.top
//                        anchors.bottom: parent.bottom
//                        anchors.topMargin: 20
//                        anchors.bottomMargin: 20
//                        anchors.leftMargin: 500
//                        anchors.rightMargin: 20

//                        initialItem: Qt.resolvedUrl("pages/HomePage.qml")
//                    }

                    Loader{
                        id: pageHomeLoader

                        width: 300

                        source: Qt.resolvedUrl("pages/HomePage.qml")

                        visible: true

                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        anchors.topMargin: 20
                        anchors.bottomMargin: 20
                        anchors.rightMargin: 20
                    }

                    Loader{
                        id: pageSettingsLoader

                        width: 300

                        source: Qt.resolvedUrl("pages/SettingsPage.qml")

                        visible: false

                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        anchors.topMargin: 20
                        anchors.bottomMargin: 20
                        anchors.rightMargin: 20
                    }
                }

                Rectangle {
                    id: bottomBar

                    color: "#272741"

                    anchors.left: leftMenu.right
                    anchors.right: parent.right
                    anchors.top: contentAreaContainer.bottom
                    anchors.bottom: parent.bottom
                    anchors.rightMargin: 0
                    anchors.leftMargin: 0
                    anchors.bottomMargin: 0
                    anchors.topMargin: 0

                    Label {
                        id: bottomInfoLabel

                        x: 10
                        y: -2

                        color: "#d9d9d9"

                        text: qsTr("It is like Full Auto, but with Full Customization!")

                        verticalAlignment: Text.AlignVCenter
                        
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        anchors.topMargin: 0
                        anchors.rightMargin: 310
                        anchors.leftMargin: 10
                        anchors.bottomMargin: 0
                    }

                    MouseArea {
                        id: resizeWindowBottomRight

                        x: 894
                        y: 8

                        width: 10
                        height: 10

                        anchors.right: parent.right
                        anchors.bottom: parent.bottom
                        anchors.rightMargin: -5
                        anchors.bottomMargin: -5

                        cursorShape: Qt.SizeFDiagCursor

                        // Resize the window by dragging the bottom right corner.
                        DragHandler{
                            target: null
                            onActiveChanged: if(active){
                                                 mainWindow.startSystemResize(Qt.RightEdge | Qt.BottomEdge)
                                             }
                        }

                    }

                    Image {
                        id: resizeCornerImage

                        x: 891
                        y: 8

                        width: 25
                        height: 25

                        source: "../images/svg_images/resize_icon.svg"
                        sourceSize.height: 300
                        sourceSize.width: 300
                        fillMode: Image.PreserveAspectFit

                        antialiasing: false
                        opacity: 0.5

                        anchors.right: parent.right
                        anchors.bottom: parent.bottom
                        anchors.rightMargin: 0
                        anchors.bottomMargin: 0
                    }
                }
            }
        }
    }

    // This drop shadow effect will appear below the window.
    DropShadow{
        anchors.fill: background

        color: "#80000000"

        horizontalOffset: 0
        verticalOffset: 0

        radius: 12
        samples: 16
        
        source: background
        z: 0 // The background container has its z set to 1.
    }

    MouseArea {
        id: resizeWindowLeft

        width: 10

        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 10
        anchors.leftMargin: 0
        anchors.topMargin: 10

        cursorShape: Qt.SizeHorCursor

        // Resize the window by dragging the left side of the window.
        DragHandler{
            target: null
            onActiveChanged: if(active){
                                 mainWindow.startSystemResize(Qt.LeftEdge)
                             }
        }
    }

    MouseArea {
        id: resizeWindowRight

        width: 10

        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 10
        anchors.topMargin: 10
        anchors.rightMargin: 0

        cursorShape: Qt.SizeHorCursor

        // Resize the window by dragging the right side of the window.
        DragHandler{
            target: null
            onActiveChanged: if(active){
                                 mainWindow.startSystemResize(Qt.RightEdge)
                             }
        }
    }

    MouseArea {
        id: resizeWindowBottom

        height: 10

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.rightMargin: 10
        anchors.leftMargin: 10
        anchors.bottomMargin: 0

        cursorShape: Qt.SizeVerCursor

        // Resize the window by dragging the bottom side of the window.
        DragHandler{
            target: null
            onActiveChanged: if(active){
                                 mainWindow.startSystemResize(Qt.BottomEdge)
                             }
        }
    }

    MouseArea {
        id: resizeWindowTop

        height: 10

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.topMargin: 0
        anchors.rightMargin: 10
        anchors.leftMargin: 10

        cursorShape: Qt.SizeVerCursor

        // Resize the window by dragging the top side of the window.
        DragHandler{
            target: null
            onActiveChanged: if(active){
                                 mainWindow.startSystemResize(Qt.TopEdge)
                             }
        }
    }
}













/*##^##
Designer {
    D{i:0;formeditorZoom:0.66}
}
##^##*/
