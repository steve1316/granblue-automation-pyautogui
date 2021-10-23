import { Command } from "@tauri-apps/api/shell"
import { useContext, useEffect } from "react"
import { MessageLogContext } from "../../context/MessageLogContext"
import { BotStateContext } from "../../context/BotStateContext"

const Start = () => {
    const { log, message, start } = useContext(MessageLogContext)
    const { running, start, stop } = useContext(BotStateContext)
    const [messageLog, setMessageLog] = log
    const [asyncMessages, setAsyncMessages] = message
    const [startFlag, _setStartFlag] = start

    // Append the messages acquired from the async bot process to the message log. This is needed to actually reflect the new messages to the Home page.
    useEffect(() => {
        const newLog = [...messageLog, ...asyncMessages]
        setMessageLog(newLog)
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [asyncMessages])

    // Start the bot.
    useEffect(() => {
        if (startFlag) {
            handleStart()
        }
    }, [startFlag])

    // Begin the bot process here.
    // Note: newlines are not sent over through stdout so they need to be manually added here in the frontend.
    const handleStart = async () => {
        // Construct the shell command using Tauri Command API.
        const command = new Command("python", "backend/test.py")

        // Attach event listeners.
        command.on("close", (data) => {
            let newLog = [...asyncMessages, `\nChild process finished with code ${data.code} and signal ${data.signal}`]
            setAsyncMessages(newLog)
        })
        command.on("error", (error) => {
            let newLog = [...asyncMessages, `\nChild process error: ${error}`]
            setAsyncMessages(newLog)
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
    }

    // function delay(ms: number) {
    //     return new Promise((res) => setTimeout(res, ms))
    // }

    return null
}

export default Start
