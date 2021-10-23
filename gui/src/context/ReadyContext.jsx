import { createContext, useState } from "react"

export const ReadyContext = createContext()

export const ReadyProvider = ({ children }) => {
    const [readyStatus, setReadyStatus] = useState(false)
    const [refreshAlert, setRefreshAlert] = useState(false)

    return <ReadyContext.Provider value={{ status: [readyStatus, setReadyStatus], alert: [refreshAlert, setRefreshAlert] }}>{children}</ReadyContext.Provider>
}
