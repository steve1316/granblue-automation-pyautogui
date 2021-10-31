import { createContext, useState } from "react"

export interface IProviderProps {
    readyStatus: boolean
    setReadyStatus: (readyStatus: boolean) => void
    isBotRunning: boolean
    setIsBotRunning: (isBotRunning: boolean) => void
    startBot: boolean
    setStartBot: (startBot: boolean) => void
    stopBot: boolean
    setStopBot: (stopBot: boolean) => void
    refreshAlert: boolean
    setRefreshAlert: (refreshAlert: boolean) => void

    // Game settings.
    combatScriptName: string
    setCombatScriptName: (combatScriptName: string) => void
    combatScript: string[]
    setCombatScript: (combatScript: string[]) => void
    farmingMode: string
    setFarmingMode: (farmingMode: string) => void
    item: string
    setItem: (item: string) => void
    mission: string
    setMission: (mission: string) => void
    map: string
    setMap: (map: string) => void
    itemAmount: number
    setItemAmount: (itemAmount: number) => void
    summons: string[]
    setSummons: (summons: string[]) => void
    groupNumber: number
    setGroupNumber: (groupNumber: number) => void
    partyNumber: number
    setPartyNumber: (partyNumber: number) => void
    debugMode: boolean
    setDebugMode: (debugMode: boolean) => void
}

export const BotStateContext = createContext<IProviderProps>({} as IProviderProps)

// https://stackoverflow.com/a/60130448 and https://stackoverflow.com/a/60198351
export const BotStateProvider = ({ children }: any): JSX.Element => {
    const [readyStatus, setReadyStatus] = useState<boolean>(false)
    const [isBotRunning, setIsBotRunning] = useState<boolean>(false)
    const [startBot, setStartBot] = useState<boolean>(false)
    const [stopBot, setStopBot] = useState<boolean>(false)
    const [refreshAlert, setRefreshAlert] = useState<boolean>(false)

    const [combatScriptName, setCombatScriptName] = useState<string>("")
    const [combatScript, setCombatScript] = useState<string[]>([])
    const [farmingMode, setFarmingMode] = useState<string>("")
    const [item, setItem] = useState<string>("")
    const [mission, setMission] = useState<string>("")
    const [map, setMap] = useState<string>("")
    const [itemAmount, setItemAmount] = useState<number>(1)
    const [summons, setSummons] = useState<string[]>([])
    const [groupNumber, setGroupNumber] = useState<number>(1)
    const [partyNumber, setPartyNumber] = useState<number>(1)
    const [debugMode, setDebugMode] = useState<boolean>(false)

    const providerValues: IProviderProps = {
        readyStatus,
        setReadyStatus,
        isBotRunning,
        setIsBotRunning,
        startBot,
        setStartBot,
        stopBot,
        setStopBot,
        refreshAlert,
        setRefreshAlert,
        combatScriptName,
        setCombatScriptName,
        combatScript,
        setCombatScript,
        farmingMode,
        setFarmingMode,
        item,
        setItem,
        mission,
        setMission,
        map,
        setMap,
        itemAmount,
        setItemAmount,
        summons,
        setSummons,
        groupNumber,
        setGroupNumber,
        partyNumber,
        setPartyNumber,
        debugMode,
        setDebugMode,
    }

    return <BotStateContext.Provider value={providerValues}>{children}</BotStateContext.Provider>
}
