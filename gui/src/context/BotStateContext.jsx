import { createContext, useState } from "react"

export const BotStateContext = createContext()

export const BotStateProvider = ({ children }) => {
    const [readyStatus, setReadyStatus] = useState(false)
    const [isBotRunning, setIsBotRunning] = useState(false)
    const [startBot, setStartBot] = useState(false)
    const [stopBot, setStopBot] = useState(false)
    const [refreshAlert, setRefreshAlert] = useState(false)

    return (
        <BotStateContext.Provider
            value={{
                status: [readyStatus, setReadyStatus],
                running: [isBotRunning, setIsBotRunning],
                alert: [refreshAlert, setRefreshAlert],
                start: [startBot, setStartBot],
                stop: [stopBot, setStopBot],
            }}
        >
            {children}
        </BotStateContext.Provider>
    )
}
