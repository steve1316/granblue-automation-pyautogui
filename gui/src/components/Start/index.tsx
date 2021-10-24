import { Command } from "@tauri-apps/api/shell"
import { useContext, useEffect, useState } from "react"
import { MessageLogContext } from "../../context/MessageLogContext"
import { BotStateContext } from "../../context/BotStateContext"

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
