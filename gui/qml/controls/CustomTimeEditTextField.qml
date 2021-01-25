import QtQuick 2.15
import QtQuick.Controls 2.15

TextField {
    id: timeEditTextField

    width: 100
    height: 50

    horizontalAlignment: Text.AlignHCenter
    font.bold: true
    font.pointSize: 12

    placeholderText: "HH:MM:SS"

    // Validate only numbers from 0-9 for HH:MM:SS format.
    // Additionally, if user presses Backspace, delete numbers.
    validator: RegExpValidator { regExp: /^([0-1\s]?[0-9\s]|2[0-3\s]):([0-5\s][0-9\s]):([0-5\s][0-9\s])$/ }

    onTextChanged: {
        // The inputMask is used to make sure the user types in HH:MM:SS format.
        timeEditTextField.inputMask = "99:99:99"
        timeEditTextField.inputMethodHints = Qt.ImhDigitsOnly
    }
}

/*##^##
Designer {
    D{i:0;formeditorZoom:1.66}
}
##^##*/
