import { Command } from "@tauri-apps/api/shell"
import { useContext, useEffect, useState } from "react"
import { MessageLogContext } from "../../context/MessageLogContext"
import { BotStateContext } from "../../context/BotStateContext"
import { FsTextFileOption, readTextFile, writeFile } from "@tauri-apps/api/fs"

const Start = () => {
    const [PID, setPID] = useState(0)
    const [firstTimeSetup, setFirstTimeSetup] = useState(true)

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
            execute("powershell", "$path=Get-Location \nmd -Force $path/logs/") // Windows-specific
            handleStart()
        } else if (botStateContext?.stopBot && botStateContext?.isBotRunning) {
            if (PID !== 0) {
                handleStop()
            }
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [botStateContext?.startBot, botStateContext?.stopBot])

    // Get the current date and time for the filename of the text log file.
    const getCurrentDateAndTime = (separator = "") => {
        let newDate = new Date()
        let date = newDate.getDate()
        let month = newDate.getMonth() + 1
        let year = newDate.getFullYear()

        let hour = newDate.getHours()
        let minute = newDate.getMinutes()
        let second = newDate.getSeconds()

        return `${year}${separator}${month < 10 ? `0${month}` : `${month}`}${separator}${date} ${hour < 10 ? `0${hour}` : `${hour}`}${separator}${
            minute < 10 ? `0${minute}` : `${minute}`
        }${separator}${second < 10 ? `0${second}` : `${second}`}`
    }

    // Attempt to kill the bot process if it is still active.
    const handleStop = async () => {
        if (PID !== 0) {
            console.log("Killing process now...")
            const output = await new Command("powershell", `taskkill /F /PID ${PID}`).execute() // Windows specific
            console.log(`Result of killing bot process using PID ${PID}: ${output.code}`)
            setPID(0)
        }
    }

    // Load settings from JSON file on program start.
    useEffect(() => {
        try {
            readTextFile("backend/settings.json")
                .then((settings) => {
                    interface ParsedSettings {
                        combatScriptName: string
                        combatScript: string[]
                        farmingMode: string
                        item: string
                        mission: string
                        map: string
                        itemAmount: number
                        summons: string[]
                        groupNumber: number
                        partyNumber: number
                        debugMode: boolean
                    }

                    const decoded: ParsedSettings = JSON.parse(settings)
                    console.log(`Loaded settings from settings.json: ${JSON.stringify(decoded, null, 4)}`)

                    // Save the settings to state.
                    botStateContext?.setCombatScriptName(decoded.combatScriptName)
                    botStateContext?.setCombatScript(decoded.combatScript)
                    botStateContext?.setFarmingMode(decoded.farmingMode)
                    botStateContext?.setItem(decoded.item)
                    botStateContext?.setMission(decoded.mission)
                    botStateContext?.setMap(decoded.map)
                    botStateContext?.setItemAmount(decoded.itemAmount)
                    botStateContext?.setSummons(decoded.summons)
                    botStateContext?.setGroupNumber(decoded.groupNumber)
                    botStateContext?.setPartyNumber(decoded.partyNumber)
                    botStateContext?.setDebugMode(decoded.debugMode)

                    setFirstTimeSetup(false)
                })
                .catch((err) => {
                    console.log(`Encountered read exception while loading settings from settings.json ${err}`)
                    messageLogContext?.setMessageLog([
                        ...messageLogContext?.messageLog,
                        `\nEncountered read exception while loading settings from settings.json: ${err}\nThe settings.json file might not exist because this is your first time booting up this application.`,
                    ])
                })
        } catch (e) {
            console.log(`Encountered exception while loading settings from settings.json: ${e}`)
            messageLogContext?.setMessageLog([...messageLogContext?.messageLog, `\nEncountered exception while loading settings from local JSON file: ${e}`])
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    // Save current settings to JSON file.
    useEffect(() => {
        if (!firstTimeSetup) {
            try {
                const settings = {
                    combatScriptName: botStateContext?.combatScriptName,
                    combatScript: botStateContext?.combatScript,
                    farmingMode: botStateContext?.farmingMode,
                    item: botStateContext?.item,
                    mission: botStateContext?.mission,
                    map: botStateContext?.map,
                    itemAmount: botStateContext?.itemAmount,
                    summons: botStateContext?.summons,
                    groupNumber: botStateContext?.groupNumber,
                    partyNumber: botStateContext?.partyNumber,
                    debugMode: botStateContext?.debugMode,
                }

                // Stringify the contents and prepare for writing to the specified file.
                const jsonString = JSON.stringify(settings, null, 4)
                const settingsFile: FsTextFileOption = { path: "backend/settings.json", contents: jsonString }
                writeFile(settingsFile)
                    .then(() => {
                        console.log(`Successfully saved settings to settings.json`)
                    })
                    .catch((err) => {
                        console.log(`Encountered write exception while saving settings to settings.json: ${err}`)
                        messageLogContext?.setMessageLog([
                            ...messageLogContext?.messageLog,
                            `\nEncountered write exception while saving settings to settings.json: ${err}\nThe current directory or parent directory might be write-protected`,
                        ])
                    })
            } catch (e) {
                console.log(`Encountered exception while saving settings to settings.json:\n${e}`)
                messageLogContext?.setMessageLog([...messageLogContext?.messageLog, `\nEncountered exception while saving settings to settings.json:\n${e}`])
            }
        }

        handleReady()
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [
        botStateContext?.combatScriptName,
        botStateContext?.combatScript,
        botStateContext?.farmingMode,
        botStateContext?.item,
        botStateContext?.mission,
        botStateContext?.map,
        botStateContext?.itemAmount,
        botStateContext?.summons,
        botStateContext?.groupNumber,
        botStateContext?.partyNumber,
        botStateContext?.debugMode,
    ])

    // Save current message log to text file inside the /logs/ folder.
    useEffect(() => {
        if (messageLogContext?.messageLog.find((message) => message.includes("Child process finished with code")) !== undefined) {
            // Save message log to text file.
            const fileName = `log ${getCurrentDateAndTime("-")}`
            var fileContent = ""
            messageLogContext?.messageLog.forEach((message) => {
                fileContent = fileContent.concat(message)
            })
            console.log(`Messages to save: ${messageLogContext?.messageLog}`)
            const logFile: FsTextFileOption = { path: `logs/${fileName}.txt`, contents: fileContent }
            writeFile(logFile)
                .then(() => {
                    console.log(`Successfully saved message log to ${fileName}.txt`)
                })
                .catch((err) => {
                    console.log(`Encountered write exception: ${err}`)
                })
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [messageLogContext?.messageLog])

    // Async function to execute a Tauri API command.
    const execute = async (program: string, args: string | string[]) => {
        await new Command(program, args).execute()
    }

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
        // TODO: Replace with main.py to start the bot.
        const command = new Command("python", "backend/test.py")

        // Attach event listeners.
        command.on("close", (data) => {
            const fileName = `log ${getCurrentDateAndTime("-")}`
            let newLog = [...messageLogContext?.asyncMessages, `\nWill save message log to ${fileName}.txt`, `\nChild process finished with code ${data.code}`]
            messageLogContext?.setAsyncMessages(newLog)
            botStateContext?.setIsBotRunning(false)
            botStateContext?.setStartBot(false)
            botStateContext?.setStopBot(false)

            handleStop()
        })
        command.on("error", (error) => {
            const fileName = `log ${getCurrentDateAndTime("-")}`
            let newLog = [...messageLogContext?.asyncMessages, `\nWill save message log to ${fileName}.txt`, `\nChild process error: ${error}`]
            messageLogContext?.setAsyncMessages(newLog)
            botStateContext?.setIsBotRunning(false)
            botStateContext?.setStartBot(false)
            botStateContext?.setStopBot(false)

            handleStop()
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
