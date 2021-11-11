import { createContext, useState } from "react"

interface IProviderProps {
    messageLog: string[]
    setMessageLog: (messageLog: string[]) => void
    asyncMessages: string[]
    setAsyncMessages: (asyncMessages: string[]) => void
}

export const MessageLogContext = createContext<IProviderProps>({} as IProviderProps)

// https://stackoverflow.com/a/60130448 and https://stackoverflow.com/a/60198351
export const MessageLogProvider = ({ children }: any): JSX.Element => {
    const [messageLog, setMessageLog] = useState<string[]>([])
    const [asyncMessages, setAsyncMessages] = useState<string[]>([])

    const providerValues: IProviderProps = {
        messageLog,
        setMessageLog,
        asyncMessages,
        setAsyncMessages,
    }

    return <MessageLogContext.Provider value={providerValues}>{children}</MessageLogContext.Provider>
}
