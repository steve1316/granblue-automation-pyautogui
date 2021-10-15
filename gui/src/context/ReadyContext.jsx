import React, { createContext, useState } from "react"

export const ReadyContext = createContext()

export const ReadyProvider = ({ children }) => {
    const [status, setStatus] = useState(false)

    return <ReadyContext.Provider value={{ status, setStatus }}>{children}</ReadyContext.Provider>
}
