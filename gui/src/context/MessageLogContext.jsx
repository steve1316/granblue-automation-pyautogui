import { createContext, useState } from "react"

export const MessageLogContext = createContext()

export const MessageLogProvider = ({ children }) => {
    const [messageLog, setMessageLog] = useState([""])
    const [asyncMessages, setAsyncMessages] = useState([""])

    return <MessageLogContext.Provider value={{ log: [messageLog, setMessageLog], message: [asyncMessages, setAsyncMessages] }}>{children}</MessageLogContext.Provider>
}
