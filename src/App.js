import { useState, useEffect } from "react"
import { BrowserRouter as Router, Route, Switch } from "react-router-dom"
import NavBar from "./components/NavBar"
import Start from "./components/Start"
import { BotStateProvider } from "./context/BotStateContext"
import { MessageLogProvider } from "./context/MessageLogContext"
import Adjustments from "./pages/Adjustments"
import ExtraSettings from "./pages/ExtraSettings"
import Home from "./pages/Home"
import Settings from "./pages/Settings"

import * as app from "@tauri-apps/api/app"
import { emit, listen } from "@tauri-apps/api/event"
import Snackbar from "@mui/material/Snackbar"
import { Button } from "@mui/material"

function App() {
    const [updateAvailable, setUpdateAvailable] = useState(false)
    const [updateMessage, setUpdateMessage] = useState("Update available")
    const [isOpen, setIsOpen] = useState(true)

    // Check if update is available.
    useEffect(() => {
        emit("tauri://update")

        listen("tauri://update-available", (res) => {
            console.log("New version: ", res)
            setUpdateAvailable(true)
            getVersion(res.payload.version)
        })
    }, [])

    // Grab the program version.
    const getVersion = async (newVersion) => {
        await app
            .getVersion()
            .then((version) => {
                setUpdateMessage(`Update available: v${version} -> v${newVersion}`)
            })
            .catch(() => {
                setUpdateMessage("Update available")
            })
    }

    const handleClose = () => {
        setIsOpen(false)
    }

    return (
        <Router>
            <BotStateProvider>
                <MessageLogProvider>
                    <NavBar />
                    <Start />
                    <Switch>
                        <Route path="/" exact>
                            {updateAvailable ? (
                                <Snackbar
                                    anchorOrigin={{ vertical: "top", horizontal: "center" }}
                                    open={isOpen}
                                    message={updateMessage}
                                    ContentProps={{
                                        sx: {
                                            backgroundColor: "rgb(56, 142, 60)",
                                        },
                                    }}
                                    action={
                                        <>
                                            <Button
                                                size="small"
                                                variant="contained"
                                                color="error"
                                                onClick={() => {
                                                    window.open("https://github.com/steve1316/granblue-automation-pyautogui/releases", "_blank")
                                                    handleClose()
                                                }}
                                            >
                                                Go to GitHub
                                            </Button>
                                        </>
                                    }
                                    onClick={handleClose}
                                    onClose={handleClose}
                                ></Snackbar>
                            ) : null}

                            <Home />
                        </Route>
                        <Route path="/settings" exact>
                            <Settings />
                        </Route>
                        <Route path="/extrasettings" exact>
                            <ExtraSettings />
                        </Route>
                        <Route path="/adjustments" exact>
                            <Adjustments />
                        </Route>
                    </Switch>
                </MessageLogProvider>
            </BotStateProvider>
        </Router>
    )
}

export default App
