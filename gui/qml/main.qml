import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15
import "controls"

Window {
    id: main_window
    width: 1000
    height: 580
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

        // Removes or adds back in the window margins when maximizing or restoring.
        function maximizeRestore(){
            if(windowStatus == 0){
                main_window.showMaximized()
                windowStatus = 1
                windowMargin = 0

                buttonMaximize.buttonIconSource = "../images/svg_images/restore_icon.svg"
            }else{
                main_window.showNormal()
                windowStatus = 0
                windowMargin = 10

                buttonMaximize.buttonIconSource = "../images/svg_images/maximize_icon.svg"
            }
        }

        // Reset the window back to normal when dragging the title bar around.
        function restoreWindowStatus(){
            if(windowStatus == 1){
                main_window.showNormal()
                windowStatus = 0
                windowMargin = 10

                buttonMaximize.buttonIconSource = "../images/svg_images/maximize_icon.svg"
            }
        }

        // Restore the window status and margins to default when restoring the window to normal.
        function restoreWindowMargin(){
            windowStatus = 0
            windowMargin = 10

            buttonMaximize.buttonIconSource = "../images/svg_images/maximize_icon.svg"
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
                        text: qsTr("Application description")
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
                            id: button
                            width: left_menu.width
                            text: qsTr("Home")
                            buttonColorMouseOver: "#323741"
                            isActiveMenu: true
                        }

                        LeftMenu {
                            id: button1
                            width: left_menu.width
                            text: qsTr("Settings")
                            buttonColorMouseOver: "#323741"
                            buttonIconSource: "../images/svg_images/settings_icon.svg"
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
                    anchors.rightMargin: 0
                    anchors.leftMargin: 0
                    anchors.bottomMargin: 25
                    anchors.topMargin: 0
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
}







/*##^##
Designer {
    D{i:0;formeditorZoom:2}
}
##^##*/
