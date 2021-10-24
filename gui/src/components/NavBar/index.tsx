import { useState, useEffect, useContext } from "react"
import { Alert, AppBar, Button, ButtonGroup, Divider, Drawer, IconButton, List, ListItem, ListItemIcon, ListItemText, Snackbar, Toolbar, Typography } from "@mui/material"
import { Close, CropSquare, HomeRounded, Menu, Minimize, Settings } from "@mui/icons-material"
import { Link as RouterLink, useHistory } from "react-router-dom"
import "./index.scss"
import { appWindow } from "@tauri-apps/api/window"
import { BotStateContext } from "../../context/BotStateContext"
import { readTextFile } from "@tauri-apps/api/fs"

const NavBar = () => {
    const history = useHistory()
    const [isDrawerOpen, setIsDrawerOpen] = useState(false)

    const botStateContext = useContext(BotStateContext)

    // Warn the user about refreshing the page.
    window.onbeforeunload = function (e) {
        if (botStateContext?.refreshAlert) {
            return false
        }
    }

    // This event listener will fire before the onbeforeunload. This is so the Snackbar can show itself before the window popup appears.
    window.addEventListener("keydown", function (e) {
        if (e.key === "F5") {
            botStateContext?.setRefreshAlert(true)
        }
    })

    // Load settings from JSON file on program start.
    useEffect(() => {
        try {
            readTextFile("settings.json")
                .then((settings) => {
                    interface ParsedSettings {
                        currentCombatScriptName: string
                        currentCombatScript: string
                        farmingMode: string
                        item: string
                        mission: string
                        itemAmount: number
                        groupNumber: number
                        partyNumber: number
                        debugMode: boolean
                    }

                    const decoded: ParsedSettings = JSON.parse(settings)

                    // TODO: Create proper logic to enable the ready status.
                    botStateContext?.setReadyStatus(decoded.debugMode)
                })
                .catch((err) => {
                    console.log(`Encountered read exception: ${err}`)
                })
        } catch (e) {
            console.log(`Encountered exception while loading settings from local JSON file:\n${e}`)
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    const toggleDrawer = () => {
        setIsDrawerOpen(!isDrawerOpen)
    }

    return (
        <AppBar position="fixed" id="header">
            <Snackbar
                open={botStateContext?.refreshAlert}
                anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
                autoHideDuration={10000}
                onClose={() => botStateContext?.setRefreshAlert(false)}
                onClick={() => botStateContext?.setRefreshAlert(false)}
            >
                <Alert severity="error">Do NOT reload/F5/refresh the "page" while the bot is RUNNING. You will have a runaway program.</Alert>
            </Snackbar>
            <Toolbar variant="dense" className="toolbar" data-tauri-drag-region>
                <IconButton className="menuButton" size="large" edge="start" color="inherit" aria-label="menu" sx={{ mr: 2 }} onClick={toggleDrawer}>
                    <Menu />
                </IconButton>
                <Drawer anchor="left" open={isDrawerOpen} onClose={toggleDrawer}>
                    <List className="list">
                        <RouterLink to="/" className="link">
                            <ListItem button key="home">
                                <ListItemIcon>
                                    <HomeRounded />
                                </ListItemIcon>
                                <ListItemText primary="Home" />
                            </ListItem>
                            <Divider />
                        </RouterLink>
                        <RouterLink to="/settings" className="link">
                            <ListItem button key="settings">
                                <ListItemIcon>
                                    <Settings />
                                </ListItemIcon>
                                <ListItemText primary="Settings" />
                            </ListItem>
                            <Divider />
                        </RouterLink>
                    </List>
                </Drawer>
                <Typography
                    variant="h6"
                    className="title"
                    onClick={() => {
                        history.push("/")
                    }}
                >
                    Granblue Automation
                </Typography>
                <div className="emptyDivider" />
                {botStateContext?.readyStatus ? (
                    <Typography variant="caption" sx={{ display: "flex", flexDirection: "column", justifyContent: "flex-end", marginRight: "10px", color: "#76ff03" }}>
                        Status: Ready
                    </Typography>
                ) : (
                    <Typography variant="caption" sx={{ display: "flex", flexDirection: "column", justifyContent: "flex-end", marginRight: "10px", color: "red" }}>
                        Status: Not Ready
                    </Typography>
                )}
                <ButtonGroup variant="outlined" className="group">
                    <Button
                        className="navButton"
                        onClick={() =>
                            setTimeout(() => {
                                appWindow.minimize()
                            }, 100)
                        }
                    >
                        <Minimize />
                    </Button>
                    <Button
                        className="navButton"
                        onClick={() =>
                            setTimeout(() => {
                                appWindow.toggleMaximize()
                            }, 100)
                        }
                    >
                        <CropSquare />
                    </Button>
                    <Button
                        className="navButton"
                        onClick={() =>
                            setTimeout(() => {
                                appWindow.close()
                            }, 100)
                        }
                    >
                        <Close />
                    </Button>
                </ButtonGroup>
            </Toolbar>
        </AppBar>
    )
}

export default NavBar
