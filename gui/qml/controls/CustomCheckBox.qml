import QtQuick 2.15
import QtQuick.Controls 2.15

CheckBox {
    id: checkBox

    x: 10
    y: 200
    width: 104
    height: 38

    text: qsTr("Placeholder Text")
    tristate: false
    anchors.leftMargin: 10

    indicator: Rectangle {
            implicitWidth: 26
            implicitHeight: 26
            x: checkBox.leftPadding
            y: parent.height / 2 - height / 2
            radius: 3
            border.color: checkBox.down ? "#17a81a" : "#21be2b"

            Rectangle {
                width: 14
                height: 14
                x: 6
                y: 6
                radius: 2
                color: checkBox.down ? "#17a81a" : "#21be2b"
                visible: checkBox.checked
            }
    }

    contentItem: Text {
        text: checkBox.text
        font: checkBox.font
        opacity: enabled ? 1.0 : 0.3
        color: checkBox.down ? "#17a81a" : "#21be2b"
        verticalAlignment: Text.AlignVCenter
        leftPadding: checkBox.indicator.width + checkBox.spacing
    }
}
