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
    summonElements: string[]
    setSummonElements: (summonElements: string[]) => void
    groupNumber: number
    setGroupNumber: (groupNumber: number) => void
    partyNumber: number
    setPartyNumber: (partyNumber: number) => void
    debugMode: boolean
    setDebugMode: (debugMode: boolean) => void

    // Extra Settings.
    twitterAPIKey: string
    setTwitterAPIKey: (twitterAPIKey: string) => void
    twitterAPIKeySecret: string
    setTwitterAPIKeySecret: (twitterAPIKeySecret: string) => void
    twitterAccessToken: string
    setTwitterAccessToken: (twitterAccessToken: string) => void
    twitterAccessTokenSecret: string
    setTwitterAccessTokenSecret: (twitterAccessTokenSecret: string) => void
    enableTwitterStreamAPI: boolean
    setEnableTwitterStreamAPI: (enableTwitterStreamAPI: boolean) => void
    enableDiscordNotifications: boolean
    setEnableDiscordNotifications: (enableDiscordNotifications: boolean) => void
    discordToken: string
    setDiscordToken: (discordToken: string) => void
    discordUserID: string
    setDiscordUserID: (userID: string) => void
    enableAutoRestore: boolean
    setEnableAutoRestore: (enableAutoRestore: boolean) => void
    enableFullElixir: boolean
    setEnableFullElixir: (enableFullElixir: boolean) => void
    enableSoulBalm: boolean
    setEnableSoulBalm: (enableSoulBalm: boolean) => void
    enableBezierCurveMouseMovement: boolean
    setEnableBezierCurveMouseMovement: (enableSoulBalm: boolean) => void
    mouseSpeed: number
    setMouseSpeed: (enableSoulBalm: number) => void
    enableDelayBetweenRuns: boolean
    setEnableDelayBetweenRuns: (enableDelayBetweenRuns: boolean) => void
    delayBetweenRuns: number
    setDelayBetweenRuns: (delayBetweenRuns: number) => void
    enableRandomizedDelayBetweenRuns: boolean
    setEnableRandomizedDelayBetweenRuns: (enableRandomizedDelayBetweenRuns: boolean) => void
    delayBetweenRunsLowerBound: number
    setDelayBetweenRunsLowerBound: (delayBetweenRunsLowerBound: number) => void
    delayBetweenRunsUpperBound: number
    setDelayBetweenRunsUpperBound: (delayBetweenRunsUpperBound: number) => void
}

export const BotStateContext = createContext<IProviderProps>({} as IProviderProps)

// https://stackoverflow.com/a/60130448 and https://stackoverflow.com/a/60198351
export const BotStateProvider = ({ children }: any): JSX.Element => {
    const [readyStatus, setReadyStatus] = useState<boolean>(false)
    const [isBotRunning, setIsBotRunning] = useState<boolean>(false)
    const [startBot, setStartBot] = useState<boolean>(false)
    const [stopBot, setStopBot] = useState<boolean>(false)
    const [refreshAlert, setRefreshAlert] = useState<boolean>(false)

    // Game settings.
    const [combatScriptName, setCombatScriptName] = useState<string>("")
    const [combatScript, setCombatScript] = useState<string[]>([])
    const [farmingMode, setFarmingMode] = useState<string>("")
    const [item, setItem] = useState<string>("")
    const [mission, setMission] = useState<string>("")
    const [map, setMap] = useState<string>("")
    const [itemAmount, setItemAmount] = useState<number>(1)
    const [summons, setSummons] = useState<string[]>([])
    const [summonElements, setSummonElements] = useState<string[]>([])
    const [groupNumber, setGroupNumber] = useState<number>(1)
    const [partyNumber, setPartyNumber] = useState<number>(1)
    const [debugMode, setDebugMode] = useState<boolean>(false)

    // Extra Settings.
    const [twitterAPIKey, setTwitterAPIKey] = useState<string>("")
    const [twitterAPIKeySecret, setTwitterAPIKeySecret] = useState<string>("")
    const [twitterAccessToken, setTwitterAccessToken] = useState<string>("")
    const [twitterAccessTokenSecret, setTwitterAccessTokenSecret] = useState<string>("")
    const [enableTwitterStreamAPI, setEnableTwitterStreamAPI] = useState<boolean>(true)
    const [enableDiscordNotifications, setEnableDiscordNotifications] = useState<boolean>(false)
    const [discordToken, setDiscordToken] = useState<string>("")
    const [discordUserID, setDiscordUserID] = useState<string>("")
    const [enableAutoRestore, setEnableAutoRestore] = useState<boolean>(false)
    const [enableFullElixir, setEnableFullElixir] = useState<boolean>(false)
    const [enableSoulBalm, setEnableSoulBalm] = useState<boolean>(false)
    const [enableBezierCurveMouseMovement, setEnableBezierCurveMouseMovement] = useState<boolean>(false)
    const [mouseSpeed, setMouseSpeed] = useState<number>(0.2)
    const [enableDelayBetweenRuns, setEnableDelayBetweenRuns] = useState<boolean>(false)
    const [delayBetweenRuns, setDelayBetweenRuns] = useState<number>(15)
    const [enableRandomizedDelayBetweenRuns, setEnableRandomizedDelayBetweenRuns] = useState<boolean>(false)
    const [delayBetweenRunsLowerBound, setDelayBetweenRunsLowerBound] = useState<number>(15)
    const [delayBetweenRunsUpperBound, setDelayBetweenRunsUpperBound] = useState<number>(60)

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

        // Game Settings.
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
        summonElements,
        setSummonElements,
        groupNumber,
        setGroupNumber,
        partyNumber,
        setPartyNumber,
        debugMode,
        setDebugMode,

        // Extra Settings.
        twitterAPIKey,
        setTwitterAPIKey,
        twitterAPIKeySecret,
        setTwitterAPIKeySecret,
        twitterAccessToken,
        setTwitterAccessToken,
        twitterAccessTokenSecret,
        setTwitterAccessTokenSecret,
        enableTwitterStreamAPI,
        setEnableTwitterStreamAPI,
        enableDiscordNotifications,
        setEnableDiscordNotifications,
        discordToken,
        setDiscordToken,
        discordUserID,
        setDiscordUserID,
        enableAutoRestore,
        setEnableAutoRestore,
        enableFullElixir,
        setEnableFullElixir,
        enableSoulBalm,
        setEnableSoulBalm,
        enableBezierCurveMouseMovement,
        setEnableBezierCurveMouseMovement,
        mouseSpeed,
        setMouseSpeed,
        enableDelayBetweenRuns,
        setEnableDelayBetweenRuns,
        delayBetweenRuns,
        setDelayBetweenRuns,
        enableRandomizedDelayBetweenRuns,
        setEnableRandomizedDelayBetweenRuns,
        delayBetweenRunsLowerBound,
        setDelayBetweenRunsLowerBound,
        delayBetweenRunsUpperBound,
        setDelayBetweenRunsUpperBound,
    }

    return <BotStateContext.Provider value={providerValues}>{children}</BotStateContext.Provider>
}
