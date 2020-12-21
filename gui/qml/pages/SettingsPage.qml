import QtQuick 2.15
import QtQuick.Controls 2.15

Item{
    Rectangle {
        id: rectangle
        color: "#323741"
        anchors.fill: parent

        Label {
            id: label
            x: 305
            y: 176
            color: "#ffffff"
            text: qsTr("Settings Screen")
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            font.pointSize: 16
        }
    }
}
