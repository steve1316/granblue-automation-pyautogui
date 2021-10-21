import { useContext } from "react"
import { Button, Fade, Stack } from "@mui/material"
import { Box } from "@mui/system"
import "./index.scss"
import { ReadyContext } from "../../context/ReadyContext"

const Home = () => {
    const { status } = useContext(ReadyContext)

    const initialMessage = `Welcome to Granblue Automation!
    \n***************************\n\nInstructions\n----------------
    \nNote: The START button is disabled until the following steps are followed through.
    \n1. Have your game window and the Bottom Menu visible. Set the game window size set to the second "notch". 
    \n2. Go to the Settings Page of the bot and fill out the sections until the status at the top says "Ready".
    \n3. You can now head back to the Home Page of the bot and click START.
    \n***************************`

    return (
        <Fade in={true}>
            <Box className="homeContainer" id="homeContainer">
                <Stack direction="row" sx={{ height: "100%" }}>
                    <div className="logOuterContainer">
                        <div className="logInnerContainer">
                            <p id="log">{initialMessage}</p>
                        </div>
                    </div>
                    <div className="rightOuterContainer">
                        <div className="rightContainer">
                            <Button disabled={!status} variant="contained">
                                {status ? "Start" : "Not Ready"}
                            </Button>
                        </div>
                    </div>
                </Stack>
            </Box>
        </Fade>
    )
}

export default Home
