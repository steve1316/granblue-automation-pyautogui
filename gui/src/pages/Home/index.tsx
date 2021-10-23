import { useContext } from "react"
import { Button, Fade, Stack } from "@mui/material"
import { Box } from "@mui/system"
import "./index.scss"
import { MessageLogContext } from "../../context/MessageLogContext"
import { BotStateContext } from "../../context/BotStateContext"

const Home = () => {
    const { status, running, start, stop } = useContext(BotStateContext)
    const { log, start } = useContext(MessageLogContext)
    const [messageLog, _setMessageLog] = log
    const [readyStatus, setReadyStatus] = status
    const [_startFlag, setStartFlag] = start

    const initialMessage = `****************************************\nWelcome to Granblue Automation!\n****************************************\nInstructions\n----------------\nNote: The START button is disabled until the following steps are followed through.\n
    1. Have your game window and the Bottom Menu visible. Set the game window size set to the second "notch". 
    2. Go to the Settings Page of the bot and fill out the sections until the status at the top says "Ready".
    3. You can now head back to the Home Page of the bot and click START.
    \nWarning: Do not refresh/F5 the program's "page" while the bot process is running. Otherwise in order to stop it, you will need to kill it using CTRL+C via the terminal.\n****************************************`

    // Start the bot process. Actual logic is based in Start.tsx component.
    const handleClick = () => {
        setStartFlag(true)
    }

    return (
        <Fade in={true}>
            <Box className="homeContainer" id="homeContainer">
                <Stack direction="row" sx={{ height: "100%" }}>
                    <div className="logOuterContainer">
                        <div className="logInnerContainer">
                            <p id="log">{initialMessage + messageLog.join("\r")}</p>
                        </div>
                    </div>
                    <div className="rightOuterContainer">
                        <div className="rightContainer">
                            <Button disabled={!readyStatus} variant="contained" onClick={handleClick}>
                                {readyStatus ? "Start" : "Not Ready"}
                            </Button>
                        </div>
                    </div>
                </Stack>
            </Box>
        </Fade>
    )
}

export default Home
