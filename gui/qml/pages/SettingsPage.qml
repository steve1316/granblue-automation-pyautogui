import QtQuick 2.15
import QtQuick.Controls 2.15

Item{
    Rectangle {
        id: settingsContainer

        color: "#323741"
        anchors.fill: parent

        Label {
            id: settingsPageLabel

            x: 305
            y: 176

            color: "#ffffff"

            text: qsTr("Settings Screen")
            font.pointSize: 16

            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }
}
