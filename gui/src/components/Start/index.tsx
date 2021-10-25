import { Command } from "@tauri-apps/api/shell"
import { useContext, useEffect, useState } from "react"
import { MessageLogContext } from "../../context/MessageLogContext"
import { BotStateContext } from "../../context/BotStateContext"
import { FsTextFileOption, readTextFile, writeFile } from "@tauri-apps/api/fs"

const Start = () => {
    const [PID, setPID] = useState(0)

    const messageLogContext = useContext(MessageLogContext)
    const botStateContext = useContext(BotStateContext)

    // Append the messages acquired from the async bot process to the message log. This is needed to actually reflect the new messages to the Home page.
    useEffect(() => {
        const newLog = [...messageLogContext?.messageLog, ...messageLogContext?.asyncMessages]
        messageLogContext?.setMessageLog(newLog)
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [messageLogContext?.asyncMessages])

    // Start or stop the bot.
    useEffect(() => {
        if (botStateContext?.startBot && !botStateContext?.isBotRunning) {
            handleStart()
        } else if (botStateContext?.stopBot && botStateContext?.isBotRunning) {
            if (PID !== 0) {
                handleStop()
            }
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [botStateContext?.startBot, botStateContext?.stopBot])

    const handleStop = async () => {
        console.log("Killing process now...")
        const output = await new Command("powershell", `taskkill /F /PID ${PID}`).execute() // Windows specific
        console.log(`Result of killing bot process using PID ${PID}: ${output.code}`)
        setPID(0)
    }

    // Load settings from JSON file on program start.
    useEffect(() => {
        try {
            readTextFile("settings.json")
                .then((settings) => {
                    interface ParsedSettings {
                        currentCombatScriptName: string
                        currentCombatScript: string
                        farmingMode: string
                        item: string
                        mission: string
                        itemAmount: number
                        summons: string[]
                        groupNumber: number
                        partyNumber: number
                        debugMode: boolean
                    }

                    const decoded: ParsedSettings = JSON.parse(settings)

                    // Save the settings to state.
                    botStateContext?.setCombatScriptName(decoded.currentCombatScriptName)
                    botStateContext?.setCombatScript(decoded.currentCombatScript)
                    botStateContext?.setFarmingMode(decoded.farmingMode)
                    botStateContext?.setItem(decoded.item)
                    botStateContext?.setMission(decoded.mission)
                    botStateContext?.setItemAmount(decoded.itemAmount)
                    botStateContext?.setSummons(decoded.summons)
                    botStateContext?.setGroupNumber(decoded.groupNumber)
                    botStateContext?.setPartyNumber(decoded.partyNumber)
                    botStateContext?.setDebugMode(decoded.debugMode)
                })
                .catch((err) => {
                    console.log(`Encountered read exception while loading settings from local JSON file: ${err}`)
                })
        } catch (e) {
            console.log(`Encountered exception while loading settings from local JSON file: ${e}`)
        }

        handleReady()
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    // Save current settings to JSON file.
    useEffect(() => {
        try {
            const settings = {
                combatScriptName: botStateContext?.combatScriptName,
                combatScript: botStateContext?.combatScript,
                farmingMode: botStateContext?.farmingMode,
                item: botStateContext?.item,
                mission: botStateContext?.mission,
                itemAmount: botStateContext?.itemAmount,
                summons: botStateContext?.summons,
                groupNumber: botStateContext?.groupNumber,
                partyNumber: botStateContext?.partyNumber,
                debugMode: botStateContext?.debugMode,
            }

            // Stringify the contents and prepare for writing to the specified file.
            const jsonString = JSON.stringify(settings, null, 4)
            const settingsFile: FsTextFileOption = { path: "settings.json", contents: jsonString }

            console.log(`Saved Settings: ${jsonString}`)

            writeFile(settingsFile)
                .then(() => {
                    console.log(`Successfully saved settings to settings.json`)
                })
                .catch((err) => {
                    console.log(`Encountered write exception: ${err}`)
                })

            handleReady()
        } catch (e) {
            console.log(`Encountered exception while saving settings to local JSON file:\n${e}`)
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [
        botStateContext?.combatScriptName,
        botStateContext?.combatScript,
        botStateContext?.farmingMode,
        botStateContext?.item,
        botStateContext?.mission,
        botStateContext?.itemAmount,
        botStateContext?.summons,
        botStateContext?.groupNumber,
        botStateContext?.partyNumber,
        botStateContext?.debugMode,
    ])

    // Determine whether the bot is ready to start.
    const handleReady = () => {
        if (botStateContext?.farmingMode !== "Coop" && botStateContext?.farmingMode !== "") {
            if (botStateContext?.item !== "" && botStateContext?.mission !== "" && botStateContext?.summons.length !== 0) {
                botStateContext?.setReadyStatus(true)
            } else {
                botStateContext?.setReadyStatus(false)
            }
        } else if (botStateContext?.farmingMode === "Coop") {
            if (botStateContext?.item !== "" && botStateContext?.mission !== "") {
                botStateContext?.setReadyStatus(true)
            } else {
                botStateContext?.setReadyStatus(false)
            }
        } else {
            botStateContext?.setReadyStatus(false)
        }
    }

    // Begin the bot process here.
    // Note: newlines are not sent over through stdout so they need to be manually added here in the frontend.
    const handleStart = async () => {
        // Construct the shell command using Tauri Command API.
        const command = new Command("python", "backend/test.py")

        // Attach event listeners.
        command.on("close", (data) => {
            let newLog = [...messageLogContext?.asyncMessages, `\nChild process finished with code ${data.code}`]
            messageLogContext?.setAsyncMessages(newLog)
            botStateContext?.setIsBotRunning(false)
            botStateContext?.setStartBot(false)
            botStateContext?.setStopBot(false)
        })
        command.on("error", (error) => {
            let newLog = [...messageLogContext?.asyncMessages, `\nChild process error: ${error}`]
            messageLogContext?.setAsyncMessages(newLog)
            botStateContext?.setIsBotRunning(false)
            botStateContext?.setStartBot(false)
            botStateContext?.setStopBot(false)
        })
        command.stdout.on("data", (line) => {
            let newLog = [...messageLogContext?.asyncMessages, `\nChild process stdout: "${line}"`]
            messageLogContext?.setAsyncMessages(newLog)
        })
        command.stderr.on("data", (line) => {
            let newLog = [...messageLogContext?.asyncMessages, `\nChild process stderr: "${line}"`]
            messageLogContext?.setAsyncMessages(newLog)
        })

        // Create the child process.
        const child = await command.spawn()
        console.log("PID: ", child.pid)
        setPID(child.pid)
        botStateContext?.setIsBotRunning(true)
    }

    return null
}

export default Start
