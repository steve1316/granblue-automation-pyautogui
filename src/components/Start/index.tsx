import { Command } from "@tauri-apps/api/shell"
import { useContext, useEffect, useState } from "react"
import { MessageLogContext } from "../../context/MessageLogContext"
import { BotStateContext } from "../../context/BotStateContext"
import { FsTextFileOption, readTextFile, writeFile } from "@tauri-apps/api/fs"

import summonData from "../../data/summons.json"

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
            console.log("Killing process tree now...")
            const output = await new Command("powershell", `taskkill /F /T /PID ${PID}`).execute() // Windows specific
            console.log(`Result of killing bot process using PID ${PID}: \n${output.stdout}`)
            setPID(0)
        }
    }

    useEffect(() => {
        try {
            readTextFile("backend/config.ini")
                .then(() => {
                    console.log(`config.ini already exists.`)
                })
                .catch(() => {
                    console.log(`config.ini does not exist. Creating it now...`)

                    const configString = `
############################################################
; Customize the bot's internals by editing the following to your liking.
; Do not enclose anything in double quotes, " ".
############################################################

############################################################
# Read the instructions on the GitHub repository README.md on how to setup Discord notifications.
############################################################
[discord]
enable_discord = False
discord_token = 
user_id = 0

############################################################
# Read the instructions on the GitHub repository README.md on how to get these keys in order to allow the bot to farm Raids via Twitter.
############################################################
[twitter]
api_key = 
api_key_secret = 
access_token = 
access_token_secret = 
set_stream_api_default = True

[refill]
############################################################
# NOTE: Enable the 'enabled_auto_restore' field if you have enabled the 'AP/EP Auto-Restore Settings' under the Misc settings in-game.
# This includes the 'Auto-Restore Notification Settings' being set to Hide. This will shave off about 10s per run.
############################################################
refill_using_full_elixir = False
refill_using_soul_balms = False
enabled_auto_restore = True

[configuration]
############################################################
# Mouse speed in this application is the amount of time in seconds needed to move the mouse from Point A to Point B. Default is 0.2 seconds.
############################################################
mouse_speed = 0.2

############################################################
# Enables the usage of the Bezier Curve to have the bot mimic human-like but slow mouse movements.
# If disabled, the bot will use bot-like but fast linear mouse movement.
############################################################
enable_bezier_curve_mouse_movement = true

############################################################
# Enable delay in seconds between runs to serve as a resting period.
# Default is 15 seconds.
# Note: If both this and randomized delay is turned on, only this delay will be used.
############################################################
enable_delay_between_runs = False
delay_in_seconds = 15

############################################################
# Enable randomized delay in seconds between runs in the range between the lower and upper bounds inclusive to serve as a resting period.
# Default is 15 seconds for the lower bound and 60 seconds for the upper bound.
############################################################
enable_randomized_delay_between_runs = False
delay_in_seconds_lower_bound = 15
delay_in_seconds_upper_bound = 60

############################################################
# The following settings below follow pretty much the same template provided. They default to the settings selected for Farming Mode if nothing is set.

# Enables this fight or skip it if false.
# enable_*** =

# The file name of the combat script to use inside the /scripts/ folder. If set to nothing, defaults to the one selected for Farming Mode. Example: full_auto
# ***_combat_script =

# Select what Summon(s) separated by commas to use in order from highest priority to least. Example: Shiva, Colossus Omega, Varuna, Agni
# https://github.com/steve1316/granblue-automation-pyautogui/wiki/Selectable-Summons
# ***_summon_list =

# Indicate what element(s) the Summon(s) are in order from ***_summon_list separated by commas. Accepted values are: Fire, Water, Earth, Wind, Light, Dark, Misc.
# ***__summon_element_list =

# Set what Party to select and under what Group to run for the specified fight. Accepted values are: Group [1, 2, 3, 4, 5, 6, 7] and Party [1, 2, 3, 4, 5, 6].
# ***_group_number =
# ***_party_number =
############################################################

[dimensional_halo]
enable_dimensional_halo = False
dimensional_halo_combat_script = 
dimensional_halo_summon_list = 
dimensional_halo_summon_element_list = 
dimensional_halo_group_number = 0
dimensional_halo_party_number = 0

[event]
enable_event_nightmare = False
event_nightmare_combat_script = 
event_nightmare_summon_list = 
event_nightmare_summon_element_list = 
event_nightmare_group_number = 0
event_nightmare_party_number = 0

[rise_of_the_beasts]
enable_rotb_extreme_plus = False
rotb_extreme_plus_combat_script = 
rotb_extreme_plus_summon_list = 
rotb_extreme_plus_summon_element_list = 
rotb_extreme_plus_group_number = 0
rotb_extreme_plus_party_number = 0

[xeno_clash]
enable_xeno_clash_nightmare = False
xeno_clash_nightmare_combat_script = 
xeno_clash_nightmare_summon_list = 
xeno_clash_nightmare_summon_element_list = 
xeno_clash_nightmare_group_number = 0
xeno_clash_nightmare_party_number = 0

[arcarum]
enable_stop_on_arcarum_boss = True`
                    const configFile: FsTextFileOption = { path: "backend/config.ini", contents: configString }
                    writeFile(configFile)
                        .then(() => {
                            console.log(`config.ini created successfully.`)
                        })
                        .catch((err) => {
                            console.log(`Encountered write exception while saving settings to backend/config.ini: ${err}`)
                            messageLogContext?.setMessageLog([
                                ...messageLogContext?.messageLog,
                                `\nEncountered write exception while saving settings to backend/config.ini: ${err}\nThe current directory or parent directory might be write-protected`,
                            ])
                        })
                })
        } catch (e) {
            console.log(`Encountered exception while reading backend/config.ini: ${e}`)
            messageLogContext?.setMessageLog([...messageLogContext?.messageLog, `\nEncountered exception while reading backend/config.ini: ${e}`])
        }
    }, [])

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
                        summonElements: string[]
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
                    botStateContext?.setSummonElements(decoded.summonElements)
                    botStateContext?.setGroupNumber(decoded.groupNumber)
                    botStateContext?.setPartyNumber(decoded.partyNumber)
                    botStateContext?.setDebugMode(decoded.debugMode)
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

        setFirstTimeSetup(false)
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    // Save current settings to JSON file.
    useEffect(() => {
        if (!firstTimeSetup) {
            try {
                var newSummonElementsList: string[] = botStateContext?.summonElements
                botStateContext?.summons.forEach((summon) => {
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

                botStateContext?.setSummonElements(newSummonElementsList)

                const settings = {
                    combatScriptName: botStateContext?.combatScriptName,
                    combatScript: botStateContext?.combatScript,
                    farmingMode: botStateContext?.farmingMode,
                    item: botStateContext?.item,
                    mission: botStateContext?.mission,
                    map: botStateContext?.map,
                    itemAmount: botStateContext?.itemAmount,
                    summons: botStateContext?.summons,
                    summonElements: newSummonElementsList,
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
        if (botStateContext?.farmingMode !== "Coop" && botStateContext?.farmingMode !== "Arcarum" && botStateContext?.farmingMode !== "") {
            if (botStateContext?.item !== "" && botStateContext?.mission !== "" && botStateContext?.summons.length !== 0) {
                botStateContext?.setReadyStatus(true)
            } else {
                botStateContext?.setReadyStatus(false)
            }
        } else if (botStateContext?.farmingMode === "Coop" || botStateContext?.farmingMode === "Arcarum") {
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
        const command = new Command("python", "backend/main.py")

        // Attach event listeners.
        command.on("close", (data) => {
            const fileName = `log ${getCurrentDateAndTime("-")}`
            let newLog = [...messageLogContext?.asyncMessages, `\n\nWill save message log to ${fileName}.txt`, `\nChild process finished with code ${data.code}`]
            messageLogContext?.setAsyncMessages(newLog)
            botStateContext?.setIsBotRunning(false)
            botStateContext?.setStartBot(false)
            botStateContext?.setStopBot(false)

            handleStop()
        })
        command.on("error", (error) => {
            const fileName = `log ${getCurrentDateAndTime("-")}`
            let newLog = [...messageLogContext?.asyncMessages, `\n\nWill save message log to ${fileName}.txt`, `\nChild process error: ${error}`]
            messageLogContext?.setAsyncMessages(newLog)
            botStateContext?.setIsBotRunning(false)
            botStateContext?.setStartBot(false)
            botStateContext?.setStopBot(false)

            handleStop()
        })
        command.stdout.on("data", (line) => {
            let newLog = [...messageLogContext?.asyncMessages, `\n${line}`]
            messageLogContext?.setAsyncMessages(newLog)
        })
        command.stderr.on("data", (line) => {
            let newLog = [...messageLogContext?.asyncMessages, `\n${line}`]
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
