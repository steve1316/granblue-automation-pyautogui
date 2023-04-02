import { FsTextFileOption, readTextFile, writeFile } from "@tauri-apps/api/fs"
import { Command } from "@tauri-apps/api/shell"
import axios, { AxiosError, AxiosResponse } from "axios"
import { useContext, useEffect, useState } from "react"
import { BotStateContext, Settings, defaultSettings } from "../context/BotStateContext"
import { MessageLogContext } from "../context/MessageLogContext"
import summonData from "../data/summons.json"

const StartHelper = () => {
    const [PID, setPID] = useState(0)
    const [firstTimeSetup, setFirstTimeSetup] = useState(true)
    const [firstTimeAPIRequest, setFirstTimeAPIRequest] = useState(true)
    let successfulAPILogin = false

    const mlc = useContext(MessageLogContext)
    const bsc = useContext(BotStateContext)

    // Do not update to React 18. State updates in batch will break and stdout log will not work properly.
    // Append the messages acquired from the async bot process to the message log. This is needed to actually reflect the new messages to the Home page.
    useEffect(() => {
        const newLog = [...mlc.messageLog, ...mlc.asyncMessages]
        mlc.setMessageLog(newLog)

        if (mlc.asyncMessages.length > 0 && mlc.asyncMessages[mlc.asyncMessages.length - 1].includes("Closing Python process")) {
            handleStop()
        }

        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [mlc.asyncMessages])

    // Start or stop the bot process.
    useEffect(() => {
        if (bsc.startBot && !bsc.isBotRunning) {
            execute("powershell", "$path=Get-Location \nmd -Force $path/logs/") // Windows-specific
            handleStart()
        } else if (bsc.stopBot && bsc.isBotRunning) {
            if (PID !== 0) {
                handleStop()
            }
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [bsc.startBot, bsc.stopBot])

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
            bsc.setIsBotRunning(false)
            bsc.setStartBot(false)
            bsc.setStopBot(false)

            console.log("Killing process tree now...")
            const output = await new Command("powershell", `taskkill /F /T /PID ${PID}`).execute() // Windows specific
            console.log(`Result of killing bot process using PID ${PID}: \n${output.stdout}`)
            setPID(0)
        }
    }

    // Load settings from JSON file on program start.
    useEffect(() => {
        try {
            readTextFile("backend/settings.json")
                .then((settings) => {
                    const decoded: Settings = JSON.parse(settings)
                    console.log(`Loaded settings from settings.json: ${JSON.stringify(decoded, null, 4)}`)

                    var fixedSettings: Settings = fixSettings(decoded)

                    // Save the settings to state.
                    bsc.setSettings(fixedSettings)

                    setFirstTimeSetup(false)
                })
                .catch((err) => {
                    console.log(`Encountered read exception while loading settings from settings.json ${err}`)
                    setFirstTimeSetup(false)
                })
        } catch (e) {
            console.log(`Encountered exception while loading settings from settings.json: ${e}`)
            mlc.setMessageLog([...mlc.messageLog, `\nEncountered exception while loading settings from local JSON file: ${e}`])
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    // Attempt to fix missing key-value pairs in the settings before commiting them to state.
    const fixSettings = (decoded: Settings) => {
        var newSettings: Settings = decoded
        Object.keys(defaultSettings).forEach((key) => {
            if (decoded[key as keyof Settings] === undefined) {
                newSettings = {
                    ...newSettings,
                    [key as keyof Settings]: defaultSettings[key as keyof Settings],
                }
            }
        })

        return newSettings
    }

    const fetchSummonElements = (summonList: string[]) => {
        var newSummonElementsList: string[] = []
        summonList.forEach((summon) => {
            if (summonData.Fire.summons.indexOf(summon) !== -1) {
                newSummonElementsList = newSummonElementsList.concat("Fire")
            } else if (summonData.Water.summons.indexOf(summon) !== -1) {
                newSummonElementsList = newSummonElementsList.concat("Water")
            } else if (summonData.Earth.summons.indexOf(summon) !== -1) {
                newSummonElementsList = newSummonElementsList.concat("Earth")
            } else if (summonData.Wind.summons.indexOf(summon) !== -1) {
                newSummonElementsList = newSummonElementsList.concat("Wind")
            } else if (summonData.Light.summons.indexOf(summon) !== -1) {
                newSummonElementsList = newSummonElementsList.concat("Light")
            } else if (summonData.Dark.summons.indexOf(summon) !== -1) {
                newSummonElementsList = newSummonElementsList.concat("Dark")
            } else if (summonData.Misc.summons.indexOf(summon) !== -1) {
                newSummonElementsList = newSummonElementsList.concat("Misc")
            }
        })

        return newSummonElementsList
    }

    // Save current settings to JSON file.
    useEffect(() => {
        if (!firstTimeSetup && import.meta.env.VITE_APP_ENVIRONMENT !== "development") {
            try {
                // Grab a local copy of the current settings.
                const localSettings: Settings = bsc.settings

                // Find the elements of the support Summons for the Farming Mode first and then for Nightmare if available.
                localSettings.game.summonElements = fetchSummonElements(localSettings.game.summons)
                localSettings.nightmare.nightmareSummonElements = fetchSummonElements(localSettings.nightmare.nightmareSummons)

                // Stringify the contents and prepare for writing to the specified file.
                const jsonString = JSON.stringify(localSettings, null, 4)
                const settingsFile: FsTextFileOption = { path: "backend/settings.json", contents: jsonString }
                writeFile(settingsFile)
                    .then(() => {
                        console.log(`Successfully saved settings to settings.json`)
                    })
                    .catch((err) => {
                        console.log(`Encountered write exception while saving settings to settings.json: ${err}`)
                        mlc.setMessageLog([
                            ...mlc.messageLog,
                            `\nEncountered write exception while saving settings to settings.json: ${err}\nThe current directory or parent directory might be write-protected`,
                        ])
                    })
            } catch (e) {
                console.log(`Encountered exception while saving settings to settings.json:\n${e}`)
                mlc.setMessageLog([...mlc.messageLog, `\nEncountered exception while saving settings to settings.json:\n${e}`])
            }
        }

        handleReady()
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [bsc.settings])

    // Save current message log to text file inside the /logs/ folder.
    useEffect(() => {
        if (mlc.messageLog.find((message) => message.includes("Child process finished with code")) !== undefined) {
            // Save message log to text file.
            const fileName = `log ${getCurrentDateAndTime("-")}`
            var fileContent = ""
            mlc.messageLog.forEach((message) => {
                fileContent = fileContent.concat(message)
            })
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
    }, [mlc.messageLog])

    // Async function to execute a Tauri API command.
    const execute = async (program: string, args: string | string[]) => {
        await new Command(program, args).execute()
    }

    // Determine whether the program is ready to start.
    const handleReady = () => {
        const farmingMode = bsc.settings.game.farmingMode
        if (farmingMode !== "Coop" && farmingMode !== "Arcarum" && farmingMode !== "Generic" && farmingMode !== "") {
            bsc.setReadyStatus(bsc.settings.game.item !== "" && bsc.settings.game.mission !== "" && bsc.settings.game.summons.length !== 0)
        } else if (farmingMode === "Coop" || farmingMode === "Arcarum") {
            bsc.setReadyStatus(bsc.settings.game.item !== "" && bsc.settings.game.mission !== "")
        } else {
            bsc.setReadyStatus(farmingMode === "Generic" && bsc.settings.game.item !== "" && bsc.settings.game.summons.length !== 0)
        }
    }

    // Begin the bot process here.
    // Note: newlines are not sent over through stdout so they need to be manually added here in the frontend.
    const handleStart = async () => {
        // Construct the shell command using Tauri Command API.
        const command = new Command("python", "backend/main.py")

        // Attach event listeners.
        command.on("close", (data) => {
            const fileName = `log ${getCurrentDateAndTime("-")}`
            let newLog = [...mlc.asyncMessages, `\n\nSaved message log to: ${fileName}.txt`, `\nChild process finished with code ${data.code}`]
            mlc.setAsyncMessages(newLog)
            handleStop()
        })
        command.on("error", (error) => {
            let newLog = [...mlc.asyncMessages, `\nChild process error: ${error}`]
            mlc.setAsyncMessages(newLog)
        })
        command.stdout.on("data", (line: string) => {
            // If the line contains this, then send a API request to Granblue Automation Statistics.
            if (successfulAPILogin && line.includes("API-RESULT")) {
                // Format of the line is API-RESULT|ITEM NAME|ITEM AMOUNT|TIME
                let newLog: string[] = []
                const splitLine = line.split("|")
                if (splitLine.length !== 4) {
                    console.log(`Unable to send API request to Granblue Automation Statistics: Invalid request format of ${splitLine.length}.`)
                    newLog = [...mlc.asyncMessages, `\nUnable to send API request to Granblue Automation Statistics: Invalid request format of ${splitLine.length}.`]
                } else if (Number.isNaN(parseInt(splitLine[2]))) {
                    console.log(`Unable to send API request to Granblue Automation Statistics: Invalid type for item amount.`)
                    newLog = [...mlc.asyncMessages, `\nUnable to send API request to Granblue Automation Statistics: Invalid type for item amount.`]
                } else {
                    sendAPIRequest(splitLine[1], parseInt(splitLine[2]), splitLine[3])
                }

                newLog = [...newLog, `\n${line}`]
                mlc.setAsyncMessages(newLog)
            } else {
                // Do not update to React 18. State updates in batch will break and stdout log will not work properly.
                let newLog = [...mlc.asyncMessages, `\n${line}`]
                mlc.setAsyncMessages(newLog)
            }
        })
        command.stderr.on("data", (line: string) => {
            let newLog = [...mlc.asyncMessages, `\n${line}`]
            mlc.setAsyncMessages(newLog)
        })

        // Login to API.
        if (bsc.settings.api.enableOptInAPI) {
            await loginToAPI()
        }

        // Create the child process.
        const child = await command.spawn()
        console.log("PID: ", child.pid)
        setPID(child.pid)
        bsc.setIsBotRunning(true)
        setFirstTimeAPIRequest(true)
    }

    // Login to the Granblue Automation Statistics API.
    const loginToAPI = async () => {
        await axios
            .post(
                `${bsc.entryPoint}/api/login`,
                {
                    username: bsc.settings.api.username,
                    password: bsc.settings.api.password,
                },
                {
                    withCredentials: true,
                }
            )
            .then(() => {
                let newLog = [...mlc.asyncMessages, `Successfully logged into Granblue Automation Statistics API.\n`]
                mlc.setAsyncMessages(newLog)
                successfulAPILogin = true
            })
            .catch((e: AxiosError) => {
                let newLog = [...mlc.asyncMessages, `Failed to login to Granblue Automation Statistics API: ${e}\n`]
                mlc.setAsyncMessages(newLog)
            })
    }

    // Send a API request to create a new result in the database.
    const sendAPIRequest = async (itemName: string, amount: number, elapsedTime: string) => {
        // If this is the first time, create the item if it does not already exist in the database.
        let newLog: string[] = []
        if (firstTimeAPIRequest) {
            await axios
                .post(
                    `${bsc.entryPoint}/api/create-item`,
                    {
                        username: bsc.settings.api.username,
                        password: bsc.settings.api.password,
                        farmingMode: bsc.settings.game.farmingMode,
                        mission: bsc.settings.game.mission,
                        itemName: itemName,
                    },
                    { withCredentials: true }
                )
                .then(async (res: AxiosResponse) => {
                    console.log("[API] ", res.data)
                    newLog = [...mlc.asyncMessages, `\n[API] ${res.data}`]
                    setFirstTimeAPIRequest(false)
                    await axios
                        .post(
                            `${bsc.entryPoint}/api/create-result`,
                            {
                                username: bsc.settings.api.username,
                                password: bsc.settings.api.password,
                                farmingMode: bsc.settings.game.farmingMode,
                                mission: bsc.settings.game.mission,
                                itemName: itemName,
                                platform: "GA",
                                amount: amount,
                                elapsedTime: elapsedTime,
                                appVersion: bsc.appVersion,
                            },
                            { withCredentials: true }
                        )
                        .then((res: AxiosResponse) => {
                            console.log("[API] ", res.data)
                            newLog = [...newLog, `\n[API] ${res.data}`]
                        })
                        .catch((e) => {
                            newLog = [...newLog, `\n[API] Failed to create result: ${e?.response?.data}`]
                        })
                        .finally(() => {
                            mlc.setAsyncMessages(newLog)
                        })
                })
                .catch((e: AxiosError) => {
                    console.error(`[API] Failed to create item for the first time: ${e}`)
                    newLog = [...mlc.asyncMessages, `\n[API] Failed to create item for the first time: ${e}`]
                    mlc.setAsyncMessages(newLog)
                })
        } else {
            let newLog: string[] = []
            await axios
                .post(
                    `${bsc.entryPoint}/api/create-result`,
                    {
                        username: bsc.settings.api.username,
                        password: bsc.settings.api.password,
                        farmingMode: bsc.settings.game.farmingMode,
                        mission: bsc.settings.game.mission,
                        itemName: itemName,
                        platform: "GA",
                        amount: amount,
                        elapsedTime: elapsedTime,
                        appVersion: bsc.appVersion,
                    },
                    { withCredentials: true }
                )
                .then((res: AxiosResponse) => {
                    console.log("[API] ", res.data)
                    newLog = [...mlc.asyncMessages, `\n[API] ${res.data}`]
                })
                .catch((e) => {
                    newLog = [...mlc.asyncMessages, `\n[API] Failed to create result: ${e?.response?.data}`]
                })
                .finally(() => {
                    mlc.setAsyncMessages(newLog)
                })
        }
    }

    return null
}

export default StartHelper
