import { createContext, useState } from "react"

export const MessageLogContext = createContext()

export const MessageLogProvider = ({ children }) => {
    const [messageLog, setMessageLog] = useState([""])
    const [asyncMessages, setAsyncMessages] = useState([""])
    const [botStartFlag, setBotFlag] = useState(false)

    // TODO: Create another state to check if bot is already running to prevent creating another child process again.

    return (
        <MessageLogContext.Provider value={{ log: [messageLog, setMessageLog], message: [asyncMessages, setAsyncMessages], start: [botStartFlag, setBotFlag] }}>{children}</MessageLogContext.Provider>
    )
}
