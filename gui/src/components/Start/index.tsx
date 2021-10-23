import { Command } from "@tauri-apps/api/shell"
import { useContext, useEffect, useState } from "react"
import { MessageLogContext } from "../../context/MessageLogContext"
import { BotStateContext } from "../../context/BotStateContext"

const Start = () => {
    const { log, message } = useContext(MessageLogContext)
    const { running, start, stop } = useContext(BotStateContext)
    const [messageLog, setMessageLog] = log
    const [asyncMessages, setAsyncMessages] = message
    const [isBotRunning, setIsBotRunning] = running
    const [startBot, setStartBot] = start
    const [stopBot, setStopBot] = stop
    const [PID, setPID] = useState(0)

    // Append the messages acquired from the async bot process to the message log. This is needed to actually reflect the new messages to the Home page.
    useEffect(() => {
        const newLog = [...messageLog, ...asyncMessages]
        setMessageLog(newLog)
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [asyncMessages])

    // Start or stop the bot.
    useEffect(() => {
        if (startBot && !isBotRunning) {
            handleStart()
        } else if (stopBot && isBotRunning) {
            if (PID !== 0) {
                handleStop()
            }
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [startBot, stopBot])

    const handleStop = async () => {
        console.log("Killing process now...")
        const output = await new Command("powershell", `taskkill /F /PID ${PID}`).execute() // Windows specific
        console.log(`Result of killing bot process using PID ${PID}: ${output.code}`)
        setPID(0)
    }

    // Begin the bot process here.
    // Note: newlines are not sent over through stdout so they need to be manually added here in the frontend.
    const handleStart = async () => {
        // Construct the shell command using Tauri Command API.
        const command = new Command("python", "backend/test.py")

        // Attach event listeners.
        command.on("close", (data) => {
            let newLog = [...asyncMessages, `\nChild process finished with code ${data.code}`]
            setAsyncMessages(newLog)
            setIsBotRunning(false)
            setStartBot(false)
            setStopBot(false)
        })
        command.on("error", (error) => {
            let newLog = [...asyncMessages, `\nChild process error: ${error}`]
            setAsyncMessages(newLog)
            setIsBotRunning(false)
            setStartBot(false)
            setStopBot(false)
        })
        command.stdout.on("data", (line) => {
            let newLog = [...asyncMessages, `\nChild process stdout: "${line}"`]
            setAsyncMessages(newLog)
        })
        command.stderr.on("data", (line) => {
            let newLog = [...asyncMessages, `\nChild process stderr: "${line}"`]
            setAsyncMessages(newLog)
        })

        // Create the child process.
        const child = await command.spawn()
        console.log("PID: ", child.pid)
        setPID(child.pid)
        setIsBotRunning(true)
    }

    return null
}

export default Start
