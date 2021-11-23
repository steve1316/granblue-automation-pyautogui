import { Button, Fade, Stack } from "@mui/material"
import { Box } from "@mui/system"
import { useContext, useEffect, useRef } from "react"
import { BotStateContext } from "../../context/BotStateContext"
import { MessageLogContext } from "../../context/MessageLogContext"
import "./index.scss"

const Home = () => {
    const botStateContext = useContext(BotStateContext)
    const messageLogContext = useContext(MessageLogContext)

    const msgRef = useRef<HTMLDivElement | null>(null)

    const initialMessage = `****************************************\nWelcome to Granblue Automation!\n****************************************\nInstructions\n----------------\nNote: The START button is disabled until the following steps are followed through.\n
    1. Have your game window and the Bottom Menu visible. Set the game window size set to the second "notch". 
    2. Go to the Settings Page of the bot and fill out the sections until the status at the top says "Ready".
    3. You can now head back to the Home Page of the bot and click START.
    \nWarning: Do not refresh/F5 the program's "page" while the bot process is running. Otherwise in order to stop it, you will need to kill it by completely exiting the program.\n****************************************\n`

    // Scroll to the bottom of the message log window when new messages are added.
    useEffect(() => {
        if (msgRef) {
            const bottom: number = msgRef.current!!.scrollHeight - msgRef.current!!.clientHeight
            msgRef.current!!.scrollTo(0, bottom)
        }
    }, [messageLogContext.messageLog])

    // Reset message log and then start the bot process. Actual logic is based in Start.tsx component.
    const handleStart = () => {
        messageLogContext.setMessageLog([])
        messageLogContext.setAsyncMessages([])
        botStateContext.setStartBot(true)
        botStateContext.setStopBot(false)
    }

    // Stop the bot process. Actual logic is based in Start.tsx component.
    const handleStop = () => {
        botStateContext.setStartBot(false)
        botStateContext.setStopBot(true)
    }

    return (
        <Fade in={true}>
            <Box className={botStateContext.settings.misc.guiLowPerformanceMode ? "homeContainerLowPerformance" : "homeContainer"} id="homeContainer">
                <Stack direction="row" sx={{ height: "100%" }}>
                    <div className="logOuterContainer">
                        <div ref={msgRef} className="logInnerContainer">
                            <p id="log">{initialMessage + messageLogContext.messageLog.join("\r")}</p>
                        </div>
                    </div>
                    <div className="rightOuterContainer">
                        <div className="rightContainer">
                            {botStateContext.isBotRunning ? (
                                <Button color="error" variant="contained" onClick={handleStop}>
                                    Stop
                                </Button>
                            ) : (
                                <Button disabled={!botStateContext.readyStatus} variant="contained" onClick={handleStart}>
                                    {botStateContext.readyStatus ? "Start" : "Not Ready"}
                                </Button>
                            )}
                        </div>
                    </div>
                </Stack>
            </Box>
        </Fade>
    )
}

export default Home
