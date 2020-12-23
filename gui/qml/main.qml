import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15
import "controls"

Window {
    id: main_window
    width: 1200
    height: 600

    minimumWidth: 1000
    minimumHeight: 400

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
                main_window.showMaximized()
                windowStatus = 1
                windowMargin = 0

                internal.hideResizeArea()

                buttonMaximize.buttonIconSource = "../images/svg_images/restore_icon.svg"
            }else{
                main_window.showNormal()
                windowStatus = 0
                windowMargin = 10

                internal.showResizeArea()

                buttonMaximize.buttonIconSource = "../images/svg_images/maximize_icon.svg"
            }
        }

        // Reset the window back to normal when dragging the title bar around.
        function restoreWindowStatus(){
            if(windowStatus == 1){
                main_window.showNormal()
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
            resize_window_bottomright.visible = false
            resize_left.visible = false
            resize_right.visible = false
            resize_bottom.visible = false
        }

        // Restores the resizing arrows when the window is normal.
        function showResizeArea(){
            resize_window_bottomright.visible = true
            resize_left.visible = true
            resize_right.visible = true
            resize_bottom.visible = true
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
                id: top_bar
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
                    id: top_bar_description
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
                        id: label_left_info
                        color: "#d9d9d9"
                        text: qsTr("Bot Status: Not Running")
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        verticalAlignment: Text.AlignVCenter
                        anchors.rightMargin: 300
                        anchors.leftMargin: 10
                        anchors.bottomMargin: 0
                        anchors.topMargin: 0
                    }

                    Label {
                        id: label_right_info
                        color: "#d9d9d9"
                        text: qsTr("| HOME")
                        anchors.left: label_left_info.right
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        horizontalAlignment: Text.AlignRight
                        verticalAlignment: Text.AlignVCenter
                        anchors.rightMargin: 10
                        anchors.leftMargin: 0
                        anchors.bottomMargin: 0
                        anchors.topMargin: 0
                    }
                }

                Rectangle {
                    id: title_bar
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
                                             main_window.startSystemMove()

                                             internal.restoreWindowStatus()
                                         }
                    }

                    Image {
                        id: app_icon
                        width: 22
                        height: 22
                        anchors.left: parent.left
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        source: "../images/svg_images/icon_app_top.svg"
                        anchors.leftMargin: 5
                        anchors.bottomMargin: 0
                        anchors.topMargin: 0
                        fillMode: Image.PreserveAspectFit
                    }

                    Label {
                        id: label_app_name
                        color: "#ffffff"
                        text: qsTr("Granblue Automation")
                        anchors.left: app_icon.right
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        font.pointSize: 10
                        anchors.leftMargin: 5
                    }
                }

                Row {
                    id: row_buttons
                    x: 764
                    width: 105
                    height: 35
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.rightMargin: 0
                    anchors.topMargin: 0

                    // The following 3 buttons allow for minimizing, maximizing, and closing the window.
                    TopBarButton{
                        id: buttonMinimize

                        onClicked: {
                            main_window.showMinimized()
                            internal.restoreWindowMargin()
                        }
                    }

                    TopBarButton {
                        id: buttonMaximize
                        buttonIconSource: "../images/svg_images/maximize_icon.svg"

                        onClicked: internal.maximizeRestore()
                    }

                    TopBarButton {
                        id: buttonClose
                        buttonColorClicked: "#cc0000"
                        buttonIconSource: "../images/svg_images/close_icon.svg"

                        onClicked: main_window.close()
                    }
                }

                MouseArea {
                    id: resize_top_bar_doubleclick
                    x: 75
                    y: 0
                    anchors.left: parent.left
                    anchors.right: row_buttons.left
                    anchors.top: parent.top
                    anchors.bottom: top_bar_description.top
                    anchors.rightMargin: 0
                    anchors.leftMargin: 70
                    anchors.bottomMargin: 0
                    anchors.topMargin: 0

                    onDoubleClicked: internal.maximizeRestore()
                }

                MouseArea {
                    id: resize_window_topright
                    x: 963
                    y: -10
                    width: 10
                    height: 10
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.rightMargin: -5
                    anchors.topMargin: -5

                    cursorShape: Qt.SizeBDiagCursor

                    DragHandler {
                        target: null
                        onActiveChanged: if(active){
                                             main_window.startSystemResize(Qt.RightEdge | Qt.TopEdge)
                                         }
                    }
                }
            }

            Rectangle {
                id: content_container
                color: "#00000000"
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: top_bar.bottom
                anchors.bottom: parent.bottom
                anchors.topMargin: 0

                Rectangle {
                    id: left_menu
                    width: 70
                    color: "#242424"
                    anchors.left: parent.left
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    clip: true
                    anchors.topMargin: 0
                    anchors.bottomMargin: 0
                    anchors.leftMargin: 0

                    // PropertyAnimation will handle the LeftMenu's width when expanding and retracting.
                    PropertyAnimation{
                        id: animationMenu
                        target: left_menu
                        property: "width"
                        to: if(left_menu.width == 70){
                                return 200;
                            }else{
                                return 70;
                            }

                        duration: 500
                        easing.type: Easing.InOutBack
                    }

                    Column {
                        id: column
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
                            width: left_menu.width
                            text: qsTr("Home")
                            buttonColorMouseOver: "#323741"
                            isActiveMenu: true

                            onClicked: {
                                if(homeButton.isActiveMenu == false){
                                    homeButton.isActiveMenu = true
                                    settingsButton.isActiveMenu = false

                                    //stackView.push(Qt.resolvedUrl("pages/HomePage.qml"))
                                    page_home.visible = true
                                    page_settings.visible = false

                                    label_right_info.text = qsTr("| HOME")
                                }
                            }
                        }

                        LeftMenu {
                            id: settingsButton
                            width: left_menu.width
                            text: qsTr("Settings")
                            buttonColorMouseOver: "#323741"
                            buttonIconSource: "../images/svg_images/settings_icon.svg"

                            onClicked: {
                                if(settingsButton.isActiveMenu == false){
                                    homeButton.isActiveMenu = false
                                    settingsButton.isActiveMenu = true

                                    //stackView.push(Qt.resolvedUrl("pages/SettingsPage.qml"))
                                    page_home.visible = false
                                    page_settings.visible = true

                                    label_right_info.text = qsTr("| SETTINGS")
                                }
                            }
                        }
                    }

                    MouseArea {
                        id: resize_window_bottomleft
                        x: 65
                        y: 493
                        width: 10
                        height: 10
                        anchors.left: parent.left
                        anchors.bottom: parent.bottom
                        anchors.bottomMargin: -5
                        anchors.leftMargin: -5

                        cursorShape: Qt.SizeBDiagCursor

                        DragHandler {
                            target: null
                            onActiveChanged: if(active){
                                                 main_window.startSystemResize(Qt.LeftEdge | Qt.BottomEdge)
                                             }
                        }
                    }

                    MouseArea {
                        id: resize_window_topleft
                        x: 62
                        width: 15
                        height: 15
                        anchors.left: parent.left
                        anchors.top: parent.top
                        anchors.topMargin: -68
                        anchors.leftMargin: -7

                        cursorShape: Qt.SizeFDiagCursor

                        DragHandler {
                            target: null
                            onActiveChanged: if(active){
                                                 main_window.startSystemResize(Qt.LeftEdge | Qt.TopEdge)
                                             }
                        }
                    }
                }

                Rectangle {
                    id: content_area
                    color: "#2e2e4d"
                    anchors.left: left_menu.right
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    clip: true
                    anchors.rightMargin: 0
                    anchors.leftMargin: 0
                    anchors.bottomMargin: 25
                    anchors.topMargin: 0

                    Rectangle {
                        id: scrollViewContainer
                        y: 38
                        color: "#2f2f2f"
                        radius: 10
                        anchors.left: parent.left
                        anchors.right: page_home.left
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        anchors.rightMargin: 20
                        clip: false
                        anchors.leftMargin: 20
                        anchors.bottomMargin: 20
                        anchors.topMargin: 20

                        Flickable {
                            id: scrollView
                            x: -10
                            y: 0
                            anchors.left: parent.left
                            anchors.right: parent.right
                            anchors.top: parent.top
                            anchors.bottom: parent.bottom

                            contentHeight: console_log_text.contentHeight + 50 // Update the scrollView's content height to always have room for the console log text.
                            contentWidth: 280

                            ScrollBar.vertical: ScrollBar {
                                id: scrollBar
                                 policy: ScrollBar.AlwaysOn // Always display the scrollbar.
                            }


                            clip: true
                            anchors.rightMargin: 10
                            anchors.leftMargin: 10
                            anchors.bottomMargin: 10
                            anchors.topMargin: 10

                            TextArea.flickable: TextArea {
                                id: console_log_text

                                textMargin: 10

                                color: "#ffffff"
                                text: "Hello there!"
                                anchors.left: parent.left
                                anchors.right: parent.right
                                anchors.top: parent.top
                                anchors.bottom: parent.bottom
                                font.pixelSize: 12
                                horizontalAlignment: Text.AlignLeft
                                verticalAlignment: Text.AlignTop
                                wrapMode: Text.NoWrap
                                anchors.rightMargin: 10
                                anchors.leftMargin: 10
                                anchors.bottomMargin: 10
                                anchors.topMargin: 10
                                clip: false
                                textFormat: Text.PlainText

                                readOnly: true
                                selectByMouse: true
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
                        id: page_home
                        width: 300
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        anchors.topMargin: 20
                        anchors.bottomMargin: 20
                        anchors.rightMargin: 20

                        source: Qt.resolvedUrl("pages/HomePage.qml")

                        visible: true
                    }

                    Loader{
                        id: page_settings
                        width: 300
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        anchors.topMargin: 20
                        anchors.bottomMargin: 20
                        anchors.rightMargin: 20

                        source: Qt.resolvedUrl("pages/SettingsPage.qml")

                        visible: false
                    }
                }

                Rectangle {
                    id: bottom_bar
                    color: "#272741"
                    anchors.left: left_menu.right
                    anchors.right: parent.right
                    anchors.top: content_area.bottom
                    anchors.bottom: parent.bottom
                    anchors.rightMargin: 0
                    anchors.leftMargin: 0
                    anchors.bottomMargin: 0
                    anchors.topMargin: 0

                    Label {
                        id: label_bottom_info
                        x: 10
                        y: -2
                        color: "#d9d9d9"
                        text: qsTr("Application description")
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        verticalAlignment: Text.AlignVCenter
                        anchors.topMargin: 0
                        anchors.rightMargin: 310
                        anchors.leftMargin: 10
                        anchors.bottomMargin: 0
                    }

                    MouseArea {
                        id: resize_window_bottomright
                        x: 894
                        y: 8
                        width: 10
                        height: 10
                        anchors.right: parent.right
                        anchors.bottom: parent.bottom
                        anchors.rightMargin: -5
                        anchors.bottomMargin: -5

                        cursorShape: Qt.SizeFDiagCursor

                        DragHandler{
                            target: null
                            onActiveChanged: if(active){
                                                 main_window.startSystemResize(Qt.RightEdge | Qt.BottomEdge)
                                             }
                        }

                    }

                    Image {
                        id: resize_image
                        x: 891
                        y: 8
                        width: 25
                        height: 25
                        opacity: 0.5
                        anchors.right: parent.right
                        anchors.bottom: parent.bottom
                        source: "../images/svg_images/resize_icon.svg"
                        anchors.rightMargin: 0
                        anchors.bottomMargin: 0
                        sourceSize.height: 300
                        sourceSize.width: 300
                        fillMode: Image.PreserveAspectFit

                        antialiasing: false
                    }
                }
            }
        }
    }

    // This drop shadow effect will go below the bg Rectangle.
    DropShadow{
        anchors.fill: background
        horizontalOffset: 0
        verticalOffset: 0
        radius: 12
        samples: 16
        color: "#80000000"
        source: background
        z: 0
    }

    MouseArea {
        id: resize_left
        width: 10
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 10
        anchors.leftMargin: 0
        anchors.topMargin: 10

        cursorShape: Qt.SizeHorCursor

        DragHandler{
            target: null
            onActiveChanged: if(active){
                                 main_window.startSystemResize(Qt.LeftEdge)
                             }
        }
    }

    MouseArea {
        id: resize_right
        width: 10
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 10
        anchors.topMargin: 10
        anchors.rightMargin: 0

        cursorShape: Qt.SizeHorCursor

        DragHandler{
            target: null
            onActiveChanged: if(active){
                                 main_window.startSystemResize(Qt.RightEdge)
                             }
        }
    }

    MouseArea {
        id: resize_bottom
        height: 10
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.rightMargin: 10
        anchors.leftMargin: 10
        anchors.bottomMargin: 0

        cursorShape: Qt.SizeVerCursor

        DragHandler{
            target: null
            onActiveChanged: if(active){
                                 main_window.startSystemResize(Qt.BottomEdge)
                             }
        }
    }

    MouseArea {
        id: resize_top
        height: 10
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.topMargin: 0
        anchors.rightMargin: 10
        anchors.leftMargin: 10

        cursorShape: Qt.SizeVerCursor

        DragHandler{
            target: null
            onActiveChanged: if(active){
                                 main_window.startSystemResize(Qt.TopEdge)
                             }
        }
    }

}













/*##^##
Designer {
    D{i:0;formeditorZoom:1.33}
}
##^##*/
