import { Container, createStyles, Text } from "@mantine/core"
import { useContext, useEffect, useRef } from "react"
import { MessageLogContext } from "../../context/MessageLogContext"

const Home = () => {
    const mlc = useContext(MessageLogContext)

    const msgRef = useRef<HTMLDivElement | null>(null)

    const useStyles = createStyles((theme) => ({
        container: {
            width: "100%",
            maxWidth: "100%",
            height: "100%",
            display: "table", // This and having the inner container inherit the height is necessary to keep the log container from not overflowing the wrong way.
            backgroundColor: "#2f2f2f",
            padding: "10px 20px 10px 20px",
            fontSize: "8pt",
            whiteSpace: "pre-wrap",
            borderRadius: 10,
            margin: 0,
        },
        innerContainer: {
            height: "inherit",
            overflowY: "auto",
        },
    }))

    const { classes } = useStyles()

    // Scroll to the bottom of the message log window when new messages are added.
    useEffect(() => {
        if (msgRef) {
            msgRef.current!!.scrollIntoView({ behavior: "smooth" })
        }
    }, [mlc.messageLog])

    const initialMessage = `****************************************\nWelcome to Granblue Automation!\n****************************************\nInstructions\n----------------\nNote: The START button is disabled until the following steps are followed through.\n
    1. Have your game window and the Bottom Menu visible. Set the game window size set to the second "notch".
    2. Go to the Settings Page of the bot and fill out the sections until the status at the top says "Ready".
    3. You can now head back to the Home Page of the bot and click START.
    \nWarning: Do not refresh/F5 the program's "page" while the bot process is running. Otherwise in order to stop it, you will need to kill it by completely exiting the program.\n****************************************\n`

    return (
        <Container className={classes.container}>
            <Text id="log" className={classes.innerContainer}>
                {initialMessage + mlc.messageLog.join("\r")}
                <div ref={msgRef} />
            </Text>
        </Container>
    )
}

export default Home
